import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data into a DataFrame
df = pd.read_excel('emans_data_lite.xlsx')

# Only keep the 'Date' and 'Goals' columns
df = df[['Date', 'Goals']]

# Filter out rows with wrong number of semicolons
df = df[df['Goals'].str.count(';') == 6]

# Convert Goal into a format we can analyze
def process_goal(goal_string):
    goals = goal_string.split(';')
    processed_goals = []
    for goal in goals:
        if goal.endswith('e'):
            processed_goals.append(goal[:-1])
        elif goal.endswith('l'):
            processed_goals.append(goal[:-1] + 'l')
        else:
            processed_goals.append(goal)
    return processed_goals

df['Goals'] = df['Goals'].apply(process_goal)

# Create a list of all goal transitions
goal_transitions = []
for goal_list in df['Goals']:
    for i in range(len(goal_list) - 1):
        goal_transitions.append((goal_list[i], goal_list[i+1]))

# Create a DataFrame of transition counts
goal_order = ['G-l', 'G-', 'Gl', 'G', 'G+l', 'G+']
transition_counts = pd.DataFrame(index=goal_order, columns=goal_order)
transition_counts = transition_counts.fillna(0)

for transition in goal_transitions:
    if transition[0] in transition_counts.index and transition[1] in transition_counts.columns:
        transition_counts.loc[transition[0], transition[1]] += 1

# Convert counts to probabilities
transition_probabilities = transition_counts.divide(transition_counts.sum(axis=1), axis=0)

# Create the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(transition_probabilities, annot=True, cmap='coolwarm', fmt='.2f', annot_kws={'size': 10}, xticklabels=goal_order, yticklabels=goal_order)

# Add sample size to each square
for i in range(len(goal_order)):
    for j in range(len(goal_order)):
        count = transition_counts.loc[goal_order[i], goal_order[j]]
        prob = transition_probabilities.loc[goal_order[i], goal_order[j]]
        text = f'\n\n({count})'
        plt.text(j + 0.5, i + 0.5, text, ha='center', va='center', color='black', fontsize=10)

plt.title('Goal Transition Probabilities with Sample Size')
plt.ylabel('Current Goal')
plt.xlabel('Next Goal')

plt.show()
