import streamlit as st
import json
import os
from datetime import datetime

def setup_google_drive_credentials():
    """Configurar las credenciales de Google Drive paso a paso"""
    
    st.title("🔧 Configuración de Google Drive Backup")
    st.markdown("### Configura el backup automático a solpeschuk@gmail.com")
    
    # Paso 1: Verificar si ya existen credenciales
    if os.path.exists('google_drive_credentials.json'):
        st.success("✅ Ya existe un archivo de credenciales")
        
        with open('google_drive_credentials.json', 'r') as f:
            creds = json.load(f)
        
        st.write("📋 Credenciales actuales:")
        st.json(creds)
        
        if st.button("🔄 Usar estas credenciales", type="primary"):
            st.success("✅ Credenciales listas para usar")
            return True
    
    # Paso 2: Instrucciones para crear credenciales
    st.markdown("---")
    st.subheader("📋 PASO 1: Crear Proyecto en Google Cloud")
    
    st.markdown("""
    1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
    2. Crea un nuevo proyecto llamado **"Dashboard IES Backup"**
    3. Habilita las siguientes APIs:
       - **Google Drive API**
       - **Google Sheets API**
    4. Ve a **"IAM y administración"** > **"Cuentas de servicio"**
    5. Crea una nueva cuenta de servicio
    6. Descarga la clave JSON
    7. Renombra el archivo a **google_drive_credentials.json**
    8. Coloca el archivo en esta misma carpeta
    """)
    
    # Paso 3: Subir archivo de credenciales
    st.markdown("---")
    st.subheader("📁 PASO 2: Subir Archivo de Credenciales")
    
    uploaded_file = st.file_uploader(
        "Sube tu archivo google_drive_credentials.json",
        type=['json'],
        help="Sube el archivo JSON que descargaste de Google Cloud"
    )
    
    if uploaded_file is not None:
        try:
            # Guardar el archivo
            with open('google_drive_credentials.json', 'wb') as f:
                f.write(uploaded_file.getbuffer())
            
            st.success("✅ Archivo de credenciales guardado correctamente")
            
            # Verificar el contenido
            with open('google_drive_credentials.json', 'r') as f:
                creds = json.load(f)
            
            st.write("📋 Contenido del archivo:")
            st.json(creds)
            
            # Verificar campos necesarios
            required_fields = ['type', 'project_id', 'private_key_id', 'private_key', 'client_email', 'client_id']
            missing_fields = [field for field in required_fields if field not in creds]
            
            if missing_fields:
                st.error(f"❌ Faltan campos requeridos: {missing_fields}")
            else:
                st.success("✅ Archivo de credenciales válido")
                
                if st.button("🚀 Probar Conexión", type="primary"):
                    test_google_drive_connection()
            
        except Exception as e:
            st.error(f"❌ Error al guardar el archivo: {e}")
    
    # Paso 4: Compartir acceso
    st.markdown("---")
    st.subheader("🔗 PASO 3: Compartir Acceso")
    
    st.markdown("""
    Una vez configurado, el sistema:
    1. Creará automáticamente un spreadsheet en Google Drive
    2. Lo compartirá con **solpeschuk@gmail.com**
    3. Enviarás un email para aceptar el acceso
    4. Los datos se guardarán automáticamente
    
    **Email destino**: solpeschuk@gmail.com
    """)
    
    # Paso 5: Template de credenciales
    st.markdown("---")
    st.subheader("📋 PASO 4: Template de Credenciales")
    
    st.markdown("""
    Tu archivo google_drive_credentials.json debe verse así:
    ```json
    {
      "type": "service_account",
      "project_id": "dashboard-ies-backup-12345",
      "private_key_id": "clave-privada-id",
      "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7...\\n-----END PRIVATE KEY-----\\n",
      "client_email": "dashboard-backup@dashboard-ies-backup-12345.iam.gserviceaccount.com",
      "client_id": "123456789012345678901",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token"
    }
    ```
    """)
    
    return False

def test_google_drive_connection():
    """Probar la conexión con Google Drive"""
    try:
        from google_drive_backup import GoogleDriveBackup
        
        backup = GoogleDriveBackup()
        
        if backup.setup_credentials():
            if backup.create_or_get_spreadsheet():
                st.success("✅ Conexión exitosa con Google Drive!")
                st.info(f"📁 Spreadsheet: {backup.get_spreadsheet_url()}")
                
                # Probar backup de prueba
                import pandas as pd
                test_data = pd.DataFrame({
                    'Test': ['Backup Exitoso'],
                    'Fecha': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                    'Estado': ['Conectado']
                })
                
                if backup.backup_data(test_data, "Prueba"):
                    st.success("✅ Backup de prueba completado!")
                    st.balloons()
                    return True
                else:
                    st.error("❌ Error en backup de prueba")
                    return False
            else:
                st.error("❌ Error al crear spreadsheet")
                return False
        else:
            st.error("❌ Error en configuración de credenciales")
            return False
            
    except ImportError:
        st.error("❌ Módulo google_drive_backup no encontrado")
        return False
    except Exception as e:
        st.error(f"❌ Error en conexión: {e}")
        return False

def create_manual_credentials():
    """Crear credenciales manualmente para testing"""
    st.markdown("---")
    st.subheader("🔧 Crear Credenciales de Prueba")
    
    st.warning("⚠️ Esta es una configuración de prueba. Para producción, usa tus propias credenciales de Google Cloud.")
    
    # Formulario para credenciales
    with st.form("manual_credentials"):
        st.write("📋 Completa los datos de tu cuenta de servicio:")
        
        project_id = st.text_input("Project ID:", placeholder="dashboard-ies-backup-12345")
        private_key_id = st.text_input("Private Key ID:", placeholder="clave-privada-id")
        private_key = st.text_area("Private Key:", placeholder="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n", height=200)
        client_email = st.text_input("Client Email:", placeholder="dashboard-backup@...gserviceaccount.com")
        client_id = st.text_input("Client ID:", placeholder="123456789012345678901")
        
        submitted = st.form_submit_button("💾 Guardar Credenciales", type="primary")
        
        if submitted and all([project_id, private_key_id, private_key, client_email, client_id]):
            # Crear JSON de credenciales
            credentials = {
                "type": "service_account",
                "project_id": project_id,
                "private_key_id": private_key_id,
                "private_key": private_key,
                "client_email": client_email,
                "client_id": client_id,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
            
            # Guardar archivo
            with open('google_drive_credentials.json', 'w') as f:
                json.dump(credentials, f, indent=2)
            
            st.success("✅ Credenciales guardadas correctamente")
            st.info("📋 Ahora puedes probar la conexión")
            
            # Probar conexión automáticamente
            test_google_drive_connection()

if __name__ == "__main__":
    setup_google_drive_credentials()
    create_manual_credentials()
