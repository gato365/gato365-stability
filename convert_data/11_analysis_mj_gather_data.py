# Import the necessary library
import pandas as pd

# Load your DataFrame
df = pd.read_excel('emans_data.xlsx')

# Assume 'MJ' is one of the columns in the DataFrame and its values are as stated in your question

# Creating new columns 'MJ' and 'Love' from existing 'MJ' column
df['MJ_new'] = df['MJ'].apply(lambda x: 1 if any(substring in str(x) for substring in ['1-love', '1-Love', '1']) else 0)
df['Love'] = df['MJ'].apply(lambda x: 1 if any(substring in str(x) for substring in ['1-love', '1-Love','Love','love']) else 0)

# Rename the original 'MJ' column to 'MJ_original' to avoid confusion
df.rename(columns={'MJ': 'MJ_original'}, inplace=True)

# Select only MJ, MJ_new, Love columns
df = df[['Date', 'MJ_original', 'MJ_new', 'Love']]

# Now, df contains the newly created columns 'MJ_new' and 'Love' based on the conditions you described
df.to_csv('temp.csv', index=False)
