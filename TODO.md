# TODO: Implement Full CRUD Modules and Sidebar Navigation

## Database Schema Updates
- [ ] Add simulations table (id, project_id, name, params JSON, results JSON, created_at)
- [ ] Add visualizations table (id, simulation_id, type, figure JSON, created_at)
- [ ] Update users table if needed for additional fields
- [ ] Add CRUD methods in AuthManager: create_project, delete_project, search_projects, create_simulation, view_simulations, search_simulations, create_visualization, view_visualizations, download_visualization, create_user, edit_user, delete_user, search_users

## UI Modules Implementation
- [ ] ProjectsManager: Add create/edit/delete/search forms and callbacks
- [ ] SimulationsManager: New class with table, create form, run simulation
- [ ] VisualizationsManager: New class with table, create/download functionality
- [ ] UsersManager: New class with admin-only CRUD and search

## App Integration
- [ ] Enhance login: Add session persistence with dcc.Store
- [ ] Update navigation callbacks: Load content from managers with user_id
- [ ] Add global callbacks for CRUD actions
- [ ] Ensure sidebar shows/hides based on user role

## Models Integration
- [ ] BusinessScenario: Add DB save/load methods for simulations

## Testing and Validation
- [ ] Test login with admin/admin123
- [ ] Run app and verify all sidebar modules work
- [ ] Test CRUD operations in each module
- [ ] Add error handling and confirmations
