# Gray matter mask

`custom_gm_mask.nii.gz`: [See refernce here](https://neurovault.org/images/312614/)

## Description

Clean up cerebellum and medial wall by H-T Wang.

SPM gray matter probability mask thresholded at 50% and binarised, remove cerebellum and subcortical mask.

Subcortical and brain stem mask by Gorgolewski [neurovault link](https://identifiers.org/neurovault.image:39877).

Binarised cerebellum mask from FSLeyes supplied `Cerebellum-MNIfnirt.nii.gz`.

## Why use this mask?

Useing a gray matter mask constrains the analysis to regions with BOLD signals.
During data collection, brain stem and cerebellum are cut off for various subjects due to head size. 
To reflect this constrain in the analysis, we used not only a gray matter mask, but one that removes the area with variability in missing data.
