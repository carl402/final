# 🚀 Guía: GitHub + Netlify Deploy

## 📂 Paso 1: Subir a GitHub

### Opción A: Desde línea de comandos
```bash
# Ya ejecutado:
git init
git add .
git commit -m "🎯 Sistema Monte Carlo con Base de Datos Neon - Listo para deploy"

# Ahora ejecutar:
git branch -M main
git remote add origin https://github.com/TU-USUARIO/monte-carlo-decision-engine
git push -u origin main
```

### Opción B: Desde GitHub Desktop
1. Abre GitHub Desktop
2. File → Add Local Repository
3. Selecciona la carpeta: `c:\Users\Usuario\monte_carlo_decision_engine`
4. Publish repository

### Opción C: Crear repo manualmente
1. Ve a [github.com](https://github.com)
2. Click "New repository"
3. Nombre: `monte-carlo-decision-engine`
4. Descripción: `🎯 Sistema de Decisiones Empresariales con Simulaciones Monte Carlo`
5. Público/Privado según prefieras
6. Create repository
7. Sigue las instrucciones para "push existing repository"

## 🌐 Paso 2: Deploy en Netlify

### Método 1: Desde GitHub (Recomendado)
1. Ve a [netlify.com](https://netlify.com)
2. Sign up/Login
3. "New site from Git"
4. Conecta GitHub
5. Selecciona tu repositorio `monte-carlo-decision-engine`
6. Build settings:
   - Build command: `pip install -r requirements.txt`
   - Publish directory: `.`
7. **Environment variables**:
   - `NEON_DATABASE_URL`: `postgresql://neondb_owner:npg_4mMh2SLfErRe@ep-orange-sky-ahkv6g5o-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require`
8. Deploy site

### Método 2: Drag & Drop
1. Comprime toda la carpeta en ZIP
2. Ve a [netlify.com](https://netlify.com)
3. Arrastra el ZIP a la zona de deploy
4. Configura variables de entorno después

## ⚠️ Limitaciones de Netlify

**Netlify es para sitios estáticos**, tu app Python necesita un servidor. 

### Alternativas Recomendadas:

#### 🔥 **Railway** (Mejor opción)
1. Ve a [railway.app](https://railway.app)
2. "Deploy from GitHub"
3. Selecciona tu repo
4. Agrega variable: `NEON_DATABASE_URL`
5. Deploy automático ✅

#### 🚀 **Render**
1. Ve a [render.com](https://render.com)
2. "New Web Service"
3. Conecta GitHub
4. Build: `pip install -r requirements.txt`
5. Start: `python main.py`
6. Agrega variable: `NEON_DATABASE_URL`

#### 💜 **Heroku**
```bash
heroku create monte-carlo-app
heroku config:set NEON_DATABASE_URL="tu-url"
git push heroku main
```

## 🎯 URLs Finales

- **GitHub**: `https://github.com/TU-USUARIO/monte-carlo-decision-engine`
- **Railway**: `https://monte-carlo-production.up.railway.app`
- **Render**: `https://monte-carlo.onrender.com`
- **Heroku**: `https://monte-carlo-app.herokuapp.com`

## ✅ Estado Actual
- ✅ Código en Git local
- ✅ Listo para push a GitHub
- ✅ Configurado para deploy en múltiples plataformas
- ✅ Base de datos Neon configurada