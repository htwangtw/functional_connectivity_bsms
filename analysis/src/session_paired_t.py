import os
import sys
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


seed = Path(sys.argv[1])
subject = sys.argv[2]

project_path = Path(__file__).parents[1]

print(subject)
results_path = project_path / f"results/subject_level/sub-{subject}"
placebol_path = (project_path / f"results/subject_level/sub-{subject}/ses-placebo/{seed}_effect_size.nii.gz")
typhoid_path = (project_path / f"results/subject_level/sub-{subject}/ses-typhoid/{seed}_effect_size.nii.gz")

# create design matrix
design_matrix = pd.DataFrame([-1, 1], columns=["typhoid_wrt_placebo"])
input_imgs = [
    str(placebol_path),
    str(typhoid_path),
]
print("fit model")
session_level_model = SecondLevelModel(verbose=2)
session_level_model = session_level_model.fit(input_imgs, design_matrix=design_matrix)
t_map = session_level_model.compute_contrast("typhoid_wrt_placebo", output_type='effect_size')
t_map.to_filename(str(results_path / f"{seed}_typhoid_wrt_placebo_effect_size.nii.gz"))
print("done")