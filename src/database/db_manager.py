import os
import psycopg2
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class SimulationRecord(Base):
    __tablename__ = 'simulations'
    
    id = Column(Integer, primary_key=True)
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

class DatabaseManager:
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')
        if not self.database_url:
            raise Exception("DATABASE_URL no encontrada en variables de entorno")
        self.engine = create_engine(self.database_url)
        self.Session = sessionmaker(bind=self.engine)
        self.create_tables()
    
    def create_tables(self):
        Base.metadata.create_all(self.engine)
    
    def save_simulation(self, scenario, result, metrics):
        session = self.Session()
        try:
            record = SimulationRecord(
                scenario_name=scenario.name,
                initial_investment=scenario.initial_investment,
                revenue_mean=scenario.revenue_mean,
                revenue_std=scenario.revenue_std,
                cost_mean=scenario.cost_mean,
                cost_std=scenario.cost_std,
                inflation_rate=scenario.inflation_rate,
                market_volatility=scenario.market_volatility,
                mean_npv=result.mean_npv,
                success_probability=result.success_probability,
                roi_mean=metrics['roi_medio'],
                var_95=result.var_95,
                metrics=metrics
            )
            session.add(record)
            session.commit()
            return record.id
        finally:
            session.close()
    
    def get_simulations(self, limit=50):
        session = self.Session()
        try:
            return session.query(SimulationRecord).order_by(SimulationRecord.created_at.desc()).limit(limit).all()
        finally:
            session.close()