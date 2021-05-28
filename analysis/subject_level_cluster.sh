# subject level seed-based conntectivity maps
# always execute this script at
# /research/cisc1/projects/eccles_mcpf/functional_connectivity
#
#
#!/bin/bash
#$ -N first_level
#$ -o /research/cisc1/projects/eccles_mcpf/functional_connectivity/logs
#$ -j y
#$ -pe openmp 4
#$ -l m_mem_free=4G
#$ -t 1-72
#$ -tc 36

i=$((SGE_TASK_ID - 1))

PROJECT_PATH=/research/cisc1/projects/eccles_mcpf/functional_connectivity
SUBJECT_LIST=($(awk -F"," 'NR>1{print $1}' ${PROJECT_PATH}/analysis/group_design.csv))
SUBJECT=${SUBJECT_LIST[${i}]}

# path to NIFTI mask for seeds
INSULA=${PROJECT_PATH}/atlas/icbm_insula.nii.gz
PCC=${PROJECT_PATH}/atlas/difumo64_pcc.nii.gz

module add sge
module add easybuild/software
module add Anaconda3/2020.02

source activate sbfc

# Add more seeds like this:
# input arguments of subject_level.py: seed, CISC ID, placebo/typhoid session
# SEED=${PROJECT_PATH}/atlas/my_roi.nii.gz
# python "${PROJECT_PATH}/analysis/src/subject_level.py" ${SEED} ${SUBJECT} placebo
# python "${PROJECT_PATH}/analysis/src/subject_level.py" ${SEED} ${SUBJECT} typhoid

python "${PROJECT_PATH}/analysis/src/subject_level.py" ${INSULA} ${SUBJECT} placebo
python "${PROJECT_PATH}/analysis/src/subject_level.py" ${INSULA} ${SUBJECT} typhoid
python "${PROJECT_PATH}/analysis/src/subject_level.py" ${PCC} ${SUBJECT} placebo
python "${PROJECT_PATH}/analysis/src/subject_level.py" ${PCC} ${SUBJECT} typhoid

python "${PROJECT_PATH}/scripts/src/session_paired_t.py" difumo64_pcc ${SUBJECT}
python "${PROJECT_PATH}/scripts/src/session_paired_t.py" icbm_insula ${SUBJECT}

