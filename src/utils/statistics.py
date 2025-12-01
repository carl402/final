import numpy as np
import pandas as pd
from typing import Dict, List
from ..models.business_scenario import SimulationResult

class StatisticsCalculator:
    """Calculadora de estadísticas avanzadas para análisis de riesgo"""
    
    @staticmethod
    def calculate_risk_metrics(result: SimulationResult) -> Dict:
        """Calcula métricas de riesgo empresarial"""
        
        npv_values = result.net_present_values
        
        # Métricas básicas
        metrics = {
            'media_npv': result.mean_npv,
            'desviacion_std': result.std_npv,
            'coeficiente_variacion': result.std_npv / abs(result.mean_npv) if result.mean_npv != 0 else float('inf'),
            'probabilidad_exito': result.success_probability,
            'var_95': result.var_95,
            'cvar_95': np.mean(npv_values[npv_values <= result.var_95]),  # Conditional VaR
        }
        
        # Métricas de distribución
        metrics.update({
            'asimetria': float(pd.Series(npv_values).skew()),
            'curtosis': float(pd.Series(npv_values).kurtosis()),
            'percentil_10': np.percentile(npv_values, 10),
            'percentil_25': np.percentile(npv_values, 25),
            'mediana': np.percentile(npv_values, 50),
            'percentil_75': np.percentile(npv_values, 75),
            'percentil_90': np.percentile(npv_values, 90),
        })
        
        # Métricas de ROI
        roi_values = result.roi_values
        metrics.update({
            'roi_medio': np.mean(roi_values),
            'roi_std': np.std(roi_values),
            'roi_min': np.min(roi_values),
            'roi_max': np.max(roi_values),
            'prob_roi_positivo': np.mean(roi_values > 0) * 100,
        })
        
        # Análisis de break-even
        break_even = result.break_even_months
        metrics.update({
            'break_even_medio': np.mean(break_even),
            'break_even_mediano': np.median(break_even),
            'prob_break_even_6m': np.mean(break_even <= 6) * 100,
            'prob_break_even_12m': np.mean(break_even <= 12) * 100,
        })
        
        return metrics
    
    @staticmethod
    def compare_scenarios(results: List[SimulationResult]) -> pd.DataFrame:
        """Compara múltiples escenarios de negocio"""
        
        comparison_data = []
        
        for result in results:
            metrics = StatisticsCalculator.calculate_risk_metrics(result)
            metrics['escenario'] = result.scenario_name
            comparison_data.append(metrics)
        
        df = pd.DataFrame(comparison_data)
        df = df.set_index('escenario')
        
        # Ranking por atractivo (combinación de NPV medio y probabilidad de éxito)
        df['score_atractivo'] = (df['media_npv'] / df['media_npv'].max() * 0.6 + 
                                df['probabilidad_exito'] / 100 * 0.4)
        
        return df.sort_values('score_atractivo', ascending=False)
    
    @staticmethod
    def sensitivity_analysis(base_scenario, engine, parameter_ranges: Dict) -> Dict:
        """Análisis de sensibilidad de parámetros"""
        
        sensitivity_results = {}
        
        for param, (min_val, max_val, steps) in parameter_ranges.items():
            param_values = np.linspace(min_val, max_val, steps)
            npv_means = []
            success_probs = []
            
            for value in param_values:
                # Crear escenario modificado
                scenario_copy = base_scenario.__class__(**base_scenario.__dict__)
                setattr(scenario_copy, param, value)
                
                # Simular
                result = engine.simulate_scenario(scenario_copy)
                npv_means.append(result.mean_npv)
                success_probs.append(result.success_probability)
            
            sensitivity_results[param] = {
                'values': param_values,
                'npv_means': npv_means,
                'success_probs': success_probs,
                'elasticity_npv': np.std(npv_means) / np.mean(npv_means) if np.mean(npv_means) != 0 else 0
            }
        
        return sensitivity_results