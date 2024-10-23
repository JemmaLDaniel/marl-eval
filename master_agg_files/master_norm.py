import json

def remove_win_rate(data):
    if isinstance(data, dict):
        for key in list(data.keys()):
            if key == "win_rate":
                del data[key]
            else:
                data[key] = remove_win_rate(data[key])
    elif isinstance(data, list):
        return [remove_win_rate(item) for item in data]
    return data


def process_json_data(input_file="merged_json_files/metrics.json", output_file="merged_json_files/metrics_filtered_master_norm.json"):
    # Load the JSON data
    with open(input_file, "r") as f:
        data = json.load(f)

    # Remove win_rate from the data
    data = remove_win_rate(data)

    # Find min and max values for each environment
    env_min_max = {}
    for env_name, env_data in data.items():
        all_returns = []
        for task_data in env_data.values():
            for algo_data in task_data.values():
                for seed_data in algo_data.values():
                    # Add absolute metrics
                    if "absolute_metrics" in seed_data:
                        all_returns.extend(
                            seed_data["absolute_metrics"].get("mean_episode_return", [])
                        )

                    # Add step metrics
                    for step_data in seed_data.values():
                        if (
                            isinstance(step_data, dict)
                            and "mean_episode_return" in step_data
                        ):
                            all_returns.extend(step_data["mean_episode_return"])

        if all_returns:
            env_min_max[env_name] = (min(all_returns), max(all_returns))
        else:
            print(
                f"Warning: No valid mean_episode_return values found for environment {env_name}"
            )
            env_min_max[env_name] = (0, 1)  # Default range if no data

        # Manually adding known env min-max values
        if env_name == "Smax":
            print(f"Setting min-max values for {env_name} to (0, 2)")
            env_min_max[env_name] = (0, 2)
        elif env_name == "LevelBasedForaging":
            print(f"Setting min-max values for {env_name} to (0, 1)")
            env_min_max[env_name] = (0, 1)
        elif env_name == "RobotWarehouse":
            print(f"Setting min value for {env_name} to (0,)")
            env_min_max[env_name] = (0, env_min_max[env_name][1])  # keep the max as is

    # Min-max normalize the data
    for env_name, env_data in data.items():
        env_min, env_max = env_min_max[env_name]
        if env_min == env_max:
            print(
                f"Warning: All mean_episode_return values are the same for environment {env_name}"
            )
            env_max = env_min + 1  # Avoid division by zero

        for task_data in env_data.values():
            for algo_data in task_data.values():
                for seed_data in algo_data.values():
                    # Normalize absolute metrics
                    if "absolute_metrics" in seed_data:
                        seed_data["absolute_metrics"]["mean_episode_return"] = [
                            (x - env_min) / (env_max - env_min)
                            for x in seed_data["absolute_metrics"].get(
                                "mean_episode_return", []
                            )
                        ]

                    # Normalize step metrics
                    for step_data in seed_data.values():
                        if (
                            isinstance(step_data, dict)
                            and "mean_episode_return" in step_data
                        ):
                            step_data["mean_episode_return"] = [
                                (x - env_min) / (env_max - env_min)
                                for x in step_data["mean_episode_return"]
                            ]

    # Combine all environments under 'AllEnvs'
    all_envs_data = {}
    for env_data in data.values():
        for task_name, task_data in env_data.items():
            if task_name not in all_envs_data:
                all_envs_data[task_name] = {}
            all_envs_data[task_name].update(task_data)

    # Create the final output structure
    output_data = {"AllEnvs": all_envs_data}

    # Save the processed data to a new JSON file
    with open(output_file, "w") as f:
        json.dump(output_data, f, indent=2)

    print(f"Processed data saved to {output_file}")

process_json_data()  # have to run in debug mode??