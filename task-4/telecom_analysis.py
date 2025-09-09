import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from plotly.offline import plot

# Read the dataset
data = pd.read_csv('telecom_customer_call_records_100.csv')

# Add duration in minutes
data['Call_Duration_min'] = data['Call_Duration_sec'] / 60

# 1. SCATTERPLOT MATRIX
print("Creating Scatterplot Matrix...")
scatter_matrix = sns.pairplot(
    data, 
    vars=['Call_Duration_sec'], 
    hue='Place',
    height=3
)
scatter_matrix.fig.suptitle('Scatterplot Matrix - Call Data')
plt.savefig('scatterplot_matrix.png')

# 2. PARALLEL COORDINATES
print("Creating Parallel Coordinates Plot...")
# Create numerical encoding for categorical data
data['Place_code'] = pd.factorize(data['Place'])[0]

# Create parallel coordinates plot
fig_parallel = px.parallel_coordinates(
    data,
    color='Call_Duration_sec',
    dimensions=['Call_Duration_sec', 'Place_code'],
    labels={'Call_Duration_sec': 'Call Duration (sec)', 'Place_code': 'Location'}
)
plot(fig_parallel, filename='parallel_coordinates.html', auto_open=False)

# 3. LINE GRAPH
print("Creating Line Graph...")
avg_by_place = data.groupby('Place')['Call_Duration_sec'].mean().sort_values(ascending=False).reset_index()

plt.figure(figsize=(10, 5))
plt.plot(avg_by_place['Place'], avg_by_place['Call_Duration_sec'], marker='o')
plt.title('Average Call Duration by Location')
plt.xlabel('Location')
plt.ylabel('Call Duration (seconds)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('line_graph.png')

# 4. STACKED BAR CHART
print("Creating Stacked Bar Chart...")
# Categorize durations
duration_bins = [0, 500, 1500, 2500, 4000]
duration_labels = ['Short', 'Medium', 'Long', 'Very Long']
data['Duration_Category'] = pd.cut(data['Call_Duration_sec'], bins=duration_bins, labels=duration_labels)

# Create stacked bar chart
call_by_place = pd.crosstab(data['Place'], data['Duration_Category'])
call_by_place.plot(kind='bar', stacked=True, figsize=(10, 6))
plt.title('Call Duration Categories by Location')
plt.xlabel('Location')
plt.ylabel('Number of Calls')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('stacked_bar_chart.png')

print("All visualizations have been saved.")


