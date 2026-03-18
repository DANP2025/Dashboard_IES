# 🚀 Instrucciones para Subir a GitHub y Streamlit

## 📋 Pasos para GitHub:

1. **Crear repositorio en GitHub:**
   - Ve a https://github.com
   - Click en "New repository"
   - Nombre: `dashboard-ies`
   - Descripción: "Dashboard de Gestión de Alumnos - IES"
   - Marca "Public" o "Private" (como prefieras)
   - NO marques "Add README" (ya tenemos uno)
   - Click en "Create repository"

2. **Subir el código:**
   ```bash
   git remote add origin https://github.com/TU_USUARIO/dashboard-ies.git
   git branch -M main
   git push -u origin main
   ```

## 🌐 Pasos para Streamlit Cloud:

1. **Ve a Streamlit Cloud:**
   - https://share.streamlit.io
   - Inicia sesión con tu cuenta de GitHub

2. **Conecta tu repositorio:**
   - Click en "New app"
   - Selecciona tu repositorio `dashboard-ies`
   - Archivo principal: `app.py`
   - Click en "Deploy!"

3. **Link final será:**
   - `https://tu-usuario-dashboard-ies.streamlit.app`

## 📁 Archivos importantes:
- `app.py` - Aplicación principal
- `utils.py` - Funciones de datos
- `packages.txt` - Dependencias para Streamlit Cloud
- `requirements.txt` - Para desarrollo local
- `.gitignore` - Ignora archivos temporales

## ⚠️ Nota sobre datos:
- Los datos se guardarán en la nube (Streamlit Cloud)
- Para backup local, exporta desde el dashboard
- El Excel se crea automáticamente en la nube

## 🔧 Si necesitas ayuda:
- GitHub: https://docs.github.com
- Streamlit: https://docs.streamlit.io/streamlit-cloud
