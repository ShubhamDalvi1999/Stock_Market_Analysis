import logging
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import pandas as pd
import os
from dash import html
from dash.exceptions import PreventUpdate
import numpy as np
from pathlib import Path

logger = logging.getLogger('data_visualization')

def load_latest_data():
    """Load the latest analysis data."""
    try:
        # Get the latest analysis file
        data_dir = Path('data/visualization')
        analysis_files = list(data_dir.glob('Processed_*.csv'))
        if not analysis_files:
            logging.error("No analysis files found")
            return pd.DataFrame()
            
        latest_file = max(analysis_files, key=lambda x: x.stat().st_mtime)
        logging.info(f"Loading data from {latest_file}")
        
        df = pd.read_csv(latest_file)
        
        required_columns = [
            'INSTRUMENT', 'SYMBOL', 'CLOSE', 'CLOSE_prev', 
            'OPEN_INT', 'OPEN_INT_prev', 'CHG_IN_OI', 'OI_PATTERN'
        ]
        
        if not all(col in df.columns for col in required_columns):
            logging.error(f"Missing required columns in {latest_file}")
            return pd.DataFrame()
        
        # Calculate percentage changes if not present
        if 'PRICE_CHANGE_PCT' not in df.columns:
            df['PRICE_CHANGE_PCT'] = ((df['CLOSE'] - df['CLOSE_prev']) / df['CLOSE_prev'] * 100)
            
        if 'OI_CHANGE_PCT' not in df.columns:
            df['OI_CHANGE_PCT'] = ((df['OPEN_INT'] - df['OPEN_INT_prev']) / df['OPEN_INT_prev'] * 100)
            
        logging.info(f"Successfully loaded {len(df)} records")
        return df
        
    except Exception as e:
        logging.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

def create_stock_card(symbol, instrument, price_change, oi_change):
    """Create a card displaying stock information."""
    return html.Div([
        html.Div([
            html.Strong(f"{symbol} ({instrument})", style={
                'fontSize': '16px',
                'color': '#2c3e50'
            }),
            html.Div([
                html.Span(f"Price: {price_change:+.2f}%", style={
                    'color': '#2ecc71' if price_change > 0 else '#e74c3c',
                    'marginRight': '15px',
                    'fontSize': '14px'
                }),
                html.Span(f"OI: {oi_change:+.2f}%", style={
                    'color': '#2ecc71' if oi_change > 0 else '#e74c3c',
                    'fontSize': '14px'
                })
            ])
        ])
    ], style={
        'padding': '10px',
        'borderBottom': '1px solid #eee',
        'transition': 'background-color 0.3s',
        'cursor': 'pointer',
        ':hover': {'backgroundColor': '#f8f9fa'}
    })

