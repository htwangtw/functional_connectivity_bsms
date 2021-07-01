"""Create ROIs from Glasser atlas index
Authors: Marisa Amato and Hao-Ting Wang
Date: May 13, 2021
"""
from pathlib import Path

import numpy as np
import nibabel as nb
from nilearn.regions import connected_label_regions
# from nilearn import plotting

# define paths
atlas_dir = Path(__file__).parents[2] / "atlas"
atlas_path = atlas_dir / "HCPMMP1_on_MNI152_ICBM2009a_2mm_LOWRES.nii.gz"
roi_path = atlas_dir / "icbm_insula.nii.gz"

# labels of ROI in the atlas
glasser_insula = [103, 106, 108, 109, 110, 111, 112, 114, 115, 167, 168]
glasser_cingulate = [161]


def creat_roi_nifti(atlas_path, roi_path, glasser_index):
    """ROI from icmb glasser atlas index."""
    atlas = nb.load(str(atlas_path))
    atlas_data = atlas.get_fdata().astype(int)

    roi_mask = np.zeros(atlas.shape)
    for id in glasser_index:
        current_region = np.where(atlas_data == id, id, 0)
        roi_mask += current_region

    roi_mask = (roi_mask > 0).astype(int)
    roi_nifti = nb.Nifti1Image(roi_mask, affine=atlas.affine, header=atlas.header)
    roi_nifti.to_filename(str(roi_path))


if __name__ == "__main__":
    creat_roi_nifti(atlas_path,
                    atlas_dir / "icbm_insula-both.nii.gz",
                    glasser_insula)
    icbm_insula = connected_label_regions(
        str(atlas_dir / "icbm_insula-both.nii.gz"),
        min_size=500)
    icbm_insula.to_filename(atlas_dir / "icbm_insula-both.nii.gz")
    creat_roi_nifti(atlas_dir / "icbm_insula.nii.gz", atlas_dir / "icbm_insula-R.nii.gz", [1])
    creat_roi_nifti(atlas_dir / "icbm_insula.nii.gz", atlas_dir / "icbm_insula-L.nii.gz", [2])
    creat_roi_nifti(atlas_path,
                    atlas_dir / "icbm_cingulate_idx-161.nii.gz",
                    glasser_cingulate)