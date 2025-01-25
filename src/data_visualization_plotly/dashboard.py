import os
import logging
import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Set up logging
if not os.path.exists('logs'):
    os.makedirs('logs')
logging.basicConfig(
    filename='logs/data_visualization_plotly.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('data_visualization_plotly')

def load_data():
    """Load and prepare data for visualization."""
    try:
        # Get the latest processed analysis file
        directory_path = "data/visualization"
        analysis_files = [f for f in os.listdir(directory_path) if f.startswith('Processed_')]
        summary_files = [f for f in os.listdir(directory_path) if f.startswith('Summary_')]
        
        if not analysis_files or not summary_files:
            logger.error("No processed analysis or summary files found")
            return pd.DataFrame(), {}
            
        latest_analysis_file = sorted(analysis_files)[-1]
        latest_summary_file = sorted(summary_files)[-1]
        
        logger.info(f"Loading analysis data from {latest_analysis_file}")
        logger.info(f"Loading summary data from {latest_summary_file}")
        
        analysis_df = pd.read_csv(os.path.join(directory_path, latest_analysis_file))
        summary_df = pd.read_csv(os.path.join(directory_path, latest_summary_file))
        
        # Convert summary DataFrame to dictionary
        data_overview = dict(zip(summary_df['Metric'], summary_df['Value']))
        
        logger.info(f"Successfully loaded {len(analysis_df)} records")
        return analysis_df, data_overview
        
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        return pd.DataFrame(), {}

def create_price_chart(df):
    """Create price analysis chart."""
    fig = go.Figure()
    
    # Add current close price
    fig.add_trace(go.Scatter(
        x=df['SYMBOL'],
        y=df['CLOSE'],
        name='Current Close',
        mode='lines+markers',
        line=dict(color='#2ecc71', width=2),
        marker=dict(size=8)
    ))
    
    # Add previous close price
    fig.add_trace(go.Scatter(
        x=df['SYMBOL'],
        y=df['CLOSE_prev'],
        name='Previous Close',
        mode='lines+markers',
        line=dict(color='#3498db', width=2, dash='dash'),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title='Price Analysis',
        xaxis_title='Symbol',
        yaxis_title='Price',
        template='plotly_white',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_oi_chart(df):
    """Create open interest analysis chart."""
    fig = go.Figure()
    
    colors = ['#2ecc71' if x > 0 else '#e74c3c' for x in df['CHG_IN_OI']]
    
    fig.add_trace(go.Bar(
        x=df['SYMBOL'],
        y=df['CHG_IN_OI'],
        name='Change in OI',
        marker_color=colors,
        opacity=0.7
    ))
    
    fig.update_layout(
        title='Open Interest Analysis',
        xaxis_title='Symbol',
        yaxis_title='Change in Open Interest',
        template='plotly_white',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_buildup_chart(df):
    """Create build-up analysis chart."""
    fig = go.Figure()
    
    # Create scatter plot with quadrants
    fig.add_trace(go.Scatter(
        x=df['OI_CHANGE_PCT'],
        y=df['PRICE_CHANGE_PCT'],
        mode='markers+text',
        marker=dict(
            size=10,
            color=df['OI_PATTERN'].map({
                'Long Build-up': '#2ecc71',
                'Short Build-up': '#e74c3c',
                'Long Unwinding': '#f1c40f',
                'Short Covering': '#3498db'
            })
        ),
        text=df['SYMBOL'],
        textposition='top center',
        name='Stocks'
    ))
    
    # Add quadrant lines
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_vline(x=0, line_dash="dash", line_color="gray", opacity=0.5)
    
    # Add quadrant labels
    fig.add_annotation(x=50, y=50, text="Long Build-up", showarrow=False, font=dict(color="#2ecc71"))
    fig.add_annotation(x=50, y=-50, text="Short Build-up", showarrow=False, font=dict(color="#e74c3c"))
    fig.add_annotation(x=-50, y=-50, text="Long Unwinding", showarrow=False, font=dict(color="#f1c40f"))
    fig.add_annotation(x=-50, y=50, text="Short Covering", showarrow=False, font=dict(color="#3498db"))
    
    fig.update_layout(
        title='Build-up Analysis',
        xaxis_title='OI Change %',
        yaxis_title='Price Change %',
        template='plotly_white',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_pattern_chart(df):
    """Create pattern distribution chart."""
    pattern_counts = df['OI_PATTERN'].value_counts()
    
    colors = {
        'Long Build-up': '#2ecc71',
        'Short Build-up': '#e74c3c',
        'Long Unwinding': '#f1c40f',
        'Short Covering': '#3498db'
    }
    
    fig = go.Figure(data=[
        go.Bar(
            x=pattern_counts.index,
            y=pattern_counts.values,
            marker_color=[colors.get(x, '#95a5a6') for x in pattern_counts.index]
        )
    ])
    
    fig.update_layout(
        title='Pattern Distribution',
        xaxis_title='Pattern',
        yaxis_title='Count',
        template='plotly_white',
        showlegend=False
    )
    
    return fig

def main():
    """Initialize and run the Dash application."""
    logger.info("Initializing Dash application...")
    
    try:
        # Load data
        analysis_df, data_overview = load_data()
        
        if analysis_df.empty:
            raise ValueError("No data available for visualization")
        
        # Initialize Dash app
        app = Dash(__name__)
        
        # Create layout
        app.layout = html.Div([
            # Header
            html.Div([
                html.H1('Stock Market Analysis Dashboard',
                    style={
                        'textAlign': 'center',
                        'color': 'white',
                        'padding': '20px',
                        'marginBottom': '20px'
                    }
                )
            ], style={
                'backgroundColor': '#2c3e50',
                'marginBottom': '20px'
            }),
            
            # Filters
            html.Div([
                html.Div([
                    html.Label('Instrument Type'),
                    dcc.Dropdown(
                        id='instrument-filter',
                        options=[{'label': i, 'value': i} for i in sorted(analysis_df['INSTRUMENT'].unique())],
                        value='FUTIDX'
                    )
                ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '20px'}),
                
                html.Div([
                    html.Label('Symbol'),
                    dcc.Dropdown(id='symbol-filter')
                ], style={'width': '30%', 'display': 'inline-block'})
            ], style={'marginBottom': '20px', 'padding': '20px', 'backgroundColor': 'white'}),
            
            # Charts
            html.Div([
                html.Div([
                    dcc.Graph(id='price-chart')
                ], style={'width': '50%', 'display': 'inline-block'}),
                
                html.Div([
                    dcc.Graph(id='oi-chart')
                ], style={'width': '50%', 'display': 'inline-block'}),
                
                html.Div([
                    dcc.Graph(id='buildup-chart')
                ], style={'width': '50%', 'display': 'inline-block'}),
                
                html.Div([
                    dcc.Graph(id='pattern-chart')
                ], style={'width': '50%', 'display': 'inline-block'})
            ])
        ])
        
        # Callbacks
        @app.callback(
            Output('symbol-filter', 'options'),
            [Input('instrument-filter', 'value')]
        )
        def update_symbol_options(selected_instrument):
            filtered_df = analysis_df[analysis_df['INSTRUMENT'] == selected_instrument]
            return [{'label': i, 'value': i} for i in sorted(filtered_df['SYMBOL'].unique())]
        
        @app.callback(
            [Output('price-chart', 'figure'),
             Output('oi-chart', 'figure'),
             Output('buildup-chart', 'figure'),
             Output('pattern-chart', 'figure')],
            [Input('instrument-filter', 'value'),
             Input('symbol-filter', 'value')]
        )
        def update_charts(selected_instrument, selected_symbol):
            filtered_df = analysis_df[analysis_df['INSTRUMENT'] == selected_instrument]
            
            if selected_symbol:
                filtered_df = filtered_df[filtered_df['SYMBOL'] == selected_symbol]
            
            return (
                create_price_chart(filtered_df),
                create_oi_chart(filtered_df),
                create_buildup_chart(filtered_df),
                create_pattern_chart(filtered_df)
            )
        
        # Start the server
        logger.info("Starting dashboard server...")
        app.run_server(debug=True)
        
    except Exception as e:
        logger.error(f"Error starting dashboard: {str(e)}")
        raise e

if __name__ == '__main__':
    main() 