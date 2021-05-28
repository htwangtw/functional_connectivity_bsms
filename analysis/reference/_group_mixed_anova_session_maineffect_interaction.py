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
report_path = project_path / "results/icbm_insula_mixed_anova_session-maineffect_interaction.html"

report_title = "Insula: Mixed-effect ANOVA session main effect and interaction"

if not results_path.exists():
    os.makedirs(results_path)

# gm_mask = str(project_path / "atlas/gm_mask.nii.gz")
gm_mask = fetch_icbm152_brain_gm_mask(data_dir=str(project_path / "atlas"), threshold=0.5)


def group_level(input_imgs, design_matrix, contrasts, title, results_path, report_path):
    # gray matter mask to remove area with no BOLD signal
    group_level_model = SecondLevelModel(mask_img=gm_mask, smoothing_fwhm=5.0, verbose=2)

    group_level_model = group_level_model.fit(second_level_input["effects_map_path"].tolist(),
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
dm_PTvsHC = group_info[["Sex", "Age", "patient"]]
dm_PTvsHC = dm_PTvsHC.rename(columns={"patient": "interaction"})
sub_ids = dm_PTvsHC.index.tolist()
subject_effects = pd.DataFrame(
    np.vstack((np.eye(n_subjects), np.eye(n_subjects))),
    columns=sub_ids, index=sub_ids * 2)

dm_typhoid = dm_PTvsHC.copy()
dm_typhoid["typhoid vs placebo"] = 1
dm_typhoid["interaction"] = group_info["control"].values - group_info["patient"].values

dm_placebo = dm_PTvsHC.copy()
dm_placebo["typhoid vs placebo"] = -1
dm_placebo["interaction"] = group_info["patient"].values - group_info["control"].values

second_level_input = pd.concat([typhoid, placebo], axis=0)
input_imgs = second_level_input["effects_map_path"].tolist()
design_matrix = pd.concat([dm_typhoid, dm_placebo], axis=0)
design_matrix = pd.concat([design_matrix, subject_effects], axis=1)

design_matrix.to_csv(results_path / "design_matrix_interaction.csv")

contrasts = {
    "typhoid_vs_placebo": "typhoid vs placebo",
    "interaction": "interaction"
}

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
