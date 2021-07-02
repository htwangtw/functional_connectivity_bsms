"""Extract beta weight from first level contrast with group level significant clusters

Authors: Hao-Ting Wang
Date: May 17, 2021
"""
import sys
from pathlib import Path

import nibabel as nb
from nilearn.image import math_img
from nilearn.input_data import NiftiLabelsMasker
from nilearn.regions import connected_label_regions
import pandas as pd


seed = sys.argv[1]

project_path = Path(__file__).parents[2]
thresh_z_paths = [
    (
        project_path
        / f"results/group_level/{seed}_ses-placebo_patient_wrt_control/control_wrt_patient_thresh_zstat.nii.gz"
    ),
    (
        project_path
        / f"results/group_level/{seed}_double_twosample_t/placebol_wrt_typhoid_thresh_zstat.nii.gz"
    ),
]

subject_stats_path = [
    [
        str(p)
        for p in project_path.glob(
            f"results/subject_level/sub-*/ses-typhoid/{seed}_effect_size.nii.gz"
        )
    ],
    [
        str(p)
        for p in project_path.glob(
            f"results/subject_level/sub-*/ses-placebo/{seed}_effect_size.nii.gz"
        )
    ],
]

group_info = pd.read_csv(project_path / "analysis/group_design.csv", index_col=0)

for map_path in thresh_z_paths:
    thresh_z = nb.load(str(map_path))
    analysis_name = (
        str(map_path.parent).split("/")[-1] + "_" + map_path.name.split("_thresh")[0]
    )
    bin_cluster = math_img("(img > 0).astype(int)", img=thresh_z)
    label_regions = connected_label_regions(bin_cluster)
    label_regions.to_filename(
        str(project_path / f"results/group_level/{analysis_name}_cluster_label.nii.gz")
    )

    masker = NiftiLabelsMasker(label_regions)
    beta_weight = pd.read_csv(project_path / "analysis/group_design.csv", index_col=0)
    for ses in subject_stats_path:
        session_name = ses[0].split("ses-")[-1].split("/")[0]
        cluster_data = masker.fit_transform(ses)
        cisc_id = [int(sub.split("sub-")[-1].split("/")[0]) for sub in ses]
        data = pd.DataFrame(cluster_data, index=cisc_id)
        col_name = [f"ses-{session_name}_cluster_{col + 1:02d}" for col in data.columns]
        data.columns = col_name
        beta_weight = pd.concat([beta_weight, data], axis=1)
    beta_weight.to_csv(
        project_path / f"results/group_level/{analysis_name}_beta_weight.csv"
    )
