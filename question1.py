from datetime import datetime, timedelta
import requests
import json
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

def request_data():
  # Define the API endpoint and parameters
  base_url = 'https://api.weather.gc.ca/collections/climate-monthly/items'
  params = {
      'f': 'json',
      'lang': 'en-CA',
      'limit': 10,
      'skipGeometry': 'false',
      'CLIMATE_IDENTIFIER': '8202251'
  }

  # Define the start and end dates of the interval
  start_date = datetime(2013, 11, 1)
  end_date = datetime(2024, 3, 31)

  properties_list = []
  # Loop through each year within the past 10 years
  for i in range(11):
    # Calculate the current year based on the iteration
    current_year = start_date.year + i
    
    # Construct the datetime interval for the current year
    interval_start = datetime(current_year, 11, 1).strftime('%Y-%m-%dT00:00:00Z')
    interval_end = datetime(current_year + 1, 3, 31, 23, 59, 59).strftime('%Y-%m-%dT23:59:59Z')
  
    # Update the datetime parameter in the API URL
    params['datetime'] = f'{interval_start}/{interval_end}'

    # Make the API request
    response = requests.get(url=base_url, params=params)
    
    # Parse the JSON response
    parsed_json = json.loads(response.text)

    # Extract properties from features and create a list of dictionaries
    for feature in parsed_json['features']:
      properties = feature['properties']
      properties_list.append(properties)

    
  # Create DataFrame from the list of dictionaries
  df = pd.DataFrame(properties_list)

  # Write DataFrame to CSV file
  df.to_csv(FILE_NAME, index=False)  # Set index=False to exclude row numbers

def file_exists(file_name):
    return os.path.exists(file_name)

def open_file(file_name):
    try:
      df = pd.read_csv(FILE_NAME)
      return df
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")

def plot_descriptive_statistics(df):
  # Call describe() on the DataFrame to obtain descriptive statistics
  desc_stats = df.describe()

  # Plotting using Matplotlib
  fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))

  # Bar plot for 'count'
  axes[0, 0].bar(desc_stats.columns, desc_stats.loc['count'])
  axes[0, 0].set_title('Count')

  # Bar plot for 'mean'
  axes[0, 1].bar(desc_stats.columns, desc_stats.loc['mean'])
  axes[0, 1].set_title('Mean')

  # Bar plot for 'min'
  axes[1, 0].bar(desc_stats.columns, desc_stats.loc['min'])
  axes[1, 0].set_title('Min')

  # Bar plot for 'max'
  axes[1, 1].bar(desc_stats.columns, desc_stats.loc['max'])
  axes[1, 1].set_title('Max')

  # Adjust layout and display the plots
  plt.tight_layout()
  plt.show()

def plot_monthly_heatmap(df):
  pivot_table = df.pivot_table(values='MIN_TEMPERATURE', index=df['LOCAL_DATE'].dt.month, columns=df['LOCAL_DATE'].dt.year)
  plt.figure(figsize=(10, 8))
  sns.heatmap(pivot_table, cmap='coolwarm', annot=True, fmt=".1f", linewidths=.5)
  plt.title('Monthly Minimum Temperature Trends (2013-2024)')
  plt.xlabel('Year')
  plt.ylabel('Month')
  plt.show()

# Calculate statistics for each winter season
def calculate_statistics(data):
    statistics = {}
    statistics['Mean Temperature'] = data['MEAN_TEMPERATURE'].mean()
    statistics['Total Snowfall'] = data['TOTAL_SNOWFALL'].sum()
    statistics['Total Precipitation'] = data['TOTAL_PRECIPITATION'].sum()
    return statistics

def main(df):
  # Sort DataFrame by 'LOCAL_DATE' (monthly date) in ascending order
  df['LOCAL_DATE'] = pd.to_datetime(df['LOCAL_DATE'])  # Convert to datetime
  df = df.sort_values(by='LOCAL_DATE')

  # Extract data for specific periods
  winter_2024 = df[(df['LOCAL_DATE'] >= '2023-11-01') & (df['LOCAL_DATE'] <= '2024-03-31')]
  past_10_years = df[(df['LOCAL_DATE'] >= '2013-11-01') & (df['LOCAL_DATE'] <= '2023-10-31')]

  # plot_monthly_heatmap(df)

  # Group past 10 years data by winter seasons (November to March each year)
  winter_groups = past_10_years.groupby(past_10_years['LOCAL_DATE'].dt.year)

  winter_statistics_per_year = {}
  for year, group in winter_groups:
    winter_statistics_per_year[year] = calculate_winter_statistics(group)




FILE_NAME = 'q1_data.csv'
if __name__ == '__main__':
  df = None
  if file_exists(FILE_NAME):
    print(f"FILE {FILE_NAME} exit, opening file")
    df = open_file(FILE_NAME)
  else:
    print(f"File '{FILE_NAME}' does not exist. Making a request to fetch data...")
    request_data()
    df = open_file(FILE_NAME)


  main(df)