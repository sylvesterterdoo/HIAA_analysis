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
      df = pd.read_csv(file_name)
      return df
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")

def descriptive_statistics(winter_2024, past_10_years):
  # Calculate statistics for winter 2024
  winter_statistics_2024 = {
    2024:calculate_winter_statistics(winter_2024)
  }

  # Calculate statistics for each winter season over the past 10 years
  winter_groups = past_10_years.groupby(past_10_years['LOCAL_DATE'].dt.year)
  winter_statistics_per_year_past_10_years = {
      year: calculate_winter_statistics(group) for year, group in winter_groups
  }

  # Convert data to DataFrame for past 10 years
  past_10_years_df = pd.DataFrame(winter_statistics_per_year_past_10_years).T

  # Convert data to DataFrame for winter 2024
  # winter_2024_df = pd.DataFrame(winter_statistics_2024, index=['2024']).T
  winter_2024_df = pd.DataFrame.from_dict(winter_statistics_2024, orient='index')

  # Combine past 10 years and winter 2024 data
  combined_df = pd.concat([past_10_years_df, winter_2024_df])

  # Print descriptive statistics for each metric
  print("Descriptive Statistics for Mean Temperature:")
  print(combined_df['Mean Temperature'].describe())
  print("\nDescriptive Statistics for Total Snowfall:")
  print(combined_df['Total Snowfall'].describe())
  print("\nDescriptive Statistics for Total Precipitation:")
  print(combined_df['Total Precipitation'].describe())

  combined_df.index = combined_df.index.astype(str)

  # Plot mean temperature comparison
  plt.figure(figsize=(10, 6))
  plt.bar(combined_df.index, combined_df['Mean Temperature'], color='b', alpha=0.7)
  plt.xlabel('Winter Season (Year)')
  plt.ylabel('Mean Temperature (°C)')
  plt.title('Comparison of Mean Temperature (Past 10 Years + Winter 2024)')
  plt.grid(True)
  plt.xticks(rotation=45)
  plt.show()

  # Plot total snowfall comparison
  plt.figure(figsize=(10, 6))
  plt.bar(combined_df.index, combined_df['Total Snowfall'], color='g', alpha=0.7)
  plt.xlabel('Winter Season (Year)')
  plt.ylabel('Total Snowfall (mm)')
  plt.title('Comparison of Total Snowfall (Past 10 Years + Winter 2024)')
  plt.grid(True)
  plt.xticks(rotation=45)
  plt.show()

  # Plot total precipitation comparison
  plt.figure(figsize=(10, 6))
  plt.bar(combined_df.index, combined_df['Total Precipitation'], color='r', alpha=0.7)
  plt.xlabel('Winter Season (Year)')
  plt.ylabel('Total Precipitation (mm)')
  plt.title('Comparison of Total Precipitation (Past 10 Years + Winter 2024)')
  plt.grid(True)
  plt.xticks(rotation=45)
  plt.show()

def plot_monthly_heatmap(df):
  pivot_table = df.pivot_table(values='MIN_TEMPERATURE', index=df['LOCAL_DATE'].dt.month, columns=df['LOCAL_DATE'].dt.year)
  plt.figure(figsize=(10, 8))
  sns.heatmap(pivot_table, cmap='coolwarm', annot=True, fmt=".1f", linewidths=.5)
  plt.title('Monthly Minimum Temperature Trends (2013-2024)')
  plt.xlabel('Year')
  plt.ylabel('Month')
  plt.show()

# Define a function to calculate statistics for a given winter season
def calculate_winter_statistics(data):
    winter_statistics = {}
    winter_statistics['Mean Temperature'] = data['MEAN_TEMPERATURE'].mean()
    winter_statistics['Total Snowfall'] = data['TOTAL_SNOWFALL'].sum()
    winter_statistics['Total Precipitation'] = data['TOTAL_PRECIPITATION'].sum()
    return winter_statistics

def plot_2024_winter_with_past_10_years(winter_2024, past_10_years):
  # Group past 10 years data by winter seasons (November to March each year)
  winter_groups = past_10_years.groupby(past_10_years['LOCAL_DATE'].dt.year)

  winter_statistics_per_year = {}
  for year, group in winter_groups:
    winter_statistics_per_year[year] = calculate_winter_statistics(group)

  # Convert winter statistics to DataFrame
  winter_statistics_df = pd.DataFrame(winter_statistics_per_year).T

  # Plot comparison of winter 2024 with past 10 years' winters
  plt.figure(figsize=(12, 6))
  plt.plot(winter_statistics_df.index, winter_statistics_df['Mean Temperature'], label='Mean Temperature (Past 10 Years)')
  plt.axhline(y=winter_2024['MEAN_TEMPERATURE'].mean(), color='r', linestyle='--', label='Mean Temperature (Winter 2024)')
  plt.xlabel('Winter Season (Year)')
  plt.ylabel('Mean Temperature (°C)')
  plt.title('Comparison of Winter Mean Temperature (Past 10 Years vs. Winter 2024)')
  plt.legend()
  plt.grid(True)
  plt.xticks(winter_statistics_df.index)
  plt.show()


def main(df):
  # Sort DataFrame by 'LOCAL_DATE' (monthly date) in ascending order
  df['LOCAL_DATE'] = pd.to_datetime(df['LOCAL_DATE'])  # Convert to datetime
  df = df.sort_values(by='LOCAL_DATE')

  # Extract data for specific periods
  winter_2024 = df[(df['LOCAL_DATE'] >= '2023-11-01') & (df['LOCAL_DATE'] <= '2024-03-31')]
  past_10_years = df[(df['LOCAL_DATE'] >= '2013-11-01') & (df['LOCAL_DATE'] <= '2023-10-31')]

  descriptive_statistics(winter_2024, past_10_years)
  plot_monthly_heatmap(df)
  plot_2024_winter_with_past_10_years(winter_2024, past_10_years)

FILE_NAME = 'q1_data.csv'
if __name__ == '__main__':
  df = None
  if file_exists(FILE_NAME):
    print(f"Opening file")
    df = open_file(FILE_NAME)
  else:
    print(f"File '{FILE_NAME}' does not exist. Making a request to fetch data...")
    request_data()
    df = open_file(FILE_NAME)


  main(df)

"""
Interpretations:

Mean Temperature:
The mean temperature for the past 10 winters ranges from approximately -3.06°C (coldest) to -0.11°C (mildest), with an average of around -1.33°C.
The mean temperature for winter 2024 was -0.50°C, which is slightly milder than the average temperature over the past 10 years.
Total Snowfall:
The total snowfall for the past 10 winters ranges from 83.5 mm to 394.6 mm, with an average of approximately 227.8 mm.
Winter 2024 had a total snowfall of 238.6 mm, which is consistent with the historical average.
Total Precipitation:
The total precipitation (rainfall + snowfall) for the past 10 winters varies from 337.9 mm to 1027.0 mm, averaging around 700.2 mm.
Winter 2024 experienced a total precipitation of 863.8 mm, which is on the higher end compared to the historical average.
These descriptive statistics provide insights into the weather conditions during the past 10 winter seasons and how winter 2024 compares in terms of mean temperature, snowfall, and precipitation. Winter 2024 generally exhibits similar characteristics to historical winters in terms of temperature and snowfall, but with slightly higher precipitation
"""