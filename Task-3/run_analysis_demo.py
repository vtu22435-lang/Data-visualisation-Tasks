#!/usr/bin/env python3
"""
Bivariate Analysis Demo - Simplified Results
===========================================

This script demonstrates the key results from both analysis scripts
without complex plotting to avoid display issues.
"""

import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

def analyze_data():
    """Analyze customer summary report data"""
    
    print("="*60)
    print("BIVARIATE ANALYSIS DEMONSTRATION")
    print("Using customer_summary_report.csv")
    print("="*60)
    
    # Load data
    df = pd.read_csv('customer_summary_report.csv')
    
    # Prepare data
    df['Call Start Time'] = pd.to_datetime(df['Call Start Time'])
    df['Call Start Hour'] = df['Call Start Time'].dt.hour
    df['Duration_Minutes'] = df['Duration (seconds)'] / 60
    df['Tower_Number'] = df['Tower ID'].str.extract(r'(\d+)').astype(int)
    
    print(f"Dataset loaded: {df.shape[0]} records, {df.shape[1]} columns")
    
    # 1. CONTINUOUS vs CONTINUOUS ANALYSIS
    print("\n" + "="*50)
    print("1. CONTINUOUS vs CONTINUOUS ANALYSIS")
    print("="*50)
    
    continuous_vars = ['Duration (seconds)', 'Call Start Hour', 'Duration_Minutes', 'Tower_Number']
    
    print("Available continuous variables:")
    for var in continuous_vars:
        print(f"  - {var}: Mean = {df[var].mean():.2f}, Std = {df[var].std():.2f}")
    
    # Key correlations
    print("\nKey Correlations:")
    corr_pairs = [
        ('Duration (seconds)', 'Call Start Hour'),
        ('Duration (seconds)', 'Tower_Number'),
        ('Call Start Hour', 'Tower_Number'),
        ('Duration (seconds)', 'Duration_Minutes')
    ]
    
    for var1, var2 in corr_pairs:
        if var1 in df.columns and var2 in df.columns:
            corr = df[var1].corr(df[var2])
            pearson_corr, p_val = stats.pearsonr(df[var1], df[var2])
            print(f"  {var1} ↔ {var2}: r = {corr:.3f} (p = {p_val:.4f})")
    
    print("\n📊 SCATTERPLOT WITH FIT LINES:")
    print("✓ Creates 6 scatterplots with linear and polynomial fit lines")
    print("✓ Shows correlation coefficients and statistical significance")
    print("✓ Includes regression analysis with R-squared values")
    
    # 2. CATEGORICAL vs CONTINUOUS ANALYSIS
    print("\n" + "="*50)
    print("2. CATEGORICAL vs CONTINUOUS ANALYSIS")
    print("="*50)
    
    categorical_vars = ['Call Type', 'Call Status', 'Tower ID']
    continuous_target = 'Duration (seconds)'
    
    print("Available categorical variables:")
    for var in categorical_vars:
        print(f"  - {var}: {df[var].unique()}")
    
    # Analysis by category
    print(f"\nAnalysis of {continuous_target} by categories:")
    
    # Call Type vs Duration
    print("\nCALL TYPE vs DURATION:")
    call_type_stats = df.groupby('Call Type')[continuous_target].agg(['count', 'mean', 'std'])
    print(call_type_stats.round(2))
    
    # Statistical test
    groups = [df[df['Call Type'] == ct][continuous_target] for ct in df['Call Type'].unique()]
    if len(groups) == 2:
        t_stat, p_val = stats.ttest_ind(groups[0], groups[1])
        print(f"T-test: t = {t_stat:.3f}, p = {p_val:.4f}")
    
    # Call Status vs Duration
    print("\nCALL STATUS vs DURATION:")
    status_stats = df.groupby('Call Status')[continuous_target].agg(['count', 'mean', 'std'])
    print(status_stats.round(2))
    
    # ANOVA test
    status_groups = [df[df['Call Status'] == cs][continuous_target] for cs in df['Call Status'].unique()]
    status_groups = [g for g in status_groups if len(g) > 0]  # Remove empty groups
    if len(status_groups) > 1:
        f_stat, p_val = stats.f_oneway(*status_groups)
        print(f"ANOVA: F = {f_stat:.3f}, p = {p_val:.4f}")
    
    # Tower ID vs Duration
    print("\nTOWER ID vs DURATION:")
    tower_stats = df.groupby('Tower ID')[continuous_target].agg(['count', 'mean', 'std'])
    print(tower_stats.round(2))
    
    print("\n📊 CATEGORICAL vs CONTINUOUS VISUALIZATIONS:")
    print("✓ Bar Charts - Summary statistics (mean, median, std)")
    print("✓ Box Plots - Distribution quartiles and outliers")
    print("✓ Violin Plots - Distribution shapes and density")
    print("✓ Grouped Kernel Density Plots - Overlapping distributions")
    print("✓ Ridgeline Plots - Stacked density curves")
    print("✓ Beeswarm Plots - Individual data points with jitter")
    
    # Summary insights
    print("\n" + "="*50)
    print("KEY INSIGHTS")
    print("="*50)
    
    # Call duration insights
    voice_duration = df[df['Call Type'] == 'Voice']['Duration (seconds)'].mean()
    sms_duration = df[df['Call Type'] == 'SMS']['Duration (seconds)'].mean()
    
    print(f"📞 Voice calls average {voice_duration:.1f} seconds")
    print(f"📱 SMS messages average {sms_duration:.1f} seconds")
    
    # Status insights
    connected_rate = (df['Call Status'] == 'Connected').mean() * 100
    failed_rate = (df['Call Status'] == 'Failed').mean() * 100
    
    print(f"✅ {connected_rate:.1f}% of calls successfully connected")
    print(f"❌ {failed_rate:.1f}% of calls failed")
    
    # Tower insights
    busiest_tower = df['Tower ID'].value_counts().index[0]
    busiest_count = df['Tower ID'].value_counts().iloc[0]
    
    print(f"📡 Busiest tower: {busiest_tower} with {busiest_count} calls")
    
    # Time insights
    peak_hour = df['Call Start Hour'].mode()[0]
    peak_count = (df['Call Start Hour'] == peak_hour).sum()
    
    print(f"⏰ Peak calling hour: {peak_hour}:00 with {peak_count} calls")
    
    print("\n" + "="*60)
    print("ANALYSIS SCRIPTS READY!")
    print("="*60)
    print("Run these scripts to generate visualizations:")
    print("1. python 1_continuous_vs_continuous_scatterplots.py")
    print("2. python 2_categorical_vs_continuous_plots.py")
    print("\nGenerated files will include:")
    print("- continuous_vs_continuous_scatterplots.png")
    print("- regression_analysis.png")
    print("- bar_charts_summary_statistics.png")
    print("- box_and_violin_plots.png")
    print("- density_and_ridgeline_plots.png")
    print("- beeswarm_plots.png")
    print("="*60)

if __name__ == "__main__":
    try:
        analyze_data()
    except FileNotFoundError:
        print("Error: customer_summary_report.csv not found!")
    except Exception as e:
        print(f"Error: {str(e)}")