"""Extract beta weight from first level contrast with group level significant clusters

Authors: Hao-Ting Wang
Date: May 17, 2021
"""
from pathlib import Path

import nibabel as nb
from nilearn.image import math_img
from nilearn.input_data import NiftiLabelsMasker
from nilearn.regions import connected_label_regions
import pandas as pd


project_path = Path(__file__).parents[2]
thresh_z_paths = [(project_path /
    "results/group_level/icbm_insula_ses-placebo_patient_wrt_control/control_wrt_patient_thresh_zstat.nii.gz"),
    (project_path /
    "results/group_level/icbm_insula_double_twosample_t/placebol_wrt_typhoid_thresh_zstat.nii.gz"),
    ]

subject_stats_path = [
    [str(p) for p in project_path.glob("results/subject_level/sub-*/ses-placebo/icbm_insula_effect_size.nii.gz")],
    [str(p) for p in project_path.glob("results/subject_level/sub-*/icbm_insula_typhoid_wrt_placebo_effect_size.nii.gz")],
    ]

beta_weight = pd.read_csv(project_path / "analysis/group_design.csv", index_col=0)

for map_path, subject_stats in zip(thresh_z_paths, subject_stats_path):
    thresh_z = nb.load(str(map_path))
    bin_cluster = math_img("(img > 0).astype(int)", img=thresh_z)
    label_regions = connected_label_regions(bin_cluster)
    masker = NiftiLabelsMasker(label_regions)
    cluster_data = masker.fit_transform(subject_stats)

    cisc_id = [
        int(sub.split("sub-")[-1].split("/")[0])
        for sub in subject_stats
    ]
    analysis_name = str(map_path.parent).split("/")[-1] + "_" + map_path.name.split("_thresh")[0]

    label_regions.to_filename(str(project_path / f"results/group_level/{analysis_name}_cluster_label.nii.gz"))

    data = pd.DataFrame(cluster_data, index=cisc_id)
    col_name = [f"{analysis_name}_cluster_{col + 1:02d}"for col in data.columns]
    data.columns = col_name
    beta_weight = pd.concat([beta_weight, data], axis=1)

beta_weight.to_csv(project_path / "results/group_level/insula_connectivity_beta_weight.csv")