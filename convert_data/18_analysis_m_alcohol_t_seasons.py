import pandas as pd
import matplotlib.pyplot as plt

# Load the data into a DataFrame
df = pd.read_excel('emans_data_lite.xlsx')

# ------------------Preprocessing the data------------------
# Filter out rows with wrong number of semicolons
df = df[df['Mood'].str.count(';') == 6]

## Change alcohol to Alcohol
df.rename(columns={'alcohol': 'Alcohol'}, inplace=True)

# Only keep the 'Date', 'Mood', 'Weight_AM', and 'Alcohol' columns
df = df[['Date', 'Mood', 'Weight_AM', 'Alcohol']]

# Rename Weight_AM to Weight
df.rename(columns={'Weight_AM': 'Weight'}, inplace=True)

# Convert 'Date' to a datetime object
df['Date'] = pd.to_datetime(df['Date'])
df['Mood'] = df['Mood'].str.split(';')

# Assign numerical values to the moods and calculate average mood
mood_dict = {'M-': -1, 'M': 0, 'M+': 1, 'M-e': -1, 'M+e': 1, 'M-l': -1, 'M+l': 1, 'Ml': 0, 'M': 0,'Me': 0}
df['Average_Mood'] = df['Mood'].apply(lambda x: sum(mood_dict[i.strip()] for i in x if i.strip() in mood_dict) / len(x))

# Calculate the running sum of Alcohol
df['Alcohol_Running_Sum'] = df['Alcohol'].cumsum()

# If your weight data is in another DataFrame or Series:
# Make sure that your weight data aligns correctly with your existing DataFrame.
# If your weight data is a separate DataFrame or Series, you may want to merge or join it to your existing DataFrame.
# For example:
# df = df.merge(weight_df, on='Date', how='left')

# Descriptive Statistics
print("Average Mood: ", df['Average_Mood'].mean())
print("Mood Standard Deviation: ", df['Average_Mood'].std())
print("Average Weight: ", df['Weight'].mean())
print("Weight Standard Deviation: ", df['Weight'].std())

# Correlation Analysis
print("Correlation between Mood and Weight: ", df[['Average_Mood', 'Weight']].corr())

# Visualization
plt.figure(figsize=(10, 5))
## x-axis is Alcohol_Running_Sum
plt.plot(df['Alcohol_Running_Sum'], df['Average_Mood'], label='Average Mood')
## y-axis is  Average_Mood
# plt.plot(df['Date'], df['Weight'], label='Weight')
# plt.plot(df['Date'], df['Average_Mood'], label='Average Mood')
# plt.plot(df['Date'], df['Alcohol_Running_Sum'], label='Alcohol Running Sum')
plt.legend()
plt.show()
