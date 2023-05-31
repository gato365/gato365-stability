import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

# Calculate ratio of MJ_new to Love, replace division by zero with 0
df_weekly['MJ_Love_ratio'] = np.where(df_weekly['Love'] != 0, df_weekly['MJ_new'] / df_weekly['Love'], 0)

# Plot the weekly ratio of 'MJ_new' to 'Love'
plt.figure(figsize=(10, 6))
plt.plot(df_weekly.index, df_weekly['MJ_Love_ratio'], label='MJ_new / Love', color='purple')
plt.xlabel('Week')
plt.ylabel('Ratio')
plt.title('Weekly ratio of MJ_new to Love')
plt.legend()
plt.show()
