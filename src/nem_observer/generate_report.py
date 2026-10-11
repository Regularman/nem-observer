import json
import pandas as pd
import matplotlib.pyplot as plt
import math

file_path = "./src/nem_observer/data/08-29-08-30-nem_data-2026.json"

# Read the JSON file outputted by get_data.py
with open(file_path, "r") as f:
    raw_data = json.load(f)

## Plot the power outputs for each battery in the data
unit_codes = list(raw_data.keys())  # This will show the unit codes in the data
print(f"There are {len(unit_codes)} batteries operating in the NEM, in NSW")

for unit in unit_codes:
    plt.figure(figsize=(12, 6))
    timestamps = [timestamp for timestamp in raw_data[unit]['power'].keys()]
    values = [value for value in raw_data[unit]['power'].values()]

    plt.plot(timestamps, values, marker='', linestyle='-', linewidth=1, color='red', label=unit)
    plt.title(f"Power Output for Battery {unit} in NSW")

    # Snap y-axis to the next highest 10s
    y_max = math.ceil(max(values) / 10) * 10
    y_min = math.floor(min(values) / 10) * 10 if min(values) < 0 else 0
    plt.ylim(y_min, y_max)
    plt.ylabel("Power Output (MW)")

    # 2. Turn on minor ticks and configure both grids
    plt.minorticks_on()
    plt.grid(visible=True, which="major", linestyle="-", linewidth=0.5, color="gray")
    plt.grid(visible=True, which="minor", linestyle=":", linewidth=0.25, color="lightgray")

    plt.xlim(timestamps[0], timestamps[-1])
    plt.xticks(
        ticks=timestamps[::12],  # Tick positions
        labels=timestamps[::12],  # Tick text labels
        rotation=45,
    )
    plt.tight_layout()
    plt.savefig(f"./src/nem_observer/plots/{unit}_power_output.png")
    plt.close()

