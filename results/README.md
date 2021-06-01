# What's in the results directory

General organisation:

```
results/
├── group_level/
│   ├── <analysis_name>/
│   │   ├── <contrast_name>_thresh_zstat.nii.gz
│   │   ├── <contrast_name>_zstat.nii.gz
│   │   ├── inputs.csv
│   │   └── <analysis_type>_design-matrix.csv
│   ├── <analysis_name>_<contrast_name>_cluster_label.nii.gz
│   └── insula_connectivity_beta_weight.csv
├── subject_level/
│   ├── sub-<cisc_id>/
│   │   ├── ses-<session>/
│   │   │   ├── <seed_name>_effect_size.nii.gz
│   │   │   ├── <seed_name>_effect_variance.nii.gz
│   │   │   ├── <seed_name>_p_value.nii.gz
│   │   │   ├── <seed_name>_stat.nii.gz
│   │   │   └── <seed_name>_z_score.nii.gz
│   │   └── <seed_name>_typhoid_wrt_placebo_effect_size.nii.gz
│   └── sub-<cisc_id>_ses-<session>_seed-<seed_name>.html
├── <analysis_name>.html
└── README.md

```

Group level results are `group_level/<analysis_name>.html` for quick access.
Significant custer label mask: `group_level/<analysis_name>_<contrast_name>_cluster_label.nii.gz`.
Find the relevant threshould stats map: `group_level/<analysis_name>/<contrast_name>_thresh_zstat.nii.gz`
Use **threshold stats map** for visualisation.

For significant clusters of all analysis, the beta-weight (coefficient scores from the relevant first level contrast `<seed_name>_effect_size.nii.gz`) are stored in `group_level/insula_connectivity_beta_weight.csv`. This is conceptually equivilant to [`FSL featquery`](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FEAT/UserGuide#Featquery_-_FEAT_Results_Interrogation)

These results can be used for further analysis, such as comparing between subjects, correlation with other variables.
