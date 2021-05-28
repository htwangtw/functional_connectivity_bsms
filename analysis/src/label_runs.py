'''Make sure the placebo and typhoid scans are labeled correctly.'''
import json
from pathlib import Path
import pandas as pd
import warnings


project_path = Path(__file__).parents[1]
base_path = Path('/research/cisc1/projects/eccles_mcpf/hcpdata76')

def find_run_no(typhoid_info):
    ''''
    pacbol or typhoid: 0 vs 1
    participant visit 1: file name 1, 2; visit 2:file name3, 4
    '''
    visit_info = {'Visit_1': ['1', '2'], 'Visit_2': ['3', '4']}
    if typhoid_info['Visit_1'] == 1:
        vac, plac = visit_info['Visit_1'], visit_info['Visit_2']
    if typhoid_info['Visit_2'] == 1:
        vac, plac = visit_info['Visit_2'], visit_info['Visit_1']
    return {'placebo': plac, 'typhoid': vac}

def get_path(subject_id, i):
    nii_path = base_path / f'{subject_id}/MNINonLinear/Results/rfMRI_REST{i}_AP/rfMRI_REST{i}_AP_hp2000_clean.nii.gz'
    if nii_path.exists():
        return str(nii_path), str(nii_path.parent / "Movement_Regressors.txt")
    else:
        warnings.warn(UserWarning('path doesn\'t exist.', str(nii_path)))
        return None, None

def flatten_list(_2d_list):
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list:
            # If the element is of type list, iterate through the sublist
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list

participants = pd.read_csv(project_path / 'sourcedata/participant_info.csv', skipinitialspace=True)

# test with 4 subjects
# participants = participants.iloc[:1, :]

# parse subject info
base_path = Path('/research/cisc1/projects/eccles_mcpf/hcpdata76')
scan_info = {'placebo':{}, 'typhoid':{},}
missing = set()
for idx, row in participants.iterrows():
    subject_id = row['CISC']
    if subject_id not in [18525, 20059, 22147]:
        typhoid_info = row.loc['Visit_1':].to_dict()
        run_info = find_run_no(typhoid_info)
        nii_path = base_path / f'{subject_id}/MNINonLinear/Results/'

        for key in run_info:
            cur_ses = {'func': [], 'confound': []}
            for i, run in enumerate(run_info[key]):
                func, conf = get_path(subject_id, run)
                if func:
                    cur_ses['func'].append(func)
                    cur_ses['confound'].append(conf)
            if None in flatten_list(cur_ses['func']):
                missing.add(idx)
            else:
                scan_info[key][subject_id] = cur_ses
    else:
        missing.add(idx)

# clean up and update group design
with open(project_path / 'analysis/scan_info.json', 'w') as f:
    json.dump(scan_info, f, indent=2)

participants = participants.drop(index=missing, columns=['MCPF ', 'Visit_1', 'Visit_2'])
participants = participants.rename(columns={'CISC': 'subject_label', 'Group': 'patient'})
participants['control'] = 1 - participants['patient']
participants.to_csv(project_path / 'analysis/group_design.csv', index=False)

