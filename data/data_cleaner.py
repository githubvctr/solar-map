import pandas as pd
import json

# Load installed capacities data
raw = pd.read_csv("data/raw/Installed_capacities_per_municipalities_2024_Q2.csv", sep=';', header=3)

# Pivot the data to get one row per municipality
pivoted = raw.pivot(index='Regio\'s', columns='Onderwerp', values='2024 eerste helft*').reset_index()
pivoted = pivoted.rename(columns={
    "Regio's": "Name",
    "Opgesteld vermogen van zonnepanelen": "Opgesteld vermogen van zonnepanelen (kW)",
    "Installaties": "Installaties (aantal)"
})

# Convert numeric columns
pivoted["Opgesteld vermogen van zonnepanelen (kW)"] = pd.to_numeric(pivoted["Opgesteld vermogen van zonnepanelen (kW)"].str.replace('.', '', regex=False), errors='coerce')
pivoted["Installaties (aantal)"] = pd.to_numeric(pivoted["Installaties (aantal)"].str.replace('.', '', regex=False), errors='coerce')

# Load municipalities geojson file
with open("data/raw/municipalities.geojson") as f:
    geo = json.load(f)

# Extract name and coordinates
muni_data = []
for feature in geo["features"]:
    name = feature["properties"]["name"]
    coords = feature["geometry"]["coordinates"]
    muni_data.append({"Name": name, "Coordinates": coords})
muni_df = pd.DataFrame(muni_data)

# Merge on Name
merged = pd.merge(pivoted, muni_df, on="Name", how="inner")

# Select and order columns
final = merged[["Name", "Opgesteld vermogen van zonnepanelen (kW)", "Installaties (aantal)", "Coordinates"]]

# Write to CSV
final.to_csv("data/processed/2024_solar_data_and_coordinates_NL.csv", index=False)