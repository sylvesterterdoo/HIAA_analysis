
import json
import requests
import pandas as pd
from datetime import datetime, timedelta
from question1 import file_exists, open_file
import matplotlib.pyplot as plt

# 2024-02-02 – 2024-02-04, and 2024-02-13
# 2024-02-02T00:00:00Z/2024-02-14T23:59:59Z
def request_data():
  # Define the API endpoint and parameters
  base_url = 'https://api.weather.gc.ca/collections/climate-daily/items'
  params = {
      'f': 'json',
      'lang': 'en-CA',
      'limit': 15,
      'skipGeometry': 'false',
      'CLIMATE_IDENTIFIER': '8202251'
  }

  properties_list = []
  df = None
  # Loop through each year within the past 10 years
  for year in range(2014, 2025): # 2025

     # Define the interval start and end dates for the current year
    year_interval_start = datetime(year, 2, 2).strftime('%Y-%m-%dT00:00:00Z')
    year_interval_end = datetime(year, 2, 13).strftime('%Y-%m-%dT23:59:59Z')
      
    # Update the datetime parameter in the API URL
    params['datetime'] = f'{year_interval_start}/{year_interval_end}'
    
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

  # # Reorder columns to have 'id' as the first column
  cols = df.columns.tolist()
  cols = ['ID'] + [col for col in cols if col != 'ID']
  df = df[cols]

  df['LOCAL_DATE'] = pd.to_datetime(df['LOCAL_DATE'])  # Convert to datetime
  df = df.sort_values(by='LOCAL_DATE')

  # # # Write DataFrame to CSV file
  df.to_csv(FILE_NAME, index=False)  # Set index=False to exclude row numbers


def main(df):

  # Convert 'LOCAL_DATE' to datetime format
  df['LOCAL_DATE'] = pd.to_datetime(df['LOCAL_DATE'])

  # Filter data for the specific periods of interest in February 2024
  february_first_event = df[(df['LOCAL_DATE'] >= '2024-02-02') & (df['LOCAL_DATE'] <= '2024-02-04')]
  february_second_event = df[(df['LOCAL_DATE'] >= '2024-02-12') & (df['LOCAL_DATE'] <= '2024-02-13')]

  # Filter data for the past ten winter seasons (from January 1, 2014, to October 31, 2023)
  past_10_years = df[(df['LOCAL_DATE'] >= '2014-01-01') & (df['LOCAL_DATE'] <= '2023-10-31')]

  # Calculate total snowfall for the two specific events in February 2024
  total_snowfall_event_1 = february_first_event['TOTAL_SNOW'].sum()
  total_snowfall_event_2 = february_second_event['TOTAL_SNOW'].sum()

  # Aggregate snowfall data by year for the past ten winter seasons
  february_snowfall_past_years = past_10_years[past_10_years['LOCAL_DATE'].dt.month == 2]
  february_snowfall_past_years = february_snowfall_past_years.groupby(past_10_years['LOCAL_DATE'].dt.year)['TOTAL_SNOW'].sum()

  # Determine if the February snow events in 2024 were rare compared to the past ten winter seasons
  rare_event_1 = (february_snowfall_past_years >= total_snowfall_event_1).sum() == 0
  rare_event_2 = (february_snowfall_past_years >= total_snowfall_event_2).sum() == 0

  # Plotting snowfall data
  plt.figure(figsize=(10, 6))

  # Plot historical snowfall data for past ten winter seasons
  plt.plot(february_snowfall_past_years.index, february_snowfall_past_years.values, marker='o', label='Historical Snowfall (2014-2023)')

  # Plot snowfall for February 2024 events
  plt.bar([2024], [total_snowfall_event_1], color='blue', label='Feb 2-4, 2024')
  plt.bar([2024], [total_snowfall_event_2], color='green', label='Feb 12-13, 2024')

  # Highlight rare events with different colors
  if rare_event_1:
      plt.bar([2024], [total_snowfall_event_1], color='red')
  if rare_event_2:
      plt.bar([2024], [total_snowfall_event_2], color='orange')

  plt.xlabel('Year')
  plt.ylabel('Total Snowfall (mm)')
  plt.title('Snowfall Comparison: Feb 2024 vs. Historical (2014-2023)')
  plt.legend()
  plt.grid(True)
  plt.xticks(february_snowfall_past_years.index.append(pd.Index([2024])))  # Ensure all years are shown on x-axis

  plt.show()


