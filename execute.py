import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import seaborn as sns
from scipy.ndimage import gaussian_filter1d  # For smoothing the line plot

""" FIXES
- remove the extra id
- explore the heat map (yours looks good)
- add the extra month (11 instead of 10)
data.csv"""

def main():
  df = pd.read_csv('data.csv')
  # Sort DataFrame by 'LOCAL_DATE' (monthly date) in ascending order
  df['LOCAL_DATE'] = pd.to_datetime(df['LOCAL_DATE'])  # Convert to datetime
  df = df.sort_values(by='LOCAL_DATE')

  statistical_analysisq1(df)

def statistical_analysisq1(df):
  # Sample data (assuming 'data' is the provided dataset in a list of dictionaries)
  # data = [
  #     {'id': 50620.2014.3, 'LOCAL_YEAR': 2014, 'MEAN_TEMPERATURE': -4.112903225806452, 'NORMAL_SNOWFALL': 11.3, 'NORMAL_PRECIPITATION': 685.5},
  #     {'id': 50620.2013.11, 'LOCAL_YEAR': 2013, 'MEAN_TEMPERATURE': 2.6266666666666665, 'NORMAL_SNOWFALL': 16.3, 'NORMAL_PRECIPITATION': 461.2},
  #     # Add more data entries here...
  # ]

  # Filter data for the 2024 winter season (November 2023 to March 2024)
  # winter_2024 = df[(df['LOCAL_YEAR'] == 2024) & (df['LOCAL_MONTH'].isin([11, 12, 1, 2, 3]))]
  winter_2024 = df[(df['LAST_UPDATED'] >= '2023-11-01') & (df['LAST_UPDATED'] <= '2024-03-31')]

  # Filter data for the past ten winter seasons
  # past_winters = df[df['LOCAL_YEAR'].isin(range(2013, 2022))]  # Assuming historical data from 2003 to 2013

  past_winters = df.drop(winter_2024.index)  # Exclude bad weather period rows

  # Compute aggregate statistics for the 2024 winter season
  winter_2024_stats = {
      'Mean Temperature': winter_2024['MEAN_TEMPERATURE'].mean(),
      'Total Snowfall': winter_2024['TOTAL_SNOWFALL'].mean(),
      'Total Precipitation': winter_2024['TOTAL_PRECIPITATION'].mean(),
      'Minimum Temperature': winter_2024['MIN_TEMPERATURE'].mean(),
      'Maximum Temperature': winter_2024['MAX_TEMPERATURE'].mean()
  }

  # Compute aggregate statistics for the past ten winter seasons
  past_winters_stats = {
      'Mean Temperature': past_winters['MEAN_TEMPERATURE'].mean(),
      'Total Snowfall': past_winters['TOTAL_SNOWFALL'].mean(),
      'Total Precipitation': past_winters['TOTAL_PRECIPITATION'].mean(),
      'Minimum Temperature': past_winters['MIN_TEMPERATURE'].mean(),
      'Maximum Temperature': past_winters['MAX_TEMPERATURE'].mean()
  }


# Extract categories and values for bar plotting
categories = list(winter_2024_stats.keys())
winter_2024_values = list(winter_2024_stats.values())
past_winters_values = list(past_winters_stats.values())

# Calculate positions for bars
bar_width = 0.35
r1 = np.arange(len(categories))
r2 = [x + bar_width for x in r1]

# Create side-by-side bar plots
plt.bar(r1, winter_2024_values, color='b', width=bar_width, label='2024 Winter Season')
plt.bar(r2, past_winters_values, color='r', width=bar_width, label='Past Ten Winter Seasons')

# Customize the plot
plt.xlabel('Weather Parameters')
plt.ylabel('Aggregate Statistics')
plt.title('Comparison of 2024 Winter Season with Past Ten Winter Seasons')
plt.xticks([r + bar_width / 2 for r in range(len(categories))], categories)
plt.legend()

# Show plot
plt.show()




