#%%
import os
import requests
import pandas as pd
import numpy as np

def download_datasets(personality_url, assets_url, supa_api_key):
    """
    Download datasets from GitHub and Supabase, 
    merge them, and save all to CSV files.
    """

    # Check if the datasets directory exists, create it if not
    if not os.path.exists('datasets'):
        os.makedirs('datasets')

    # Download personality dataset
    print('Downloading personality dataset from GitHub...')
    df_personality = pd.read_csv(personality_url)
    df_personality.to_csv('datasets/personality.csv', index=False)

    # Set up headers for Supabase API requests
    headers = {
            'apikey': supa_api_key,
            'Authorization': f'Bearer {supa_api_key}',
            'Accept': 'application/json',
        }

    # Download assets dataset
    print('Downloading assets dataset from Supabase...')
    resp = requests.get(assets_url, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    df_assets = pd.DataFrame(data)
    df_assets.to_csv('datasets/assets.csv', index=False)

    # Merge datasets on the "_id" column
    merged_df = pd.merge(df_personality, df_assets, on='_id', how='outer')
    merged_df.to_csv('datasets/merged_dataset.csv', index=False)


# Credentials and URLs hardcoded from "https://github.com/karwester/behavioural-finance-task"
GITHUB_CSV_URL = (
    "https://raw.githubusercontent.com/karwester/behavioural-finance-task/"
    "main/personality.csv"
)
SUPABASE_URL = "https://pvgaaikztozwlfhyrqlo.supabase.co"
ASSETS_ENDPOINT = f"{SUPABASE_URL}/rest/v1/assets?select=*"

API_KEY = os.getenv(
    "SUPABASE_API_KEY",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6"
    "InB2Z2FhaWt6dG96d2xmaHlycWxvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc4NDE2"
    "MjUsImV4cCI6MjA2MzQxNzYyNX0.iAqMXnJ_sJuBMtA6FPNCRcYnKw95YkJvY3OhCIZ77vI",
)

download_datasets(personality_url=GITHUB_CSV_URL,
                  assets_url=ASSETS_ENDPOINT,
                  supa_api_key=API_KEY)