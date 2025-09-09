import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import gaussian_kde
import warnings
warnings.filterwarnings('ignore')

def main():
    # Load and prepare data
    df = pd.read_csv('customer_summary_report.csv')
    df['Call Start Time'] = pd.to_datetime(df['Call Start Time'])
    df['Call Start Hour'] = df['Call Start Time'].dt.hour
    df['Duration_Minutes'] = df['Duration (seconds)'] / 60
    df['Tower_Number'] = df['Tower ID'].str.extract(r'(\d+)').astype(int)
    df['Time_Period'] = pd.cut(df['Call Start Hour'], bins=[0, 6, 12, 18, 24], 
                              labels=['Night', 'Morning', 'Afternoon', 'Evening'], include_lowest=True)
    df['Duration_Category'] = pd.cut(df['Duration (seconds)'], bins=[0, 30, 300, 600, float('inf')], 
                                   labels=['Very Short', 'Short', 'Medium', 'Long'])
    
    print("="*60)
    print("CATEGORICAL vs CONTINUOUS BIVARIATE ANALYSIS")
    print(f"Dataset: {df.shape[0]} records")
    
    # 1. Bar Charts
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Bar Charts - Summary Statistics', fontsize=16, fontweight='bold')
    
    chart_data = [
        ('Call Type', 'Duration (seconds)', axes[0,0]),
        ('Call Status', 'Duration (seconds)', axes[0,1]),
        ('Time_Period', 'Call Start Hour', axes[1,0]),
        ('Tower ID', 'Duration (seconds)', axes[1,1])
    ]
    
    for cat_var, cont_var, ax in chart_data:
        summary = df.groupby(cat_var)[cont_var].agg(['mean', 'median', 'std']).reset_index()
        x_pos = np.arange(len(summary))
        width = 0.25
        
        ax.bar(x_pos - width, summary['mean'], width, label='Mean', alpha=0.8, color='skyblue')
        ax.bar(x_pos, summary['median'], width, label='Median', alpha=0.8, color='lightgreen')
        ax.bar(x_pos + width, summary['std'], width, label='Std', alpha=0.8, color='salmon')
        
        ax.set_xlabel(cat_var)
        ax.set_ylabel(cont_var)
        ax.set_title(f'{cat_var} vs {cont_var}')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(summary[cat_var], rotation=45 if len(summary) > 3 else 0)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('bar_charts_summary_statistics.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 2. Box and Violin Plots
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    fig.suptitle('Box Plots and Violin Plots', fontsize=16, fontweight='bold')
    
    plot_data = [
        ('Call Type', 'Duration (seconds)'),
        ('Call Status', 'Duration (seconds)'),
        ('Time_Period', 'Call Start Hour'),
        ('Duration_Category', 'Tower_Number')
    ]
    
    for i, (cat_var, cont_var) in enumerate(plot_data):
        # Box plots (top row)
        categories = df[cat_var].dropna().unique()
        data_by_cat = [df[df[cat_var] == cat][cont_var].dropna() for cat in categories]
        axes[0,i].boxplot(data_by_cat, labels=categories)
        axes[0,i].set_title(f'Box: {cat_var} vs {cont_var}')
        axes[0,i].set_xlabel(cat_var)
        axes[0,i].set_ylabel(cont_var)
        if i > 1: axes[0,i].tick_params(axis='x', rotation=45)
        axes[0,i].grid(True, alpha=0.3)
        
        # Violin plots (bottom row)
        colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow']
        for j, cat in enumerate(categories):
            data = df[df[cat_var] == cat][cont_var].dropna()
            if len(data) > 1:
                parts = axes[1,i].violinplot([data], positions=[j+1], widths=0.6)
                for pc in parts['bodies']:
                    pc.set_facecolor(colors[j % len(colors)])
                    pc.set_alpha(0.7)
        
        axes[1,i].set_title(f'Violin: {cat_var} vs {cont_var}')
        axes[1,i].set_xlabel(cat_var)
        axes[1,i].set_ylabel(cont_var)
        axes[1,i].set_xticks(range(1, len(categories)+1))
        axes[1,i].set_xticklabels(categories, rotation=45 if i > 1 else 0)
        axes[1,i].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('box_and_violin_plots.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 3. Density and Ridgeline Plots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Grouped Kernel Density and Ridgeline Plots', fontsize=16, fontweight='bold')
    
    density_data = [
        ('Call Type', 'Duration (seconds)', axes[0,0]),
        ('Call Status', 'Duration (seconds)', axes[0,1])
    ]
    
    ridgeline_data = [
        ('Call Type', 'Duration (seconds)', axes[1,0]),
        ('Call Status', 'Duration (seconds)', axes[1,1])
    ]
    
    # Grouped Density Plots
    for cat_var, cont_var, ax in density_data:
        categories = df[cat_var].unique()
        colors = ['blue', 'green', 'red', 'orange']
        for i, cat in enumerate(categories):
            data = df[df[cat_var] == cat][cont_var].dropna()
            if len(data) > 1:
                ax.hist(data, alpha=0.6, label=cat, density=True, bins=15, color=colors[i % len(colors)])
        ax.set_xlabel(cont_var)
        ax.set_ylabel('Density')
        ax.set_title(f'Density: {cat_var} vs {cont_var}')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    # Ridgeline Plots
    for cat_var, cont_var, ax in ridgeline_data:
        categories = df[cat_var].unique()
        colors = ['blue', 'green', 'red', 'orange']
        y_offset = 0
        
        for i, cat in enumerate(categories):
            data = df[df[cat_var] == cat][cont_var].dropna()
            if len(data) > 5:
                density = gaussian_kde(data)
                x_range = np.linspace(data.min(), data.max(), 100)
                y_density = density(x_range) / density(x_range).max() * 0.8
                y_pos = y_offset + y_density
                
                ax.fill_between(x_range, y_offset, y_pos, alpha=0.7, color=colors[i % len(colors)], label=cat)
                ax.plot(x_range, y_pos, color='black', linewidth=1)
            y_offset += 1
        
        ax.set_xlabel(cont_var)
        ax.set_ylabel(cat_var)
        ax.set_title(f'Ridgeline: {cat_var} vs {cont_var}')
        ax.set_yticks(range(len(categories)))
        ax.set_yticklabels(categories)
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('density_and_ridgeline_plots.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 4. Beeswarm Plots
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('Beeswarm Plots (Strip Plots with Jitter)', fontsize=16, fontweight='bold')
    
    beeswarm_data = [
        ('Call Type', 'Duration (seconds)', axes[0]),
        ('Call Status', 'Duration (seconds)', axes[1]),
        ('Tower ID', 'Duration (seconds)', axes[2])
    ]
    
    for cat_var, cont_var, ax in beeswarm_data:
        categories = df[cat_var].unique()
        colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
        
        for i, cat in enumerate(categories):
            data = df[df[cat_var] == cat][cont_var].dropna()
            if len(data) > 0:
                x_jitter = np.random.normal(i, 0.1, size=len(data))
                ax.scatter(x_jitter, data, alpha=0.6, s=30, color=colors[i], label=cat)
        
        ax.set_xlabel(cat_var)
        ax.set_ylabel(cont_var)
        ax.set_title(f'Beeswarm: {cat_var} vs {cont_var}')
        ax.set_xticks(range(len(categories)))
        ax.set_xticklabels(categories, rotation=45 if len(categories) > 3 else 0)
        if len(categories) <= 6: ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('beeswarm_plots.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Statistical Tests
    print("\n" + "="*60)
    print("STATISTICAL TESTS")
    print("="*60)
    
    # Call Type vs Duration
    call_types = df['Call Type'].unique()
    groups = [df[df['Call Type'] == ct]['Duration (seconds)'].dropna() for ct in call_types]
    if len(groups) == 2 and all(len(g) > 0 for g in groups):
        t_stat, p_val = stats.ttest_ind(groups[0], groups[1])
        print(f"\nCall Type vs Duration - t-test: t={t_stat:.4f}, p={p_val:.4f}")
        for i, ct in enumerate(call_types):
            print(f"  {ct}: Mean={groups[i].mean():.2f}, N={len(groups[i])}")
        print(f"  → {'Significant' if p_val < 0.05 else 'Not significant'}")
    
    # Call Status vs Duration
    call_statuses = df['Call Status'].unique()
    groups = [df[df['Call Status'] == cs]['Duration (seconds)'].dropna() for cs in call_statuses]
    if len(groups) > 2 and all(len(g) > 0 for g in groups):
        f_stat, p_val = stats.f_oneway(*groups)
        print(f"\nCall Status vs Duration - ANOVA: F={f_stat:.4f}, p={p_val:.4f}")
        for i, cs in enumerate(call_statuses):
            print(f"  {cs}: Mean={groups[i].mean():.2f}, N={len(groups[i])}")
        print(f"  → {'Significant' if p_val < 0.05 else 'Not significant'}")
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE!")
    print("Generated: bar_charts_summary_statistics.png, box_and_violin_plots.png,")
    print("          density_and_ridgeline_plots.png, beeswarm_plots.png")
    print("="*60)

if __name__ == "__main__":
    main()