def temporary():
  # Filter data for the 2024 winter season (November 2023 to March 2024)
  # winter_2024 = df[(df['LOCAL_YEAR'] == 2024) & (df['LOCAL_MONTH'].isin([11, 12, 1, 2, 3]))]
  winter_2024 = df[(df['LAST_UPDATED'] >= '2023-11-01') & (df['LAST_UPDATED'] <= '2024-03-31')]

  # Filter data for the past ten winter seasons
  # past_winters = df[df['LOCAL_YEAR'].isin(range(2013, 2022))]  # Assuming historical data from 2003 to 2013

  past_winters = df.drop(winter_2024.index)  # Exclude bad weather period rows

  # Compute aggregate statistics for the 2024 winter season
  winter_2024_stats = {
      'Mean Temperature': winter_2024['MEAN_TEMPERATURE'].mean(),
      'Total Snowfall': winter_2024['TOTAL_SNOWFALL'].mean(),
      'Total Precipitation': winter_2024['TOTAL_PRECIPITATION'].mean(),
      'Minimum Temperature': winter_2024['MIN_TEMPERATURE'].mean(),
      'Maximum Temperature': winter_2024['MAX_TEMPERATURE'].mean()
  }

  # Compute aggregate statistics for the past ten winter seasons
  past_winters_stats = {
      'Mean Temperature': past_winters['MEAN_TEMPERATURE'].mean(),
      'Total Snowfall': past_winters['TOTAL_SNOWFALL'].mean(),
      'Total Precipitation': past_winters['TOTAL_PRECIPITATION'].mean(),
      'Minimum Temperature': past_winters['MIN_TEMPERATURE'].mean(),
      'Maximum Temperature': past_winters['MAX_TEMPERATURE'].mean()
  }


# Extract categories and values for bar plotting
categories = list(winter_2024_stats.keys())
winter_2024_values = list(winter_2024_stats.values())
past_winters_values = list(past_winters_stats.values())

# Calculate positions for bars
bar_width = 0.35
r1 = np.arange(len(categories))
r2 = [x + bar_width for x in r1]

# Create side-by-side bar plots
plt.bar(r1, winter_2024_values, color='b', width=bar_width, label='2024 Winter Season')
plt.bar(r2, past_winters_values, color='r', width=bar_width, label='Past Ten Winter Seasons')

# Customize the plot
plt.xlabel('Weather Parameters')
plt.ylabel('Aggregate Statistics')
plt.title('Comparison of 2024 Winter Season with Past Ten Winter Seasons')
plt.xticks([r + bar_width / 2 for r in range(len(categories))], categories)
plt.legend()

# Show plot
plt.show()
  # Visualize the comparison
  # categories = list(winter_2024_stats.keys())
  # winter_2024_values = list(winter_2024_stats.values())
  # past_winters_values = list(past_winters_stats.values())

  # plt.bar(categories, winter_2024_values, label='2024 Winter Season')
  # plt.bar(categories, past_winters_values, label='Past Ten Winter Seasons', alpha=0.5)
  # plt.xlabel('Weather Parameters')
  # plt.ylabel('Aggregate Statistics')
  # plt.title('Comparison of 2024 Winter Season with Past Ten Winter Seasons')
  # plt.legend()
  # plt.show()


def box_plot(df):
  plt.figure(figsize=(10, 8))
  sns.boxplot(x=df['LOCAL_DATE'].dt.month, y='MIN_TEMPERATURE', hue=df['LOCAL_DATE'].dt.year, data=df)
  plt.title('Monthly Minimum Temperature Distribution (2013-2015)')
  plt.xlabel('Month')
  plt.ylabel('Minimum Temperature (°C)')
  plt.legend(title='Year')
  plt.show()



