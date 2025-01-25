from dash import html, dcc

def create_header():
    return html.Div([
        html.H1(
            'Stock Market Analysis Dashboard',
            style={
                'textAlign': 'center',
                'color': '#ffffff',
                'padding': '25px 0',
                'margin': 0,
                'fontSize': '32px',
                'fontWeight': 'bold',
                'letterSpacing': '1px'
            }
        ),
        html.P(
            'Real-time analysis of market trends and patterns',
            style={
                'textAlign': 'center',
                'color': 'rgba(255, 255, 255, 0.9)',
                'margin': 0,
                'fontSize': '16px',
                'paddingBottom': '20px'
            }
        )
    ], style={
        'background': 'linear-gradient(180deg, #000000 0%, rgba(193, 122, 235, 0.8) 100%)',
        'marginBottom': 30,
        'boxShadow': '0 4px 6px rgba(0,0,0,0.2)'
    })

def create_data_overview_section(data_overview):
    """Create the data overview section with statistics and pattern cards."""
    return html.Div([
        html.H3('Market Overview', style={
            'marginBottom': 25,
            'color': '#ffffff',
            'fontSize': '24px',
            'fontWeight': 'bold',
            'borderBottom': '1px solid rgba(255, 255, 255, 0.1)',
            'paddingBottom': '10px'
        }),
        
        # Statistics Cards Row
        html.Div([
            # Total Records Card
            html.Div([
                html.H4('Total Records', style={'color': '#ffffff', 'fontSize': '16px', 'marginBottom': '10px'}),
                html.P(str(data_overview.get('Total Records', 0)), style={
                    'fontSize': '32px',
                    'fontWeight': 'bold',
                    'color': '#ffffff',
                    'margin': 0
                })
            ], className='glass-effect stats-card'),
            
            # Instruments Card
            html.Div([
                html.H4('Instruments', style={'color': '#ffffff', 'fontSize': '16px', 'marginBottom': '10px'}),
                html.P(str(data_overview.get('Unique Instruments', 0)), style={
                    'fontSize': '32px',
                    'fontWeight': 'bold',
                    'color': '#ffffff',
                    'margin': 0
                })
            ], className='glass-effect stats-card'),
            
            # Symbols Card
            html.Div([
                html.H4('Symbols', style={'color': '#ffffff', 'fontSize': '16px', 'marginBottom': '10px'}),
                html.P(str(data_overview.get('Unique Symbols', 0)), style={
                    'fontSize': '32px',
                    'fontWeight': 'bold',
                    'color': '#ffffff',
                    'margin': 0
                })
            ], className='glass-effect stats-card')
        ], className='stats-cards-container'),
        
        # Pattern Analysis Grid
        html.Div([
            # Long Build-up Card
            html.Div([
                html.H5('Long Build-up', style={
                    'color': '#c17aeb',
                    'fontSize': '18px',
                    'fontWeight': 'bold',
                    'marginBottom': '15px'
                }),
                html.Div([
                    html.Strong("Count: ", style={'color': '#ffffff'}),
                    html.Span(str(data_overview.get('Long Build-up Count', 0)),
                        style={'fontSize': '24px', 'color': '#c17aeb', 'fontWeight': 'bold'}
                    )
                ], style={'marginBottom': '15px'}),
                html.Div([
                    html.Div([
                        html.Span('●', style={'color': '#c17aeb', 'fontSize': '24px', 'marginRight': '8px'}),
                        html.Span('Buy', style={'color': '#c17aeb', 'fontWeight': 'bold'})
                    ], style={'marginBottom': '8px'}),
                    html.P("Strong uptrend potential", style={'color': '#ffffff', 'margin': '8px 0'}),
                    html.P("• Price ↑ & OI ↑", style={'color': '#ffffff', 'margin': '8px 0'}),
                    html.P("• Bulls adding positions", style={'color': '#ffffff', 'margin': '8px 0'})
                ])
            ], className='glass-effect'),
            
            # Short Build-up Card
            html.Div([
                html.H5('Short Build-up', style={
                    'color': '#7a8ceb',
                    'fontSize': '18px',
                    'fontWeight': 'bold',
                    'marginBottom': '15px'
                }),
                html.Div([
                    html.Strong("Count: ", style={'color': '#ffffff'}),
                    html.Span(str(data_overview.get('Short Build-up Count', 0)),
                        style={'fontSize': '24px', 'color': '#7a8ceb', 'fontWeight': 'bold'}
                    )
                ], style={'marginBottom': '15px'}),
                html.Div([
                    html.Div([
                        html.Span('●', style={'color': '#7a8ceb', 'fontSize': '24px', 'marginRight': '8px'}),
                        html.Span('Sell', style={'color': '#7a8ceb', 'fontWeight': 'bold'})
                    ], style={'marginBottom': '8px'}),
                    html.P("Strong downtrend potential", style={'color': '#ffffff', 'margin': '8px 0'}),
                    html.P("• Price ↓ & OI ↑", style={'color': '#ffffff', 'margin': '8px 0'}),
                    html.P("• Bears adding positions", style={'color': '#ffffff', 'margin': '8px 0'})
                ])
            ], className='glass-effect'),
            
            # Long Unwinding Card
            html.Div([
                html.H5('Long Unwinding', style={
                    'color': '#9e8ceb',
                    'fontSize': '18px',
                    'fontWeight': 'bold',
                    'marginBottom': '15px'
                }),
                html.Div([
                    html.Strong("Count: ", style={'color': '#ffffff'}),
                    html.Span(str(data_overview.get('Long Unwinding Count', 0)),
                        style={'fontSize': '24px', 'color': '#9e8ceb', 'fontWeight': 'bold'}
                    )
                ], style={'marginBottom': '15px'}),
                html.Div([
                    html.Div([
                        html.Span('●', style={'color': '#9e8ceb', 'fontSize': '24px', 'marginRight': '8px'}),
                        html.Span('Hold', style={'color': '#9e8ceb', 'fontWeight': 'bold'})
                    ], style={'marginBottom': '8px'}),
                    html.P("Wait for trend reversal", style={'color': '#ffffff', 'margin': '8px 0'}),
                    html.P("• Price ↓ & OI ↓", style={'color': '#ffffff', 'margin': '8px 0'}),
                    html.P("• Bulls exiting positions", style={'color': '#ffffff', 'margin': '8px 0'})
                ])
            ], className='glass-effect'),
            
            # Short Covering Card
            html.Div([
                html.H5('Short Covering', style={
                    'color': '#7aafeb',
                    'fontSize': '18px',
                    'fontWeight': 'bold',
                    'marginBottom': '15px'
                }),
                html.Div([
                    html.Strong("Count: ", style={'color': '#ffffff'}),
                    html.Span(str(data_overview.get('Short Covering Count', 0)),
                        style={'fontSize': '24px', 'color': '#7aafeb', 'fontWeight': 'bold'}
                    )
                ], style={'marginBottom': '15px'}),
                html.Div([
                    html.Div([
                        html.Span('●', style={'color': '#7aafeb', 'fontSize': '24px', 'marginRight': '8px'}),
                        html.Span('Exit', style={'color': '#7aafeb', 'fontWeight': 'bold'})
                    ], style={'marginBottom': '8px'}),
                    html.P("Potential trend reversal", style={'color': '#ffffff', 'margin': '8px 0'}),
                    html.P("• Price ↑ & OI ↓", style={'color': '#ffffff', 'margin': '8px 0'}),
                    html.P("• Bears exiting positions", style={'color': '#ffffff', 'margin': '8px 0'})
                ])
            ], className='glass-effect')
        ], className='pattern-cards-grid')
    ], className='container')

