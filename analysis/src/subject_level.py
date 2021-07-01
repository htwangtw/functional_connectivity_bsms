"""Run fist level seed base funtional connectivity analysis

Authors: Hao-Ting Wang
Date: May 18, 2021
"""
import json
import os
import sys
from pathlib import Path
from nilearn.reporting import make_glm_report

from sbfc import model as sm


seed = Path(sys.argv[1])
sub_id = sys.argv[2]
key = sys.argv[3]

# generate path for outputs
project_path = Path(__file__).parents[2]

with open(project_path / "analysis/scan_info.json", "r") as f:
    scan_info = json.load(f)
seed_name = seed.name.split(".")[0]
report_path = (
    project_path / f"results/subject_level/sub-{sub_id}_ses-{key}_seed-{seed_name}.html"
)
output_path = project_path / f"results/subject_level/sub-{sub_id}/ses-{key}/"
if not output_path.exists():
    os.makedirs(output_path)

items = scan_info[key][sub_id].copy()
print(key)
print(sub_id)

# fit GLM
subject_lvl, subject_lvl_contrast = sm.subject_level(
    str(seed),
    items["func"],
    subject_label=sub_id,
    write_dir=str(output_path),
    verbose=3,
    n_jobs=-1,
    smoothing_fwhm=8.0,
    drift_model=None,
    hrf_model=None,
    mask_img=None,
)

# fit generate report
make_glm_report(
    subject_lvl,
    contrasts=subject_lvl_contrast,
    plot_type="glass",
    title=f"sub-{sub_id}_ses-{key}_seed-{seed_name}",
    alpha=0.001,
    height_control="bonferroni",
).save_as_html(report_path)
