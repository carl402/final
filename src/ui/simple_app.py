import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go

class SimpleApp:
    def __init__(self):
        self.app = dash.Dash(__name__)
        self.logged_in = False
        self.setup_layout()
        self.setup_callbacks()
    
    def setup_layout(self):
        self.app.layout = html.Div([
            dcc.Store(id='session', data={'logged_in': False}),
            html.Div(id='main-container')
        ])
    
    def setup_callbacks(self):
        @self.app.callback(
            Output('main-container', 'children'),
            Input('session', 'data')
        )
        def display_main(session_data):
            if session_data and session_data.get('logged_in'):
                return self.dashboard_layout()
            return self.login_layout()
        
        @self.app.callback(
            Output('session', 'data'),
            Input('login-btn', 'n_clicks'),
            State('username', 'value'),
            State('password', 'value'),
            prevent_initial_call=True
        )
        def handle_login(n_clicks, username, password):
            if username == 'admin' and password == 'admin123':
                return {'logged_in': True}
            return {'logged_in': False}
    
    def login_layout(self):
        return html.Div([
            html.Div([
                html.H1("🎯 Monte Carlo Decision Engine", 
                       style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 40}),
                html.Div([
                    html.H3("Iniciar Sesión", style={'textAlign': 'center', 'marginBottom': 30}),
                    dcc.Input(
                        id='username',
                        placeholder='Usuario (admin)',
                        type='text',
                        value='admin',
                        style={'width': '100%', 'padding': '12px', 'margin': '10px 0', 'borderRadius': '5px'}
                    ),
                    dcc.Input(
                        id='password',
                        placeholder='Contraseña (admin123)',
                        type='password',
                        value='admin123',
                        style={'width': '100%', 'padding': '12px', 'margin': '10px 0', 'borderRadius': '5px'}
                    ),
                    html.Button(
                        'Iniciar Sesión',
                        id='login-btn',
                        style={
                            'width': '100%', 'padding': '12px', 'backgroundColor': '#3498db',
                            'color': 'white', 'border': 'none', 'borderRadius': '5px',
                            'fontSize': '16px', 'cursor': 'pointer'
                        }
                    )
                ], style={
                    'maxWidth': '400px', 'margin': '0 auto', 'padding': '40px',
                    'backgroundColor': 'white', 'borderRadius': '10px',
                    'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'
                })
            ], style={
                'minHeight': '100vh', 'backgroundColor': '#ecf0f1',
                'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'
            })
        ])
    
    def dashboard_layout(self):
        return html.Div([
            # Header
            html.Div([
                html.H1("🎯 Monte Carlo Decision Engine", 
                       style={'color': 'white', 'margin': 0, 'padding': '20px'})
            ], style={'backgroundColor': '#2c3e50'}),
            
            # Content
            html.Div([
                html.H2("📊 Dashboard Principal", style={'color': '#2c3e50', 'marginBottom': 30}),
                
                # Menu Cards
                html.Div([
                    html.Div([
                        html.H3("📁 Proyectos"),
                        html.P("Gestionar proyectos y escenarios"),
                        html.Button("Ir a Proyectos", style={'padding': '10px 20px', 'backgroundColor': '#3498db', 'color': 'white', 'border': 'none', 'borderRadius': '5px'})
                    ], style={'backgroundColor': 'white', 'padding': '30px', 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)', 'margin': '15px', 'textAlign': 'center'}),
                    
                    html.Div([
                        html.H3("🧮 Simulaciones"),
                        html.P("Ejecutar simulaciones Monte Carlo"),
                        html.Button("Nueva Simulación", style={'padding': '10px 20px', 'backgroundColor': '#27ae60', 'color': 'white', 'border': 'none', 'borderRadius': '5px'})
                    ], style={'backgroundColor': 'white', 'padding': '30px', 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)', 'margin': '15px', 'textAlign': 'center'}),
                    
                    html.Div([
                        html.H3("📈 Visualizaciones"),
                        html.P("Ver gráficos y análisis"),
                        html.Button("Ver Gráficos", style={'padding': '10px 20px', 'backgroundColor': '#e74c3c', 'color': 'white', 'border': 'none', 'borderRadius': '5px'})
                    ], style={'backgroundColor': 'white', 'padding': '30px', 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)', 'margin': '15px', 'textAlign': 'center'}),
                    
                    html.Div([
                        html.H3("👥 Usuarios"),
                        html.P("Gestión de usuarios del sistema"),
                        html.Button("Gestionar", style={'padding': '10px 20px', 'backgroundColor': '#9b59b6', 'color': 'white', 'border': 'none', 'borderRadius': '5px'})
                    ], style={'backgroundColor': 'white', 'padding': '30px', 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)', 'margin': '15px', 'textAlign': 'center'})
                ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(300px, 1fr))', 'gap': '20px'}),
                
                # Proyectos Recientes
                html.Div([
                    html.H3("📁 Proyectos Recientes"),
                    html.Div([
                        html.Div([
                            html.H4("Proyecto Alpha"),
                            html.P("Lanzamiento de producto premium"),
                            html.Small("Creado: 2024-01-15 | 3 escenarios")
                        ], style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '8px', 'margin': '10px 0', 'borderLeft': '4px solid #3498db'}),
                        
                        html.Div([
                            html.H4("Proyecto Beta"),
                            html.P("Expansión mercado local"),
                            html.Small("Creado: 2024-01-10 | 2 escenarios")
                        ], style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '8px', 'margin': '10px 0', 'borderLeft': '4px solid #27ae60'})
                    ])
                ], style={'marginTop': '40px'}),
                
                # Buscador
                html.Div([
                    html.H3("🔍 Buscar Proyectos"),
                    dcc.Input(
                        placeholder='Buscar proyectos...',
                        style={'width': '100%', 'padding': '12px', 'borderRadius': '5px', 'border': '1px solid #ddd'}
                    )
                ], style={'marginTop': '30px'})
                
            ], style={'padding': '30px', 'maxWidth': '1200px', 'margin': '0 auto'})
        ])
    
    def run_server(self, debug=False, port=8050):
        self.app.run(debug=debug, port=port, host='0.0.0.0')