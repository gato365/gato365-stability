import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data into a DataFrame
df = pd.read_excel('emans_data.xlsx')

# ------------------Preprocessing the data------------------
# Filter out rows with wrong number of semicolons
df = df[df['Mood'].str.count(';') == 6]

# Only keep the 'Date' and re'Mood' columns
df = df[['Date', 'Mood','Weight_AM']]

# Rename Weight_AM to Weight
df.rename(columns={'Weight_AM': 'Weight'}, inplace=True)

# Convert 'Date' to a datetime object
df['Date'] = pd.to_datetime(df['Date'])
df['Mood'] = df['Mood'].str.split(';')

# Assign numerical values to the moods and calculate average mood
mood_dict = {'M-': -1, 'M': 0, 'M+': 1, 'M-e': -1, 'M+e': 1, 'M-l': -1, 'M+l': 1, 'Ml': 0, 'M': 0,'Me': 0}
df['Average_Mood'] = df['Mood'].apply(lambda x: sum(mood_dict[i.strip()] for i in x if i.strip() in mood_dict) / len(x))

# Calculate rolling mean of 'Average_Mood' and 'Weight' and find the best correlation
best_corr = 0
best_window = 0

for window in range(1, 31):  # Loop from 1 to 30
    df['Average_Mood_rolling'] = df['Average_Mood'].rolling(window).mean()
    df['Weight_rolling'] = df['Weight'].rolling(window).mean()

    # Calculate the correlation
    corr = df[['Average_Mood_rolling', 'Weight_rolling']].corr().iloc[0, 1]
    
    # Check if this window's correlation is higher than the current best correlation
    if np.abs(corr) > np.abs(best_corr):
        best_corr = corr
        best_window = window

print(f"The highest absolute correlation is {best_corr} and occurs with a {best_window}-day rolling average.")

# Visualization with best window
df['Average_Mood_rolling'] = df['Average_Mood'].rolling(best_window).mean()
df['Weight_rolling'] = df['Weight'].rolling(best_window).mean()

plt.figure(figsize=(10,5))
plt.scatter(df['Average_Mood_rolling'], df['Weight_rolling'], label=f'{best_window}-Day Average Weight vs. Mood')
plt.xlabel(f'{best_window}-Day Average Mood')
plt.ylabel(f'{best_window}-Day Average Weight')
plt.legend()
plt.show()
