import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
import numpy as np
from ..simulation.monte_carlo_engine import MonteCarloEngine
from ..models.business_scenario import BusinessScenario
from ..utils.statistics import StatisticsCalculator

class SimpleApp:
    def __init__(self):
        self.app = dash.Dash(__name__)
        self.engine = MonteCarloEngine(n_simulations=5000)
        self.logged_in = False
        self.setup_layout()
        self.setup_callbacks()
    
    def setup_layout(self):
        self.app.layout = html.Div([
            dcc.Store(id='session', data={'logged_in': False}),
            dcc.Store(id='current-page', data='dashboard'),
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
        
        @self.app.callback(
            Output('current-page', 'data'),
            [Input('btn-projects', 'n_clicks'),
             Input('btn-simulations', 'n_clicks'),
             Input('btn-visualizations', 'n_clicks'),
             Input('btn-users', 'n_clicks'),
             Input('btn-dashboard', 'n_clicks')],
            prevent_initial_call=True
        )
        def navigate(proj, sim, vis, users, dash):
            ctx = dash.callback_context
            if not ctx.triggered:
                return 'dashboard'
            
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if button_id == 'btn-projects':
                return 'projects'
            elif button_id == 'btn-simulations':
                return 'simulations'
            elif button_id == 'btn-visualizations':
                return 'visualizations'
            elif button_id == 'btn-users':
                return 'users'
            return 'dashboard'
        
        @self.app.callback(
            Output('page-content', 'children'),
            Input('current-page', 'data')
        )
        def display_page_content(page):
            if page == 'projects':
                return self.projects_page()
            elif page == 'simulations':
                return self.simulations_page()
            elif page == 'visualizations':
                return self.visualizations_page()
            elif page == 'users':
                return self.users_page()
            return self.dashboard_content()
        
        @self.app.callback(
            Output('simulation-results', 'children'),
            Input('run-simulation', 'n_clicks'),
            [State('scenario-name', 'value'),
             State('initial-investment', 'value'),
             State('revenue-mean', 'value'),
             State('revenue-std', 'value')],
            prevent_initial_call=True
        )
        def run_simulation(n_clicks, name, investment, revenue_mean, revenue_std):
            if not n_clicks:
                return html.Div()
            
            scenario = BusinessScenario(
                name=name or "Escenario Test",
                initial_investment=investment or 100000,
                revenue_mean=revenue_mean or 25000,
                revenue_std=revenue_std or 5000,
                cost_mean=15000,
                cost_std=3000
            )
            
            result = self.engine.simulate_scenario(scenario)
            metrics = StatisticsCalculator.calculate_risk_metrics(result)
            
            return html.Div([
                html.H3("📈 Resultados de la Simulación", style={'color': '#2c3e50'}),
                html.Div([
                    html.Div([
                        html.H2(f"${metrics['media_npv']:,.0f}", style={'color': 'white', 'margin': 0}),
                        html.P("NPV Promedio", style={'color': 'white', 'margin': 0})
                    ], style={'backgroundColor': '#27ae60', 'padding': '20px', 'borderRadius': '8px', 'textAlign': 'center', 'margin': '10px', 'minWidth': '200px'}),
                    
                    html.Div([
                        html.H2(f"{metrics['probabilidad_exito']:.1f}%", style={'color': 'white', 'margin': 0}),
                        html.P("Probabilidad Éxito", style={'color': 'white', 'margin': 0})
                    ], style={'backgroundColor': '#3498db', 'padding': '20px', 'borderRadius': '8px', 'textAlign': 'center', 'margin': '10px', 'minWidth': '200px'}),
                    
                    html.Div([
                        html.H2(f"{metrics['roi_medio']:.1f}%", style={'color': 'white', 'margin': 0}),
                        html.P("ROI Promedio", style={'color': 'white', 'margin': 0})
                    ], style={'backgroundColor': '#e74c3c', 'padding': '20px', 'borderRadius': '8px', 'textAlign': 'center', 'margin': '10px', 'minWidth': '200px'})
                ], style={'display': 'flex', 'justifyContent': 'center', 'flexWrap': 'wrap'})
            ])
    
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
                       style={'color': 'white', 'margin': 0, 'padding': '20px', 'display': 'inline-block'}),
                html.Button("🏠 Dashboard", id='btn-dashboard', 
                           style={'float': 'right', 'margin': '20px', 'padding': '10px 15px', 'backgroundColor': '#34495e', 'color': 'white', 'border': 'none', 'borderRadius': '5px'})
            ], style={'backgroundColor': '#2c3e50', 'overflow': 'hidden'}),
            
            # Content
            html.Div(id='page-content', children=[
                self.dashboard_content()
            ], style={'padding': '30px', 'maxWidth': '1200px', 'margin': '0 auto'})
        ])
    
    def dashboard_content(self):
        return html.Div([
                html.H2("📊 Dashboard Principal", style={'color': '#2c3e50', 'marginBottom': 30}),
                
                # Menu Cards
                html.Div([
                    html.Div([
                        html.H3("📁 Proyectos"),
                        html.P("Gestionar proyectos y escenarios"),
                        html.Button("Ir a Proyectos", id='btn-projects', style={'padding': '10px 20px', 'backgroundColor': '#3498db', 'color': 'white', 'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer'})
                    ], style={'backgroundColor': 'white', 'padding': '30px', 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)', 'margin': '15px', 'textAlign': 'center'}),
                    
                    html.Div([
                        html.H3("🧮 Simulaciones"),
                        html.P("Ejecutar simulaciones Monte Carlo"),
                        html.Button("Nueva Simulación", id='btn-simulations', style={'padding': '10px 20px', 'backgroundColor': '#27ae60', 'color': 'white', 'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer'})
                    ], style={'backgroundColor': 'white', 'padding': '30px', 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)', 'margin': '15px', 'textAlign': 'center'}),
                    
                    html.Div([
                        html.H3("📈 Visualizaciones"),
                        html.P("Ver gráficos y análisis"),
                        html.Button("Ver Gráficos", id='btn-visualizations', style={'padding': '10px 20px', 'backgroundColor': '#e74c3c', 'color': 'white', 'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer'})
                    ], style={'backgroundColor': 'white', 'padding': '30px', 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)', 'margin': '15px', 'textAlign': 'center'}),
                    
                    html.Div([
                        html.H3("👥 Usuarios"),
                        html.P("Gestión de usuarios del sistema"),
                        html.Button("Gestionar", id='btn-users', style={'padding': '10px 20px', 'backgroundColor': '#9b59b6', 'color': 'white', 'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer'})
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
        ])
    
    def projects_page(self):
        return html.Div([
            html.H2("📁 Gestión de Proyectos", style={'color': '#2c3e50'}),
            html.Button("+ Nuevo Proyecto", style={'padding': '10px 20px', 'backgroundColor': '#27ae60', 'color': 'white', 'border': 'none', 'borderRadius': '5px', 'marginBottom': '20px'}),
            html.Div([
                html.Div([
                    html.H4("Proyecto Alpha"),
                    html.P("Lanzamiento de producto premium"),
                    html.P("3 escenarios | Última simulación: 2024-01-15"),
                    html.Button("Ver Detalles", style={'padding': '8px 15px', 'backgroundColor': '#3498db', 'color': 'white', 'border': 'none', 'borderRadius': '3px'})
                ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px', 'marginBottom': '15px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
            ])
        ])
    
    def simulations_page(self):
        return html.Div([
            html.H2("🧮 Simulaciones Monte Carlo", style={'color': '#2c3e50'}),
            html.Div([
                html.H3("📈 Configurar Escenario"),
                html.Div([
                    html.Div([
                        html.Label("Nombre del Escenario:"),
                        dcc.Input(id='scenario-name', value='Nuevo Escenario', type='text', style={'width': '100%', 'padding': '8px', 'margin': '5px 0'})
                    ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '4%'}),
                    html.Div([
                        html.Label("Inversión Inicial ($):"),
                        dcc.Input(id='initial-investment', value=100000, type='number', style={'width': '100%', 'padding': '8px', 'margin': '5px 0'})
                    ], style={'width': '48%', 'display': 'inline-block'})
                ]),
                html.Div([
                    html.Div([
                        html.Label("Ingresos Mensuales - Media ($):"),
                        dcc.Input(id='revenue-mean', value=25000, type='number', style={'width': '100%', 'padding': '8px', 'margin': '5px 0'})
                    ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '4%'}),
                    html.Div([
                        html.Label("Ingresos - Desv. Estándar ($):"),
                        dcc.Input(id='revenue-std', value=5000, type='number', style={'width': '100%', 'padding': '8px', 'margin': '5px 0'})
                    ], style={'width': '48%', 'display': 'inline-block'})
                ], style={'marginTop': '15px'}),
                html.Button("🚀 Ejecutar Simulación", id='run-simulation', 
                           style={'marginTop': '20px', 'padding': '12px 30px', 'backgroundColor': '#e74c3c', 'color': 'white', 'border': 'none', 'borderRadius': '5px', 'fontSize': '16px', 'cursor': 'pointer'})
            ], style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '8px', 'marginBottom': '20px'}),
            html.Div(id='simulation-results')
        ])
    
    def visualizations_page(self):
        return html.Div([
            html.H2("📈 Visualizaciones", style={'color': '#2c3e50'}),
            html.P("Visualizaciones recientes de simulaciones Monte Carlo"),
            html.Div([
                html.Div("Gráfico NPV - Proyecto Alpha", style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '8px', 'margin': '10px 0', 'borderLeft': '4px solid #3498db'}),
                html.Div("Análisis de Riesgo - Proyecto Beta", style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '8px', 'margin': '10px 0', 'borderLeft': '4px solid #27ae60'})
            ])
        ])
    
    def users_page(self):
        return html.Div([
            html.H2("👥 Gestión de Usuarios", style={'color': '#2c3e50'}),
            html.P("Panel de administración de usuarios"),
            html.Button("+ Nuevo Usuario", style={'padding': '10px 20px', 'backgroundColor': '#9b59b6', 'color': 'white', 'border': 'none', 'borderRadius': '5px'})
        ])
    
    def run_server(self, debug=False, port=8050):
        self.app.run(debug=debug, port=port, host='0.0.0.0')