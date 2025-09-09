import pandas as pd
import matplotlib.pyplot as plt
import squarify
import os

# Read the data
file_path = 'telecom_customer_call_records_100.csv'
data = pd.read_csv(file_path)

# Group data by Place and calculate total call duration
place_call_duration = data.groupby('Place')['Call_Duration_sec'].sum().reset_index()
place_call_duration = place_call_duration.sort_values('Call_Duration_sec', ascending=False)

# Create TreeMap
plt.figure(figsize=(12, 8))
squarify.plot(sizes=place_call_duration['Call_Duration_sec'], 
              label=[f"{place}\n{duration:,} sec" for place, duration in zip(place_call_duration['Place'], place_call_duration['Call_Duration_sec'])], 
              alpha=0.8,
              color=plt.cm.Spectral_r(range(len(place_call_duration))))

plt.axis('off')
plt.title('Call Duration by City (TreeMap)', fontsize=16)

# Save the figure
plt.tight_layout()
plt.savefig('treemap_visualization.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"TreeMap visualization saved as 'treemap_visualization.png'")

