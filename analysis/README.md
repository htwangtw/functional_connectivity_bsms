# Analysis directory overview

```bash
analysis/
├── src
│   ├── create_roi.py
│   ├── extract_stats.py
│   ├── group_placebo_twosamplet.py
│   ├── group_twosamplet_interaction.py
│   ├── label_runs.py
│   ├── session_paired_t.py
│   └── subject_level.py
├── group_design.csv
├── python_qsub_wrapper.sh
├── README.md
├── scan_info.json
└── subject_level_cluster.sh
```

Each script in `src/` has a summary of what it does.

For techncal summary, please see [`methods.md`](./methods.md)

## Run the existing scripts

- Get the subjects ready

```bash
cd /research/cisc1/projects/eccles_mcpf/functional_connectivity/analysis
python src/label_runs.py
```

- run first and second level analysis on the cluster

```bash
cd /research/cisc1/projects/eccles_mcpf/functional_connectivity/analysis
qsub subject_level_cluster.sh
```

- run any group level analysis on the cluster

```bash
cd /research/cisc1/projects/eccles_mcpf/functional_connectivity/analysis
qsub python_qsub_wrapper.sh src/group_placebo_twosamplet.py
qsub python_qsub_wrapper.sh src/group_twosamplet_interaction.py
```

- Extract significant clusters of the two analysis above

```bash
cd /research/cisc1/projects/eccles_mcpf/functional_connectivity/analysis
python extract_stats.py
```

## Notes from Marisa to Hao-Ting

- Subjects to exclude: 18587, 20059, 22147
