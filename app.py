import streamlit as st
import pandas as pd
from datetime import datetime

st.markdown("""
<style>
[data-testid="stSidebar"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }
aside[data-testid="stSidebar"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Google Drive Backup",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🔧 Google Drive Backup")
st.write("🚀 Configuración segura vía Streamlit Secrets")

try:
    CREDENTIALS = dict(st.secrets["gcp_service_account"])
    CREDENTIALS["private_key"] = CREDENTIALS["private_key"].replace("\\n", "\n")
    FOLDER_ID = st.secrets["folder_id"]
    st.success("✅ Credenciales cargadas correctamente!")
    st.info(f"📧 Email: {CREDENTIALS['client_email']}")
    st.info(f"📁 Carpeta destino configurada")
except Exception as e:
    st.error(f"❌ Error cargando credenciales: {e}")
    st.stop()

st.markdown("---")
st.subheader("🚀 Probar Conexión a Google Drive")

if st.button("🚀 Probar Conexión y Activar Backup", type="primary", use_container_width=True):
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build

        with st.spinner("Conectando con Google Drive..."):

            scope = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]

            creds = Credentials.from_service_account_info(CREDENTIALS, scopes=scope)
            drive_service = build("drive", "v3", credentials=creds)

            file_metadata = {
                "name": "Dashboard IES - Backup Automático",
                "mimeType": "application/vnd.google-apps.spreadsheet",
                "parents": [FOLDER_ID]
            }

            file = drive_service.files().create(
                body=file_metadata,
                fields="id, webViewLink"
            ).execute()

            file_id = file.get("id")
            file_url = file.get("webViewLink")

            st.success("✅ Conexión exitosa con Google Drive!")
            st.info(f"📁 Spreadsheet creado en tu Drive: {file_url}")
            st.info("🎉 El archivo está directamente en tu carpeta personal!")

            client = gspread.authorize(creds)
            spreadsheet = client.open_by_key(file_id)

            test_data = pd.DataFrame({
                "Test": ["Backup Configurado Automáticamente"],
                "Fecha": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                "Email": ["solpeschuk@gmail.com"],
                "Estado": ["Activo y Funcionando"],
                "Project_ID": [CREDENTIALS["project_id"]]
            })

            try:
                worksheet = spreadsheet.add_worksheet(title="Datos de Prueba", rows="100", cols="10")
                worksheet.append_row(test_data.columns.tolist())
                for _, row in test_data.iterrows():
                    worksheet.append_row(row.tolist())
                st.success("✅ Datos de prueba guardados correctamente!")
            except Exception as ws_error:
                try:
                    worksheet = spreadsheet.get_worksheet(0)
                    worksheet.update("A1", [test_data.columns.tolist()] + test_data.values.tolist())
                    st.success("✅ Datos guardados (método alternativo)!")
                except Exception as e2:
                    st.error(f"❌ No se pudieron guardar los datos: {e2}")

            st.balloons()

    except ImportError as ie:
        st.error(f"❌ Biblioteca no instalada: {ie}")
        st.info("📦 Verificá tu requirements.txt")
    except Exception as e:
        st.error(f"❌ Error en conexión: {e}")

st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📁 Credenciales", "✅ Seguras")
with col2:
    st.metric("🔧 Carpeta", "Tu Drive Personal")
with col3:
    st.metric("📧 Email", "solpeschuk@gmail.com")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
    <strong>🔧 Google Drive Backup - Configuración Segura</strong><br>
    Email destino: solpeschuk@gmail.com
</div>
""", unsafe_allow_html=True)
