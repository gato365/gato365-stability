# Import the necessary library
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

# Calculate the number of 1's in 'MJ_new' and 'Love' columns
count_mj = df['MJ_new'].sum()
count_love = df['Love'].sum()

# Prepare data for plotting
data = {'MJ_new': count_mj, 'Love': count_love}

# Create bar plot
plt.figure(figsize=(10,6))
plt.bar(data.keys(), data.values())
plt.xlabel('Variable')
plt.ylabel('Count')
plt.title('Count of 1\'s in MJ_new and Love')
plt.show()
