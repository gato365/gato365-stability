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

# Assign season based on month
def assign_season(month):
    if month in [3, 4, 5]:   # Spring
        return 'Spring'
    elif month in [6, 7, 8]: # Summer
        return 'Summer'
    elif month in [9, 10, 11]: # Fall
        return 'Fall'
    else: # Winter
        return 'Winter'

df['Season'] = df['Date'].dt.month.apply(assign_season)

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
melted_df = pd.melt(df, id_vars=['Date', 'Season'], value_vars=times_of_day, var_name='Time_of_Day', value_name='Mood')

# First, calculate the mean mood for each time of the day
mean_moods = melted_df.groupby(['Season', 'Time_of_Day'])['Mood'].mean().reset_index()

# Plot mean mood by time of day for each season
## Enforce the order of the time of day

mean_moods['Time_of_Day'] = pd.Categorical(mean_moods['Time_of_Day'], times_of_day)
mean_moods.sort_values('Time_of_Day', inplace=True)
plt.figure(figsize=(12, 6))
sns.lineplot(x='Time_of_Day', y='Mood', hue='Season', data=mean_moods, marker='o')
plt.title('Average Mood by Time of Day across Seasons')
plt.xlabel('Time of Day')
plt.ylabel('Mean Mood')
plt.show()
