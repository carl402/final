import numpy as np
from typing import Tuple
from ..models.business_scenario import BusinessScenario, SimulationResult
from ..database.neon_db import NeonDB
from ..utils.statistics import StatisticsCalculator

class MonteCarloEngine:
    """Motor de simulación Monte Carlo para decisiones empresariales"""
    
    def __init__(self, n_simulations: int = 10000, use_database: bool = True):
        self.n_simulations = n_simulations
        self.use_database = use_database
        if use_database:
            try:
                self.db = NeonDB()
                self.db.create_tables()
            except Exception as e:
                print(f"⚠️ No se pudo conectar a la base de datos: {e}")
                self.use_database = False
        np.random.seed(42)
    
    def simulate_scenario(self, scenario: BusinessScenario) -> SimulationResult:
        """Ejecuta simulación Monte Carlo para un escenario de negocio"""
        
        # Arrays para almacenar resultados
        npv_values = np.zeros(self.n_simulations)
        roi_values = np.zeros(self.n_simulations)
        break_even_months = np.zeros(self.n_simulations)
        
        for i in range(self.n_simulations):
            # Generar variables aleatorias
            monthly_revenues = self._generate_revenue_series(scenario)
            monthly_costs = self._generate_cost_series(scenario)
            inflation_factors = self._generate_inflation_factors(scenario)
            
            # Calcular flujos de caja descontados
            cash_flows = (monthly_revenues - monthly_costs) * inflation_factors
            
            # NPV usando integración Monte Carlo: ∫ CF(t) * e^(-r*t) dt
            discount_rates = np.array([1/(1+0.1)**(t/12) for t in range(scenario.time_horizon)])
            npv = np.sum(cash_flows * discount_rates) - scenario.initial_investment
            
            # ROI
            total_profit = np.sum(cash_flows)
            roi = (total_profit / scenario.initial_investment) * 100 if scenario.initial_investment > 0 else 0
            
            # Break-even
            cumulative_cash = np.cumsum(cash_flows) - scenario.initial_investment
            break_even = np.argmax(cumulative_cash > 0) + 1 if np.any(cumulative_cash > 0) else scenario.time_horizon
            
            npv_values[i] = npv
            roi_values[i] = roi
            break_even_months[i] = break_even
        
        result = self._calculate_statistics(scenario.name, npv_values, roi_values, break_even_months)
        
        # Guardar en base de datos si está habilitada
        if self.use_database:
            try:
                scenario_id = self.db.save_scenario(scenario)
                metrics = StatisticsCalculator.calculate_risk_metrics(result)
                self.db.save_simulation_result(scenario_id, result, metrics)
                print(f"✅ Escenario '{scenario.name}' guardado en base de datos")
            except Exception as e:
                print(f"⚠️ Error guardando en base de datos: {e}")
        
        return result
    
    def _generate_revenue_series(self, scenario: BusinessScenario) -> np.ndarray:
        """Genera serie temporal de ingresos con tendencia y volatilidad"""
        base_revenues = np.random.normal(scenario.revenue_mean, scenario.revenue_std, scenario.time_horizon)
        # Añadir tendencia de crecimiento
        growth_trend = np.array([1 + 0.02 * t for t in range(scenario.time_horizon)])
        # Añadir volatilidad del mercado
        market_shocks = np.random.normal(1, scenario.market_volatility, scenario.time_horizon)
        return np.maximum(base_revenues * growth_trend * market_shocks, 0)
    
    def _generate_cost_series(self, scenario: BusinessScenario) -> np.ndarray:
        """Genera serie temporal de costos con inflación"""
        base_costs = np.random.normal(scenario.cost_mean, scenario.cost_std, scenario.time_horizon)
        return np.maximum(base_costs, 0)
    
    def _generate_inflation_factors(self, scenario: BusinessScenario) -> np.ndarray:
        """Genera factores de inflación estocásticos"""
        inflation_shocks = np.random.normal(scenario.inflation_rate, 0.01, scenario.time_horizon)
        return np.array([1 - sum(inflation_shocks[:t+1])/12 for t in range(scenario.time_horizon)])
    
    def _calculate_statistics(self, name: str, npv_values: np.ndarray, 
                            roi_values: np.ndarray, break_even_months: np.ndarray) -> SimulationResult:
        """Calcula estadísticas del resultado de simulación"""
        
        success_probability = np.mean(npv_values > 0) * 100
        mean_npv = np.mean(npv_values)
        std_npv = np.std(npv_values)
        percentile_5 = np.percentile(npv_values, 5)
        percentile_95 = np.percentile(npv_values, 95)
        var_95 = np.percentile(npv_values, 5)  # Value at Risk
        
        return SimulationResult(
            scenario_name=name,
            net_present_values=npv_values,
            roi_values=roi_values,
            break_even_months=break_even_months,
            success_probability=success_probability,
            mean_npv=mean_npv,
            std_npv=std_npv,
            percentile_5=percentile_5,
            percentile_95=percentile_95,
            var_95=var_95
        )