"""Run two sample T-test

Authors: Hao-Ting Wang
Date: May 20, 2021
"""
import os, sys
from pathlib import Path
import pandas as pd

from nilearn.glm.second_level import SecondLevelModel
from nilearn.glm.thresholding import threshold_stats_img
from nilearn.reporting import make_glm_report


seed = sys.argv[1]
multiple_comparison = sys.argv[2]

project_path = Path(__file__).parents[2]

alpha = {
    "bonferroni": 0.05,
    "fpr": 0.001
}

placebol_path = (project_path / "results/subject_level").glob(
    f"sub-*/ses-placebo/{seed}*effect_size.nii.gz"
)
results_path = (
    project_path / f"results/group_level/{seed}_ses-placebo_patient_wrt_control"
)
report_path = project_path / f"results/{seed}_ses-placebo_patient_wrt_control.html"
report_title = f"{seed}: Patients vs Controls in placebo session"

if not results_path.exists():
    os.makedirs(results_path)

gm_mask = str(project_path / "atlas/custom_gm_mask.nii.gz")


def group_level(input_imgs, design_matrix, contrasts, title, results_path):
    # gray matter mask to remove area with no BOLD signal
    group_level_model = SecondLevelModel(mask_img=gm_mask, smoothing_fwhm=0, verbose=1)
    print("fit parametric model")
    group_level_model = group_level_model.fit(input_imgs, design_matrix=design_matrix)

    for con_name, con in contrasts.items():
        print(con_name)
        z_map = group_level_model.compute_contrast(con, output_type="z_score")
        z_map.to_filename(str(results_path / f"{con_name}_zstat.nii.gz"))
        thresh_z, _ = threshold_stats_img(
            z_map,
            gm_mask,
            height_control=multiple_comparison,
            alpha=alpha[multiple_comparison],
            cluster_threshold=10,
        )
        thresh_z.to_filename(str(results_path / f"{con_name}_thresh_zstat.nii.gz"))
    return group_level_model


# load first level effect maps
second_level_input = pd.DataFrame()
for file in placebol_path:
    effects_map_path = str(file)
    subject_label = str(file.parents[1]).split("sub-")[-1]
    df = pd.DataFrame(
        [subject_label, effects_map_path], index=["subject_label", "effects_map_path"]
    ).T
    second_level_input = pd.concat([second_level_input, df], axis=0)
second_level_input = second_level_input.set_index("subject_label").sort_index()

# create design matrix
group_info = pd.read_csv(project_path / "analysis/group_design.csv", index_col=0)
group_info.index = group_info.index.map(str)
group_info = pd.concat([second_level_input, group_info], axis=1)
group_info.to_csv(results_path / "inputs.csv")
design_matrix = group_info[["Sex", "Age", "control", "patient"]]
design_matrix.to_csv(results_path / "two-sample-t-test_design-matrix.csv")

# generate parametric report
input_imgs = group_info["effects_map_path"].tolist()
print("generate parametric report")
design_matrix = group_info[["Sex", "Age", "control", "patient"]]
contrasts = {
    "control": [
        0,
        0,
        1,
        0,
    ],
    "patient": [
        0,
        0,
        0,
        1,
    ],
    "control_wrt_patient": [0, 0, 1, -1],
    "patient_wrt_control": [0, 0, -1, 1],
}

group_level_model = group_level(
    input_imgs, design_matrix, contrasts, report_title, results_path
)

report = make_glm_report(
    group_level_model,
    contrasts=contrasts,
    title=report_title,
    height_control=multiple_comparison,
    alpha=alpha[multiple_comparison],
    cluster_threshold=10,
)
report.save_as_html(report_path)
