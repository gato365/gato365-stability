import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data into a DataFrame
df = pd.read_excel('emans_data.xlsx')

# ------------------Preprocessing the data------------------
# Filter out rows with wrong number of semicolons
df = df[df['Mood'].str.count(';') == 6]

# Only keep the 'Date', 'Mood', and 'Weight_AM' columns
df = df[['Date', 'Mood', 'Weight_AM']]

# Rename Weight_AM to Weight
df.rename(columns={'Weight_AM': 'Weight'}, inplace=True)

# Convert 'Date' to a datetime object
df['Date'] = pd.to_datetime(df['Date'])
df['Mood'] = df['Mood'].str.split(';')

# Assign numerical values to the moods and calculate average mood
mood_dict = {'M-': -1, 'M': 0, 'M+': 1, 'M-e': -1, 'M+e': 1, 'M-l': -1, 'M+l': 1, 'Ml': 0, 'M': 0,'Me': 0}
df['Average_Mood'] = df['Mood'].apply(lambda x: sum(mood_dict[i.strip()] for i in x if i.strip() in mood_dict) / len(x))

# Time slots
times_of_day = ['4AM', '7:45AM', '10:45AM', '12PM', '3PM', '6PM', '8:30PM']

# Expand 'Mood' list into multiple columns and assign each column to a time of day
mood_df = df['Mood'].apply(pd.Series)
mood_df.columns = times_of_day
for time in times_of_day:
    mood_df[time] = mood_df[time].map(mood_dict)

# Merge the new mood columns with the original DataFrame
df = pd.concat([df, mood_df], axis=1)

# Plotting the average mood by time of day
melted_df = pd.melt(df, id_vars=['Date'], value_vars=times_of_day, var_name='Time_of_Day', value_name='Mood')


# Print the summary of each time of day of Mood 
for time in times_of_day:
    print(f"Summary of {time}:")
    print(melted_df[melted_df['Time_of_Day'] == time]['Mood'].describe())
    print()


# First, calculate the mean mood for each time of the day
mean_moods = melted_df.groupby('Time_of_Day')['Mood'].mean()[times_of_day]
## Add Error Bars
# Calculate the standard deviation of mood for each time of the day
std_moods = melted_df.groupby('Time_of_Day')['Mood'].std()[times_of_day]

# Plot mean mood by time of day
plt.figure(figsize=(12, 6))
sns.lineplot(x=times_of_day, y=mean_moods, marker='o', sort=False)
# plt.errorbar(x=times_of_day, y=mean_moods, yerr=std_moods, linestyle='', color='black')
plt.title('Average Mood by Time of Day')
plt.xlabel('Time of Day')
plt.ylabel('Mean Mood')
plt.show()

