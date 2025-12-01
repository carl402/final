import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..database.models import Base, User
from dotenv import load_dotenv

load_dotenv()

class AuthManager:
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')
        if not self.database_url:
            raise Exception("DATABASE_URL no encontrada")
        self.engine = create_engine(self.database_url)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
        self._create_default_user()
    
    def _create_default_user(self):
        session = self.Session()
        try:
            if not session.query(User).filter_by(username='admin').first():
                admin = User(username='admin', email='admin@sistema.com')
                admin.set_password('admin123')
                session.add(admin)
                session.commit()
        finally:
            session.close()
    
    def login(self, username, password):
        session = self.Session()
        try:
            user = session.query(User).filter_by(username=username, is_active=True).first()
            if user and user.check_password(password):
                return {'success': True, 'user': {'id': user.id, 'username': user.username, 'email': user.email}}
            return {'success': False, 'message': 'Credenciales inválidas'}
        finally:
            session.close()
    
    def create_user(self, username, email, password):
        session = self.Session()
        try:
            if session.query(User).filter_by(username=username).first():
                return {'success': False, 'message': 'Usuario ya existe'}
            
            user = User(username=username, email=email)
            user.set_password(password)
            session.add(user)
            session.commit()
            return {'success': True, 'message': 'Usuario creado'}
        finally:
            session.close()
    
    def get_users(self):
        session = self.Session()
        try:
            users = session.query(User).all()
            return [{'id': u.id, 'username': u.username, 'email': u.email, 'is_active': u.is_active} for u in users]
        finally:
            session.close()
    
    def update_user(self, user_id, **kwargs):
        session = self.Session()
        try:
            user = session.query(User).get(user_id)
            if user:
                for key, value in kwargs.items():
                    if key == 'password':
                        user.set_password(value)
                    else:
                        setattr(user, key, value)
                session.commit()
                return {'success': True}
            return {'success': False, 'message': 'Usuario no encontrado'}
        finally:
            session.close()