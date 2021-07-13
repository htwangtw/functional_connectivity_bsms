# python qsub wrapper for any generic python script in this project
# always execute this script at
# /research/cisc1/projects/eccles_mcpf/functional_connectivity/analysis
#
#!/bin/bash
#$ -N beta
#$ -o /research/cisc1/projects/eccles_mcpf/functional_connectivity/logs
#$ -j y
#$ -pe openmp 8
#$ -l m_mem_free=4G

module add sge
module add easybuild/software
module add Anaconda3/2020.02
source activate sbfc

PROJECT_PATH=/research/cisc1/projects/eccles_mcpf/functional_connectivity

# significant results only
python ${PROJECT_PATH}/analysis/src/extract_stats.py \
    difumo64_pcc ses-placebo_patient_wrt_control control_wrt_patient
python ${PROJECT_PATH}/analysis/src/extract_stats.py \
    difumo64_pcc double_twosample_t placebol_wrt_typhoid
python ${PROJECT_PATH}/analysis/src/extract_stats.py \
    icbm_insula-R double_twosample_t placebol_wrt_typhoid
