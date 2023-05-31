import pandas as pd
import matplotlib.pyplot as plt

# Load your DataFrame
df = pd.read_excel('emans_data.xlsx')

# Convert 'Date' to datetime if not already done
df['Date'] = pd.to_datetime(df['Date'])

# Creating new columns 'MJ' and 'Love' from existing 'MJ' column
df['MJ_new'] = df['MJ'].apply(lambda x: 1 if any(substring in str(x) for substring in ['1-love', '1-Love', '1']) else 0)
df['Love'] = df['MJ'].apply(lambda x: 1 if any(substring in str(x) for substring in ['1-love', '1-Love','Love','love']) else 0)

# Rename the original 'MJ' column to 'MJ_original' to avoid confusion
df.rename(columns={'MJ': 'MJ_original'}, inplace=True)

# Set 'Date' as index to use resample function
df.set_index('Date', inplace=True)

# Calculate the weekly sum of 'MJ_new' and 'Love' columns
df_weekly = df[['MJ_new', 'Love']].resample('M').sum()

# Plot the weekly sum of 'MJ_new' and 'Love'
plt.figure(figsize=(10, 6))
plt.plot(df_weekly.index, df_weekly['MJ_new'], label='MJ_new', color='blue')
plt.plot(df_weekly.index, df_weekly['Love'], label='Love', color='red')
plt.xlabel('Week')
plt.ylabel('Count')
plt.title('Weekly count of 1\'s in MJ_new and Love')
plt.legend()
plt.show()
