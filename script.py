import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import seaborn as sns
import numpy as np
from scipy.ndimage import gaussian_filter1d  # For smoothing the line plot

""" FIXES
- remove the extra id
- explore the heat map (yours looks good)
- add the extra month (11 instead of 10)
data.csv"""

def main():
  q1()

def read_and_write_data():
  # Define the API endpoint and parameters
  base_url = 'https://api.weather.gc.ca/collections/climate-daily/items'
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
      
      # Debug Info 
      # Process the data (replace this with your desired logic)
      print(f"Data for {current_year}-{current_year + 1}:")
      print(parsed_json)
      print("=" * 50)

  # Create DataFrame from the list of dictionaries
  df = pd.DataFrame(properties_list)

  # Reorder columns to have 'id' as the first column
  cols = df.columns.tolist()
  cols = ['id'] + [col for col in cols if col != 'id']
  df = df[cols]

  # Write DataFrame to CSV file
  df.to_csv('dailyData.csv', index=False)  # Set index=False to exclude row numbers


def q1():
  # Load the new dataset
  df = pd.read_csv('dailyData.csv')
  # Convert 'LAST_UPDATED' column to datetime
  df['LOCAL_DATE'] = pd.to_datetime(df['LOCAL_DATE'])


  # Filter data for the past ten winter seasons
  # past_ten_winter_seasons = df[(df['LOCAL_MONTH'].isin([11, 12, 1, 2, 3])) & (df['LOCAL_YEAR'].isin([2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005]))]

  # Filter data for the specific dates of interest in 2024
  # feb_2024_events = df[df['LOCAL_DATE'].isin(['2024-02-02', '2024-02-03', '2024-02-04', '2024-02-13'])]

  # Filter data for the February snow events in 2024
  feb_2024_events = df[df['LOCAL_DATE'].isin(['2024-02-02', '2024-02-03', '2024-02-04', '2024-02-13'])]

  # Filter data for the past ten winter seasons
  past_ten_winter_seasons = df[df['LOCAL_DATE'].str.contains('-11-|-12-|^-01-|^02-|^03-', regex=True) & (df['LOCAL_YEAR'].isin(range(2013, 2023)))]


  print(feb_2024_events)

  ## Calculate aggregate statistics for snowfall during the February 2024 events
  #feb_2024_snowfall_stats = {
  #    'Mean Snowfall': feb_2024_events['TOTAL_SNOW'].mean(),
  #    'Maximum Snowfall': feb_2024_events['TOTAL_SNOW'].max()
  #}

  ## Calculate aggregate statistics for snowfall during the past ten winter seasons
  #past_ten_winter_snowfall_stats = {
  #    'Mean Snowfall': past_ten_winter_seasons['TOTAL_SNOW'].mean(),
  #    'Maximum Snowfall': past_ten_winter_seasons['TOTAL_SNOW'].max()
  #}

  ## Determine if the February snow events in 2024 were rare compared to the past ten winter seasons
  #is_rare_event = (
  #    feb_2024_snowfall_stats['Mean Snowfall'] > past_ten_winter_snowfall_stats['Mean Snowfall'] and
  #    feb_2024_snowfall_stats['Maximum Snowfall'] > past_ten_winter_snowfall_stats['Maximum Snowfall']
  #)

  #if is_rare_event:
  #    print("The February snow events in 2024 were rare compared to the past ten winter seasons.")
  #else:
  #    print("The February snow events in 2024 were not rare compared to the past ten winter seasons.")

  # other parts

  # # Filter data for the past ten winter seasons
  # past_ten_winter_seasons = df[(df['LOCAL_MONTH'].isin([11, 12, 1, 2, 3])) & (df['LOCAL_YEAR'].isin([2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005]))]

  # # Filter data for the specific dates of interest in 2024
  # feb_2024_events = df[df['LOCAL_DATE'].isin(['2024-02-02', '2024-02-03', '2024-02-04', '2024-02-13'])]

  # print(feb_2024_events)

  # # Calculate aggregate statistics for snowfall during the specific dates in 2024
  # feb_2024_snowfall_stats = {
  #     'Mean Snowfall': feb_2024_events['TOTAL_SNOWFALL'].mean(),
  #     'Maximum Snowfall': feb_2024_events['TOTAL_SNOWFALL'].max()
  # }

  # # Calculate aggregate statistics for snowfall during the specific dates over the past ten winter seasons
  # past_ten_winter_snowfall_stats = {
  #     'Mean Snowfall': past_ten_winter_seasons['TOTAL_SNOWFALL'].mean(),
  #     'Maximum Snowfall': past_ten_winter_seasons['TOTAL_SNOWFALL'].max()
  # }

  # # Determine if the February snow events in 2024 were rare compared to the past ten winter seasons
  # is_rare_event = (
  #     feb_2024_snowfall_stats['Mean Snowfall'] > past_ten_winter_snowfall_stats['Mean Snowfall'] and
  #     feb_2024_snowfall_stats['Maximum Snowfall'] > past_ten_winter_snowfall_stats['Maximum Snowfall']
  # )

  # if is_rare_event:
  #     print("The February snow events in 2024 were rare compared to the past ten winter seasons.")
  # else:
  #     print("The February snow events in 2024 were not rare compared to the past ten winter seasons.")



