import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the DataFrame
df = pd.read_excel('emans_data.xlsx')

# Filter out rows with wrong number of semicolons
df = df[df['Mood'].str.count(';') == 6]

# Convert 'Date' to datetime if not already done
df['Date'] = pd.to_datetime(df['Date'])

# Creating new columns 'MJ' and 'Love' from existing 'MJ' column
df['MJ_new'] = df['MJ'].apply(lambda x: 1 if any(substring in str(x) for substring in ['1-love', '1-Love', '1']) else 0)
df['Love'] = df['MJ'].apply(lambda x: 1 if any(substring in str(x) for substring in ['1-love', '1-Love','Love','love']) else 0)




# Rename the original 'MJ' column to 'MJ_original' to avoid confusion
df.rename(columns={'MJ': 'MJ_original'}, inplace=True)

# Let's assume the 'Average_Mood' is calculated and available in the DataFrame
# Assign numerical values to the moods and calculate average mood
mood_dict = {'M-': -1, 'M': 0, 'M+': 1, 'M-e': -1, 'M+e': 1, 'M-l': -1, 'M+l': 1, 'Ml': 0, 'M': 0,'Me': 0}
# Split the 'Mood' column
df['Mood'] = df['Mood'].str.split(';')

# Then calculate the 'Average_Mood' as before
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


# Now we will calculate the correlation between 'MJ_new', 'Love', 'Average_Mood'
corr = df[['MJ_new', 'Love', 'Average_Mood']].corr()

# Display the correlation matrix
print(corr)

# Plotting the correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation between MJ_new, Love, and Average Mood')
plt.show()
