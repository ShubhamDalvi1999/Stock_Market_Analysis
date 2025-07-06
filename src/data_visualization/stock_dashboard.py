import os
import logging
from pathlib import Path
import pandas as pd
from dash import Dash
from layouts import create_main_layout
from callbacks import register_callbacks

# Configure logging
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent
logs_dir = project_root / 'logs'

if not logs_dir.exists():
    logs_dir.mkdir(parents=True, exist_ok=True)
    
logging.basicConfig(
    filename=logs_dir / 'data_visualization.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_data():
    """Load data for the dashboard."""
    try:
        # Use the project root directory defined at module level
        data_dir = project_root / 'data' / 'visualization'
        
        # Check if data directory exists
        if not data_dir.exists():
            logging.error(f"Data directory not found: {data_dir}")
            return pd.DataFrame(), {}
        
        # Get the latest analysis file
        analysis_files = list(data_dir.glob('Processed_*.csv'))
        if not analysis_files:
            logging.error(f"No analysis files found in {data_dir}")
            return pd.DataFrame(), {}
            
        latest_file = max(analysis_files, key=lambda x: x.stat().st_mtime)
        logging.info(f"Loading analysis data from {latest_file}")
        analysis_df = pd.read_csv(latest_file)
        
        # Get the latest summary file
        summary_files = list(data_dir.glob('Summary_*.csv'))
        if not summary_files:
            logging.error(f"No summary files found in {data_dir}")
            return analysis_df, {}
            
        latest_summary = max(summary_files, key=lambda x: x.stat().st_mtime)
        logging.info(f"Loading summary data from {latest_summary}")
        summary_df = pd.read_csv(latest_summary)
        
        # Convert summary to dictionary
        data_overview = dict(zip(summary_df['Metric'], summary_df['Value']))
        logging.info(f"Successfully loaded {len(analysis_df)} records with columns: {analysis_df.columns.tolist()}")
        
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