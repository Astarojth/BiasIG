# Tools

This directory contains helper utilities used to maintain the BiasIG prompt set and benchmark metadata.

## Contents

- `occhar.py`: helper logic for occupation and characteristic prompt maintenance
- `sr.py`: helper logic for social-relation prompt maintenance
- `weight.py`: helper logic for benchmark weighting metadata
- `human_eval_sheet.xlsx`: annotation sheet used during benchmark validation and analysis

## When to use these tools

Use the scripts in this folder when you need to:

- extend or revise the released prompt files
- regenerate supporting benchmark metadata after prompt edits
- update weighting files or intermediate maintenance artifacts

If you only want to reproduce the released benchmark, you do not need to run anything in this folder.
