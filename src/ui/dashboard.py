import dash
from dash import dcc, html, Input, Output, State, dash_table
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from ..simulation.monte_carlo_engine import MonteCarloEngine
from ..models.business_scenario import BusinessScenario
from ..utils.statistics import StatisticsCalculator
from ..database.db_manager import DatabaseManager

class DecisionDashboard:
    """Dashboard interactivo para análisis de decisiones empresariales"""
    
    def __init__(self):
        self.app = dash.Dash(__name__)
        self.engine = MonteCarloEngine(n_simulations=5000)
        self.db = DatabaseManager()
        self.setup_layout()
        self.setup_callbacks()
    
    def setup_layout(self):
        """Configura el layout del dashboard"""
        
        self.app.layout = html.Div([
            html.H1("🎯 Asistente de Decisiones Empresariales - Monte Carlo", 
                   style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),
            
            # Panel de configuración
            html.Div([
                html.H3("📊 Configuración del Escenario"),
                html.Div([
                    html.Div([
                        html.Label("Nombre del Escenario:"),
                        dcc.Input(id='scenario-name', value='Lanzamiento Producto A', type='text', style={'width': '100%'})
                    ], className='input-group'),
                    
                    html.Div([
                        html.Label("Inversión Inicial ($):"),
                        dcc.Input(id='initial-investment', value=100000, type='number', style={'width': '100%'})
                    ], className='input-group'),
                    
                    html.Div([
                        html.Label("Ingresos Mensuales - Media ($):"),
                        dcc.Input(id='revenue-mean', value=25000, type='number', style={'width': '100%'})
                    ], className='input-group'),
                    
                    html.Div([
                        html.Label("Ingresos - Desv. Estándar ($):"),
                        dcc.Input(id='revenue-std', value=5000, type='number', style={'width': '100%'})
                    ], className='input-group'),
                ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '15px'}),
                
                html.Div([
                    html.Div([
                        html.Label("Costos Mensuales - Media ($):"),
                        dcc.Input(id='cost-mean', value=15000, type='number', style={'width': '100%'})
                    ], className='input-group'),
                    
                    html.Div([
                        html.Label("Costos - Desv. Estándar ($):"),
                        dcc.Input(id='cost-std', value=3000, type='number', style={'width': '100%'})
                    ], className='input-group'),
                    
                    html.Div([
                        html.Label("Tasa de Inflación:"),
                        dcc.Input(id='inflation-rate', value=0.03, type='number', step=0.01, style={'width': '100%'})
                    ], className='input-group'),
                    
                    html.Div([
                        html.Label("Volatilidad del Mercado:"),
                        dcc.Input(id='market-volatility', value=0.15, type='number', step=0.01, style={'width': '100%'})
                    ], className='input-group'),
                ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '15px', 'marginTop': '15px'}),
                
                html.Button("🚀 Ejecutar Simulación", id='run-simulation', 
                           style={'marginTop': '20px', 'padding': '10px 20px', 'fontSize': '16px'})
            ], style={'backgroundColor': '#ecf0f1', 'padding': '20px', 'borderRadius': '10px', 'marginBottom': '20px'}),
            
            # Resultados
            html.Div(id='results-container'),
            
        ], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '20px'})
    
    def setup_callbacks(self):
        """Configura los callbacks del dashboard"""
        
        @self.app.callback(
            Output('results-container', 'children'),
            Input('run-simulation', 'n_clicks'),
            [State('scenario-name', 'value'),
             State('initial-investment', 'value'),
             State('revenue-mean', 'value'),
             State('revenue-std', 'value'),
             State('cost-mean', 'value'),
             State('cost-std', 'value'),
             State('inflation-rate', 'value'),
             State('market-volatility', 'value')]
        )
        def run_simulation(n_clicks, name, investment, rev_mean, rev_std, 
                          cost_mean, cost_std, inflation, volatility):
            
            if not n_clicks:
                return html.Div("👆 Configure los parámetros y ejecute la simulación", 
                               style={'textAlign': 'center', 'color': '#7f8c8d', 'fontSize': '18px'})
            
            # Crear escenario
            scenario = BusinessScenario(
                name=name,
                initial_investment=investment,
                revenue_mean=rev_mean,
                revenue_std=rev_std,
                cost_mean=cost_mean,
                cost_std=cost_std,
                inflation_rate=inflation,
                market_volatility=volatility
            )
            
            # Ejecutar simulación
            result = self.engine.simulate_scenario(scenario)
            metrics = StatisticsCalculator.calculate_risk_metrics(result)
            
            # Guardar en base de datos
            try:
                self.db.save_simulation(scenario, result, metrics)
            except Exception as e:
                print(f"Error guardando simulación: {e}")
            
            return self.create_results_layout(result, metrics)
    
    def create_results_layout(self, result, metrics):
        """Crea el layout de resultados"""
        
        return html.Div([
            # Métricas principales
            html.H3("📈 Resultados de la Simulación"),
            html.Div([
                self.create_metric_card("NPV Promedio", f"${metrics['media_npv']:,.0f}", 
                                       "green" if metrics['media_npv'] > 0 else "red"),
                self.create_metric_card("Probabilidad de Éxito", f"{metrics['probabilidad_exito']:.1f}%", 
                                       "green" if metrics['probabilidad_exito'] > 50 else "orange"),
                self.create_metric_card("ROI Promedio", f"{metrics['roi_medio']:.1f}%", 
                                       "green" if metrics['roi_medio'] > 0 else "red"),
                self.create_metric_card("Break-even Promedio", f"{metrics['break_even_medio']:.1f} meses", "blue"),
            ], style={'display': 'flex', 'gap': '15px', 'marginBottom': '20px'}),
            
            # Gráficos
            html.Div([
                html.Div([
                    dcc.Graph(figure=self.create_npv_histogram(result))
                ], style={'width': '50%'}),
                html.Div([
                    dcc.Graph(figure=self.create_risk_metrics_chart(metrics))
                ], style={'width': '50%'}),
            ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px'}),
            
            # Tabla de estadísticas detalladas
            html.H4("📊 Estadísticas Detalladas"),
            self.create_statistics_table(metrics)
        ])
    
    def create_metric_card(self, title, value, color):
        """Crea una tarjeta de métrica"""
        return html.Div([
            html.H4(title, style={'margin': '0', 'color': '#2c3e50'}),
            html.H2(value, style={'margin': '10px 0', 'color': color})
        ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px', 
                 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center', 'flex': '1'})
    
    def create_npv_histogram(self, result):
        """Crea histograma de distribución NPV"""
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=result.net_present_values,
            nbinsx=50,
            name='Distribución NPV',
            marker_color='rgba(55, 128, 191, 0.7)'
        ))
        
        # Líneas de percentiles
        fig.add_vline(x=result.percentile_5, line_dash="dash", line_color="red", 
                     annotation_text=f"P5: ${result.percentile_5:,.0f}")
        fig.add_vline(x=result.percentile_95, line_dash="dash", line_color="green", 
                     annotation_text=f"P95: ${result.percentile_95:,.0f}")
        
        fig.update_layout(
            title="Distribución de Valor Presente Neto (NPV)",
            xaxis_title="NPV ($)",
            yaxis_title="Frecuencia",
            showlegend=False
        )
        return fig
    
    def create_risk_metrics_chart(self, metrics):
        """Crea gráfico de métricas de riesgo"""
        categories = ['Prob. Éxito', 'ROI > 0%', 'Break-even 6m', 'Break-even 12m']
        values = [
            metrics['probabilidad_exito'],
            metrics['prob_roi_positivo'],
            metrics['prob_break_even_6m'],
            metrics['prob_break_even_12m']
        ]
        
        fig = go.Figure(data=[
            go.Bar(x=categories, y=values, marker_color=['green', 'blue', 'orange', 'purple'])
        ])
        
        fig.update_layout(
            title="Métricas de Probabilidad (%)",
            yaxis_title="Probabilidad (%)",
            yaxis=dict(range=[0, 100])
        )
        return fig
    
    def create_statistics_table(self, metrics):
        """Crea tabla de estadísticas"""
        data = [
            {"Métrica": "NPV Promedio", "Valor": f"${metrics['media_npv']:,.0f}"},
            {"Métrica": "Desviación Estándar", "Valor": f"${metrics['desviacion_std']:,.0f}"},
            {"Métrica": "VaR 95%", "Valor": f"${metrics['var_95']:,.0f}"},
            {"Métrica": "CVaR 95%", "Valor": f"${metrics['cvar_95']:,.0f}"},
            {"Métrica": "Coef. Variación", "Valor": f"{metrics['coeficiente_variacion']:.2f}"},
            {"Métrica": "Asimetría", "Valor": f"{metrics['asimetria']:.2f}"},
            {"Métrica": "Curtosis", "Valor": f"{metrics['curtosis']:.2f}"},
        ]
        
        return dash_table.DataTable(
            data=data,
            columns=[{"name": i, "id": i} for i in data[0].keys()],
            style_cell={'textAlign': 'left', 'padding': '10px'},
            style_header={'backgroundColor': '#3498db', 'color': 'white', 'fontWeight': 'bold'},
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#f8f9fa'
                }
            ]
        )
    
    def run_server(self, debug=True, port=8050):
        """Ejecuta el servidor del dashboard"""
        self.app.run_server(debug=debug, port=port, host='0.0.0.0')