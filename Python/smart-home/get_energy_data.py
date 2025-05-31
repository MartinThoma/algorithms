"""Read data from a Tasmota device and save it to a CSV file."""

import requests
import csv
import time
from datetime import datetime

TASMOTA_IP = "http://192.168.178.30"
CMD = "Status 8"
CSV_FILE = "energy_data.csv"
POLL_INTERVAL = 1  # seconds

def fetch_data():
    try:
        response = requests.get(f"{TASMOTA_IP}/cm", params={"cmnd": CMD}, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[{datetime.now()}] Error: {e}")
        return None

def extract_data(json_data):
    try:
        sns = json_data.get("StatusSNS", {})
        timestamp = sns.get("Time")
        ehz = sns.get("eHZ", {})
        return {
            "timestamp": timestamp,
            "E_in": ehz.get("E_in"),
            "E_out": ehz.get("E_out"),
            "Power": ehz.get("Power")
        }
    except Exception as e:
        print(f"Error extracting data: {e}")
        return None

def write_csv_header():
    # Check if the file exists and write header only if it doesn't
    try:
        with open(CSV_FILE, mode='r') as file:
            return  # File exists, do nothing
    except FileNotFoundError:
        # File does not exist, create it and write the header
        print(f"Creating new CSV file: {CSV_FILE}")
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["timestamp", "E_in", "E_out", "Power"])
        writer.writeheader()

def append_to_csv(data):
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["timestamp", "E_in", "E_out", "Power"])
        writer.writerow(data)

if __name__ == "__main__":
    print("Starting data collection...")
    write_csv_header()
    try:
        while True:
            raw_data = fetch_data()
            if raw_data:
                parsed_data = extract_data(raw_data)
                if parsed_data:
                    append_to_csv(parsed_data)
                    print(f"[{parsed_data['timestamp']}] Wrote: {parsed_data}")
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("\nStopped by user.")
