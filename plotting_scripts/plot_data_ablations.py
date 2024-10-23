import json
import os

import matplotlib.pyplot as plt

from marl_eval.plotting_tools.plotting import (
    plot_single_task,
)
from marl_eval.utils.data_processing_utils import (
    create_matrices_for_rliable,
    data_process_pipeline,
)

ENV_NAME = "RobotWarehouse"
SAVE_PDF = True

data_dir = "./concatenated_json_files_ablations/metrics.json"
png_plot_dir = "./plots/png/"
pdf_plot_dir = "./plots/pdf/"

legend_map = {
    "mat": "MAT",
    "mat_mamba_lns_v2": "Full Mamba-MAT",
    "mat_mamba_v2_encoder": "Mamba sequential encoder",
    "mat_mamba_v2_self_attn": "Mamba sequential self-attention",
    "mat_mamba_v2_decoder": "Mamba decoder",
    "mat_mamba_v2_cross_attn": "Mamba cross-attention",
    "mat_bimamba_v2": "Full BiMamba-MAT",
}

##############################
# Read in and process data
##############################
METRICS_TO_NORMALIZE = ["mean_episode_return"]
# METRICS_TO_NORMALIZE = []

with open(data_dir) as f:
    raw_data = json.load(f)

processed_data = data_process_pipeline(
    raw_data=raw_data,
    metrics_to_normalize=METRICS_TO_NORMALIZE,
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

##############################
# Plot episode return data
##############################

# Get all tasks
tasks = list(processed_data[ENV_NAME.lower()].keys())

# Aggregate data over a single task
for task in tasks:
    title = "Mamba in the multi-agent transformer on RobotWarehouse small-4ag"

    fig = plot_single_task(
        processed_data=processed_data,
        environment_name=ENV_NAME,
        task_name=task,
        metric_name="mean_episode_return",
        metrics_to_normalize=METRICS_TO_NORMALIZE,
        legend_map=legend_map,
        title=title,
    )

    fig.figure.savefig(
        f"{png_plot_dir}rware{task}_agg_return_ablations.png", bbox_inches="tight"
    )
    if SAVE_PDF:
        fig.figure.savefig(
            f"{pdf_plot_dir}rware{task}_agg_return_ablations.pdf", bbox_inches="tight"
        )

    # Close the figure object
    plt.close(fig.figure)
