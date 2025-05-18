import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Example data
device_data = {
    # Gemessen
    "Heizen\nKlimaanlage": 2.6,
    "Kühlschrank": 0.43,
    "Heizungspumpe": 0.42,
    "TV": 0.4,
    "Saug-Wisch-Roboter (2x Q-Revo)": 0.4,
    "Büro": 0.37,
    "Spülmaschine\n(täglich)": 0.75,
    # Geschätzt (hohe sicherheit)
    "Fritz!Box 7530\n(Schätzung)": 0.3,
    "Waschmaschine\n(2x alle 5 Tage)": 0.3,
    # Geschätzt (geringe Sicherheit)
    "Kochen\n(Herd, Ofen, Wasserkocher, Heißluftfritteuse)": 2.0,
    "Licht\n(8x 8W für 5h)": 0.3,
    "Kameras\n(5x)": 0.8, 
}

# Sort data
items = sorted(device_data.items(), key=lambda x: x[1], reverse=True)
df = pd.DataFrame(items, columns=["Device", "Usage_kWh_per_day"])

# Normalize values for color mapping
norm = (df['Usage_kWh_per_day'] - df['Usage_kWh_per_day'].min()) / (df['Usage_kWh_per_day'].max() - df['Usage_kWh_per_day'].min())
cmap = plt.cm.coolwarm
colors = [cmap(val) for val in norm]

# Plot
sns.set(style="whitegrid")
plt.figure(figsize=(8, 5))
bars = plt.barh(df["Device"], df["Usage_kWh_per_day"], color=colors)

plt.xlabel(f'Energy Usage (kWh per day, total: {sum(device_data.values()):.2f} kWh)')
plt.ylabel('')
plt.title('Täglicher Energieverbrauch nach Geräten\nMärz 2025')
plt.gca().invert_yaxis()
plt.tight_layout()

# Save and show
plt.savefig('energy_usage_by_device.png', dpi=300)
plt.show()
