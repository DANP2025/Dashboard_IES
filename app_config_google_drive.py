import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
from utils import DataManagement
import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter
import json

# Configuración de la página
st.set_page_config(
    page_title="Configuración Google Drive",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS mínimo
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stAppDeployButton {display:none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("🔧 Configuración de Backup Automático a Google Drive")
st.markdown("### Configura el sistema para guardar datos automáticamente en solpeschuk@gmail.com")

# Verificar si existen credenciales
credentials_exist = os.path.exists('google_drive_credentials.json')

if credentials_exist:
    st.success("✅ Archivo de credenciales encontrado")
    
    # Mostrar credenciales (parcialmente)
    try:
        with open('google_drive_credentials.json', 'r') as f:
            creds = json.load(f)
        
        st.write("📋 Información de la cuenta de servicio:")
        st.info(f"📧 Email: {creds.get('client_email', 'No disponible')}")
        st.info(f"🆔 Project ID: {creds.get('project_id', 'No disponible')}")
        
        # Botón para probar conexión
        if st.button("🚀 Probar Conexión a Google Drive", type="primary", use_container_width=True):
            try:
                from google_drive_backup import GoogleDriveBackup
                
                with st.spinner("Conectando con Google Drive..."):
                    backup = GoogleDriveBackup()
                    
                    if backup.setup_credentials():
                        if backup.create_or_get_spreadsheet():
                            st.success("✅ Conexión exitosa!")
                            st.info(f"📁 Spreadsheet: {backup.get_spreadsheet_url()}")
                            
                            # Probar backup de prueba
                            test_data = pd.DataFrame({
                                'Test': ['Backup Automático'],
                                'Fecha': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                                'Email': ['solpeschuk@gmail.com'],
                                'Estado': ['Configurado']
                            })
                            
                            if backup.backup_data(test_data, "Prueba_Configuracion"):
                                st.success("✅ Backup de prueba completado!")
                                st.balloons()
                                
                                # Actualizar app principal
                                st.info("🔄 Ahora actualiza la app principal para usar el backup automático")
                            else:
                                st.error("❌ Error en backup de prueba")
                        else:
                            st.error("❌ Error al crear spreadsheet")
                    else:
                        st.error("❌ Error en configuración de credenciales")
                        
            except ImportError:
                st.error("❌ Instala las dependencias primero")
                st.code("pip install gspread oauth2client google-auth google-auth-oauthlib google-auth-httplib2")
            except Exception as e:
                st.error(f"❌ Error en conexión: {e}")
    
    except Exception as e:
        st.error(f"❌ Error al leer credenciales: {e}")
        
        # Botón para eliminar credenciales corruptas
        if st.button("🗑️ Eliminar archivo de credenciales", use_container_width=True):
            os.remove('google_drive_credentials.json')
            st.success("✅ Archivo eliminado. Sube uno nuevo.")
            st.rerun()

else:
    st.warning("⚠️ No se encontró el archivo de credenciales")
    
    st.markdown("---")
    st.subheader("📋 Pasos para configurar Google Drive Backup")
    
    # Paso 1
    st.markdown("### 🔧 PASO 1: Instalar dependencias")
    st.code("pip install gspread==5.7.2 oauth2client==4.1.3 google-auth==2.16.0 google-auth-oauthlib==1.0.0 google-auth-httplib2==0.1.1")
    
    # Paso 2
    st.markdown("### 🌐 PASO 2: Crear Proyecto en Google Cloud")
    st.markdown("""
    1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
    2. Crea un nuevo proyecto llamado **"Dashboard IES Backup"**
    3. Habilita las APIs:
       - **Google Drive API**
       - **Google Sheets API**
    4. Ve a **"IAM y administración"** > **"Cuentas de servicio"**
    5. Crea una nueva cuenta de servicio
    6. Descarga la clave JSON
    """)
    
    # Paso 3
    st.markdown("### 📁 PASO 3: Subir Archivo de Credenciales")
    
    uploaded_file = st.file_uploader(
        "Sube tu archivo google_drive_credentials.json",
        type=['json'],
        help="El archivo debe llamarse google_drive_credentials.json"
    )
    
    if uploaded_file is not None:
        try:
            # Verificar que sea el nombre correcto
            if uploaded_file.name != 'google_drive_credentials.json':
                st.error("❌ El archivo debe llamarse 'google_drive_credentials.json'")
            else:
                # Guardar el archivo
                with open('google_drive_credentials.json', 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                
                st.success("✅ Archivo de credenciales guardado correctamente")
                st.info("🔄 Refresca la página para probar la conexión")
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ Error al guardar el archivo: {e}")
    
    # Paso 4
    st.markdown("### 📋 PASO 4: Verificar Credenciales")
    st.markdown("""
    Tu archivo JSON debe contener estos campos:
    ```json
    {
      "type": "service_account",
      "project_id": "tu-project-id",
      "private_key_id": "...",
      "private_key": "-----BEGIN PRIVATE KEY-----...",
      "client_email": "...@...gserviceaccount.com",
      "client_id": "..."
    }
    ```
    """)

# Instrucciones adicionales
st.markdown("---")
st.subheader("📚 ¿Cómo funciona el backup automático?")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **🔄 Backup Automático:**
    - Cada vez que guardas un alumno
    - Cada vez que tomas asistencia
    - Cada vez que registras evaluaciones
    - Los datos se guardan en Google Drive
    - Se comparten con solpeschuk@gmail.com
    """)
    
    st.markdown("""
    **📁 Estructura en Google Drive:**
    - Spreadsheet: "Dashboard IES - Backup Automático"
    - Hojas por fecha y tipo
    - Formato organizado
    - Acceso permanente
    """)

with col2:
    st.markdown("""
    **✅ Ventajas:**
    - Backup en la nube
    - Acceso desde cualquier lugar
    - No pierdes datos
    - Compartido automáticamente
    - Historial completo
    """)
    
    st.markdown("""
    **🔧 Configuración:**
    - Solo una vez
    - Credenciales seguras
    - Acceso automático
    - Sin mantenimiento
    """)

# Botón para ir a la app principal
st.markdown("---")
if st.button("📚 Ir al Dashboard Principal", use_container_width=True, type="primary"):
    # Actualizar app.py para usar la versión con Google Drive
    try:
        with open('app.py', 'w') as f:
            f.write('# Importar la versión con Google Drive\n')
            f.write('exec(open(\'app_con_google_drive.py\').read())\n')
        
        st.success("✅ App principal actualizada para usar Google Drive")
        st.info("🔄 Reinicia Streamlit para ver los cambios")
        
    except Exception as e:
        st.error(f"❌ Error al actualizar app principal: {e}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 20px;'>
        <strong>🔧 Configuración Google Drive Backup</strong><br>
        Sistema de backup automático para Dashboard IES<br>
        <small>Email destino: solpeschuk@gmail.com</small>
    </div>
    """,
    unsafe_allow_html=True
)