def register_callbacks(app):
    """Register all callbacks for the dashboard."""
    
    @app.callback(
        Output('symbol-filter', 'options'),
        Output('symbol-filter', 'value'),
        Input('instrument-filter', 'value')
    )
    def update_symbol_dropdown(selected_instrument):
        if not selected_instrument:
            return [], None
            
        df = load_latest_data()
        if df.empty:
            return [], None
            
        symbols = sorted(df[df['INSTRUMENT'] == selected_instrument]['SYMBOL'].unique())
        return [{'label': s, 'value': s} for s in symbols], symbols[0] if symbols else None
    
    @app.callback(
        Output('price-analysis', 'figure'),
        [Input('instrument-filter', 'value'),
         Input('symbol-filter', 'value')]
    )
    def update_price_chart(selected_instrument, selected_symbol):
        if not selected_instrument or not selected_symbol:
            return go.Figure()
            
        df = load_latest_data()
        if df.empty:
            return go.Figure()
            
        filtered_df = df[(df['INSTRUMENT'] == selected_instrument) & 
                        (df['SYMBOL'] == selected_symbol)]
        
        if filtered_df.empty:
            return go.Figure()
            
        fig = go.Figure()
        
        # Add current close price line
        fig.add_trace(go.Scatter(
            x=['Previous', 'Current'],
            y=[filtered_df['CLOSE_prev'].iloc[0], filtered_df['CLOSE'].iloc[0]],
            mode='lines+markers',
            name='Current Close',
            line=dict(color='#c17aeb', width=3),
            marker=dict(size=10),
            hovertemplate='Price: ₹%{y:,.2f}<extra></extra>'
        ))
        
        # Add previous close price line
        fig.add_trace(go.Scatter(
            x=['Previous', 'Current'],
            y=[filtered_df['CLOSE_prev'].iloc[0], filtered_df['CLOSE_prev'].iloc[0]],
            mode='lines',
            name='Previous Close',
            line=dict(color='#7a8ceb', width=2, dash='dash'),
            hovertemplate='Previous Close: ₹%{y:,.2f}<extra></extra>'
        ))
        
        # Calculate price change
        price_change = filtered_df['CLOSE'].iloc[0] - filtered_df['CLOSE_prev'].iloc[0]
        price_change_pct = filtered_df['PRICE_CHANGE_PCT'].iloc[0]
        
        # Add annotation for price change
        fig.add_annotation(
            x='Current',
            y=filtered_df['CLOSE'].iloc[0],
            text=f"Δ: {price_change_pct:+.2f}%",
            showarrow=True,
            arrowhead=1,
            ax=40,
            ay=-40,
            font=dict(color='#ffffff', size=12),
            bgcolor='#c17aeb',
            bordercolor='#c17aeb',
            borderwidth=2,
            borderpad=4,
            opacity=0.8
        )
        
        fig.update_layout(
            title=dict(
                text=f"Price Analysis ({selected_symbol})",
                font=dict(color='#ffffff', size=16),
                x=0.5,
                xanchor='center'
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)',
                tickfont=dict(color='#ffffff'),
                showline=True,
                linecolor='rgba(255,255,255,0.2)'
            ),
            yaxis=dict(
                title='Price (₹)',
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)',
                tickfont=dict(color='#ffffff'),
                showline=True,
                linecolor='rgba(255,255,255,0.2)',
                tickformat=',.2f'
            ),
            showlegend=True,
            legend=dict(
                font=dict(color='#ffffff'),
                bgcolor='rgba(0,0,0,0.5)',
                bordercolor='rgba(255,255,255,0.2)',
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            ),
            margin=dict(l=40, r=40, t=60, b=40),
            height=300
        )
        
        return fig
    
    @app.callback(
        Output('pattern-distribution', 'figure'),
        [Input('instrument-filter', 'value')]
    )
    def update_pattern_distribution(selected_instrument):
        if not selected_instrument:
            return go.Figure()
            
        df = load_latest_data()
        if df.empty:
            return go.Figure()
            
        filtered_df = df[df['INSTRUMENT'] == selected_instrument]
        if filtered_df.empty:
            return go.Figure()
            
        pattern_counts = filtered_df['OI_PATTERN'].value_counts()
        
        colors = {
            'Long Build-up': '#c17aeb',
            'Short Build-up': '#7a8ceb',
            'Long Unwinding': '#9e8ceb',
            'Short Covering': '#7aafeb'
        }
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=pattern_counts.index,
            y=pattern_counts.values,
            marker_color=[colors.get(pattern, '#ffffff') for pattern in pattern_counts.index],
            hovertemplate='%{y} stocks<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(
                text=f"Pattern Distribution - {selected_instrument}",
                font=dict(color='#ffffff', size=16),
                x=0.5,
                xanchor='center'
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                showgrid=False,
                tickfont=dict(color='#ffffff'),
                showline=True,
                linecolor='rgba(255,255,255,0.2)'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)',
                tickfont=dict(color='#ffffff'),
                showline=True,
                linecolor='rgba(255,255,255,0.2)'
            ),
            margin=dict(l=40, r=40, t=40, b=40),
            height=300
        )
        
        return fig
    
    @app.callback(
        Output('open-interest-analysis', 'figure'),
        [Input('instrument-filter', 'value'),
         Input('symbol-filter', 'value')]
    )
    def update_oi_chart(selected_instrument, selected_symbol):
        if not selected_instrument or not selected_symbol:
            return go.Figure()
            
        df = load_latest_data()
        if df.empty:
            return go.Figure()
            
        filtered_df = df[(df['INSTRUMENT'] == selected_instrument) & 
                        (df['SYMBOL'] == selected_symbol)]
        
        if filtered_df.empty:
            return go.Figure()
            
        fig = go.Figure()
        
        # Add OI change bar
        oi_change = filtered_df['CHG_IN_OI'].iloc[0]
        color = '#c17aeb' if oi_change >= 0 else '#7a8ceb'
        
        fig.add_trace(go.Bar(
            x=[selected_symbol],
            y=[oi_change],
            marker_color=color,
            width=0.4,
            hovertemplate='Change in OI: %{y:,.0f}<extra></extra>'
        ))
        
        # Add annotation for OI change
        fig.add_annotation(
            x=selected_symbol,
            y=oi_change,
            text=f"OI Change: {oi_change:,.0f}",
            showarrow=False,
            yshift=10 if oi_change >= 0 else -30,
            font=dict(color='#ffffff', size=12),
            bgcolor=color,
            bordercolor=color,
            borderwidth=2,
            borderpad=4,
            opacity=0.8
        )
        
        fig.update_layout(
            title=dict(
                text=f"Open Interest Analysis ({selected_symbol})",
                font=dict(color='#ffffff', size=16),
                x=0.5,
                xanchor='center'
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                showgrid=False,
                tickfont=dict(color='#ffffff'),
                showline=True,
                linecolor='rgba(255,255,255,0.2)'
            ),
            yaxis=dict(
                title='Change in Open Interest',
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)',
                tickfont=dict(color='#ffffff'),
                showline=True,
                linecolor='rgba(255,255,255,0.2)',
                tickformat=','
            ),
            margin=dict(l=40, r=40, t=60, b=40),
            height=300
        )
        
        return fig
    
    @app.callback(
        Output('buildup-analysis', 'figure'),
        [Input('instrument-filter', 'value'),
         Input('symbol-filter', 'value')]
    )
    def update_buildup_analysis(selected_instrument, selected_symbol):
        """Update buildup analysis chart."""
        try:
            df = load_latest_data()
            if not selected_instrument or not selected_symbol:
                return go.Figure()

            filtered_df = df[(df['INSTRUMENT'] == selected_instrument) & 
                           (df['SYMBOL'] == selected_symbol)]
            
            if filtered_df.empty:
                return go.Figure()

            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=[filtered_df['OI_CHANGE_PCT'].iloc[0]],
                y=[filtered_df['PRICE_CHANGE_PCT'].iloc[0]],
                mode='markers',
                marker=dict(color='#7a8ceb', size=10),
                text=selected_symbol,
                hovertemplate='%{text}<br>OI Change: %{x:.2f}%<br>Price Change: %{y:.2f}%<extra></extra>'
            ))
            
            # Add quadrant labels
            quadrant_labels = [
                dict(x=20, y=20, text="Long Build-up", color='#c17aeb'),
                dict(x=-20, y=20, text="Short Covering", color='#7aafeb'),
                dict(x=-20, y=-20, text="Long Unwinding", color='#9e8ceb'),
                dict(x=20, y=-20, text="Short Build-up", color='#7a8ceb')
            ]

            for label in quadrant_labels:
                fig.add_annotation(
                    x=label['x'],
                    y=label['y'],
                    text=label['text'],
                    showarrow=False,
                    font=dict(color=label['color'])
                )

            # Add axes lines
            fig.add_hline(y=0, line=dict(color='rgba(255,255,255,0.2)', width=1))
            fig.add_vline(x=0, line=dict(color='rgba(255,255,255,0.2)', width=1))

            fig.update_layout(
                title=dict(
                    text=f"Build-up Analysis - {selected_symbol}",
                    font=dict(color='#ffffff', size=16),
                    x=0.5,
                    xanchor='center'
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    title='OI Change %',
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.1)',
                    tickfont=dict(color='#ffffff'),
                    showline=True,
                    linecolor='rgba(255,255,255,0.2)'
                ),
                yaxis=dict(
                    title='Price Change %',
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.1)',
                    tickfont=dict(color='#ffffff'),
                    showline=True,
                    linecolor='rgba(255,255,255,0.2)'
                ),
                margin=dict(l=40, r=40, t=40, b=40),
                height=300
            )
            
            return fig

        except Exception as e:
            logger.error(f"Error updating buildup analysis: {str(e)}")
            return go.Figure()
    
    @app.callback(
        Output('added-stocks-table', 'children'),
        [Input('submit-stock-analysis', 'n_clicks')],
        [State('stock-symbol-input', 'value'),
         State('instrument-type-input', 'value'),
         State('price-change-input', 'value'),
         State('oi-change-input', 'value'),
         State('added-stocks-table', 'children')]
    )
    def update_stocks_table(n_clicks, symbol, instrument_type, price_change, oi_change, current_table):
        """Update the table of added stocks with build-up analysis."""
        if n_clicks is None or not all([symbol, instrument_type, price_change is not None, oi_change is not None]):
            raise PreventUpdate
            
        try:
            # Determine build-up pattern
            pattern = determine_buildup_pattern(price_change, oi_change)
            
            # Create new row
            new_row = html.Tr([
                html.Td(symbol, style={'padding': '10px', 'borderBottom': '1px solid #ddd'}),
                html.Td(instrument_type, style={'padding': '10px', 'borderBottom': '1px solid #ddd'}),
                html.Td(f"{price_change:.2f}%", style={'padding': '10px', 'borderBottom': '1px solid #ddd'}),
                html.Td(f"{oi_change:.2f}%", style={'padding': '10px', 'borderBottom': '1px solid #ddd'}),
                html.Td(pattern, style={
                    'padding': '10px',
                    'borderBottom': '1px solid #ddd',
                    'color': get_pattern_color(pattern)
                })
            ])
            
            # Initialize table if it doesn't exist
            if not current_table:
                return html.Table(
                    [
                        html.Thead(
                            html.Tr([
                                html.Th('Symbol', style={'padding': '10px', 'textAlign': 'left', 'borderBottom': '2px solid #ddd'}),
                                html.Th('Instrument', style={'padding': '10px', 'textAlign': 'left', 'borderBottom': '2px solid #ddd'}),
                                html.Th('Price Change', style={'padding': '10px', 'textAlign': 'left', 'borderBottom': '2px solid #ddd'}),
                                html.Th('OI Change', style={'padding': '10px', 'textAlign': 'left', 'borderBottom': '2px solid #ddd'}),
                                html.Th('Pattern', style={'padding': '10px', 'textAlign': 'left', 'borderBottom': '2px solid #ddd'})
                            ])
                        ),
                        html.Tbody([new_row])
                    ],
                    style={'width': '100%', 'borderCollapse': 'collapse'}
                )
            
            # Add new row to existing table
            current_table['props']['children'][1]['props']['children'].append(new_row)
            return current_table
            
        except Exception as e:
            logger.error(f"Error updating stocks table: {str(e)}")
            raise PreventUpdate
    
    @app.callback(
        [Output('long-buildup-list', 'children'),
         Output('short-buildup-list', 'children'),
         Output('long-unwinding-list', 'children'),
         Output('short-covering-list', 'children')],
        [Input('display-mode', 'value')]
    )
    def update_stock_lists(show_top_3):
        """Update the stock lists with detailed information."""
        try:
            df = load_latest_data()
            if df.empty:
                return [], [], [], []

            def create_stock_row(row):
                return html.Div([
                    html.Div([
                        html.Strong(f"{row['SYMBOL']}", style={'color': '#ffffff', 'marginRight': '8px'}),
                        html.Span(f"({row['INSTRUMENT']})", style={'color': 'rgba(255, 255, 255, 0.7)'})
                    ]),
                    html.Div([
                        html.Span("OI Change: ", style={'color': '#ffffff'}),
                        html.Span(f"{row['OI_CHANGE_PCT']:.2f}%",
                                style={'color': '#c17aeb' if row['OI_CHANGE_PCT'] > 0 else '#7a8ceb',
                                      'fontWeight': 'bold'})
                    ]),
                    html.Div([
                        html.Span("Price Change: ", style={'color': '#ffffff'}),
                        html.Span(f"{row['PRICE_CHANGE_PCT']:.2f}%",
                                style={'color': '#c17aeb' if row['PRICE_CHANGE_PCT'] > 0 else '#7a8ceb',
                                      'fontWeight': 'bold'})
                    ])
                ], className='stock-row')

            # Filter and sort stocks by pattern
            patterns = {
                'Long Build-up': df[df['OI_PATTERN'] == 'Long Build-up'],
                'Short Build-up': df[df['OI_PATTERN'] == 'Short Build-up'],
                'Long Unwinding': df[df['OI_PATTERN'] == 'Long Unwinding'],
                'Short Covering': df[df['OI_PATTERN'] == 'Short Covering']
            }

            # Sort by OI change percentage
            for pattern in patterns:
                patterns[pattern] = patterns[pattern].sort_values('OI_CHANGE_PCT', ascending=False)
                if show_top_3:
                    patterns[pattern] = patterns[pattern].head(3)

            # Create lists
            lists = {
                pattern: [create_stock_row(row) for _, row in pattern_df.iterrows()]
                for pattern, pattern_df in patterns.items()
            }

            return (lists['Long Build-up'], lists['Short Build-up'],
                    lists['Long Unwinding'], lists['Short Covering'])

        except Exception as e:
            logger.error(f"Error updating stock lists: {str(e)}")
            return [], [], [], []

