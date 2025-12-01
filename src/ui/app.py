import dash
from dash import dcc, html, Input, Output, State, dash_table, callback_context
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from ..simulation.monte_carlo_engine import MonteCarloEngine
from ..models.business_scenario import BusinessScenario
from ..utils.statistics import StatisticsCalculator
from ..auth.auth_manager import AuthManager
from ..database.models import User, Project, SimulationRecord
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

class MainApp:
    def __init__(self):
        self.app = dash.Dash(__name__)
        self.engine = MonteCarloEngine(n_simulations=5000)
        try:
            self.auth = AuthManager()
            self.db_engine = create_engine(os.getenv('DATABASE_URL'))
            self.Session = sessionmaker(bind=self.db_engine)
            self.auth_enabled = True
        except Exception as e:
            print(f"⚠️ Sistema sin autenticación: {e}")
            self.auth_enabled = False
        
        self.current_user = None
        self.setup_layout()
        self.setup_callbacks()
    
    def setup_layout(self):
        self.app.layout = html.Div([
            dcc.Store(id='session-store'),
            dcc.Store(id='current-page', data='login'),
            html.Div(id='main-content')
        ])
    
    def login_layout(self):
        return html.Div([
            html.Div([
                html.H1("🎯 Monte Carlo Decision Engine", style={'textAlign': 'center', 'marginBottom': 30}),
                html.Div([
                    html.H3("Iniciar Sesión"),
                    dcc.Input(id='username', placeholder='Usuario', type='text', style={'width': '100%', 'margin': '10px 0'}),
                    dcc.Input(id='password', placeholder='Contraseña', type='password', style={'width': '100%', 'margin': '10px 0'}),
                    html.Button('Iniciar Sesión', id='login-btn', style={'width': '100%', 'padding': '10px'}),
                    html.Div(id='login-message', style={'marginTop': '10px'})
                ], style={'maxWidth': '400px', 'margin': '0 auto', 'padding': '20px', 'backgroundColor': '#f8f9fa'})
            ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'minHeight': '100vh'})
        ])
    
    def main_layout(self):
        return html.Div([
            # Header
            html.Div([
                html.H1("🎯 Monte Carlo Engine", style={'display': 'inline-block', 'margin': 0}),
                html.Div([
                    dcc.Dropdown(
                        id='menu-dropdown',
                        options=[
                            {'label': '📊 Dashboard', 'value': 'dashboard'},
                            {'label': '📁 Proyectos', 'value': 'projects'},
                            {'label': '🔬 Simulaciones', 'value': 'simulations'},
                            {'label': '📈 Visualizaciones', 'value': 'visualizations'},
                            {'label': '👥 Usuarios', 'value': 'users'},
                            {'label': '🚪 Salir', 'value': 'logout'}
                        ],
                        value='dashboard',
                        style={'width': '200px'}
                    )
                ], style={'float': 'right'})
            ], style={'padding': '20px', 'backgroundColor': '#34495e', 'color': 'white'}),
            
            html.Div(id='page-content')
        ])
    
    def dashboard_content(self):
        return html.Div([
            html.H2("📊 Dashboard de Simulación"),
            html.Div([
                html.Label("Nombre del Proyecto:"),
                dcc.Input(id='project-name', value='Nuevo Proyecto', style={'width': '100%'})
            ], style={'margin': '10px 0'}),
            html.Div([
                html.Label("Escenario:"),
                dcc.Input(id='scenario-name', value='Escenario Base', style={'width': '100%'})
            ], style={'margin': '10px 0'}),
            html.Div([
                html.Div([
                    html.Label("Inversión ($):"),
                    dcc.Input(id='investment', value=100000, type='number', style={'width': '100%'})
                ], style={'width': '48%', 'display': 'inline-block'}),
                html.Div([
                    html.Label("Ingresos ($):"),
                    dcc.Input(id='revenue', value=25000, type='number', style={'width': '100%'})
                ], style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%'})
            ]),
            html.Button("🚀 Ejecutar Simulación", id='run-sim', style={'margin': '20px 0'}),
            html.Div(id='sim-results')
        ], style={'padding': '20px'})
    
    def projects_content(self):
        return html.Div([
            html.H2("📁 Gestión de Proyectos"),
            html.Button("➕ Nuevo Proyecto", id='new-project-btn', style={'margin': '10px 0'}),
            html.Div(id='projects-list')
        ], style={'padding': '20px'})
    
    def simulations_content(self):
        return html.Div([
            html.H2("🔬 Simulaciones"),
            dcc.Input(id='search-sim', placeholder='Buscar simulaciones...', style={'width': '300px', 'margin': '10px 0'}),
            html.Div(id='simulations-list')
        ], style={'padding': '20px'})
    
    def visualizations_content(self):
        return html.Div([
            html.H2("📈 Visualizaciones Recientes"),
            html.Div(id='viz-gallery')
        ], style={'padding': '20px'})
    
    def users_content(self):
        return html.Div([
            html.H2("👥 Gestión de Usuarios"),
            html.Div([
                html.H4("Crear Usuario"),
                dcc.Input(id='new-username', placeholder='Usuario', style={'margin': '5px'}),
                dcc.Input(id='new-email', placeholder='Email', style={'margin': '5px'}),
                dcc.Input(id='new-password', placeholder='Contraseña', type='password', style={'margin': '5px'}),
                html.Button("Crear", id='create-user-btn', style={'margin': '5px'})
            ], style={'backgroundColor': '#f8f9fa', 'padding': '15px', 'margin': '10px 0'}),
            html.Div(id='users-table')
        ], style={'padding': '20px'})
    
    def setup_callbacks(self):
        @self.app.callback(
            Output('main-content', 'children'),
            [Input('session-store', 'data'), Input('current-page', 'data')]
        )
        def display_page(session_data, current_page):
            if not self.auth_enabled or session_data:
                return self.main_layout()
            return self.login_layout()
        
        @self.app.callback(
            [Output('session-store', 'data'), Output('login-message', 'children')],
            Input('login-btn', 'n_clicks'),
            [State('username', 'value'), State('password', 'value')]
        )
        def login(n_clicks, username, password):
            if n_clicks and username and password:
                if self.auth_enabled:
                    result = self.auth.login(username, password)
                    if result['success']:
                        self.current_user = result['user']
                        return result, ""
                    return None, result['message']
                else:
                    return {'user': {'username': 'demo'}}, ""
            return None, ""
        
        @self.app.callback(
            Output('page-content', 'children'),
            Input('menu-dropdown', 'value')
        )
        def display_content(page):
            if page == 'dashboard':
                return self.dashboard_content()
            elif page == 'projects':
                return self.projects_content()
            elif page == 'simulations':
                return self.simulations_content()
            elif page == 'visualizations':
                return self.visualizations_content()
            elif page == 'users':
                return self.users_content()
            return self.dashboard_content()
        
        @self.app.callback(
            Output('sim-results', 'children'),
            Input('run-sim', 'n_clicks'),
            [State('project-name', 'value'), State('scenario-name', 'value'),
             State('investment', 'value'), State('revenue', 'value')]
        )
        def run_simulation(n_clicks, project_name, scenario_name, investment, revenue):
            if not n_clicks:
                return ""
            
            scenario = BusinessScenario(
                name=scenario_name,
                initial_investment=investment,
                revenue_mean=revenue,
                revenue_std=revenue*0.2,
                cost_mean=revenue*0.6,
                cost_std=revenue*0.1,
                inflation_rate=0.03,
                market_volatility=0.15
            )
            
            result = self.engine.simulate_scenario(scenario)
            metrics = StatisticsCalculator.calculate_risk_metrics(result)
            
            return html.Div([
                html.H4("Resultados:"),
                html.P(f"NPV Promedio: ${metrics['media_npv']:,.0f}"),
                html.P(f"Probabilidad Éxito: {metrics['probabilidad_exito']:.1f}%"),
                html.P(f"ROI: {metrics['roi_medio']:.1f}%")
            ])
        
        @self.app.callback(
            Output('users-table', 'children'),
            Input('create-user-btn', 'n_clicks'),
            [State('new-username', 'value'), State('new-email', 'value'), State('new-password', 'value')]
        )
        def manage_users(n_clicks, username, email, password):
            if n_clicks and username and email and password and self.auth_enabled:
                self.auth.create_user(username, email, password)
            
            if self.auth_enabled:
                users = self.auth.get_users()
                return dash_table.DataTable(
                    data=users,
                    columns=[{'name': 'ID', 'id': 'id'}, {'name': 'Usuario', 'id': 'username'}, 
                            {'name': 'Email', 'id': 'email'}, {'name': 'Activo', 'id': 'is_active'}]
                )
            return html.P("Gestión de usuarios no disponible")
    
    def run_server(self, debug=True, port=8050):
        self.app.run(debug=debug, port=port, host='0.0.0.0')