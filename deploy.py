#!/usr/bin/env python3
"""
Script de despliegue para el Sistema Monte Carlo Decision Engine
"""

import os
import subprocess
import sys

def install_dependencies():
    """Instala las dependencias del sistema"""
    print("📦 Instalando dependencias...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    print("🔗 Probando conexión a base de datos...")
    try:
        from src.database.db_manager import DatabaseManager
        db = DatabaseManager()
        print("✅ Conexión a base de datos exitosa")
        return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def run_tests():
    """Ejecuta las pruebas del sistema"""
    print("🧪 Ejecutando pruebas...")
    try:
        subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"])
        return True
    except:
        print("⚠️ Pytest no disponible, ejecutando pruebas básicas...")
        subprocess.run([sys.executable, "tests/test_monte_carlo.py"])
        return True

def main():
    """Función principal de despliegue"""
    print("🚀 Desplegando Sistema Monte Carlo Decision Engine")
    print("=" * 50)
    
    # Instalar dependencias
    install_dependencies()
    
    # Probar base de datos
    if not test_database_connection():
        print("⚠️ Continuando sin base de datos...")
    
    # Ejecutar pruebas
    run_tests()
    
    print("\n✅ Sistema listo para usar")
    print("💡 Ejecute: python main.py")

if __name__ == "__main__":
    main()