# MARL-eval for MAM

Note: I did do some finagling with the number of evaluations between LBF, SMAX and RWARE. In particular, I downsampled where necessary using `json_edit.py`. I also had to manually set some colours when generating performance profiles.

The final plots for the MAM paper are inside `plots_final`.

The final concatenated data files are as follows:
- `concatenated_json_files_ablation_delta`
- `concatenated_json_files_ablation_latent_state`
- `concatenated_json_files_lbf`
- `concatenated_json_files_rware`
- `concatenated_json_files_smax`