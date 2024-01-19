import pandas as pd
import matplotlib.pyplot as plt

# Assuming you have already read the data into df
df = pd.read_excel('emans_data.xlsx')

# Preprocessing the data
# Assume that the 'Mood' column exists and filter out rows accordingly
df = df[df['Mood'].str.count(';') == 6]

# Only keep the 'Date' and 'Weight_AM' columns
df = df[['Date', 'Weight_AM']]

# Rename 'Weight_AM' to 'Weight'
df.rename(columns={'Weight_AM': 'Weight'}, inplace=True)

# Convert 'Date' to a datetime object
df['Date'] = pd.to_datetime(df['Date'])

# Set 'Date' as the index of the DataFrame
df.set_index('Date', inplace=True)

# Filter for dates from June 2023 to present
start_date = pd.Timestamp('2023-06-01')
df_filtered = df[df.index >= start_date]

# Resample the data by week and calculate the median weight for each week
median_weight_weekly = df_filtered['Weight'].resample('W').mean()

# Plot the median weight per week against time
plt.figure(figsize=(10,5))
median_weight_weekly.plot(marker='o', linestyle='-')
plt.title('Median Weight Per Week from June 2023')
plt.xlabel('Date')
plt.ylabel('Median Weight')
plt.grid(True)
plt.show()
