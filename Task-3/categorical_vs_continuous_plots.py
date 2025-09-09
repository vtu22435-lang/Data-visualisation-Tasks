import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
import matplotlib.patches as mpatches
from matplotlib import colors
import joypy  # For ridgeline plots
import os

# Set the style for all plots
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context("notebook", font_scale=1.2)

# Read the data
df = pd.read_csv('customer_summary_report.csv')

# Convert time columns to datetime and calculate actual duration
df['Call Start Time'] = pd.to_datetime(df['Call Start Time'])
df['Call End Time'] = pd.to_datetime(df['Call End Time'])

# Color palette
palette = sns.color_palette("viridis", 3)

# Create a figure for all plots except ridgeline (which needs special handling)
fig = plt.figure(figsize=(20, 24))
gs = GridSpec(3, 2, figure=fig)

# 1. Bar Chart (Summary Statistics)
ax1 = fig.add_subplot(gs[0, 0])
summary_stats = df.groupby('Call Type')['Duration (seconds)'].agg(['mean', 'median', 'std']).reset_index()
summary_stats = summary_stats.melt(id_vars=['Call Type'], value_vars=['mean', 'median', 'std'],
                                   var_name='Statistic', value_name='Value')
sns.barplot(x='Call Type', y='Value', hue='Statistic', data=summary_stats, palette=palette, ax=ax1)
ax1.set_title('Call Duration Statistics by Call Type')
ax1.set_ylabel('Duration (seconds)')
ax1.tick_params(axis='x', rotation=0)
ax1.legend(title='Statistic')

# 2. Grouped Kernel Density Plot
ax2 = fig.add_subplot(gs[0, 1])
for call_type in df['Call Type'].unique():
    subset = df[df['Call Type'] == call_type]
    sns.kdeplot(subset['Duration (seconds)'], label=call_type, fill=True, alpha=0.3, ax=ax2)
ax2.set_title('Kernel Density Plot of Call Duration by Call Type')
ax2.set_xlabel('Duration (seconds)')
ax2.set_ylabel('Density')
ax2.legend(title='Call Type')

# 3. Box Plot
ax3 = fig.add_subplot(gs[1, 0])
sns.boxplot(x='Call Status', y='Duration (seconds)', data=df, palette=palette, ax=ax3)
ax3.set_title('Call Duration by Call Status')
ax3.tick_params(axis='x', rotation=0)
ax3.set_ylabel('Duration (seconds)')

# 4. Violin Plot
ax4 = fig.add_subplot(gs[1, 1])
sns.violinplot(x='Call Type', y='Duration (seconds)', hue='Call Status', data=df, 
               split=True, inner='quart', palette=palette, ax=ax4)
ax4.set_title('Violin Plot of Call Duration by Call Type and Status')
ax4.tick_params(axis='x', rotation=0)
ax4.set_ylabel('Duration (seconds)')
ax4.legend(title='Call Status')

# 5. Ridgeline Plot (using joypy)
# Filter out zero durations for better visualization
df_nonzero = df[df['Duration (seconds)'] > 0]

# Create a separate figure for the ridgeline plot
ridge_fig, axes = joypy.joyplot(df_nonzero, by='Tower ID', column='Duration (seconds)', 
                         figsize=(10, 6), alpha=0.6, overlap=0.7,
                         grid=True, colormap=colors.ListedColormap(palette))
plt.title('Ridgeline Plot of Call Duration by Tower ID', fontsize=14, y=0.9)
plt.tight_layout()
plt.savefig('ridgeline_plot.png', dpi=300, bbox_inches='tight')
plt.close()

# Add the ridgeline plot as an image
ax5 = fig.add_subplot(gs[2, 0])
if os.path.exists('ridgeline_plot.png'):
    img = plt.imread('ridgeline_plot.png')
    ax5.imshow(img)
    ax5.axis('off')
    ax5.set_title('Ridgeline Plot of Call Duration by Tower ID')
else:
    ax5.text(0.5, 0.5, "Ridgeline plot image not found", 
             horizontalalignment='center', verticalalignment='center')
    ax5.axis('off')

# 6. Beeswarm Plot (using stripplot)
ax6 = fig.add_subplot(gs[2, 1])
sns.stripplot(x='Call Type', y='Duration (seconds)', hue='Call Status', data=df, 
             dodge=True, jitter=True, alpha=0.7, palette=palette, ax=ax6)
ax6.set_title('Beeswarm Plot of Call Duration by Call Type and Status')
ax6.tick_params(axis='x', rotation=0)
ax6.set_ylabel('Duration (seconds)')
ax6.legend(title='Call Status')

plt.tight_layout(pad=3.0)
plt.savefig('categorical_vs_continuous_plots.png', dpi=300, bbox_inches='tight')
plt.close()

print("Categorical vs. Continuous plots have been generated and saved as 'categorical_vs_continuous_plots.png'")