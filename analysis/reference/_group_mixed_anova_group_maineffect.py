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

placebol_path = (project_path / "results/").glob("sub-*/ses-placebo/icbm_insula*effect_size.nii.gz")
typhoid_path = (project_path / "results/").glob("sub-*/ses-typhoid/icbm_insula*effect_size.nii.gz")

results_path = project_path / "results/group_level/icbm_insula_mixed_anova"
report_path = project_path / "results/icbm_insula_mixed_anova_group-maineffect.html"

report_title = "Insula: Mixed-effect ANOVA - group main effect"

if not results_path.exists():
    os.makedirs(results_path)

# gm_mask = str(project_path / "atlas/gm_mask.nii.gz")
gm_mask = fetch_icbm152_brain_gm_mask(data_dir=str(project_path / "atlas"), threshold=0.5)


def session_level(ses1, ses2):
    group_inputs = []
    for img1, img2 in zip(ses1, ses2):
        ses_model = SecondLevelModel()
        ses_model = ses_model.fit(
            [img1, img2],
            design_matrix=pd.DataFrame(np.array([[1], [1]]), columns=["mean"]))
        effect_map = ses_model.compute_contrast(output_type='effect_size')
        group_inputs.append(effect_map)
    return group_inputs


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
placebo = pd.DataFrame()
for file in placebol_path:
    effects_map_path = str(file)
    subject_label = str(file.parents[1]).split("sub-")[-1]
    df = pd.DataFrame([subject_label, effects_map_path],
        index=['subject_label', 'effects_map_path']).T
    placebo = pd.concat([placebo, df], axis=0)
placebo = placebo.set_index("subject_label").sort_index()
typhoid = pd.DataFrame()
for file in typhoid_path:
    effects_map_path = str(file)
    subject_label = str(file.parents[1]).split("sub-")[-1]
    df = pd.DataFrame([subject_label, effects_map_path],
        index=['subject_label', 'effects_map_path']).T
    typhoid = pd.concat([typhoid, df], axis=0)
typhoid = typhoid.set_index("subject_label").sort_index()

# create design matrix
group_info = pd.read_csv(project_path / "scripts/group_design.csv", index_col=0)
n_subjects = group_info.shape[0]
design_matrix = group_info[["Sex", "Age", "control", "patient"]]
design_matrix.to_csv(results_path / "design_matrix_main_group.csv")

contrasts = {
    "control":[0, 0, 1, 0,],
    "patient":[0, 0, 0, 1,],
    "control wrt patient":[0, 0, 1, -1,],
    "patient wrt control":[0, 0, -1, 1,],
}
input_imgs = session_level(
    typhoid["effects_map_path"].tolist(),
    placebo["effects_map_path"].tolist())

# fit model and generate report
group_level_model, z_maps = group_level(
    input_imgs,
    design_matrix,
    contrasts,
    report_title,
    results_path,
    report_path)

# proportion_true_discoveries_img = cluster_level_inference(
#     z_map, alpha=.05)

# plotting.plot_stat_map(
#     proportion_true_discoveries_img, threshold=0.,
#     display_mode='z', vmax=1, colorbar=True,
#     title='group PCC connectivity, proportion true positives')
