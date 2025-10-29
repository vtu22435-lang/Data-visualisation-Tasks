import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import numpy as np
from collections import Counter

# Load the data
df = pd.read_csv('telecom_customer_call_records_100.csv')

# Clean any potential issues
df = df.dropna()

# 1. Call Duration Distribution by City
plt.figure(figsize=(12, 6))
sns.boxplot(x='Place', y='Call_Duration_sec', data=df)
plt.title('Call Duration Distribution by City')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('call_duration_by_city.png')
plt.close()

# 2. City-based Call Volume
city_counts = df['Place'].value_counts()
plt.figure(figsize=(10, 6))
city_counts.plot(kind='bar', color=sns.color_palette("viridis", len(city_counts)))
plt.title('Number of Calls by City')
plt.xlabel('City')
plt.ylabel('Number of Calls')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('call_volume_by_city.png')
plt.close()

# 3. Network Graph of Tower Connections by City
G = nx.Graph()

# Add nodes (towers)
for _, row in df.iterrows():
    G.add_node(row['Tower_ID'], city=row['Place'])

# Connect towers based on common city
cities = df['Place'].unique()
for city in cities:
    city_towers = df[df['Place'] == city]['Tower_ID'].unique()
    # Connect each tower in the city with every other tower in that city
    for i in range(len(city_towers)):
        for j in range(i+1, len(city_towers)):
            G.add_edge(city_towers[i], city_towers[j], city=city)

# Create position layout
pos = nx.spring_layout(G, seed=42)

# Color nodes by city
city_colors = {city: idx for idx, city in enumerate(cities)}
node_colors = [city_colors[G.nodes[node]['city']] for node in G.nodes()]

plt.figure(figsize=(12, 10))
nx.draw_networkx(
    G, 
    pos=pos,
    node_color=node_colors, 
    node_size=80,
    with_labels=False,
    edge_color='gray',
    alpha=0.7,
    cmap=plt.cm.viridis
)

# Create legend for cities
city_patches = [plt.plot([], [], marker="o", ms=10, ls="", color=plt.cm.viridis(city_colors[city]/len(cities)), 
                         label=city)[0] for city in cities]
plt.legend(handles=city_patches, title="Cities", loc='upper right')

plt.title('Network of Tower Connections by City')
plt.axis('off')
plt.tight_layout()
plt.savefig('tower_network_by_city.png')
plt.close()

# 4. Heatmap of Call Durations by Tower and City
pivot_data = df.pivot_table(
    values='Call_Duration_sec', 
    index='Place',
    columns='Tower_ID',
    aggfunc='mean'
).fillna(0)

# Limit to top 15 towers for readability
top_towers = df.groupby('Tower_ID')['Call_Duration_sec'].sum().nlargest(15).index
pivot_limited = pivot_data[pivot_data.columns.intersection(top_towers)]

plt.figure(figsize=(14, 8))
sns.heatmap(pivot_limited, cmap="YlOrRd", annot=False, cbar_kws={'label': 'Avg Call Duration (sec)'})
plt.title('Average Call Duration by Tower and City (Top 15 Towers)')
plt.ylabel('City')
plt.xlabel('Tower ID')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('call_duration_heatmap.png')
plt.close()

# 5. Bipartite Graph: Customers to Towers
B = nx.Graph()

# Add customer and tower nodes
customers = df['Customer_ID'].unique()
towers = df['Tower_ID'].unique()

# Add nodes with attributes for bipartite graph
B.add_nodes_from(customers, bipartite=0)  # Customers
B.add_nodes_from(towers, bipartite=1)     # Towers

# Add edges between customers and towers
for _, row in df.iterrows():
    B.add_edge(row['Customer_ID'], row['Tower_ID'], weight=row['Call_Duration_sec'])

# Custom layout for better visualization
pos = {}
pos.update((node, (1, i)) for i, node in enumerate(customers))
pos.update((node, (2, i)) for i, node in enumerate(towers))

# Create the plot with limited connections for clarity
plt.figure(figsize=(10, 12))

# Draw the graph with limited number of edges for clarity
edges_to_show = [(u, v) for u, v in list(B.edges())[:100]]
weights = [B[u][v]['weight']/500 for u, v in edges_to_show]  # Scale weights for visibility

nx.draw_networkx_edges(B, pos, edgelist=edges_to_show, width=weights, alpha=0.3)
nx.draw_networkx_nodes(B, pos, nodelist=customers, node_color='skyblue', node_size=50, label='Customers')
nx.draw_networkx_nodes(B, pos, nodelist=towers, node_color='orange', node_size=100, label='Towers')

plt.legend()
plt.title('Customer-Tower Connection Network')
plt.axis('off')
plt.tight_layout()
plt.savefig('customer_tower_network.png')
plt.close()

# 6. Call Duration Distribution
plt.figure(figsize=(10, 6))
sns.histplot(df['Call_Duration_sec'], bins=20, kde=True)
plt.title('Distribution of Call Durations')
plt.xlabel('Call Duration (seconds)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('call_duration_distribution.png')
plt.close()

print("Visualization images have been saved.")

