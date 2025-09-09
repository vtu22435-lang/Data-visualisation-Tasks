import pandas as pd
import plotly.express as px
from plotly.offline import plot

# Read the dataset
file_path = 'telecom_customer_call_records_100.csv'
data = pd.read_csv(file_path)

# Create duration categories for better visualization
data['Call_Duration_sec'] = data['Call_Duration_sec'].astype(int)
bins = [0, 500, 1500, 2500, 4000]
labels = ['Short', 'Medium', 'Long', 'Very Long']
data['Duration_Category'] = pd.cut(data['Call_Duration_sec'], bins=bins, labels=labels)

# Convert categorical to string to avoid issues
data['Duration_Category'] = data['Duration_Category'].astype(str)

# Create aggregated data for tree visualizations
tree_data = data.groupby(['Place', 'Duration_Category']).agg(
    call_count=('Customer_ID', 'count'),
    avg_duration=('Call_Duration_sec', 'mean')
).reset_index()

# Add a level for better visualization hierarchy
tree_data['All_Calls'] = 'Telecom_Data'

# Sort by call volume
tree_data = tree_data.sort_values('call_count', ascending=False)

# 5a) TreeMap Visualization
print("Creating TreeMap visualization...")
fig_treemap = px.treemap(
    tree_data,
    path=['All_Calls', 'Place', 'Duration_Category'],  # Hierarchy levels
    values='call_count',                              # Size of blocks
    color='Duration_Category',                        # Color by category
    color_discrete_sequence=px.colors.qualitative.Set3,
    title='Telecom Call Distribution by Location and Duration - TreeMap',
    hover_data=['avg_duration'],
    custom_data=['call_count', 'avg_duration']
)

# Add custom hover template
fig_treemap.update_traces(
    hovertemplate='<b>%{label}</b><br>Calls: %{customdata[0]}<br>Avg Duration: %{customdata[1]:.1f} sec<extra></extra>'
)

# Update layout for better appearance
fig_treemap.update_layout(
    margin=dict(t=50, l=25, r=25, b=25),
    font=dict(size=14)
)

# Save TreeMap visualization
treemap_path = 'telecom_treemap.html'
plot(fig_treemap, filename=treemap_path, auto_open=False)

# Save a static image version
fig_treemap.write_image('telecom_treemap.png', width=1200, height=800)
print(f"TreeMap saved as {treemap_path} and telecom_treemap.png")

# 5b) Sunburst Visualization
print("Creating Sunburst visualization...")
fig_sunburst = px.sunburst(
    tree_data,
    path=['All_Calls', 'Place', 'Duration_Category'],  # Hierarchy levels
    values='call_count',                              # Size of segments
    color='Duration_Category',                        # Color by category
    color_discrete_sequence=px.colors.qualitative.Pastel1,
    title='Telecom Call Distribution by Location and Duration - Sunburst',
    hover_data=['avg_duration'],
    custom_data=['call_count', 'avg_duration']
)

# Add custom hover template
fig_sunburst.update_traces(
    hovertemplate='<b>%{label}</b><br>Calls: %{customdata[0]}<br>Avg Duration: %{customdata[1]:.1f} sec<extra></extra>'
)

# Update layout for better appearance
fig_sunburst.update_layout(
    margin=dict(t=50, l=25, r=25, b=25),
    font=dict(size=14)
)

# Save Sunburst visualization
sunburst_path = 'telecom_sunburst.html'
plot(fig_sunburst, filename=sunburst_path, auto_open=False)

# Save a static image version
fig_sunburst.write_image('telecom_sunburst.png', width=1200, height=800)
print(f"Sunburst chart saved as {sunburst_path} and telecom_sunburst.png")

print("Tree visualizations complete!")


