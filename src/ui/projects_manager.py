from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc
import pandas as pd

class ProjectsManager:
    def __init__(self, auth_manager):
        self.auth = auth_manager

    def projects_content(self, user_id):
        """Contenido de gestión de proyectos"""
        projects = self.auth.get_user_projects(user_id)

        return html.Div([
            html.H2("📁 Mis Proyectos"),
            # Barra de búsqueda
            html.Div([
                dcc.Input(
                    id='project-search-input',
                    type='text',
                    placeholder='Buscar proyectos...',
                    style={'width': '300px', 'marginRight': '10px'}
                ),
                html.Button("🔍 Buscar", id='project-search-btn',
                           style={'padding': '8px 15px', 'backgroundColor': '#3498db', 'color': 'white', 'border': 'none'})
            ], style={'marginBottom': '20px'}),

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
                    {'name': 'Simulaciones', 'id': 'simulation_count'},
                    {'name': 'Creado', 'id': 'created_at'},
                    {'name': 'Acciones', 'id': 'actions', 'presentation': 'markdown'}
                ],
                style_cell={'textAlign': 'left', 'padding': '10px'},
                style_header={'backgroundColor': '#3498db', 'color': 'white'},
                row_selectable='single',
                markdown_options={"html": True}
            ),

            # Modal para nuevo proyecto
            dbc.Modal([
                dbc.ModalHeader("Nuevo Proyecto"),
                dbc.ModalBody([
                    dbc.Input(id='project-name-input', type='text', placeholder='Nombre del proyecto'),
                    dbc.Textarea(id='project-description-input', placeholder='Descripción (opcional)',
                               style={'marginTop': '10px'}),
                    html.Div(id='project-error', style={'color': 'red', 'marginTop': '10px'})
                ]),
                dbc.ModalFooter([
                    dbc.Button("Crear", id='create-project-btn', color='primary'),
                    dbc.Button("Cancelar", id='cancel-project-btn')
                ])
            ], id='new-project-modal'),

            # Botones de acción
            html.Div([
                html.Button("✏️ Editar", id='edit-project-btn',
                           style={'marginRight': '10px', 'padding': '8px 15px',
                                 'backgroundColor': '#f39c12', 'color': 'white', 'border': 'none'}),
                html.Button("🗑️ Eliminar", id='delete-project-btn',
                           style={'padding': '8px 15px', 'backgroundColor': '#e74c3c', 'color': 'white', 'border': 'none'})
            ], style={'marginTop': '20px'})
        ])

    def users_content(self):
        """Contenido de gestión de usuarios (solo admin)"""
        users = self.auth.get_all_users()

        return html.Div([
            html.H2("👥 Gestión de Usuarios"),
            # Barra de búsqueda
            html.Div([
                dcc.Input(
                    id='user-search-input',
                    type='text',
                    placeholder='Buscar usuarios...',
                    style={'width': '300px', 'marginRight': '10px'}
                ),
                html.Button("🔍 Buscar", id='user-search-btn',
                           style={'padding': '8px 15px', 'backgroundColor': '#3498db', 'color': 'white', 'border': 'none'})
            ], style={'marginBottom': '20px'}),

            html.Button("+ Nuevo Usuario", id='new-user-btn',
                       style={'marginBottom': '20px', 'padding': '10px 20px',
                             'backgroundColor': '#e74c3c', 'color': 'white', 'border': 'none'}),

            # Tabla de usuarios
            dash_table.DataTable(
                id='users-table',
                data=users,
                columns=[
                    {'name': 'ID', 'id': 'id'},
                    {'name': 'Usuario', 'id': 'username'},
                    {'name': 'Email', 'id': 'email'},
                    {'name': 'Rol', 'id': 'role'},
                    {'name': 'Creado', 'id': 'created_at'},
                    {'name': 'Acciones', 'id': 'actions', 'presentation': 'markdown'}
                ],
                style_cell={'textAlign': 'left', 'padding': '10px'},
                style_header={'backgroundColor': '#e74c3c', 'color': 'white'},
                row_selectable='single',
                markdown_options={"html": True}
            ),

            # Modal para nuevo usuario
            dbc.Modal([
                dbc.ModalHeader("Nuevo Usuario"),
                dbc.ModalBody([
                    dbc.Input(id='user-username-input', type='text', placeholder='Nombre de usuario'),
                    dbc.Input(id='user-email-input', type='email', placeholder='Email',
                            style={'marginTop': '10px'}),
                    dbc.Input(id='user-password-input', type='password', placeholder='Contraseña',
                            style={'marginTop': '10px'}),
                    dbc.Select(
                        id='user-role-select',
                        options=[
                            {'label': 'Usuario', 'value': 'user'},
                            {'label': 'Administrador', 'value': 'admin'}
                        ],
                        value='user',
                        style={'marginTop': '10px'}
                    ),
                    html.Div(id='user-error', style={'color': 'red', 'marginTop': '10px'})
                ]),
                dbc.ModalFooter([
                    dbc.Button("Crear", id='create-user-btn', color='primary'),
                    dbc.Button("Cancelar", id='cancel-user-btn')
                ])
            ], id='new-user-modal'),

            # Modal para editar usuario
            dbc.Modal([
                dbc.ModalHeader("Editar Usuario"),
                dbc.ModalBody([
                    dbc.Input(id='edit-user-username-input', type='text', placeholder='Nombre de usuario'),
                    dbc.Input(id='edit-user-email-input', type='email', placeholder='Email',
                            style={'marginTop': '10px'}),
                    dbc.Select(
                        id='edit-user-role-select',
                        options=[
                            {'label': 'Usuario', 'value': 'user'},
                            {'label': 'Administrador', 'value': 'admin'}
                        ],
                        style={'marginTop': '10px'}
                    ),
                    html.Div(id='edit-user-error', style={'color': 'red', 'marginTop': '10px'})
                ]),
                dbc.ModalFooter([
                    dbc.Button("Guardar", id='save-user-btn', color='primary'),
                    dbc.Button("Cancelar", id='cancel-edit-user-btn')
                ])
            ], id='edit-user-modal'),

            # Store para usuario seleccionado
            dcc.Store(id='selected-user-id')
        ])

    def simulations_content(self, user_id):
        """Contenido de gestión de simulaciones"""
        # Obtener todas las simulaciones del usuario
        simulations = self.auth.search_simulations(user_id, '')

        return html.Div([
            html.H2("🔬 Mis Simulaciones"),

            # Barra de búsqueda
            html.Div([
                dcc.Input(
                    id='simulation-search-input',
                    type='text',
                    placeholder='Buscar simulaciones...',
                    style={'width': '300px', 'marginRight': '10px'}
                ),
                html.Button("🔍 Buscar", id='simulation-search-btn',
                           style={'padding': '8px 15px', 'backgroundColor': '#3498db', 'color': 'white', 'border': 'none'})
            ], style={'marginBottom': '20px'}),

            html.Button("+ Nueva Simulación", id='new-simulation-btn',
                       style={'marginBottom': '20px', 'padding': '10px 20px',
                             'backgroundColor': '#9b59b6', 'color': 'white', 'border': 'none'}),

            # Tabla de simulaciones
            dash_table.DataTable(
                id='simulations-table',
                data=simulations,
                columns=[
                    {'name': 'ID', 'id': 'id'},
                    {'name': 'Nombre', 'id': 'name'},
                    {'name': 'Proyecto', 'id': 'project_name'},
                    {'name': 'Visualizaciones', 'id': 'visualization_count'},
                    {'name': 'Creado', 'id': 'created_at'},
                    {'name': 'Acciones', 'id': 'actions', 'presentation': 'markdown'}
                ],
                style_cell={'textAlign': 'left', 'padding': '10px'},
                style_header={'backgroundColor': '#9b59b6', 'color': 'white'},
                row_selectable='single',
                markdown_options={"html": True}
            ),

            # Modal para nueva simulación
            dbc.Modal([
                dbc.ModalHeader("Nueva Simulación"),
                dbc.ModalBody([
                    dbc.Select(id='simulation-project-select', placeholder='Seleccionar proyecto'),
                    dbc.Input(id='simulation-name-input', type='text', placeholder='Nombre de la simulación',
                            style={'marginTop': '10px'}),
                    html.Div(id='simulation-error', style={'color': 'red', 'marginTop': '10px'})
                ]),
                dbc.ModalFooter([
                    dbc.Button("Crear", id='create-simulation-btn', color='primary'),
                    dbc.Button("Cancelar", id='cancel-simulation-btn')
                ])
            ], id='new-simulation-modal'),

            # Store para simulación seleccionada
            dcc.Store(id='selected-simulation-id')
        ])

    def visualizations_content(self, user_id):
        """Contenido de gestión de visualizaciones"""
        # Por ahora vacío, se implementará después
        return html.Div([
            html.H2("📊 Mis Visualizaciones"),
            html.P("Funcionalidad próximamente disponible")
        ])
