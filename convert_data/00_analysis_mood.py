import pandas as pd
import matplotlib.pyplot as plt

# Load the data into a DataFrame
df = pd.read_excel('emans_data_lite.xlsx')

df = df[['Date', 'Mood']]

# Filter out rows with wrong number of semicolons
df = df[df['Mood'].str.count(';') == 6]

# Convert 'Date' to a datetime object
df['Date'] = pd.to_datetime(df['Date'])

# Create separate columns for each mood measurement
mood_times = ['4:00 am', '7:45 am', '10:45 am', '12:00 pm', '3:00 pm', '6:00 pm', '8:45 pm']
mood_cols = ['Mood_' + time.replace(' ', '_') for time in mood_times]
df[mood_cols] = df['Mood'].str.split(';', expand=True)


# Specify the penalty for late mood measurement
late_penalty = 0.1

# Convert Mood columns into a format we can analyze
for col in mood_cols:
    df[col] = df[col].apply(lambda x: {'M-': -1, 'M': 0, 'M+': 1}.get(x[:-2], 0) * (1 - late_penalty) if x.endswith('l') else {'M-': -1, 'M': 0, 'M+': 1}.get(x[:-2], 0) if x.endswith('e') else {'M-': -1, 'M': 0, 'M+': 1}.get(x, 0))

# Create 'Month' and 'Day_of_week' columns
df['Month'] = df['Date'].dt.month
df['Day_of_week'] = df['Date'].dt.dayofweek

# Calculate average mood for the day
df['Average_Mood'] = df[mood_cols].mean(axis=1)

# Calculate average mood for the day by month
average_mood_month = df.groupby('Month')['Average_Mood'].mean()

# Calculate average mood for the day by day of the week
average_mood_weekday = df.groupby('Day_of_week')['Average_Mood'].mean()

# Calculate average mood for the day by month and day of the week
average_mood_month_weekday = df.groupby(['Month', 'Day_of_week'])['Average_Mood'].mean()
# Calculate average mood for each time slot
average_mood_timeslot = df[mood_cols].mean()




# print(f'Average mood for the day is: {df["Average_Mood"].mean()}')
# print(f'Average mood for the day by month is:\n{average_mood_month}')
# print(f'Average mood for the day by day of the week is:\n{average_mood_weekday}')
# print(f'Average mood for the day by month and day of the week is:\n{average_mood_month_weekday}')
# print(f'Average mood for each time slot is:\n{average_mood_timeslot}')

# # To visualize the average mood fluctuation over the course of a day
# average_mood_timeslot.plot(kind='line', title='Average Mood Fluctuation Over the Day')




# # Plot average mood for the day
# plt.figure()
# plt.plot(df['Date'], df['Average_Mood'])
# plt.title('Average Mood Over Time')
# plt.xlabel('Date')
# plt.ylabel('Average Mood')
# plt.show()

# # Plot average mood for the day by month
# plt.figure()
# average_mood_month.plot(kind='bar')
# plt.title('Average Mood by Month')
# plt.xlabel('Month')
# plt.ylabel('Average Mood')
# plt.show()

# # Plot average mood for the day by day of the week
# plt.figure()
# average_mood_weekday.plot(kind='bar')
# plt.title('Average Mood by Day of the Week')
# plt.xlabel('Day of the Week')
# plt.ylabel('Average Mood')
# plt.show()

# # Plot average mood for the day by month and day of the week
# plt.figure()
# average_mood_month_weekday.unstack().plot(kind='bar')
# plt.title('Average Mood by Month and Day of the Week')
# plt.xlabel('Month')
# plt.ylabel('Average Mood')
# plt.show()

# # Plot average mood for each time slot
# plt.figure()
# average_mood_timeslot.plot(kind='line')
# plt.title('Average Mood Fluctuation Over the Day')
# plt.xlabel('Time Slot')
# plt.ylabel('Average Mood')
# plt.show()


# Create a figure with 5 subplots
fig, axs = plt.subplots(5, figsize=(15, 25))

# Plot average mood for the day
axs[0].plot(df['Date'], df['Average_Mood'])
axs[0].set_title('Average Mood Over Time')
axs[0].set_xlabel('Date')
axs[0].set_ylabel('Average Mood')

# Plot average mood for the day by month
average_mood_month.plot(kind='bar', ax=axs[1])
axs[1].set_title('Average Mood by Month')
axs[1].set_xlabel('Month')
axs[1].set_ylabel('Average Mood')

# Plot average mood for the day by day of the week
average_mood_weekday.plot(kind='bar', ax=axs[2])
axs[2].set_title('Average Mood by Day of the Week')
axs[2].set_xlabel('Day of the Week')
axs[2].set_ylabel('Average Mood')

# Plot average mood for the day by month and day of the week
average_mood_month_weekday.unstack().plot(kind='bar', ax=axs[3])
axs[3].set_title('Average Mood by Month and Day of the Week')
axs[3].set_xlabel('Month')
axs[3].set_ylabel('Average Mood')

# Plot average mood for each time slot
average_mood_timeslot.plot(kind='line', ax=axs[4])
axs[4].set_title('Average Mood Fluctuation Over the Day')
axs[4].set_xlabel('Time Slot')
axs[4].set_ylabel('Average Mood')

# Adjust layout for better visibility
plt.tight_layout()

# Show the dashboard
plt.show()