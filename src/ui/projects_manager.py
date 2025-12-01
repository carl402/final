from dash import html, dash_table
import pandas as pd

class ProjectsManager:
    def __init__(self, auth_manager):
        self.auth = auth_manager
    
    def projects_content(self, user_id):
        """Contenido de gestión de proyectos"""
        projects = self.auth.get_user_projects(user_id)
        
        return html.Div([
            html.H2("📁 Mis Proyectos"),
            html.Button("+ Nuevo Proyecto", id='new-project-btn', 
                       style={'marginBottom': '20px', 'padding': '10px 20px', 
                             'backgroundColor': '#27ae60', 'color': 'white', 'border': 'none'}),
            
            # Tabla de proyectos
            dash_table.DataTable(
                id='projects-table',
                data=projects,
                columns=[
                    {'name': 'ID', 'id': 'id'},
                    {'name': 'Nombre', 'id': 'name'},
                    {'name': 'Descripción', 'id': 'description'},
                    {'name': 'Escenarios', 'id': 'scenario_count'},
                    {'name': 'Creado', 'id': 'created_at'}
                ],
                style_cell={'textAlign': 'left', 'padding': '10px'},
                style_header={'backgroundColor': '#3498db', 'color': 'white'},
                row_selectable='single'
            )
        ])
    
    def users_content(self):
        """Contenido de gestión de usuarios (solo admin)"""
        return html.Div([
            html.H2("👥 Gestión de Usuarios"),
            html.P("Funcionalidad disponible solo para administradores"),
            html.Button("+ Nuevo Usuario", id='new-user-btn',
                       style={'marginBottom': '20px', 'padding': '10px 20px',
                             'backgroundColor': '#e74c3c', 'color': 'white', 'border': 'none'})
        ])