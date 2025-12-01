#!/usr/bin/env python3
"""
Script para configurar la base de datos Neon
"""

from src.database.neon_db import NeonDB

def setup_database():
    """Configura las tablas en Neon"""
    try:
        print("🔧 Configurando base de datos Neon...")
        db = NeonDB()
        db.create_tables()
        print("✅ Base de datos configurada correctamente")
        
        # Verificar conexión
        scenarios = db.get_scenarios()
        print(f"📊 Escenarios existentes: {len(scenarios)}")
        
    except Exception as e:
        print(f"❌ Error configurando base de datos: {e}")
        print("💡 Verifica tu NEON_DATABASE_URL en el archivo .env")

if __name__ == "__main__":
    setup_database()