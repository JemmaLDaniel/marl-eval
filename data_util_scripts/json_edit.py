import json
import os

def process_seed(seed_data):
    # Extract the 'absolute_metrics' which we don't want to change
    absolute_metrics = seed_data.pop("absolute_metrics")
    
    # Filtering out even step entries
    odd_steps = {k: v for k, v in seed_data.items() if k.startswith('step_') and int(k.split('_')[1]) % 2 != 0}
    
    # Sorting the steps by their original order
    sorted_steps = sorted(odd_steps.items(), key=lambda x: int(x[0].split('_')[1]))
    
    # Renaming steps sequentially
    new_steps = {f"step_{i}": v for i, (k, v) in enumerate(sorted_steps)}
    
    # Clearing seed data and updating it
    seed_data.clear()
    seed_data.update({"absolute_metrics": absolute_metrics})
    seed_data.update(new_steps)
    
    return seed_data

def process_json(data):

    # scenarios = ["tiny-4ag", "small-4ag"]  # rware mamba_mat
    # scenarios = ["tiny-4ag", "small-4ag", "tiny-2ag"]  # rware ff_mappo
    scenarios = ["15x15-4p-3f","10x10-3p-3f","2s-8x8-2p-2f-coop", "8x8-2p-2f-coop"]  # lbf mamba_mat
    # scenarios = ["27m_vs_30m", "2s3z", "3s5z", "3s5z_vs_3s6z", "6h_vs_8z", "3s_vs_5z", "smacv2_5_units", "10m_vs_11m"]  # smax mamba_mat
    # scenarios = ["27m_vs_30m", "2s3z", "3s5z", "3s5z_vs_3s6z", "6h_vs_8z", "3s_vs_5z", "smacv2_5_units", "10m_vs_11m", "5m_vs_6m", "smacv2_10_units", "smacv2_20_units"]  # smax ff_mappo

    for scenario in scenarios:
        # Retrieving the 'mamba_mat' dictionary
        # mamba_mat = data["RobotWarehouse"][scenario]["mamba_mat"]
        # mamba_mat = data["RobotWarehouse"][scenario]["ff_mappo"]
        mamba_mat = data["LevelBasedForaging"][scenario]["mamba_mat"]
        # mamba_mat = data["Smax"][scenario]["mamba_mat"]
        # mamba_mat = data["Smax"][scenario]["ff_mappo"]
        
        # Processing each seed
        for seed in list(mamba_mat.keys()):
            if seed.startswith('seed_'):
                mamba_mat[seed] = process_seed(mamba_mat[seed])
    
    return data

def save_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# Read the input JSON data from the file
with open("concatenated_json_files/metrics.json", 'r') as f:
    data = json.load(f)

processed_data = process_json(data)

# Ensure the directory exists
output_dir = 'concatenated_json_files'
os.makedirs(output_dir, exist_ok=True)

# Define the output file path
output_file_path = os.path.join(output_dir, 'metrics_new.json')

# Save the processed JSON data to the specified file
save_json(processed_data, output_file_path)

print(f"Processed JSON file saved to: {output_file_path}")