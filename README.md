# Functional connectivity analysis

## How to use python

1. load anaconda

`module add Anaconda3/2020.02`

2. install all the dependencies if doing the analysis for the first time:

`conda env create -f /research/cisc1/projects/eccles_mcpf/functional_connectivity/environment.yml`

3. In the future, activate the environment for any analysis:

`conda activate sbfc`


## Run the existing scripts

1. Get the Subjects ready

```
cd /research/cisc1/projects/eccles_mcpf/functional_connectivity/analysis
python src/label_runs.py
```

2. run first and second level analysis on the cluster

```
cd /research/cisc1/projects/eccles_mcpf/functional_connectivity/analysis
qsub subject_level_cluster.sh
```

3. run any group level analysis on the cluster
```
cd /research/cisc1/projects/eccles_mcpf/functional_connectivity/analysis
qsub python_qsub_wrapper.sh src/group_placebo_twosamplet.py
qsub python_qsub_wrapper.sh src/group_twosamplet_interaction.py
```

4. Extract significant clusters of the two analysis above
```
cd /research/cisc1/projects/eccles_mcpf/functional_connectivity/analysis
python extract_stats.py
```

## Notes from Marisa to Hao-Ting
- Subjects to exclude:
```
18587
20059
22147
```

## References
https://nilearn.github.io/auto_examples/03_connectivity/plot_seed_to_voxel_correlation.html#sphx-glr-auto-examples-03-connectivity-plot-seed-to-voxel-correlation-py