def determine_buildup_pattern(price_change, oi_change):
    """Determine the build-up pattern based on price and OI changes."""
    if price_change > 0 and oi_change > 0:
        return 'Long Build-up'
    elif price_change < 0 and oi_change > 0:
        return 'Short Build-up'
    elif price_change < 0 and oi_change < 0:
        return 'Long Unwinding'
    elif price_change > 0 and oi_change < 0:
        return 'Short Covering'
    else:
        return 'No Clear Pattern'

def get_pattern_color(pattern):
    """Get the color for a specific pattern."""
    color_map = {
        'Long Build-up': '#c17aeb',
        'Short Build-up': '#7a8ceb',
        'Long Unwinding': '#9e8ceb',
        'Short Covering': '#7aafeb',
        'No Clear Pattern': '#95a5a6'
    }
    return color_map.get(pattern, '#95a5a6')

def get_theme_colors():
    """Get the theme colors for charts."""
    return {
        'primary': '#c17aeb',  # Purple
        'secondary': '#7a8ceb',  # Blue
        'background': 'rgba(0, 0, 0, 0.3)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'text': '#ffffff',
        'grid': 'rgba(255, 255, 255, 0.1)',
        'patterns': {
            'Long Build-up': '#c17aeb',    # Purple
            'Short Build-up': '#7a8ceb',   # Blue
            'Long Unwinding': '#9e8ceb',   # Purple-Blue
            'Short Covering': '#7aafeb'    # Light Blue
        }
    }

