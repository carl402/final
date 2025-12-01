import unittest
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.business_scenario import BusinessScenario
from src.simulation.monte_carlo_engine import MonteCarloEngine
from src.utils.statistics import StatisticsCalculator

class TestMonteCarloEngine(unittest.TestCase):
    """Pruebas unitarias para el motor Monte Carlo"""
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.engine = MonteCarloEngine(n_simulations=1000)
        self.test_scenario = BusinessScenario(
            name="Test Scenario",
            initial_investment=50000,
            revenue_mean=15000,
            revenue_std=3000,
            cost_mean=8000,
            cost_std=1500,
            inflation_rate=0.03,
            market_volatility=0.15
        )
    
    def test_simulation_execution(self):
        """Prueba que la simulación se ejecute correctamente"""
        result = self.engine.simulate_scenario(self.test_scenario)
        
        # Verificar que se generaron los resultados esperados
        self.assertEqual(len(result.net_present_values), 1000)
        self.assertEqual(len(result.roi_values), 1000)
        self.assertEqual(len(result.break_even_months), 1000)
        self.assertEqual(result.scenario_name, "Test Scenario")
    
    def test_npv_calculation(self):
        """Prueba el cálculo de NPV"""
        result = self.engine.simulate_scenario(self.test_scenario)
        
        # NPV debe ser un número finito
        self.assertTrue(np.isfinite(result.mean_npv))
        self.assertTrue(np.isfinite(result.std_npv))
        
        # Verificar que hay variabilidad en los resultados
        self.assertGreater(result.std_npv, 0)
    
    def test_probability_metrics(self):
        """Prueba las métricas de probabilidad"""
        result = self.engine.simulate_scenario(self.test_scenario)
        
        # Probabilidad debe estar entre 0 y 100
        self.assertGreaterEqual(result.success_probability, 0)
        self.assertLessEqual(result.success_probability, 100)
    
    def test_statistics_calculator(self):
        """Prueba el calculador de estadísticas"""
        result = self.engine.simulate_scenario(self.test_scenario)
        metrics = StatisticsCalculator.calculate_risk_metrics(result)
        
        # Verificar métricas clave
        self.assertIn('media_npv', metrics)
        self.assertIn('probabilidad_exito', metrics)
        self.assertIn('var_95', metrics)
        self.assertIn('roi_medio', metrics)
        
        # VaR debe ser menor o igual que el percentil 5
        self.assertLessEqual(metrics['var_95'], result.percentile_5)

if __name__ == '__main__':
    unittest.main()