# Seed-based functional connectivity analysis

## Preprocessing

HCP pipeline + ICA-FIX (partial). Using A-P image only.

## First-level analysis: seed region connectivity to the whole brain

- Smoothing: 8mm full-width at half maximum (fwhm) to decrease the noise level in images, and reduce the discrepancy between individuals.
- Seeds:
  - ICBM left insula (self defined)
  - ICBM right insula (self defined)
  - ICBM index 161 cingulate (from myelin analysis)
  - [Difumo](https://parietal-inria.github.io/DiFuMo/) 64 regions component 4 posterior cingulate cortex (included for pipeline development purpose.)
- Procedure:
  - Extract average signal from the seed mask as the singular regressor, as the data was cleaned in the preprocessing.
  - Smooth the input image.
  - No HRF convolution on regressor. The regressor is derived directly from BOLD, this step is not needed.
  - Two runs of resting state scan in the same session are averaged.
  - A contrast of Typhoid > Placebo session was caculated per subject.
- software: [sbfc v0.4.6](https://github.com/htwangtw/sbfc/)

## Group level analysis

- General linear model (GLM): four regressors - sex, age, control, patient
  - Confounds: age and gender are regressed out from the model to account for their impact on results.
  - Control and patient regressors use 0 and 1 to indicate if a subject belongs to control or patient group
  - For input data and contrasts, please see the following section.
  - Gray matter mask: self defined to constrain the analysis in gray matter. See [`../atlas/README.md`](../atlas/README.md)
  - Thresholding: control of false positive rate at alpha = 0.001 (0.1% chance of declaring an inactive voxel, active, convert to z stats threshold 3.2), clusters smaller than 10 voxels are removed.
- software: [nilearn v0.7.1](https://nilearn.github.io/index.html)

### Seed-based connectivity: Patients vs Controls in Placebo session

- Input: first level functional connectivity map in placebol session
- Contrasts:
  - average activity of control
  - average activity of patients
  - patients > control
  - control > patients

### Seed-based connectivity: Patients vs Controls when Typhoid > Placebo

- Input: first level functional connectivity map contrast of typhoid session > placebol session
- Contrasts:
  - whole sample activity of typhoid > placebol contrast
  - whole sample activity of typhoid < placebol contrast
  - control sample activity of typhoid > placebol contrast
  - patients sample activity of typhoid > placebol contrast
  - patients > control of typhoid > placebol contrast
  - control > patients of typhoid > placebol contrast