def create_filters_section(analysis_df):
    return html.Div([
        html.Div([
            # Instrument Filter
            html.Div([
                html.Label('Instrument Type', 
                    style={
                        'marginBottom': 8,
                        'display': 'block',
                        'color': '#ffffff',
                        'fontSize': '14px',
                        'fontWeight': 'bold'
                    }
                ),
                dcc.Dropdown(
                    id='instrument-filter',
                    options=[{'label': i, 'value': i} for i in sorted(analysis_df['INSTRUMENT'].unique())],
                    value='FUTIDX' if 'FUTIDX' in analysis_df['INSTRUMENT'].unique() else None,
                    className='dropdown-dark'
                )
            ], style={'flex': 1, 'marginRight': 15}),
            
            # Symbol Filter
            html.Div([
                html.Label('Symbol', 
                    style={
                        'marginBottom': 8,
                        'display': 'block',
                        'color': '#ffffff',
                        'fontSize': '14px',
                        'fontWeight': 'bold'
                    }
                ),
                dcc.Dropdown(
                    id='symbol-filter',
                    className='dropdown-dark'
                )
            ], style={'flex': 1})
        ], className='filters-container')
    ], className='container', style={'marginBottom': 30})

def create_charts_section():
    """Create the charts section with proper layout."""
    return html.Section(className='charts-container', children=[
        # Price Analysis Chart
        html.Div(className='chart-card', children=[
            html.H3("Price Analysis", className='chart-title'),
            dcc.Graph(
                id='price-analysis',
                config={
                    'displayModeBar': True,
                    'displaylogo': False,
                    'modeBarButtonsToRemove': ['lasso2d', 'select2d']
                }
            )
        ]),
        
        # Open Interest Analysis Chart
        html.Div(className='chart-card', children=[
            html.H3("Open Interest Analysis", className='chart-title'),
            dcc.Graph(
                id='open-interest-analysis',
                config={
                    'displayModeBar': True,
                    'displaylogo': False,
                    'modeBarButtonsToRemove': ['lasso2d', 'select2d']
                }
            )
        ]),
        
        # Build-up Analysis Chart
        html.Div(className='chart-card', children=[
            html.H3("Build-up Analysis", className='chart-title'),
            dcc.Graph(
                id='buildup-analysis',
                config={
                    'displayModeBar': True,
                    'displaylogo': False,
                    'modeBarButtonsToRemove': ['lasso2d', 'select2d']
                }
            )
        ]),
        
        # Pattern Distribution Chart
        html.Div(className='chart-card', children=[
            html.H3("Pattern Distribution", className='chart-title'),
            dcc.Graph(
                id='pattern-distribution',
                config={
                    'displayModeBar': True,
                    'displaylogo': False,
                    'modeBarButtonsToRemove': ['lasso2d', 'select2d']
                }
            )
        ])
    ])

