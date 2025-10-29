import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from collections import Counter

# Load the data
df = pd.read_csv('telecom_customer_call_records_100.csv')

# Clean any potential issues
df = df.dropna()

# Create a simplified version of the network by grouping towers by city
G = nx.Graph()

# Create city-based nodes
cities = df['Place'].unique()
for i, city in enumerate(cities, 1):
    G.add_node(i, label=city)

# Add edges between cities based on call patterns
# Two cities are connected if they share towers or have similar call patterns
city_connections = []
for i in range(len(cities)):
    for j in range(i+1, len(cities)):
        city_i = cities[i]
        city_j = cities[j]
        
        # Get towers for each city
        towers_i = df[df['Place'] == city_i]['Tower_ID'].unique()
        towers_j = df[df['Place'] == city_j]['Tower_ID'].unique()
        
        # Check if they share any towers or have similar call patterns
        if len(set(towers_i).intersection(set(towers_j))) > 0:
            city_connections.append((i+1, j+1))
        else:
            # Check if they have similar average call durations
            avg_dur_i = df[df['Place'] == city_i]['Call_Duration_sec'].mean()
            avg_dur_j = df[df['Place'] == city_j]['Call_Duration_sec'].mean()
            
            # If average durations are within 10% of each other, consider them connected
            if abs(avg_dur_i - avg_dur_j) / max(avg_dur_i, avg_dur_j) < 0.1:
                city_connections.append((i+1, j+1))

# Add edges to graph
for i, j in city_connections:
    G.add_edge(i, j)

# Create the force-directed layout visualization
plt.figure(figsize=(10, 8))
plt.title("Transportation Network - Force-Based Layout")

# Use spring layout for force-directed positioning
pos = nx.spring_layout(G, seed=42)

# Draw nodes with a green color
nx.draw_networkx_nodes(G, pos, node_color='lightgreen', node_size=500, edgecolors='black')

# Draw edges
nx.draw_networkx_edges(G, pos, width=1.5)

# Draw labels (node numbers)
nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold')

# Remove axes
plt.axis('off')

# Save the figure
plt.tight_layout()
plt.savefig('telecom_force_network.png', dpi=300, bbox_inches='tight')
plt.close()

print("Force-based network visualization created as 'telecom_force_network.png'")

