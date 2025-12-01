import psycopg2
import json
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional
import pandas as pd

load_dotenv()

class NeonDB:
    def __init__(self):
        self.connection_string = os.getenv('NEON_DATABASE_URL')
        if not self.connection_string:
            raise ValueError("NEON_DATABASE_URL no encontrada en variables de entorno")
    
    def get_connection(self):
        return psycopg2.connect(self.connection_string)
    
    def create_tables(self):
        """Crea las tablas necesarias"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS scenarios (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        initial_investment DECIMAL(15,2),
                        revenue_mean DECIMAL(15,2),
                        revenue_std DECIMAL(15,2),
                        cost_mean DECIMAL(15,2),
                        cost_std DECIMAL(15,2),
                        inflation_rate DECIMAL(5,4),
                        market_volatility DECIMAL(5,4),
                        time_horizon INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS simulation_results (
                        id SERIAL PRIMARY KEY,
                        scenario_id INTEGER REFERENCES scenarios(id),
                        mean_npv DECIMAL(15,2),
                        std_npv DECIMAL(15,2),
                        success_probability DECIMAL(5,2),
                        var_95 DECIMAL(15,2),
                        roi_mean DECIMAL(8,2),
                        break_even_mean DECIMAL(8,2),
                        results_data JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
    
    def save_scenario(self, scenario) -> int:
        """Guarda un escenario y retorna su ID"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO scenarios (name, initial_investment, revenue_mean, revenue_std,
                                         cost_mean, cost_std, inflation_rate, market_volatility, time_horizon)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
                """, (scenario.name, scenario.initial_investment, scenario.revenue_mean,
                     scenario.revenue_std, scenario.cost_mean, scenario.cost_std,
                     scenario.inflation_rate, scenario.market_volatility, scenario.time_horizon))
                return cur.fetchone()[0]
    
    def save_simulation_result(self, scenario_id: int, result, metrics: Dict):
        """Guarda resultado de simulación"""
        results_data = {
            'npv_values': result.net_present_values.tolist(),
            'roi_values': result.roi_values.tolist(),
            'break_even_months': result.break_even_months.tolist(),
            'metrics': metrics
        }
        
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO simulation_results (scenario_id, mean_npv, std_npv, success_probability,
                                                  var_95, roi_mean, break_even_mean, results_data)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (scenario_id, result.mean_npv, result.std_npv, result.success_probability,
                     result.var_95, metrics.get('roi_medio', 0), metrics.get('break_even_medio', 0),
                     json.dumps(results_data)))
                conn.commit()
    
    def get_scenarios(self) -> List[Dict]:
        """Obtiene todos los escenarios"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM scenarios ORDER BY created_at DESC")
                columns = [desc[0] for desc in cur.description]
                return [dict(zip(columns, row)) for row in cur.fetchall()]
    
    def get_simulation_results(self, scenario_id: int) -> Optional[Dict]:
        """Obtiene resultados de simulación por escenario"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM simulation_results 
                    WHERE scenario_id = %s 
                    ORDER BY created_at DESC LIMIT 1
                """, (scenario_id,))
                row = cur.fetchone()
                if row:
                    columns = [desc[0] for desc in cur.description]
                    return dict(zip(columns, row))
                return None