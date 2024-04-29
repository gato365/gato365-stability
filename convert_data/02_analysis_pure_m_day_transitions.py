import pandas as pd

# Load the data into a DataFrame
df = pd.read_excel('emans_data.xlsx')

# Only keep the 'Date' and 'Mood' columns
df = df[['Date', 'Mood']]

# Filter out rows with wrong number of semicolons
df = df[df['Mood'].str.count(';') == 6]


# Convert Mood into a format we can analyze
df['Mood'] = df['Mood'].apply(lambda x: [i for i in x.split(';') if i and i[-1] != 'e'])

# Convert mood values to scores and calculate average mood for each day
# Define a function to handle this preprocessing
def preprocess_mood(mood):
    mood = mood.strip()  # Remove leading/trailing whitespace
    if mood.endswith('e') or mood.endswith('l'):
        mood = mood[:-1]  # Remove the last character ('e' or 'l')
    return mood

# Use this function in your lambda function
df['Average_Mood'] = df['Mood'].apply(
    lambda x: sum({'M-': -1, 'M': 0, 'M+': 1}.get(preprocess_mood(i), 0) for i in x) / len(x)
)


# Classify days
df['Day_Classification'] = pd.cut(df['Average_Mood'], bins=[-1.5, -0.5, 0.5, 1.5], labels=['Bad', 'Decent', 'Good'])

# Create transition matrix
df['Day_Classification_shifted'] = df['Day_Classification'].shift(-1)
transition_counts = pd.crosstab(df['Day_Classification'], df['Day_Classification_shifted'])
transition_probabilities = transition_counts.divide(transition_counts.sum(axis=1), axis=0)

print(transition_probabilities)
