import pandas as pd
from scipy.stats import ttest_ind
import numpy as np

# Load the data into a DataFrame
df = pd.read_excel('emans_data.xlsx')

# ------------------Preprocessing the data------------------
# Filter out rows with wrong number of semicolons
df = df[df['Mood'].str.count(';') == 6]

# Only keep the 'Date', 'Mood' and 'Weight_AM' columns
df = df[['Date', 'Mood', 'Weight_AM']]

# Rename 'Weight_AM' to 'Weight'
df.rename(columns={'Weight_AM': 'Weight'}, inplace=True)

# Convert 'Date' to a datetime object
df['Date'] = pd.to_datetime(df['Date'])
df['Mood'] = df['Mood'].str.split(';')

# Assign numerical values to the moods and calculate average mood
mood_dict = {'M-': -1, 'M': 0, 'M+': 1, 'M-e': -1, 'M+e': 1, 'M-l': -1, 'M+l': 1, 'Ml': 0, 'M': 0,'Me': 0}
df['Average_Mood'] = df['Mood'].apply(lambda x: sum(mood_dict[i.strip()] for i in x if i.strip() in mood_dict) / len(x))

# Define the date you started taking antidepressants
start_date = pd.to_datetime('2022-02-10')

# Create a new column 'Antidepressant' which indicates whether the date is before or after starting the antidepressants
df['Antidepressant'] = df['Date'].apply(lambda x: 'After' if x >= start_date else 'Before')

# Calculate the average mood before and after starting the antidepressants
average_mood_before = df[df['Antidepressant'] == 'Before']['Average_Mood'].mean(skipna=True)
average_mood_after = df[df['Antidepressant'] == 'After']['Average_Mood'].mean(skipna=True)

print(f'Average Mood Before Antidepressants: {average_mood_before}')
print(f'Average Mood After Antidepressants: {average_mood_after}')

# Perform a t-test to compare the average mood before and after starting the antidepressants
mood_before = df[df['Antidepressant'] == 'Before']['Average_Mood'].dropna()
mood_after = df[df['Antidepressant'] == 'After']['Average_Mood'].dropna()

if not mood_before.empty and not mood_after.empty:
    t_stat, p_val = ttest_ind(mood_before, mood_after)
    print(f'T-Statistic: {t_stat}')
    print(f'P-Value: {p_val}')
else:
    print("T-Test could not be performed due to insufficient data.")
