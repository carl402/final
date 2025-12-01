import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class BusinessScenario:
    """Modelo de escenario de negocio para simulación Monte Carlo"""
    name: str
    initial_investment: float
    revenue_mean: float
    revenue_std: float
    cost_mean: float
    cost_std: float
    inflation_rate: float = 0.03
    market_volatility: float = 0.15
    time_horizon: int = 12  # meses

@dataclass
class SimulationResult:
    """Resultado de simulación Monte Carlo"""
    scenario_name: str
    net_present_values: np.ndarray
    roi_values: np.ndarray
    break_even_months: np.ndarray
    success_probability: float
    mean_npv: float
    std_npv: float
    percentile_5: float
    percentile_95: float
    var_95: float  # Value at Risk al 95%