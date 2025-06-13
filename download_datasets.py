#%%
from pathlib import Path
import argparse
import os
import requests
import pandas as pd

# Credentials and URLs hardcoded from "https://github.com/karwester/behavioural-finance-task"
GITHUB_CSV_URL = (
    "https://raw.githubusercontent.com/karwester/behavioural-finance-task/"
    "main/personality.csv"
)

SUPABASE_URL = "https://pvgaaikztozwlfhyrqlo.supabase.co"
API_KEY = os.getenv(
    "SUPABASE_API_KEY",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6"
    "InB2Z2FhaWt6dG96d2xmaHlycWxvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc4NDE2"
    "MjUsImV4cCI6MjA2MzQxNzYyNX0.iAqMXnJ_sJuBMtA6FPNCRcYnKw95YkJvY3OhCIZ77vI",
)
ASSETS_ENDPOINT = f"{SUPABASE_URL}/rest/v1/assets?select=*"

# Download personality dataset
print("Downloading personality dataset from GitHub...")
df_personality = pd.read_csv(GITHUB_CSV_URL)
df_personality.to_csv("personality.csv", index=False)

# Set up headers for Supabase API requests
headers = {
        "apikey": API_KEY,
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json",
    }

# Download assets dataset
print("Downloading assets dataset from Supabase...")
resp = requests.get(ASSETS_ENDPOINT, headers=headers, timeout=30)
resp.raise_for_status()
data = resp.json()
df_assets = pd.DataFrame(data)
df_assets.to_csv("assets.csv", index=False)

# Merge datasets on the "_id" column
merged_df = pd.merge(df_personality, df_assets, on="_id", how="outer")
merged_df.to_csv("merged_dataset.csv", index=False)

# TODO Explore the merged dataset
# %%