def main_backup(df):
  # Sort DataFrame by 'LOCAL_DATE' (monthly date) in ascending order
  df['LOCAL_DATE'] = pd.to_datetime(df['LOCAL_DATE'])  # Convert to datetime
  df = df.sort_values(by='LOCAL_DATE')

  # Extract data for specific periods
  # february_2024 = df[(df['LOCAL_DATE'] >= '2024-01-01') & (df['LOCAL_DATE'] <= '2024-03-01')]
  past_10_years = df[(df['LOCAL_DATE'] >= '2014-01-01') & (df['LOCAL_DATE'] <= '2023-10-31')]

  # Specify February 2024 date ranges
  february_first_event = (pd.Timestamp('2024-02-02'), pd.Timestamp('2024-02-04'))
  february_second_event = (pd.Timestamp('2024-02-12'), pd.Timestamp('2024-02-13'))

  # Extract snowfall data for the two February 2024 events
  snow_event_1 = df[(df['LOCAL_DATE'] >= february_first_event[0]) & (df['LOCAL_DATE'] <= february_first_event[1])]
  snow_event_2 = df[(df['LOCAL_DATE'] >= february_second_event[0]) & (df['LOCAL_DATE'] <= february_second_event[1])]

  # Sum snowfall for both events
  total_snowfall_event_1 = snow_event_1['SNOW_ON_GROUND'].sum()
  total_snowfall_event_2 = snow_event_2['SNOW_ON_GROUND'].sum()

  # # Extract historical February snowfall data (2013-2023)
  # february_data = df[df['LOCAL_DATE'].dt.month == 2]

  # Aggregate data by day and compare historical events
  february_snowfall_past_years = past_10_years.groupby(past_10_years['LOCAL_DATE'].dt.year)['SNOW_ON_GROUND'].sum()

  # Compare the current events to the historical snowfall data
  rare_event_1 = (february_snowfall_past_years >= total_snowfall_event_1).sum() == 0
  rare_event_2 = (february_snowfall_past_years >= total_snowfall_event_2).sum() == 0

  # Print results
  print(f"Total Snowfall in Feb 2-4 Event (2024): {total_snowfall_event_1} mm")
  print(f"Is Feb 2-4 Event Rare? {'Yes' if rare_event_1 else 'No'}")

  print(f"Total Snowfall in Feb 12-13 Event (2024): {total_snowfall_event_2} mm")
  print(f"Is Feb 12-13 Event Rare? {'Yes' if rare_event_2 else 'No'}")


FILE_NAME = 'q2_data.csv'
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

# # Assuming 'data' is a DataFrame with the historical weather data including 2024
# # Example data structure should include date, snowfall, and other relevant columns

# # Convert to datetime if not already
# df['date'] = pd.to_datetime(df['date'])

# # Specify February 2024 date ranges
# february_first_event = (pd.Timestamp('2024-02-02'), pd.Timestamp('2024-02-04'))
# february_second_event = (pd.Timestamp('2024-02-12'), pd.Timestamp('2024-02-13'))

# # Extract snowfall data for the two February 2024 events
# snow_event_1 = df[(df['date'] >= february_first_event[0]) & (df['date'] <= february_first_event[1])]
# snow_event_2 = df[(df['date'] >= february_second_event[0]) & (df['date'] <= february_second_event[1])]

# # Sum snowfall for both events
# total_snowfall_event_1 = snow_event_1['snowfall'].sum()
# total_snowfall_event_2 = snow_event_2['snowfall'].sum()

# # Extract historical February snowfall data (2013-2023)
# february_data = df[df['date'].dt.month == 2]

# # Aggregate data by day and compare historical events
# february_snowfall_past_years = february_data.groupby(february_data['date'].dt.strftime('%Y-%m-%d'))['snowfall'].sum()

# # Compare the current events to the historical snowfall data
# rare_event_1 = (february_snowfall_past_years >= total_snowfall_event_1).sum() == 0
# rare_event_2 = (february_snowfall_past_years >= total_snowfall_event_2).sum() == 0

# # Print results
# print(f"Total Snowfall in Feb 2-4 Event (2024): {total_snowfall_event_1} mm")
# print(f"Is Feb 2-4 Event Rare? {'Yes' if rare_event_1 else 'No'}")

# print(f"Total Snowfall in Feb 12-13 Event (2024): {total_snowfall_event_2} mm")
# print(f"Is Feb 12-13 Event Rare? {'Yes' if rare_event_2 else 'No'}")