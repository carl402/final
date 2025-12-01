# 🚀 Deploy en Render - Monte Carlo Decision Engine

## Pasos para Deploy:

### 1. Conectar Repositorio
- Ir a [render.com](https://render.com)
- Crear cuenta o iniciar sesión
- Conectar con GitHub: https://github.com/carl402/final.git

### 2. Crear Web Service
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python main.py`
- **Environment**: Python 3

### 3. Variables de Entorno
```
DATABASE_URL=postgresql://neondb_owner:npg_4mMh2SLfErRe@ep-orange-sky-ahkv6g5o-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
PORT=8050
```

### 4. Deploy Automático
- Render detectará automáticamente los archivos:
  - `requirements.txt` - Dependencias
  - `Procfile` - Comando de inicio
  - `runtime.txt` - Versión Python
  - `render.yaml` - Configuración completa

### 5. URL Final
Una vez desplegado, el sistema estará disponible en:
`https://monte-carlo-engine-[random].onrender.com`

## ✅ Características Desplegadas:
- 🎯 Dashboard interactivo Monte Carlo
- 📊 Simulaciones en tiempo real
- 🗄️ Base de datos PostgreSQL conectada
- 📈 Visualizaciones y estadísticas
- 🔄 Guardado automático de simulaciones