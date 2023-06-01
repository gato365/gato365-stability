import pandas as pd
import matplotlib.pyplot as plt

# Load the data into a DataFrame
df = pd.read_excel('emans_data.xlsx')

# ------------------Preprocessing the data------------------
# Filter out rows with wrong number of semicolons
df = df[df['Mood'].str.count(';') == 6]

# Only keep the 'Date', 'Mood' and 'Weight_AM' columns
df = df[['Date', 'Mood','Weight_AM']]

# Filter on a year from today
df = df[df['Date'] > '2022-05-31']


# Rename Weight_AM to Weight
df.rename(columns={'Weight_AM': 'Weight'}, inplace=True)

# Convert 'Date' to a datetime object
df['Date'] = pd.to_datetime(df['Date'])
df['Mood'] = df['Mood'].str.split(';')

# Assign numerical values to the moods and calculate average mood
mood_dict = {'M-': -1, 'M': 0, 'M+': 1, 'M-e': -1, 'M+e': 1, 'M-l': -1, 'M+l': 1, 'Ml': 0, 'M': 0,'Me': 0}
df['Average_Mood'] = df['Mood'].apply(lambda x: sum(mood_dict[i.strip()] for i in x if i.strip() in mood_dict) / len(x))

# Calculate the num_days-day rolling mean of 'Average_Mood' and 'Weight'

num_days = 15
df['Average_Mood_30D'] = df['Average_Mood'].rolling(num_days).mean()
df['Weight_30D'] = df['Weight'].rolling(num_days).mean()

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







# Visualization of seasonal effects
seasons = ['Spring', 'Summer', 'Fall', 'Winter']

# Calculate correlation for each season
for season in seasons:
    season_df = df[df['Season'] == season]
    correlation = season_df[['Average_Mood_30D', 'Weight_30D']].corr().iloc[0,1]
    print(f"Correlation between Mood and Weight in {season}: {correlation}")



colors = ['green', 'red', 'orange', 'blue']
plt.figure(figsize=(10,5))
for season, color in zip(seasons, colors):
    season_df = df[df['Season'] == season]
    plt.scatter(season_df['Average_Mood_30D'], season_df['Weight_30D'], color=color, label=season)
plt.xlabel('30-Day Average Mood')
plt.ylabel('30-Day Average Weight')
plt.title('Seasonal Effects on Correlation between Mood and Weight')
plt.legend()
plt.show()
