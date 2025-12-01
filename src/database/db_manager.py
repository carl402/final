import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv
from .models import Base, SimulationRecord, Project

load_dotenv()



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
    
    def save_simulation(self, scenario, result, metrics, project_id=1):
        session = self.Session()
        try:
            record = SimulationRecord(
                project_id=project_id,
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