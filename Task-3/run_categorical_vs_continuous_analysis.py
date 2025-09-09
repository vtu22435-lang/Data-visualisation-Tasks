import os
import subprocess
import sys

def main():
    """
    Run the categorical vs. continuous analysis script and display the results.
    """
    print("Running Categorical vs. Continuous Analysis...")
    
    # Check if required packages are installed
    try:
        import pandas
        import numpy
        import matplotlib
        import seaborn
        import joypy
    except ImportError as e:
        print(f"Missing required package: {e}")
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Run the analysis script
    print("Generating plots...")
    subprocess.check_call([sys.executable, "categorical_vs_continuous_plots.py"])
    
    # Check if the plots were generated
    if os.path.exists("categorical_vs_continuous_plots.png") and os.path.exists("ridgeline_plot.png"):
        print("\nAnalysis completed successfully!")
        print("Generated plots:")
        print("1. categorical_vs_continuous_plots.png - Contains bar charts, kernel density plots, box plots, violin plots, and beeswarm plots")
        print("2. ridgeline_plot.png - Contains the ridgeline plot")
        
        # Try to display the images if running in an environment that supports it
        try:
            from IPython.display import Image, display
            print("\nDisplaying plots...")
            display(Image("categorical_vs_continuous_plots.png"))
            display(Image("ridgeline_plot.png"))
        except ImportError:
            print("\nTo view the plots, open the PNG files in an image viewer.")
    else:
        print("Error: Plot files were not generated.")

if __name__ == "__main__":
    main()

