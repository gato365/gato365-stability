import pandas as pd
import matplotlib.pyplot as plt

# Load the data into a DataFrame
df = pd.read_excel('emans_data_lite.xlsx')

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

# Calculate the 7-day rolling mean of 'Average_Mood' and 'Weight'
df['Average_Mood_7D'] = df['Average_Mood'].rolling(7).mean()
df['Weight_7D'] = df['Weight'].rolling(7).mean()

# Descriptive Statistics
print("Average Mood: ", df['Average_Mood_7D'].mean())
print("Mood Standard Deviation: ", df['Average_Mood_7D'].std())
print("Average Weight: ", df['Weight_7D'].mean())
print("Weight Standard Deviation: ", df['Weight_7D'].std())

# Correlation Analysis
print("Correlation between Mood and Weight: ", df[['Average_Mood_7D', 'Weight_7D']].corr())

# Visualization
plt.figure(figsize=(10,5))
plt.scatter(df['Average_Mood_7D'], df['Weight_7D'], label='7-Day Average Weight vs. Mood')
plt.xlabel('7-Day Average Mood')
plt.ylabel('7-Day Average Weight')
plt.legend()
plt.show()