def create_buildup_input_section():
    return html.Div([
        html.H3('Add Stock Build-up Analysis', style={
            'color': '#2c3e50',
            'fontSize': '24px',
            'fontWeight': 'bold',
            'marginBottom': '20px',
            'borderBottom': '2px solid #eee',
            'paddingBottom': '10px'
        }),
        html.Div([
            # Stock Input Row
            html.Div([
                html.Div([
                    html.Label('Stock Symbol', style={
                        'marginBottom': 8,
                        'display': 'block',
                        'color': '#2c3e50',
                        'fontSize': '14px',
                        'fontWeight': 'bold'
                    }),
                    dcc.Input(
                        id='stock-symbol-input',
                        type='text',
                        placeholder='Enter stock symbol',
                        style={
                            'width': '100%',
                            'padding': '8px',
                            'borderRadius': '4px',
                            'border': '1px solid #ddd'
                        }
                    )
                ], style={'flex': 1, 'marginRight': '15px'}),
                html.Div([
                    html.Label('Instrument Type', style={
                        'marginBottom': 8,
                        'display': 'block',
                        'color': '#2c3e50',
                        'fontSize': '14px',
                        'fontWeight': 'bold'
                    }),
                    dcc.Dropdown(
                        id='instrument-type-input',
                        options=[
                            {'label': 'Future Index', 'value': 'FUTIDX'},
                            {'label': 'Future Stock', 'value': 'FUTSTK'}
                        ],
                        style={'width': '100%'},
                        className='dropdown-style'
                    )
                ], style={'flex': 1})
            ], style={'display': 'flex', 'marginBottom': '20px'}),
            
            # Build-up Values Row
            html.Div([
                html.Div([
                    html.Label('Price Change (%)', style={
                        'marginBottom': 8,
                        'display': 'block',
                        'color': '#2c3e50',
                        'fontSize': '14px',
                        'fontWeight': 'bold'
                    }),
                    dcc.Input(
                        id='price-change-input',
                        type='number',
                        placeholder='Enter price change',
                        style={
                            'width': '100%',
                            'padding': '8px',
                            'borderRadius': '4px',
                            'border': '1px solid #ddd'
                        }
                    )
                ], style={'flex': 1, 'marginRight': '15px'}),
                html.Div([
                    html.Label('OI Change (%)', style={
                        'marginBottom': 8,
                        'display': 'block',
                        'color': '#2c3e50',
                        'fontSize': '14px',
                        'fontWeight': 'bold'
                    }),
                    dcc.Input(
                        id='oi-change-input',
                        type='number',
                        placeholder='Enter OI change',
                        style={
                            'width': '100%',
                            'padding': '8px',
                            'borderRadius': '4px',
                            'border': '1px solid #ddd'
                        }
                    )
                ], style={'flex': 1})
            ], style={'display': 'flex', 'marginBottom': '20px'}),
            
            # Submit Button
            html.Button(
                'Add Stock Analysis',
                id='submit-stock-analysis',
                style={
                    'backgroundColor': '#2ecc71',
                    'color': 'white',
                    'padding': '10px 20px',
                    'border': 'none',
                    'borderRadius': '4px',
                    'cursor': 'pointer',
                    'fontSize': '14px',
                    'fontWeight': 'bold'
                }
            ),
            
            # Added Stocks Table
            html.Div([
                html.H4('Added Stocks', style={
                    'color': '#2c3e50',
                    'fontSize': '18px',
                    'fontWeight': 'bold',
                    'marginTop': '30px',
                    'marginBottom': '15px'
                }),
                html.Div(id='added-stocks-table')
            ])
        ], style={
            'backgroundColor': 'white',
            'padding': '20px',
            'borderRadius': '10px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
        })
    ], style={'marginBottom': 30})

