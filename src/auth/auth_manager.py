import hashlib
import secrets
from typing import Optional, Dict
from ..database.neon_db import NeonDB

class AuthManager:
    def __init__(self):
        try:
            self.db = NeonDB()
            self.create_auth_tables()
            self.sessions = {}
        except Exception as e:
            print(f"Error inicializando AuthManager: {e}")
            self.db = None
            self.sessions = {}
    
    def create_auth_tables(self):
        """Crea tablas de usuarios y sesiones"""
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cur:
                    # Crear tabla users
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            id SERIAL PRIMARY KEY,
                            username VARCHAR(50) UNIQUE NOT NULL,
                            email VARCHAR(100) UNIQUE NOT NULL,
                            password_hash VARCHAR(255) NOT NULL,
                            role VARCHAR(20) DEFAULT 'user',
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
                    
                    # Crear tabla projects
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS projects (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(255) NOT NULL,
                            description TEXT,
                            user_id INTEGER REFERENCES users(id),
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
                    
                    conn.commit()
                    
                    # Insertar usuario admin
                    try:
                        cur.execute("""
                            INSERT INTO users (username, email, password_hash, role)
                            VALUES ('admin', 'admin@montecarlo.com', %s, 'admin')
                            ON CONFLICT (username) DO NOTHING
                        """, (self.hash_password('admin123'),))
                        conn.commit()
                    except Exception as e:
                        print(f"Usuario admin ya existe o error: {e}")
                        
        except Exception as e:
            print(f"Error creando tablas de autenticación: {e}")
    
    def hash_password(self, password: str) -> str:
        """Hash de contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self, username: str, password: str) -> Optional[Dict]:
        """Autenticar usuario"""
        if not self.db:
            return None
            
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT id, username, email, role FROM users 
                        WHERE username = %s AND password_hash = %s
                    """, (username, self.hash_password(password)))
                    
                    user = cur.fetchone()
                    if user:
                        session_id = secrets.token_hex(16)
                        user_data = {
                            'id': user[0],
                            'username': user[1],
                            'email': user[2],
                            'role': user[3]
                        }
                        self.sessions[session_id] = user_data
                        return {'session_id': session_id, 'user': user_data}
                    return None
        except Exception as e:
            print(f"Error en login: {e}")
            return None
    
    def get_user_projects(self, user_id: int):
        """Obtener proyectos del usuario"""
        with self.db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT p.id, p.name, p.description, p.created_at,
                           COUNT(sim.id) as simulation_count
                    FROM projects p
                    LEFT JOIN simulations sim ON p.id = sim.project_id
                    WHERE p.user_id = %s
                    GROUP BY p.id, p.name, p.description, p.created_at
                    ORDER BY p.created_at DESC
                """, (user_id,))

                columns = [desc[0] for desc in cur.description]
                return [dict(zip(columns, row)) for row in cur.fetchall()]

    def create_project(self, user_id: int, name: str, description: str = ""):
        """Crear nuevo proyecto"""
        with self.db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO projects (user_id, name, description)
                    VALUES (%s, %s, %s) RETURNING id
                """, (user_id, name, description))
                project_id = cur.fetchone()[0]
                conn.commit()
                return project_id

    def delete_project(self, project_id: int, user_id: int):
        """Eliminar proyecto (solo del propietario)"""
        with self.db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE FROM projects WHERE id = %s AND user_id = %s
                """, (project_id, user_id))
                conn.commit()
                return cur.rowcount > 0

    def search_projects(self, user_id: int, query: str):
        """Buscar proyectos por nombre o descripción"""
        with self.db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT p.id, p.name, p.description, p.created_at,
                           COUNT(sim.id) as simulation_count
                    FROM projects p
                    LEFT JOIN simulations sim ON p.id = sim.project_id
                    WHERE p.user_id = %s AND (p.name ILIKE %s OR p.description ILIKE %s)
                    GROUP BY p.id, p.name, p.description, p.created_at
                    ORDER BY p.created_at DESC
                """, (user_id, f'%{query}%', f'%{query}%'))

                columns = [desc[0] for desc in cur.description]
                return [dict(zip(columns, row)) for row in cur.fetchall()]

    def get_project_simulations(self, project_id: int, user_id: int):
        """Obtener simulaciones de un proyecto"""
        with self.db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT s.id, s.name, s.params, s.results, s.created_at,
                           COUNT(v.id) as visualization_count
                    FROM simulations s
                    LEFT JOIN visualizations v ON s.id = v.simulation_id
                    JOIN projects p ON s.project_id = p.id
                    WHERE s.project_id = %s AND p.user_id = %s
                    GROUP BY s.id, s.name, s.params, s.results, s.created_at
                    ORDER BY s.created_at DESC
                """, (project_id, user_id))

                columns = [desc[0] for desc in cur.description]
                return [dict(zip(columns, row)) for row in cur.fetchall()]

    def create_simulation(self, project_id: int, name: str, params: dict, results: dict = None):
        """Crear nueva simulación"""
        with self.db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO simulations (project_id, name, params, results)
                    VALUES (%s, %s, %s, %s) RETURNING id
                """, (project_id, name, params, results))
                simulation_id = cur.fetchone()[0]
                conn.commit()
                return simulation_id

    def search_simulations(self, user_id: int, query: str):
        """Buscar simulaciones por nombre"""
        with self.db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT s.id, s.name, s.params, s.results, s.created_at,
                           p.name as project_name, COUNT(v.id) as visualization_count
                    FROM simulations s
                    JOIN projects p ON s.project_id = p.id
                    LEFT JOIN visualizations v ON s.id = v.simulation_id
                    WHERE p.user_id = %s AND s.name ILIKE %s
                    GROUP BY s.id, s.name, s.params, s.results, s.created_at, p.name
                    ORDER BY s.created_at DESC
                """, (user_id, f'%{query}%'))

                columns = [desc[0] for desc in cur.description]
                return [dict(zip(columns, row)) for row in cur.fetchall()]

    def get_simulation_visualizations(self, simulation_id: int, user_id: int):
        """Obtener visualizaciones de una simulación"""
        with self.db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT v.id, v.name, v.type, v.figure, v.created_at
                    FROM visualizations v
                    JOIN simulations s ON v.simulation_id = s.id
                    JOIN projects p ON s.project_id = p.id
                    WHERE v.simulation_id = %s AND p.user_id = %s
                    ORDER BY v.created_at DESC
                """, (simulation_id, user_id))

                columns = [desc[0] for desc in cur.description]
                return [dict(zip(columns, row)) for row in cur.fetchall()]

    def create_visualization(self, simulation_id: int, name: str, viz_type: str, figure: dict):
        """Crear nueva visualización"""
        with self.db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO visualizations (simulation_id, name, type, figure)
                    VALUES (%s, %s, %s, %s) RETURNING id
                """, (simulation_id, name, viz_type, figure))
                viz_id = cur.fetchone()[0]
                conn.commit()
                return viz_id

    def get_all_users(self):
        """Obtener todos los usuarios (solo admin)"""
        with self.db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, username, email, role, created_at
                    FROM users ORDER BY created_at DESC
                """)

                columns = [desc[0] for desc in cur.description]
                return [dict(zip(columns, row)) for row in cur.fetchall()]

    def create_user(self, username: str, email: str, password: str, role: str = 'user'):
        """Crear nuevo usuario"""
        with self.db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO users (username, email, password_hash, role)
                    VALUES (%s, %s, %s, %s) RETURNING id
                """, (username, email, self.hash_password(password), role))
                user_id = cur.fetchone()[0]
                conn.commit()
                return user_id

    def update_user(self, user_id: int, username: str = None, email: str = None, role: str = None):
        """Actualizar usuario"""
        with self.db.get_connection() as conn:
            with conn.cursor() as cur:
                updates = []
                params = []
                if username:
                    updates.append("username = %s")
                    params.append(username)
                if email:
                    updates.append("email = %s")
                    params.append(email)
                if role:
                    updates.append("role = %s")
                    params.append(role)

                if updates:
                    params.append(user_id)
                    cur.execute(f"""
                        UPDATE users SET {', '.join(updates)} WHERE id = %s
                    """, params)
                    conn.commit()
                    return cur.rowcount > 0
                return False

    def delete_user(self, user_id: int):
        """Eliminar usuario"""
        with self.db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
                conn.commit()
                return cur.rowcount > 0

    def search_users(self, query: str):
        """Buscar usuarios por username o email"""
        with self.db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, username, email, role, created_at
                    FROM users
                    WHERE username ILIKE %s OR email ILIKE %s
                    ORDER BY created_at DESC
                """, (f'%{query}%', f'%{query}%'))

                columns = [desc[0] for desc in cur.description]
                return [dict(zip(columns, row)) for row in cur.fetchall()]
