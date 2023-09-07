import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data into a DataFrame
df = pd.read_excel('emans_data.xlsx')

# ------------------Preprocessing the data------------------
# Filter out rows with wrong number of semicolons for Goals and Mood at the same time
df = df[(df['Goals'].str.count(';') == 6) & (df['Mood'].str.count(';') == 6)]



# Only keep the 'Date' and re'Mood' columns
df = df[['Date', 'Mood','Weight_AM','Food_Quality','MJ','alcohol','eating_out','Goals','take_ante_dee']]

# Rename Weight_AM to Weight
df.rename(columns={'Weight_AM': 'Weight','alcohol': 'Alcohol','eating_out': 'Eating_Out','take_ante_dee':'Take_Medication'}, inplace=True)


# # Convert 'Date' to a datetime object
df['Date'] = pd.to_datetime(df['Date'])
df['Mood'] = df['Mood'].str.split(';')
df['Goals'] = df['Goals'].str.split(';')


# Assign numerical values to the moods and calculate average mood
mood_dict = {'M-': -1, 'M': 0, 'M+': 1, 'M-e': -1, 'M+e': 1, 'M-l': -1, 'M+l': 1, 'Ml': 0, 'M': 0,'Me': 0}
df['Average_Mood'] = df['Mood'].apply(lambda x: sum(mood_dict[i.strip()] for i in x if i.strip() in mood_dict) / len(x))
goal_dict = {'G-': -1, 'G': 0, 'G+': 1, 'G-e': -1, 'G+e': 1, 'G-l': -1, 'G+l': 1, 'Gl': 0, 'G': 0, 'Ge': 0}
df['Average_Goal'] = df['Goals'].apply(lambda x: sum(goal_dict[i.strip()] for i in x if i.strip() in goal_dict) / len(x))

# Creating new columns 'MJ' and 'Love' from existing 'MJ' column
df['M_J'] = df['MJ'].apply(lambda x: 1 if any(substring in str(x) for substring in ['1-love', '1-Love', '1']) else 0)
df['Love'] = df['MJ'].apply(lambda x: 1 if any(substring in str(x) for substring in ['1-love', '1-Love','Love','love']) else 0)

df.rename(columns={'MJ': 'MJ_original','M_J': 'MJ'}, inplace=True)

## Food Quality
# Split the 'Food_Quality' string into a list of individual quality ratings
df['Food_Quality'] = df['Food_Quality'].str.split(';')

# Define a dictionary to map shorthand notations to numerical values
food_quality_dict = {'L': 0, 'Ll': 0, 'Le': 0,
                     'M': 3, 'Ml': 3, 'Me': 3,
                     'H': 5, 'Hl': 5, 'He': 5}

# Calculate the average food quality based on the mapping dictionary
df['Average_FQ'] = df['Food_Quality'].apply(lambda x: sum(food_quality_dict[i.strip()] for i in x if i.strip() in food_quality_dict) / len(x)/5)

df['Weight_Change'] = df['Weight'].diff().apply(lambda x: 1 if x < 0 else 0)

# Now df_grouped will have the average Food Quality for each day

## Extract Weight, Date, Average Mood, Average Goal, Average Food Quality, MJ, Love, Alcohol, Eating_Out
df_grouped = df[['Date', 'Weight','Average_Mood','Average_Goal','Average_FQ','MJ','Love','Alcohol','Eating_Out','Weight_Change','Take_Medication']].groupby('Date').mean().reset_index()



df = df_grouped
# Initialize metric
df['Daily_Metric'] = 0

# Configure weights for each variable.
# Assuming that all variables are equally important for simplicity.
# Feel free to change these weights as you see fit.
weights = {
    'Average_Mood': 1,
    'Average_Goal': 1,
    'Average_FQ': 1,
    'MJ': 1,
    'Love': 1,
    'Alcohol': 1,
    'Eating_Out': 1,
    'Weight_Change': 1
}

# Update metric based on each variable's contribution
df['Daily_Metric'] += weights['Average_Mood'] * df['Average_Mood']
df['Daily_Metric'] += weights['Average_Goal'] * df['Average_Goal']
df['Daily_Metric'] += weights['Average_FQ'] * (1 - df['Average_FQ'])  # Closer to 0 is better, so we take 1 - value
df['Daily_Metric'] += weights['MJ'] * (1 - df['MJ'])  # 0 is good, so we take 1 - value
df['Daily_Metric'] += weights['Love'] * df['Love']  # 1 is good
df['Daily_Metric'] += weights['Alcohol'] * (1 - df['Alcohol'])  # 0 is good, so we take 1 - value
df['Daily_Metric'] += weights['Eating_Out'] * (1 - df['Eating_Out'])  # 0 is good, so we take 1 - value
df['Daily_Metric'] += weights['Weight_Change'] * df['Weight_Change']  # 1 is good

# You can also apply a rolling average if you'd like to smooth out the daily metrics.
df['Daily_Metric_Rolling_Avg'] = df['Daily_Metric'].rolling(window=7).mean()

df.to_csv('emans_data_processed.csv', index=False)



# Create a plot
plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['Daily_Metric'], marker='o')
plt.title('Daily Metric Over Time')
plt.xlabel('Date')
plt.ylabel('Daily Metric')
plt.grid(True)
plt.show()



# Create a plot
fig, ax1 = plt.subplots(figsize=(10, 6))

color = 'tab:blue'
ax1.set_xlabel('Date')
ax1.set_ylabel('Daily Metric')
ax1.grid(True)

# Scatter plot for Daily_Metric colored based on Take_Medication
scatter = ax1.scatter(df['Date'], df['Daily_Metric'], c=df['Take_Medication'], cmap='coolwarm', marker='o', label='Daily Metric')

# Add a colorbar to explain the color coding
cbar = plt.colorbar(scatter, ticks=[0,1])
cbar.set_label('Take_Medication')

plt.title('Daily Metric Over Time with Medication Info')
plt.show()







