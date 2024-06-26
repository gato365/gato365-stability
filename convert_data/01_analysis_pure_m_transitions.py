import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data into a DataFrame
df = pd.read_excel('emans_data.xlsx')

# Only keep the 'Date' and 'Mood' columns
df = df[['Date', 'Mood']]

# Filter out rows with wrong number of semicolons
df = df[df['Mood'].str.count(';') == 6]

# Convert Mood into a format we can analyze
def process_mood(mood_string):
    moods = mood_string.split(';')
    processed_moods = []
    for mood in moods:
        if mood.endswith('e'):
            processed_moods.append(mood[:-1])
        elif mood.endswith('l'):
            processed_moods.append(mood[:-1] + 'l')
        else:
            processed_moods.append(mood)
    return processed_moods

df['Mood'] = df['Mood'].apply(process_mood)

# Create a list of all mood transitions
mood_transitions = []
for mood_list in df['Mood']:
    for i in range(len(mood_list) - 1):
        mood_transitions.append((mood_list[i], mood_list[i+1]))

# # Create a DataFrame of transition counts
# transition_counts = pd.DataFrame(index=['M-', 'M', 'M+', 'M-l', 'M', 'M+l'], columns=['M-', 'M', 'M+', 'M-l', 'M', 'M+l'])
# transition_counts = transition_counts.fillna(0)

# for transition in mood_transitions:
#     if transition[0] in transition_counts.index and transition[1] in transition_counts.columns:
#         transition_counts.loc[transition[0], transition[1]] += 1

# # Convert counts to probabilities
# transition_probabilities = transition_counts.divide(transition_counts.sum(axis=1), axis=0)

# print(transition_probabilities)

# # Create the heatmap
# plt.figure(figsize=(10,8))
# sns.heatmap(transition_probabilities, annot=True, cmap='coolwarm')

# plt.title('Mood Transition Probabilities')
# plt.ylabel('Current Mood')
# plt.xlabel('Next Mood')

# plt.show()


# Create a DataFrame of transition counts
mood_order = ['M-l', 'M-', 'Ml', 'M', 'M+l', 'M+']
transition_counts = pd.DataFrame(index=mood_order, columns=mood_order)
transition_counts = transition_counts.fillna(0)

for transition in mood_transitions:
    if transition[0] in transition_counts.index and transition[1] in transition_counts.columns:
        transition_counts.loc[transition[0], transition[1]] += 1

# Convert counts to probabilities
transition_probabilities = transition_counts.divide(transition_counts.sum(axis=1), axis=0)

# Create the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(transition_probabilities, annot=True, cmap='coolwarm', fmt='.2f', annot_kws={'size': 10}, xticklabels=mood_order, yticklabels=mood_order)

# Add sample size to each square
for i in range(len(mood_order)):
    for j in range(len(mood_order)):
        count = transition_counts.loc[mood_order[i], mood_order[j]]
        prob = transition_probabilities.loc[mood_order[i], mood_order[j]]
        text = f'\n\n({count})'
        plt.text(j + 0.5, i + 0.5, text, ha='center', va='center', color='black', fontsize=10)

plt.title('Mood Transition Probabilities with Sample Size')
plt.ylabel('Current Mood')
plt.xlabel('Next Mood')

plt.show()
