#!/usr/bin/env python3
"""
Sistema de Asistente de Toma de Decisiones Empresariales con Simulaciones Monte Carlo

Descripción: Herramienta para gerentes que simula escenarios de negocio bajo incertidumbre económica
"""

import sys
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.ui.app import MainApp
from src.simulation.monte_carlo_engine import MonteCarloEngine
from src.models.business_scenario import BusinessScenario
from src.utils.statistics import StatisticsCalculator

def demo_simulation():
    """Ejecuta una simulación de demostración"""
    print("Sistema de Decisiones Empresariales - Monte Carlo")
    print("=" * 60)
    
    # Crear escenarios de ejemplo
    scenarios = [
        BusinessScenario(
            name="Lanzamiento Producto Premium",
            initial_investment=150000,
            revenue_mean=35000,
            revenue_std=8000,
            cost_mean=20000,
            cost_std=4000,
            inflation_rate=0.03,
            market_volatility=0.20
        ),
        BusinessScenario(
            name="Expansión Mercado Local",
            initial_investment=80000,
            revenue_mean=22000,
            revenue_std=5000,
            cost_mean=12000,
            cost_std=2500,
            inflation_rate=0.025,
            market_volatility=0.12
        ),
        BusinessScenario(
            name="Servicio Digital",
            initial_investment=50000,
            revenue_mean=18000,
            revenue_std=4000,
            cost_mean=8000,
            cost_std=1500,
            inflation_rate=0.02,
            market_volatility=0.25
        )
    ]
    
    # Motor de simulación
    engine = MonteCarloEngine(n_simulations=10000)
    results = []
    
    print("\nEjecutando simulaciones Monte Carlo...")
    
    for scenario in scenarios:
        print(f"\n Simulando: {scenario.name}")
        result = engine.simulate_scenario(scenario)
        results.append(result)
        
        # Mostrar resultados básicos
        metrics = StatisticsCalculator.calculate_risk_metrics(result)
        print(f"   NPV Promedio: ${metrics['media_npv']:,.0f}")
        print(f"   Probabilidad de Éxito: {metrics['probabilidad_exito']:.1f}%")
        print(f"   ROI Promedio: {metrics['roi_medio']:.1f}%")
        print(f"   VaR 95%: ${metrics['var_95']:,.0f}")
    
    # Comparación de escenarios
    print("\nComparación de Escenarios:")
    print("=" * 40)
    comparison = StatisticsCalculator.compare_scenarios(results)
    
    for idx, (scenario_name, row) in enumerate(comparison.iterrows(), 1):
        print(f"{idx}. {scenario_name}")
        print(f"   Score Atractivo: {row['score_atractivo']:.3f}")
        print(f"   NPV: ${row['media_npv']:,.0f}")
        print(f"   Prob. Éxito: {row['probabilidad_exito']:.1f}%")
        print()
    
    print("Simulación completada. Iniciando dashboard web...")
    return results

def main():
    """Función principal"""
    print("Iniciando Sistema de Decisiones Empresariales")
    
    # Ejecutar demo
    demo_results = demo_simulation()
    
    # Iniciar dashboard web
    print("\nIniciando Dashboard Web en http://localhost:8050")
    print("   Presione Ctrl+C para detener el servidor")
    
    try:
        dashboard = MainApp()
        port = int(os.environ.get('PORT', 8050))
        dashboard.run_server(debug=False, port=port)
    except KeyboardInterrupt:
        print("\nSistema detenido por el usuario")
    except Exception as e:
        print(f"\nError al iniciar dashboard: {e}")
        print(" Asegúrese de tener instaladas todas las dependencias:")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    main()