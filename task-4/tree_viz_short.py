import pandas as pd
import plotly.express as px
from plotly.offline import plot

# Read data and prepare
data = pd.read_csv('telecom_customer_call_records_100.csv')
data['Duration_Category'] = pd.cut(
    data['Call_Duration_sec'],
    bins=[0, 500, 1500, 2500, 4000],
    labels=['Short', 'Medium', 'Long', 'Very Long']
).astype(str)

# Aggregate data
tree_data = data.groupby(['Place', 'Duration_Category']).size().reset_index(name='count')
tree_data['Root'] = 'All Calls'

# 5a) TreeMap
fig_tree = px.treemap(
    tree_data,
    path=['Root', 'Place', 'Duration_Category'],
    values='count',
    color='Duration_Category',
    title='Telecom Call Distribution - TreeMap'
)
fig_tree.write_html('telecom_treemap.html')
fig_tree.write_image('telecom_treemap.png', width=900, height=700)

# 5b) Sunburst
fig_sun = px.sunburst(
    tree_data,
    path=['Root', 'Place', 'Duration_Category'],
    values='count',
    color='Duration_Category',
    title='Telecom Call Distribution - Sunburst'
)
fig_sun.write_html('telecom_sunburst.html')
fig_sun.write_image('telecom_sunburst.png', width=900, height=700)


