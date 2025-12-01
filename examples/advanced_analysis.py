#!/usr/bin/env python3
"""
Ejemplo avanzado de análisis de decisiones empresariales
Demuestra capacidades avanzadas del sistema Monte Carlo
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pandas as pd
from src.simulation.monte_carlo_engine import MonteCarloEngine
from src.models.business_scenario import BusinessScenario
from src.utils.statistics import StatisticsCalculator

def advanced_scenario_analysis():
    """Análisis avanzado de múltiples escenarios"""
    
    print("🔬 Análisis Avanzado de Escenarios Empresariales")
    print("=" * 55)
    
    # Escenarios con diferentes perfiles de riesgo
    scenarios = {
        "Conservador": BusinessScenario(
            name="Estrategia Conservadora",
            initial_investment=75000,
            revenue_mean=20000,
            revenue_std=2000,
            cost_mean=12000,
            cost_std=1000,
            inflation_rate=0.025,
            market_volatility=0.08
        ),
        "Moderado": BusinessScenario(
            name="Estrategia Moderada",
            initial_investment=100000,
            revenue_mean=28000,
            revenue_std=5000,
            cost_mean=16000,
            cost_std=2500,
            inflation_rate=0.03,
            market_volatility=0.15
        ),
        "Agresivo": BusinessScenario(
            name="Estrategia Agresiva",
            initial_investment=150000,
            revenue_mean=45000,
            revenue_std=12000,
            cost_mean=25000,
            cost_std=6000,
            inflation_rate=0.035,
            market_volatility=0.25
        )
    }
    
    engine = MonteCarloEngine(n_simulations=20000)
    results = {}
    
    print("\n📊 Ejecutando simulaciones de alta precisión (20,000 iteraciones)...")
    
    for profile, scenario in scenarios.items():
        print(f"\n🔄 Analizando perfil {profile}...")
        result = engine.simulate_scenario(scenario)
        results[profile] = result
        
        metrics = StatisticsCalculator.calculate_risk_metrics(result)
        
        print(f"   NPV Esperado: ${metrics['media_npv']:,.0f}")
        print(f"   Riesgo (Desv.Std): ${metrics['desviacion_std']:,.0f}")
        print(f"   Ratio Sharpe: {metrics['media_npv']/metrics['desviacion_std']:.3f}")
        print(f"   Prob. Pérdida: {100-metrics['probabilidad_exito']:.1f}%")
    
    return results

def main():
    """Función principal del análisis avanzado"""
    
    try:
        results = advanced_scenario_analysis()
        print("\n✅ Análisis avanzado completado exitosamente")
        
    except Exception as e:
        print(f"\n❌ Error en análisis: {e}")

if __name__ == "__main__":
    main()