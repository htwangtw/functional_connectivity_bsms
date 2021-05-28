import os
from pathlib import Path
import pandas as pd
import nibabel as nb
import numpy as np

import matplotlib.pyplot as plt

from nilearn import plotting
from nilearn.datasets import fetch_icbm152_brain_gm_mask
from nilearn.glm import cluster_level_inference
from nilearn.glm.second_level import SecondLevelModel, non_parametric_inference
from nilearn.reporting import make_glm_report

project_path = Path(__file__).parents[1]

filepath = (project_path / "results/difumo64_pcc").glob("sub-*/ses-placebo/*effect_size.nii.gz")
results_path = project_path / "results/difumo64_pcc/group_level/ses-placebo_patient_wrt_control"
report_path = project_path / "results/difumo64_pcc/ses-placebo_patient_wrt_control.html"
report_title = "PCC: patient_wrt_control"

if not results_path.exists():
    os.makedirs(results_path)

gm_mask = fetch_icbm152_brain_gm_mask(data_dir=str(project_path / "atlas"))


def group_level(input_imgs, design_matrix, contrasts, title, results_path, report_path):
    # gray matter mask to remove area with no BOLD signal
    group_level_model = SecondLevelModel(mask_img=gm_mask, smoothing_fwhm=5.0, verbose=2)

    group_level_model = group_level_model.fit(input_imgs,
                                            design_matrix=design_matrix)
    z_maps = {}
    for con_name, con in contrasts.items():
        z_map = group_level_model.compute_contrast(con, output_type='z_score')
        z_maps[con_name] = z_map
        z_maps[con_name].to_filename(str(results_path / f"{con_name}_zstat.nii.gz"))

    make_glm_report(
        group_level_model,
        contrasts=contrasts,
        title=title,
        ).save_as_html(report_path)
    return group_level_model, z_maps


# load first level effect maps
second_level_input = pd.DataFrame()
for file in filepath:
    effects_map_path = str(file)
    subject_label = str(file.parents[1]).split("sub-")[-1]
    df = pd.DataFrame([subject_label, effects_map_path],
        index=['subject_label', 'effects_map_path']).T
    second_level_input = pd.concat([second_level_input, df], axis=0)
second_level_input = second_level_input.set_index("subject_label").sort_index()
input_imgs = second_level_input["effects_map_path"].tolist()

# create design matrix
group_info = pd.read_csv(project_path / "scripts/group_design.csv", index_col=0)
design_matrix = group_info[["Sex", "Age", "control", "patient"]]
design_matrix.to_csv(results_path / "design_matrix.csv")

contrasts = {
    "group":[0, 0, 1, 1,],
    "control":[0, 0, 1, 0,],
    "patient":[0, 0, 0, 1,],
    "patient_wrt_control":[0, 0, -1, 1,],
    "control_wrt_patient":[0, 0, 1, -1,],
}

# fit model and generate report
group_level_model, z_maps = group_level(
    input_imgs,
    design_matrix,
    contrasts,
    report_title,
    results_path,
    report_path)


# from scipy.stats import norm
# p_val = 0.001
# p001_uncorrected = norm.isf(p_val)

# from nilearn.glm import cluster_level_inference
# proportion_true_discoveries_img = cluster_level_inference(
#     z_map, threshold=[3, 4, 5], alpha=.05)

# plotting.plot_stat_map(
#     proportion_true_discoveries_img, threshold=0.,
#     display_mode='z', vmax=1, colorbar=True,
#     title='group PCC, proportion true positives')

# plotting.plot_stat_map(
#     z_map, threshold=p001_uncorrected, colorbar=True, display_mode='z',
#     title='group PCC (uncorrected p < 0.001)')


# plotting.show()