def apply_theme_to_figure(fig):
    """Apply consistent theme to any figure."""
    colors = get_theme_colors()
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['paper_bgcolor'],
        font_color=colors['text'],
        title_font_color=colors['text'],
        legend_font_color=colors['text'],
        xaxis=dict(
            gridcolor=colors['grid'],
            color=colors['text'],
            tickfont=dict(color=colors['text'])
        ),
        yaxis=dict(
            gridcolor=colors['grid'],
            color=colors['text'],
            tickfont=dict(color=colors['text'])
        ),
        legend=dict(
            bgcolor='rgba(0,0,0,0.5)',
            font=dict(color=colors['text'])
        )
    )
    return fig

def create_empty_figure():
    """Create an empty figure with a message."""
    fig = go.Figure()
    fig.add_annotation(
        text="No data available",
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(color="white", size=16)
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False, showticklabels=False)
    )
    return fig

def create_price_chart(df):
    """Create price analysis chart."""
    fig = go.Figure()
    
    if not df.empty and all(col in df.columns for col in ['SYMBOL', 'CLOSE', 'CLOSE_prev']):
        # Add current close price
        fig.add_trace(go.Scatter(
            x=df['SYMBOL'],
            y=df['CLOSE'],
            name='Current Close',
            mode='lines+markers',
            line=dict(color='#c17aeb', width=2),
            marker=dict(size=8)
        ))
        
        # Add previous close price
        fig.add_trace(go.Scatter(
            x=df['SYMBOL'],
            y=df['CLOSE_prev'],
            name='Previous Close',
            mode='lines+markers',
            line=dict(color='#7a8ceb', width=2, dash='dash'),
            marker=dict(size=8)
        ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            tickfont=dict(color='white')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            tickfont=dict(color='white')
        ),
        legend=dict(
            font=dict(color='white'),
            bgcolor='rgba(0,0,0,0.5)'
        ),
        margin=dict(t=30)
    )
    
    return fig

