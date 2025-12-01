from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import hashlib

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    projects = relationship("Project", back_populates="owner")
    
    def set_password(self, password):
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    def check_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="projects")
    simulations = relationship("SimulationRecord", back_populates="project")

class SimulationRecord(Base):
    __tablename__ = 'simulations'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    scenario_name = Column(String(255), nullable=False)
    initial_investment = Column(Float, nullable=False)
    revenue_mean = Column(Float, nullable=False)
    revenue_std = Column(Float, nullable=False)
    cost_mean = Column(Float, nullable=False)
    cost_std = Column(Float, nullable=False)
    inflation_rate = Column(Float, nullable=False)
    market_volatility = Column(Float, nullable=False)
    mean_npv = Column(Float, nullable=False)
    success_probability = Column(Float, nullable=False)
    roi_mean = Column(Float, nullable=False)
    var_95 = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    metrics = Column(JSON)
    
    project = relationship("Project", back_populates="simulations")

class Visualization(Base):
    __tablename__ = 'visualizations'
    
    id = Column(Integer, primary_key=True)
    simulation_id = Column(Integer, ForeignKey('simulations.id'))
    name = Column(String(255), nullable=False)
    file_path = Column(String(500))
    chart_type = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)