def create_buildup_summary_section():
    """Create the build-up summary section with radio items for display mode."""
    return html.Div([
        # Title and Radio Items Container
        html.Div([
            html.H3('Market Build-up Analysis', 
                style={
                    'color': '#ffffff',
                    'fontSize': '28px',
                    'fontWeight': 'bold',
                    'margin': '0'
                }
            ),
            dcc.RadioItems(
                id='display-mode',
                options=[
                    {'label': 'Show All', 'value': False},
                    {'label': 'Top 3 Only', 'value': True}
                ],
                value=False,
                className='radio-items'
            )
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'marginBottom': '30px'
        }),
        
        html.Div([
            # Long Build-up List
            html.Div([
                html.H4('Long Build-up', style={'color': '#c17aeb', 'marginBottom': '15px'}),
                html.Div(id='long-buildup-list', className='stock-list')
            ], className='glass-effect'),
            
            # Short Build-up List
            html.Div([
                html.H4('Short Build-up', style={'color': '#7a8ceb', 'marginBottom': '15px'}),
                html.Div(id='short-buildup-list', className='stock-list')
            ], className='glass-effect'),
            
            # Long Unwinding List
            html.Div([
                html.H4('Long Unwinding', style={'color': '#9e8ceb', 'marginBottom': '15px'}),
                html.Div(id='long-unwinding-list', className='stock-list')
            ], className='glass-effect'),
            
            # Short Covering List
            html.Div([
                html.H4('Short Covering', style={'color': '#7aafeb', 'marginBottom': '15px'}),
                html.Div(id='short-covering-list', className='stock-list')
            ], className='glass-effect')
        ], className='pattern-cards-grid')
    ], className='container')

def create_main_layout(analysis_df, data_overview):
    """Create the main layout of the dashboard."""
    return html.Div([
        create_header(),
        html.Div([
            create_data_overview_section(data_overview),
            create_filters_section(analysis_df),
            create_charts_section(),
            create_buildup_summary_section()
        ], style={'padding': '20px', 'backgroundColor': '#000000', 'minHeight': '100vh'})
    ]) 