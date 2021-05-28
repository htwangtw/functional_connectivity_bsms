"""Create insula ROI
Authors: Marisa Amato and Hao-Ting Wang
Date: May 13, 2021
"""
from pathlib import Path

import numpy as np
import nibabel as nb
# from nilearn import plotting

# define paths
atlas_dir = Path(__file__).parents[2] / "atlas"
atlas_path = atlas_dir / "HCPMMP1_on_MNI152_ICBM2009a_2mm_LOWRES.nii.gz"
roi_path = atlas_dir / "icbm_insula.nii.gz"

# labels of ROI in the atlas
glasser_insula = [103, 106, 108, 109, 110, 111, 112, 114, 115, 167, 168]

if __name__ == "__main__":
    atlas = nb.load(str(atlas_path))
    atlas_data = atlas.get_fdata().astype(int)

    insula_mask = np.zeros(atlas.shape)
    for id in glasser_insula:
        current_region = np.where(atlas_data == id, id, 0)
        insula_mask += current_region

    insula_mask = (insula_mask > 0).astype(int)
    insula_nifti = nb.Nifti1Image(insula_mask, affine=atlas.affine, header=atlas.header)
    insula_nifti.to_filename(str(roi_path))