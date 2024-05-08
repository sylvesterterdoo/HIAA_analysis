import pandas as pd
import matplotlib.pyplot as plt

# Data for the past 10 years
past_10_years_data = {
    2013: {'Mean Temperature': -0.7995698924731183, 'Total Snowfall': 83.5, 'Total Precipitation': 382.4},
    2014: {'Mean Temperature': -1.8850583717357914, 'Total Snowfall': 193.6, 'Total Precipitation': 1027.0},
    2015: {'Mean Temperature': -3.0613809523809525, 'Total Snowfall': 394.6, 'Total Precipitation': 764.2},
    2016: {'Mean Temperature': -1.0975765665554318, 'Total Snowfall': 296.9, 'Total Precipitation': 755.6},
    2017: {'Mean Temperature': -1.6563376591274257, 'Total Snowfall': 296.4, 'Total Precipitation': 773.4},
    2018: {'Mean Temperature': -1.3403795670403014, 'Total Snowfall': 243.7, 'Total Precipitation': 722.5},
    2019: {'Mean Temperature': -2.1349769585253457, 'Total Snowfall': 199.8, 'Total Precipitation': 695.9},
    2020: {'Mean Temperature': -0.11116869782053307, 'Total Snowfall': 246.7, 'Total Precipitation': 601.4},
    2021: {'Mean Temperature': -0.6649130434782609, 'Total Snowfall': 200.2, 'Total Precipitation': 734.0},
    2022: {'Mean Temperature': -0.5902596006144392, 'Total Snowfall': 98.4, 'Total Precipitation': 731.5},
    2023: {'Mean Temperature': -2.320238095238095, 'Total Snowfall': 102.9, 'Total Precipitation': 337.9}
}

# Data for winter 2024
winter_2024_data = {
    2024: {'Mean Temperature': -0.5001112347052284, 'Total Snowfall': 238.6, 'Total Precipitation': 863.8}
}

# Convert past 10 years data to DataFrame
past_10_years_df = pd.DataFrame(past_10_years_data).T

# Create a DataFrame for winter 2024 data
winter_2024_df = pd.DataFrame.from_dict(winter_2024_data, orient='index')

# Concatenate past 10 years and winter 2024 data
combined_df = pd.concat([past_10_years_df, winter_2024_df])

# Plotting mean temperature comparison
plt.figure(figsize=(10, 6))
plt.bar(combined_df.index, combined_df['Mean Temperature'], color='b', alpha=0.7)
plt.xlabel('Winter Season (Year)')
plt.ylabel('Mean Temperature (°C)')
plt.title('Comparison of Mean Temperature (Past 10 Years + Winter 2024)')
plt.grid(True)
plt.show()

# Plotting total snowfall comparison
plt.figure(figsize=(10, 6))
plt.bar(combined_df.index, combined_df['Total Snowfall'], color='g', alpha=0.7)
plt.xlabel('Winter Season (Year)')
plt.ylabel('Total Snowfall (mm)')
plt.title('Comparison of Total Snowfall (Past 10 Years + Winter 2024)')
plt.grid(True)
plt.show()

# Plotting total precipitation comparison
plt.figure(figsize=(10, 6))
plt.bar(combined_df.index, combined_df['Total Precipitation'], color='r', alpha=0.7)
plt.xlabel('Winter Season (Year)')
plt.ylabel('Total Precipitation (mm)')
plt.title('Comparison of Total Precipitation (Past 10 Years + Winter 2024)')
plt.grid(True)
plt.show()
