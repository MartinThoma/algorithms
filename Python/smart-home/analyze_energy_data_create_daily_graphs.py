import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.dates as mdates

# Load CSV
df = pd.read_csv("energy_data.csv", parse_dates=["timestamp"])

# Remove rows where the timestamp is before 2024
df = df[df["timestamp"] > "2024-01-01"]

df.set_index("timestamp", inplace=True)

# Interpolate to get uniform 60-minute intervals
df = df.resample("60min").mean().interpolate("time")

# Compute energy usage from cumulative E_in
df["E_usage"] = df["E_in"].diff()

# Drop first row with NaN after diff
df = df.dropna(subset=["E_usage"])

# Create output directory
output_dir = "daily_graphs"
os.makedirs(output_dir, exist_ok=True)

# Plot energy usage per day
for date, group in df.groupby(df.index.date):
    # Create a full 60-minute timestamp index for the entire day
    day_start = pd.Timestamp(date)
    day_end = day_start + pd.Timedelta(days=1) - pd.Timedelta(minutes=60)
    full_index = pd.date_range(start=day_start, end=day_end, freq="60min")

    # Reindex to ensure full 24h, interpolating missing values if needed
    group_day = group.reindex(full_index)
    group_day["E_usage"] = group_day["E_usage"].interpolate("time")

    # Plot
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(group_day.index, group_day["E_usage"], width=0.01, align="center", color="skyblue")

    ax.set_title(f"Energy Usage on {date}")
    ax.set_xlabel("Time of Day")
    ax.set_ylabel("Energy Usage (Wh or kWh)")
    ax.set_ylim(0, 1.2)  # Y-axis limit = 1 kWh
    ax.grid(True)

    # Format x-axis to show only hour and minute
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.set_xlim([day_start, day_start + pd.Timedelta(days=1)])
    plt.xticks(rotation=45)

    # Save figure
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"energy_usage_{date}.png"))
    plt.close()