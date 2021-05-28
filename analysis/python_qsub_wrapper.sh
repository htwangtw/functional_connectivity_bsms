# python qsub wrapper for any generic python script in this project
# always execute this script at
# /research/cisc1/projects/eccles_mcpf/functional_connectivity/analysis
#
#!/bin/bash
#$ -N pythonjob
#$ -o /research/cisc1/projects/eccles_mcpf/functional_connectivity/logs
#$ -j y
#$ -pe openmp 8
#$ -l m_mem_free=4G

module add sge
module add easybuild/software
module add Anaconda3/2020.02
source activate sbfc

PROJECT_PATH=/research/cisc1/projects/eccles_mcpf/functional_connectivity

python "${PROJECT_PATH}/analysis/${1}"

