import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from dotenv import load_dotenv
    load_dotenv()
    
    import psycopg2
    
    # Obtener URL de conexión
    db_url = os.getenv('NEON_DATABASE_URL')
    print(f"🔗 URL de conexión: {db_url[:50]}...")
    
    # Probar conexión
    print("🔄 Probando conexión a Neon...")
    conn = psycopg2.connect(db_url)
    
    with conn.cursor() as cur:
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        print(f"✅ Conexión exitosa!")
        print(f"📊 PostgreSQL: {version[:50]}...")
        
        # Verificar tablas
        cur.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cur.fetchall()
        print(f"📋 Tablas existentes: {len(tables)}")
        for table in tables:
            print(f"   - {table[0]}")
    
    conn.close()
    print("🎯 Base de datos funcionando correctamente")
    
except ImportError as e:
    print(f"❌ Falta instalar dependencias: {e}")
    print("💡 Ejecuta: pip install psycopg2-binary python-dotenv")
except Exception as e:
    print(f"❌ Error de conexión: {e}")
    print("💡 Verifica tu NEON_DATABASE_URL en .env")