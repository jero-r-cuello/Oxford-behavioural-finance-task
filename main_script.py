#%%
"""
Exploratory Data Analysis (EDA) Script for Behavioral Financial Dataset
------------------------------------------------------------------------

This script performs an exploratory data analysis (EDA) on a behavioral
financial dataset. 
The analysis is organized into sequential sections.

Sections included:
------------------
0. Pre-processing
    - Display dataset shape, column names, and head
    - Assess value distributions per column
    - Check for missing values and data types
    - Describe numerical and categorical columns
    - Detect duplicates and convert ID columns to string

1. Univariate Analysis
    - Identify numerical and categorical variables
    - Plot distributions of numerical variables (histograms, zoomed view for asset_value)
    - Plot frequency counts for categorical variables
    - Parse and analyze temporal column ('created')

2. Bivariate Analysis
    - Generate scatter plots between numerical variables (pairplot)
    - Visualize numerical vs. categorical interactions (violin + strip plots)
    - Explore categorical relationships via normalized crosstabs (stacked barplot)
    - Compute and display correlation heatmap for numerical variables

Special Case Analysis (included in Pre-processing):
----------------------
- Identify the individual with the highest total asset value in GBP only
- Retrieve and report the corresponding risk tolerance score

Usage:
------
Run the script in a Python environment that supports interactive plotting
The output includes printed summaries and visualizations for immediate inspection.

"""
# Import necessary libraries
import pandas as pd
import numpy as np
# colored is used to make the output more readable
from termcolor import colored 
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('datasets/merged_dataset.csv')


### 0 - Pre-processing

# Print basic information about the dataset
print(colored(f'Dataset shape: ','green'), df.shape)
print(colored('Dataset columns: ', 'green'), df.columns)
print(colored('\nFirst 5 rows of the dataset:', 'green'))
print(df.head())

print(colored('\nValue counts on each column:', 'green'))
for c in df.columns:
    print(f'{df[c].value_counts()}\n')

# Check for missing values
print(colored('\nMissing values and data type in each column:', 'green'))
print(df.info())

# Describe numerical columns
print(colored('\nNumerical columns description:', 'green'))
print(df.describe(include=np.number))

# Describe categorical columns
print(colored('\nCategorical columns description:', 'green'))
print(df.describe(include=["O"]))

# Check for duplicates
print(colored('\nNumber of duplicate rows:', 'green'),
      df.duplicated().sum())

# Convert id columns to appropriate data types
df['_id'] = df['_id'].astype(str)
df['asset_allocation_id'] = df['asset_allocation_id'].astype(str)

# Describe categorical columns again after conversion
print(colored('\nCategorical columns description after conversion:', 'green'))
print(df.describe(include=["O"]))

# Risk tolerance of highest asset value person, only GBP assets
# Filter the DataFrame for GBP assets
df_gbp = df[df["asset_currency"] == "GBP"]

# Group by person ID and sum the asset values
gbp_assets_val_by_person = df_gbp.groupby("_id")["asset_value"].sum()

# Find the person with the highest total asset value
max_value = gbp_assets_val_by_person.max()
id_of_max_value = gbp_assets_val_by_person.idxmax()

# Get the risk tolerance of that person
risk_tolerance = df[df["_id"] == id_of_max_value]["risk_tolerance"].iloc[0]

print(colored(f'Highest total asset value in GBP: {max_value}, for person ID: {id_of_max_value}, with risk tolerance: {risk_tolerance}', 'red'))


### 1 - Univariate Analysis

# Identify numerical and categorical columns
num_cols = df.select_dtypes(include=['number']).columns.tolist()
print(colored(f'Numerical columns: {num_cols}', 'blue'))

cat_cols = df.select_dtypes(include=['object']).columns.tolist()
cat_cols.remove('created') # another approach is used to handle this column
cat_cols.remove('_id')
cat_cols.remove('asset_allocation_id')
print(colored(f'Categorical columns: {cat_cols}', 'blue'))

# Plotting numerical columns as histograms
print(colored('\nPlotting distributions of numerical columns:', 'blue'))
for col in num_cols:
    plt.figure(figsize=(10, 6))
    sns.histplot(df[col], kde=True, bins=30)
    plt.title(f'Distribution of {col}')
    plt.xlabel(col)
    plt.ylabel('Frequency')
    plt.grid()
    plt.show()

# Zooming in on asset_value distribution, as it has a wide range
asset_value_zoom = df[df['asset_value'] < 5000]['asset_value']

plt.figure(figsize=(10, 6))
sns.histplot(asset_value_zoom, kde=True, bins=100) # Adjusted bins for better visibility
plt.title(f'Distribution of asset_value (zoomed in < 5000)')
plt.xlabel('asset_value')
plt.ylabel('Frequency')
plt.grid()
plt.show()

# Plotting categorical columns as bar plots
print(colored('\nPlotting counts of categorical columns:', 'blue'))
for col in cat_cols:
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x=col, order=df[col].value_counts().index)
    plt.title(f'Count of {col}')
    plt.xlabel(col)
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()

# Handling the 'created' column
df['created'] = pd.to_datetime(df['created'])
frequency_by_date = df['created'].dt.date.value_counts().sort_index()

print(colored('\nFrequency of asset allocations by date:', 'blue'))
print(frequency_by_date)

# Plotting the frequency of asset allocations by date
frequency_by_date.plot(kind='bar', figsize=(15, 6))
plt.title("Frequency of Records by Date (not counting hours)")
plt.xlabel("Date")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()


### 2 - Bivariate Analysis

# Plotting relationships between numerical features as scatter plots
print(colored('\nPlotting scatter plots between numerical features:', 'magenta'))
sns.pairplot(df[num_cols], corner=True)
plt.suptitle('Scatter plots between numerical features', y=1.02)
plt.tight_layout()
plt.show()

# Plotting relationships between numerical and categorical features as violin plots
print(colored('\nPlotting relationships between numerical and categorical features:', 'magenta'))
for num in num_cols:
    for cat in cat_cols:
        plt.figure(figsize=(10, 4))
        sns.violinplot(x=cat, y=num, data=df, inner='box', palette='Set2') # palette added for better visualization
        sns.stripplot(x=cat, y=num, data=df, color='k', alpha=0.3, jitter=True, size=2) # datapoints added for better understanding
        plt.title(f'{num} vs {cat}')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

# Plotting relationships between categorical features as stacked bar plots
contingency_table = pd.crosstab(df['asset_allocation'], df['asset_currency'])
contingency_table_norm = contingency_table.div(contingency_table.sum(axis=1), axis=0)
print(colored('Proportions of asset_allocation vs asset_currency:', 'magenta'))
print(contingency_table_norm)

print(colored('\nPlotting relationships between categorical features:', 'magenta'))
contingency_table_norm.plot(kind='bar', stacked=True, figsize=(10, 4))
plt.title(f'Asset allocation vs Asset currency (proportions)')
plt.ylabel('Proportion on "asset allocation"')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plotting correlation heatmap for numerical features
df_corr = df[num_cols].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(df_corr, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Heatmap of Numerical Features')
plt.tight_layout()
plt.show()
