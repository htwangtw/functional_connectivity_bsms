import numpy as np
import nibabel as nb
# from nilearn import plotting


atlas = nb.load("HCPMMP1_on_MNI152_ICBM2009a_2mm_LOWRES.nii.gz")

atlas_data = atlas.get_fdata().astype(int)
glasser_insula = [103, 106, 108, 109, 110, 111, 112, 114, 115, 167, 168]

insula_mask = np.zeros(atlas.shape)
for id in glasser_insula:
    current_region = np.where(atlas_data == id, id, 0)
    insula_mask += current_region

insula_mask = (insula_mask > 0).astype(int)
insula_nifti = nb.Nifti1Image(insula_mask, affine=atlas.affine, header=atlas.header)
insula_nifti.to_filename("HCPMMP1_on_MNI152_ICBM2009a_2mm_insula.nii.gz")