def heat_map(df):

  pivot_table = df.pivot_table(values='MIN_TEMPERATURE', index=df['LOCAL_DATE'].dt.month, columns=df['LOCAL_DATE'].dt.year)
  plt.figure(figsize=(10, 8))
  sns.heatmap(pivot_table, cmap='coolwarm', annot=True, fmt=".1f", linewidths=.5)
  plt.title('Monthly Minimum Temperature Trends (2013-2015)')
  plt.xlabel('Year')
  plt.ylabel('Month')
  plt.show()


def initial_plot():
  # Read CSV file into DataFrame
  df = pd.read_csv('data.csv')

  # Sort DataFrame by 'LOCAL_DATE' (monthly date) in ascending order
  df['LOCAL_DATE'] = pd.to_datetime(df['LOCAL_DATE'])  # Convert to datetime
  df = df.sort_values(by='LOCAL_DATE')

  # Plot line plot for 'MIN_TEMPERATURE'
  plt.figure(figsize=(10, 6))
  plt.title('Minimum Temperature Trend (2013-2015)')
  plt.plot(df['LOCAL_DATE'], df['MIN_TEMPERATURE'], marker='o', linestyle='-', color='b')
  plt.xlabel('Local Date')
  plt.ylabel('Minimum Temperature (°C)')
  plt.xticks(rotation=45)
  plt.legend()
  plt.grid(True)
  plt.show()

def first_plot(df):

  # Convert 'LOCAL_DATE' to datetime format
  df['LOCAL_DATE'] = pd.to_datetime(df['LOCAL_DATE'])

  # Extract year from 'LOCAL_DATE' for grouping
  df['Year'] = df['LOCAL_DATE'].dt.year

  # Plot using seaborn lineplot for each year
  plt.figure(figsize=(12, 6))
  sns.lineplot(data=df, x='LOCAL_DATE', y='MIN_TEMPERATURE', hue='Year', marker='o', palette='viridis')
  plt.title('Minimum Temperature Trend by Year')
  plt.xlabel('Local Date')
  plt.ylabel('Minimum Temperature (°C)')
  plt.xticks(rotation=45)
  plt.grid(True)
  plt.legend(title='Year')
  plt.tight_layout()
  plt.show()



def compare_statistical_differences():
  # Read CSV file into DataFrame
  df = pd.read_csv('data.csv')

  # Convert 'LAST_UPDATED' column to datetime
  df['LAST_UPDATED'] = pd.to_datetime(df['LAST_UPDATED'])

  # Filter data for November 2023 to March 2024
  bad_weather_period = df[(df['LAST_UPDATED'] >= '2023-11-01') & (df['LAST_UPDATED'] <= '2024-03-31')]

  # Calculate aggregations for bad weather period
  bad_weather_stats = bad_weather_period.describe()

  # Calculate aggregations for the rest of the data
  rest_of_data = df.drop(bad_weather_period.index)  # Exclude bad weather period rows
  rest_of_data_stats = rest_of_data.describe()

  # Display statistical aggregations
  print("Statistical Aggregations for Bad Weather Period:")
  print(bad_weather_stats)

  print("\nStatistical Aggregations for Rest of the Data:")
  print(rest_of_data_stats)


  # Display the loaded DataFrame
  # print(df_loaded)

def read_and_write_data():
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

  df = None
  properties_list = []
  # Loop through each year within the past 10 years
  for i in range(10):
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
        properties['id'] = feature['id']  # Add 'id' field from the feature
        properties_list.append(properties)
      
  # Create DataFrame from the list of dictionaries
  df = pd.DataFrame(properties_list)

  # Reorder columns to have 'id' as the first column
  cols = df.columns.tolist()
  cols = ['id'] + [col for col in cols if col != 'id']
  df = df[cols]

      # Debug Info 
      # Process the data (replace this with your desired logic)
      # print(f"Data for {current_year}-{current_year + 1}:")
      # print(parsed_json)
      # print("=" * 50)

  # Write DataFrame to CSV file
  df.to_csv('data.csv', index=False)  # Set index=False to exclude row numbers



if __name__ == '__main__':
  main()
