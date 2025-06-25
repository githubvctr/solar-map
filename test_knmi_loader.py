from src.knmi_loader import download_latest_dataframe

df = download_latest_dataframe()
print(df.head())
