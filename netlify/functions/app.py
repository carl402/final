import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.ui.dashboard import DecisionDashboard

def handler(event, context):
    """Función serverless para Netlify"""
    try:
        dashboard = DecisionDashboard()
        app = dashboard.app
        
        # Configurar para serverless
        app.config.update({
            'suppress_callback_exceptions': True
        })
        
        return {
            'statusCode': 200,
            'body': 'Monte Carlo Dashboard Running'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }