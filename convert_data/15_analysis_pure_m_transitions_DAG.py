import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load the data into a DataFrame
df = pd.read_excel('emans_data_lite.xlsx')

# Only keep the 'Date' and 'Goals' columns
df = df[['Date', 'Goals']]

# Filter out rows with wrong number of semicolons
df = df[df['Goals'].str.count(';') == 6]

# Convert Goals into a format we can analyze
def process_goals(goals_string):
    goals = goals_string.split(';')
    processed_goals = []
    for goal in goals:
        goal = goal.replace('l', '').replace('e', '').replace('!', '')
        if goal != '':
            processed_goals.append(goal)
    return processed_goals

df['Goals'] = df['Goals'].apply(process_goals)

# Create a list of all goal transitions
goal_transitions = []
for goal_list in df['Goals']:
    for i in range(len(goal_list) - 1):
        goal_transitions.append((goal_list[i], goal_list[i+1]))

# Create a directed graph
graph = nx.DiGraph()

# Add edges and calculate transition probabilities
for transition in goal_transitions:
    source = transition[0]
    target = transition[1]
    if graph.has_edge(source, target):
        graph[source][target]['count'] += 1
    else:
        graph.add_edge(source, target, count=1)

# Create labels for edges with transition probabilities
edge_labels = {(u, v): f'P={d["count"] / graph.out_degree(u):.2f}' for u, v, d in graph.edges(data=True)}

# Make the graph cyclic by adding self-loops
graph.add_edges_from([(node, node) for node in graph.nodes])

# Position nodes using a spring layout
pos = nx.spring_layout(graph)

# Draw the directed graph
plt.figure(figsize=(8, 6))
nx.draw_networkx(graph, pos, arrows=True, with_labels=True, node_size=5000, node_color='lightblue', font_size=12, font_color='black')
nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=10, label_pos=0.5, font_color='red')

plt.title('Cyclic Markov Chain Diagram')
plt.axis('off')
plt.tight_layout()
plt.show()
