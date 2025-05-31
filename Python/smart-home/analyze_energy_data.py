import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt


def get_df(filename: Path) -> pd.DataFrame:
    columns = ["timestamp", "E_in", "E_out", "Power"]
    try:
        df = pd.read_csv(filename, parse_dates=["timestamp"])
        return df
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return pd.DataFrame(columns=columns)
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return pd.DataFrame(columns=columns)


def get_pv_produced_energy(filename: Path) -> pd.DataFrame:
    columns = ["timestamp", "power in Watt"]
    try:
        df = pd.read_csv(filename, parse_dates=["timestamp"])
        return df
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return pd.DataFrame(columns=columns)
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return pd.DataFrame(columns=columns)

def preprocess_df_pv(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    # Rename columns for consistency
    df.rename(columns={"power in Watt": "Power_PV"}, inplace=True)

    # Convert timestamp to datetime if not already
    if not pd.api.types.is_datetime64_any_dtype(df["timestamp"]):
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Ensure Power is float
    df["Power_PV"] = pd.to_numeric(df["Power_PV"], errors="coerce")

    # Scale to kWh
    df["Power_PV"] = df["Power_PV"] / 1000  # Convert from Watt to kW

    # Remove rows with NaN values in critical columns
    df = df.dropna(subset=["timestamp", "Power_PV"])
    return df



def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    # Remove rows where the timestamp is before 2024
    df = df[df["timestamp"] > "2024-01-01"]
    # Remove rows with NaN values in critical columns
    df = df.dropna(subset=["timestamp", "E_in", "E_out", "Power"])

    if df.empty:
        return df

    df = df.sort_values(by="timestamp")

    # Remove the first (partial) day
    first_timestamp = df["timestamp"].iloc[0]
    df = df[df["timestamp"].dt.date != first_timestamp.date()]

    # Remove the last (partial) day
    last_timestamp = df["timestamp"].iloc[-1]
    df = df[df["timestamp"].dt.date != last_timestamp.date()]

    return df


def main():
    filename = Path("energy_data.csv")
    df = get_df(filename)
    df = clean_df(df)

    df_pv = get_pv_produced_energy(Path("pv_produced_energy.csv"))
    pf_pv = preprocess_df_pv(df_pv)

    if df.empty:
        return
    if pf_pv.empty:
        print("No PV data available, skipping merging.")
        return

    # Merge into df:
    df = df.merge(pf_pv, on="timestamp", how="left", suffixes=("", "_pv"))

    print("Data summary:")
    print(f"Timestamp range: {df['timestamp'].min()} to {df['timestamp'].max()} ({len(df)} records)")

    # E_in is what my solar panels produce, E_out is what I use from the grid.
    # The values is the one of the meter, so it is cumulative.

    # Calculate total energy used in the range by using the oldest and newest E_out values:
    if len(df) < 2:
        print("Not enough data to calculate total energy used.")
    else:
        df = df.sort_values(by="timestamp")
        df["E_in"] = df["E_in"].astype(float)
        df["E_out"] = df["E_out"].astype(float)
        
        # Total energy produced and used by subtracting the first and last values
        total_energy_produced = df["E_out"].iloc[-1] - df["E_out"].iloc[0]
        total_energy_used = df["E_in"].iloc[-1] - df["E_in"].iloc[0]

        # Total time range in hours
        time_range = (df["timestamp"].max() - df["timestamp"].min()).total_seconds() / 3600


    print(f"Total Energy Produced: {total_energy_produced:.2f} kWh ({total_energy_produced * 24 / time_range:.2f} kWh/day average)")
    print(f"Total Energy Used    : {total_energy_used:.2f} kWh ({total_energy_used * 24 / time_range:.2f} kWh/day average)")
    print(f"Power Range: {df['Power'].min()} to {df['Power'].max()} Watt (negative means solar production, positive means grid consumption)")
    print(df.describe())

    # Get a dataframe that contains the energy used/produced (not cummulative)
    # To avoid that the 
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)
    df_resampled = df.resample("60min").mean().dropna()
    df_resampled["E_in"] = df_resampled["E_in"].diff().fillna(0)
    df_resampled["E_out"] = df_resampled["E_out"].diff().fillna(0)
    df_resampled["Power"] = df_resampled["Power"].diff().fillna(0)

    df_resampled["date"] = df_resampled.index.date
    df_resampled["hour"] = df_resampled.index.hour
    df_resampled["hour_decimal"] = df_resampled.index.hour + df_resampled.index.minute / 60
    df_resampled.reset_index(inplace=True)

    print(df_resampled.describe())

    plt.figure(figsize=(12, 6))
    sns.set_theme(style="whitegrid")

    show_lines_per_day = False
    show_aggregated = True

    if show_lines_per_day:
        sns.lineplot(data=df_resampled, x="hour_decimal", y="E_out", hue="date", palette="viridis", legend=None)
        plt.title("Energy Usage Over Time")
        plt.xlabel("Hour of the Day")
        plt.ylabel("Energy Used (kWh)")
        plt.xticks(range(0, 24), [f"{i}:00" for i in range(24)], rotation=45)
        plt.tight_layout()
        plt.show()

    if show_aggregated:
        sns.lineplot(data=df_resampled, x="hour", y="E_out", label="Energy to grid (kWh)", color="orange")
        sns.lineplot(data=df_resampled, x="hour", y="E_in", label="Energy from grid (kWh)", color="blue")
        sns.lineplot(data=df_resampled, x="hour", y="Power_PV", label="Energy Produced (kWh)", color="yellow")
        plt.title("Energy Usage and Production Over Time")      
        plt.xlabel("Hour of the Day")
        plt.ylabel("Energy (kWh)")
        plt.xticks(range(0, 24), [f"{i}:00" for i in range(24)], rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    main()