def create_oi_chart(df):
    """Create open interest analysis chart."""
    fig = go.Figure()
    
    if not df.empty and all(col in df.columns for col in ['SYMBOL', 'CHG_IN_OI']):
        colors = ['#c17aeb' if x > 0 else '#7a8ceb' for x in df['CHG_IN_OI']]
        
        fig.add_trace(go.Bar(
            x=df['SYMBOL'],
            y=df['CHG_IN_OI'],
            marker_color=colors,
            name='Change in OI'
        ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            tickfont=dict(color='white')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            tickfont=dict(color='white')
        ),
        margin=dict(t=30)
    )
    
    return fig

def create_buildup_chart(df):
    """Create build-up analysis chart."""
    fig = go.Figure()
    
    if not df.empty and all(col in df.columns for col in ['OI_CHANGE_PCT', 'PRICE_CHANGE_PCT', 'SYMBOL', 'OI_PATTERN']):
        # Create scatter plot
        fig.add_trace(go.Scatter(
            x=df['OI_CHANGE_PCT'],
            y=df['PRICE_CHANGE_PCT'],
            mode='markers+text',
            marker=dict(
                size=10,
                color=df['OI_PATTERN'].map({
                    'Long Build-up': '#c17aeb',
                    'Short Build-up': '#7a8ceb',
                    'Long Unwinding': '#9e8ceb',
                    'Short Covering': '#7aafeb'
                })
            ),
            text=df['SYMBOL'],
            textposition='top center',
            name='Stocks'
        ))
        
        # Add quadrant lines
        fig.add_hline(y=0, line_dash="dash", line_color="rgba(255, 255, 255, 0.2)")
        fig.add_vline(x=0, line_dash="dash", line_color="rgba(255, 255, 255, 0.2)")
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(
            title='OI Change %',
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            tickfont=dict(color='white')
        ),
        yaxis=dict(
            title='Price Change %',
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            tickfont=dict(color='white')
        ),
        margin=dict(t=30)
    )
    
    return fig

def create_pattern_chart(df):
    """Create pattern distribution chart."""
    fig = go.Figure()
    
    if not df.empty and 'OI_PATTERN' in df.columns:
        pattern_counts = df['OI_PATTERN'].value_counts()
        
        colors = {
            'Long Build-up': '#c17aeb',
            'Short Build-up': '#7a8ceb',
            'Long Unwinding': '#9e8ceb',
            'Short Covering': '#7aafeb'
        }
        
        fig.add_trace(go.Bar(
            x=pattern_counts.index,
            y=pattern_counts.values,
            marker_color=[colors.get(x, '#95a5a6') for x in pattern_counts.index],
            text=pattern_counts.values,
            textposition='auto'
        ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            tickfont=dict(color='white')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            tickfont=dict(color='white')
        ),
        margin=dict(t=30)
    )
    
    return fig