import json
import os

import matplotlib.pyplot as plt

from marl_eval.plotting_tools.plotting import (
    aggregate_scores,
    performance_profiles,
    plot_single_task,
    probability_of_improvement,
    sample_efficiency_curves,
)
from marl_eval.utils.data_processing_utils import (
    create_matrices_for_rliable,
    data_process_pipeline,
)

ENV_NAME = "AllEnvs"
SAVE_PDF = True

data_dir = "merged_json_files/metrics_filtered_master_norm.json"
png_plot_dir = "plots/png/"
pdf_plot_dir = "plots/pdf/"

legend_map = {
    "mappo": "MAPPO",
    "mat": "MAT",
    "mam": "MAM",
}

##############################
# Read in and process data
##############################
METRICS_TO_NORMALIZE = []

with open(data_dir) as f:
    raw_data = json.load(f)

processed_data = data_process_pipeline(
    raw_data=raw_data, metrics_to_normalize=METRICS_TO_NORMALIZE
)

environment_comparison_matrix, sample_efficiency_matrix = create_matrices_for_rliable(
    data_dictionary=processed_data,
    environment_name=ENV_NAME,
    metrics_to_normalize=METRICS_TO_NORMALIZE,
)

# Create folder for storing plots
if not os.path.exists(png_plot_dir):
    os.makedirs(png_plot_dir)
if not os.path.exists(pdf_plot_dir):
    os.makedirs(pdf_plot_dir)

# Aggregate data over all environment tasks.
fig, _, _ = sample_efficiency_curves(  # type: ignore
    sample_efficiency_matrix,
    metric_name="mean_episode_return",
    metrics_to_normalize=METRICS_TO_NORMALIZE,
    legend_map=legend_map,
)
fig.figure.savefig(
    f"{png_plot_dir}all_envs_sample_efficiency_curve.png", bbox_inches="tight"
)
if SAVE_PDF:
    fig.figure.savefig(
        f"{pdf_plot_dir}all_envs_sample_efficiency_curve.pdf", bbox_inches="tight"
    )