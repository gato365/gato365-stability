import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data into a DataFrame
df = pd.read_excel('emans_data.xlsx')

# ------------------Preprocessing the data------------------
# Filter out rows with wrong number of semicolons
df = df[df['Mood'].str.count(';') == 6]

# Only keep the 'Date' and 'Mood' columns
df = df[['Date', 'Mood','Weight_AM']]

# Rename Weight_AM to Weight
df.rename(columns={'Weight_AM': 'Weight'}, inplace=True)

# Convert 'Date' to a datetime object
df['Date'] = pd.to_datetime(df['Date'])
df['Mood'] = df['Mood'].str.split(';')

# Assign numerical values to the moods and calculate average mood
mood_dict = {'M-': -1, 'M': 0, 'M+': 1, 'M-e': -1, 'M+e': 1, 'M-l': -1, 'M+l': 1, 'Ml': 0, 'M': 0,'Me': 0}
df['Average_Mood'] = df['Mood'].apply(lambda x: sum(mood_dict[i.strip()] for i in x if i.strip() in mood_dict) / len(x))

# Calculate the 30-day rolling mean of 'Average_Mood' and 'Weight'
df['Average_Mood_30D'] = df['Average_Mood'].rolling(30).mean()
df['Weight_30D'] = df['Weight'].rolling(30).mean()

# Split the data into two groups
df_below_222 = df[df['Weight_30D'] <= 222]
df_above_222 = df[df['Weight_30D'] > 222]

# Correlation Analysis
print("Correlation between Mood and Weight for weights <= 222: ", df_below_222[['Average_Mood_30D', 'Weight_30D']].corr().iloc[0,1])
print("Correlation between Mood and Weight for weights > 222: ", df_above_222[['Average_Mood_30D', 'Weight_30D']].corr().iloc[0,1])

# Visualization
plt.figure(figsize=(10,5))

plt.scatter(df_below_222['Average_Mood_30D'], df_below_222['Weight_30D'], label='Weights <= 222')
plt.scatter(df_above_222['Average_Mood_30D'], df_above_222['Weight_30D'], label='Weights > 222')

plt.xlabel('30-Day Average Mood')
plt.ylabel('30-Day Average Weight')
plt.legend()
plt.show()