def question1():
  df = pd.read_csv('data.csv')
  # Sort DataFrame by 'LOCAL_DATE' (monthly date) in ascending order
  df['LOCAL_DATE'] = pd.to_datetime(df['LOCAL_DATE'])  # Convert to datetime
  df = df.sort_values(by='LOCAL_DATE')

  # Convert 'LAST_UPDATED' column to datetime format
  df['LAST_UPDATED'] = pd.to_datetime(df['LAST_UPDATED'])

  # Filter data for the 2024 winter season (November 2023 to March 2024)
  # winter_2024 = df[(df['LAST_UPDATED'] >= '2023-11-01') & (df['LAST_UPDATED'] <= '2024-03-31')]
  # Filter data for the past ten winter seasons (excluding 2024 winter season)
  # past_winters = df[~df['LAST_UPDATED'].between('2023-11-01', '2024-03-31')]


  winter_2024 = df[(df['LOCAL_DATE'] >= '2023-11-01') & (df['LOCAL_DATE'] <= '2024-03-31')]
  past_winters = df[~df['LOCAL_DATE'].between('2023-11-01', '2024-03-31')]

  # Compute aggregate statistics for the 2024 winter season
  winter_2024_stats = {
      'Mean Temperature': winter_2024['MEAN_TEMPERATURE'].mean(),
      # 'Total Snowfall': winter_2024['TOTAL_SNOWFALL'].sum(),
      # 'Total Precipitation': winter_2024['TOTAL_PRECIPITATION'].sum(),
      'Minimum Temperature': winter_2024['MEAN_TEMPERATURE'].min(),
      'Maximum Temperature': winter_2024['MEAN_TEMPERATURE'].max()
  }

  # Compute aggregate statistics for the past ten winter seasons
  past_winters_stats = {
      'Mean Temperature': past_winters['MEAN_TEMPERATURE'].mean(),
      # 'Total Snowfall': past_winters['TOTAL_SNOWFALL'].sum(),
      # 'Total Precipitation': past_winters['TOTAL_PRECIPITATION'].sum(),
      'Minimum Temperature': past_winters['MEAN_TEMPERATURE'].min(),
      'Maximum Temperature': past_winters['MEAN_TEMPERATURE'].max()
  }

  # Plotting mean temperature over time
  plt.plot(df['LAST_UPDATED'], df['MEAN_TEMPERATURE'])
  plt.xlabel('Date')
  plt.ylabel('Mean Temperature')
  plt.title('Mean Temperature Variation Over Time')
  plt.show()



def bar_plot1():
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



if __name__ == '__main__':
  main()