import pandas as pd
import plotly.express as px
import os

# Read the data
file_path = 'telecom_customer_call_records_100.csv'
data = pd.read_csv(file_path)

# Create call duration categories for better visualization
def categorize_duration(seconds):
    if seconds < 300:
        return 'Very Short (<5 min)'
    elif seconds < 900:
        return 'Short (5-15 min)'
    elif seconds < 1800:
        return 'Medium (15-30 min)'
    elif seconds < 3600:
        return 'Long (30-60 min)'
    else:
        return 'Very Long (>60 min)'

data['Duration_Category'] = data['Call_Duration_sec'].apply(categorize_duration)

# Prepare data for sunburst chart
# We'll create a hierarchy: Place > Tower_ID > Duration_Category
data_for_sunburst = data.copy()

# Create the sunburst chart
fig = px.sunburst(
    data_for_sunburst,
    path=['Place', 'Tower_ID', 'Duration_Category'],
    values='Call_Duration_sec',
    color='Call_Duration_sec',
    color_continuous_scale='RdYlGn',
    title='Call Duration by Location, Tower, and Duration Category'
)

fig.update_layout(
    width=900,
    height=800,
)

# Save the figure
fig.write_image('sunburst_visualization.png')
fig.write_html('sunburst_visualization.html')

print(f"Sunburst visualization saved as 'sunburst_visualization.png' and 'sunburst_visualization.html'")

