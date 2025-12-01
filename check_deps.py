import sys

required_modules = [
    'psycopg2',
    'dotenv',
    'numpy',
    'pandas'
]

print("🔍 Verificando dependencias...")
missing = []

for module in required_modules:
    try:
        __import__(module)
        print(f"✅ {module}")
    except ImportError:
        print(f"❌ {module} - NO INSTALADO")
        missing.append(module)

if missing:
    print(f"\n💡 Instala las dependencias faltantes:")
    print("pip install psycopg2-binary python-dotenv numpy pandas")
else:
    print("\n🎯 Todas las dependencias están instaladas")
    
    # Ahora probar conexión
    print("\n" + "="*50)
    exec(open('test_connection.py').read())