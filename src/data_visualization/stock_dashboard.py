import os
import logging
from pathlib import Path
import pandas as pd
from dash import Dash
from layouts import create_main_layout
from callbacks import register_callbacks

# Configure logging
if not os.path.exists('logs'):
    os.makedirs('logs')
logging.basicConfig(
    filename='logs/data_visualization.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_data():
    """Load data for the dashboard."""
    try:
        # Get the latest analysis file
        data_dir = Path('data/visualization')
        analysis_files = list(data_dir.glob('Processed_*.csv'))
        if not analysis_files:
            logging.error("No analysis files found")
            return pd.DataFrame(), {}
            
        latest_file = max(analysis_files, key=lambda x: x.stat().st_mtime)
        logging.info(f"Loading analysis data from {latest_file}")
        analysis_df = pd.read_csv(latest_file)
        
        # Get the latest summary file
        summary_files = list(data_dir.glob('Summary_*.csv'))
        if not summary_files:
            logging.error("No summary files found")
            return analysis_df, {}
            
        latest_summary = max(summary_files, key=lambda x: x.stat().st_mtime)
        logging.info(f"Loading summary data from {latest_summary}")
        summary_df = pd.read_csv(latest_summary)
        
        # Convert summary to dictionary
        data_overview = dict(zip(summary_df['Metric'], summary_df['Value']))
        logging.info(f"Successfully loaded {len(analysis_df)} records")
        
        return analysis_df, data_overview
        
    except Exception as e:
        logging.error(f"Error loading data: {str(e)}")
        return pd.DataFrame(), {}

# Initialize the Dash app
app = Dash(__name__, suppress_callback_exceptions=True)

# Load data
analysis_df, data_overview = load_data()

# Set the layout
app.layout = create_main_layout(analysis_df, data_overview)

# Register callbacks
register_callbacks(app)

if __name__ == '__main__':

    #  app.run_server(debug=True) # without docker
    
    # Run server with host='0.0.0.0' to make it accessible outside container
    app.run_server(debug=True, host='0.0.0.0')