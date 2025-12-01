# 🚀 Guía de Despliegue - Sistema Monte Carlo

## 📦 Opciones de Publicación

### 1. **GitHub Repository**
```bash
git init
git add .
git commit -m "Sistema Monte Carlo con Base de Datos Neon"
git remote add origin https://github.com/tu-usuario/monte-carlo-decision-engine
git push -u origin main
```

### 2. **Heroku (Gratis)**
```bash
# Crear Procfile
echo "web: python main.py" > Procfile

# Desplegar
heroku create tu-app-montecarlo
heroku config:set NEON_DATABASE_URL="tu-url-neon"
git push heroku main
```

### 3. **Railway (Gratis)**
- Conecta tu repositorio GitHub
- Agrega variable de entorno NEON_DATABASE_URL
- Deploy automático

### 4. **Render (Gratis)**
- Conecta GitHub
- Configura variables de entorno
- Deploy automático

## 🔧 Archivos Necesarios para Deploy

### Procfile (Heroku)
```
web: python main.py
```

### runtime.txt (Heroku)
```
python-3.11.0
```

### app.json (Heroku)
```json
{
  "name": "Monte Carlo Decision Engine",
  "description": "Sistema de decisiones empresariales con simulaciones Monte Carlo",
  "env": {
    "NEON_DATABASE_URL": {
      "description": "URL de conexión a base de datos Neon"
    }
  }
}
```

## 🌐 URLs de Ejemplo
- **GitHub**: `https://github.com/usuario/monte-carlo-engine`
- **Heroku**: `https://tu-app-montecarlo.herokuapp.com`
- **Railway**: `https://monte-carlo-production.up.railway.app`
- **Render**: `https://monte-carlo.onrender.com`

## ✅ Estado Actual
- ✅ Código completo y funcional
- ✅ Base de datos Neon configurada
- ✅ Variables de entorno configuradas
- ✅ Dependencias definidas
- ✅ Listo para deploy