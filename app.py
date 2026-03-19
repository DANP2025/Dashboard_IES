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
    SHEET_ID = CREDENTIALS.pop("sheet_id")
    st.success("✅ Credenciales cargadas correctamente!")
    st.info(f"📧 Email: {CREDENTIALS['client_email']}")
    st.info(f"📊 Sheet ID configurado correctamente")
except Exception as e:
    st.error(f"❌ Error cargando credenciales: {e}")
    st.stop()

st.markdown("---")
st.subheader("🚀 Probar Conexión a Google Sheets")

if st.button("🚀 Probar Conexión y Activar Backup", type="primary", use_container_width=True):
    try:
        import gspread
        from google.oauth2.service_account import Credentials

        with st.spinner("Conectando con Google Sheets..."):

            scope = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]

            creds = Credentials.from_service_account_info(CREDENTIALS, scopes=scope)
            client = gspread.authorize(creds)

            spreadsheet = client.open_by_key(SHEET_ID)

            st.success("✅ Conexión exitosa con Google Sheets!")
            st.info(f"📊 Sheet abierto: {spreadsheet.title}")

            test_data = pd.DataFrame({
                "Test": ["Backup Configurado Automáticamente"],
                "Fecha": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                "Email": ["solpeschuk@gmail.com"],
                "Estado": ["Activo y Funcionando"],
                "Project_ID": [CREDENTIALS["project_id"]]
            })

            try:
                worksheet = spreadsheet.add_worksheet(
                    title="Datos de Prueba", rows="100", cols="10"
                )
            except Exception:
                worksheet = spreadsheet.worksheet("Datos de Prueba")

            worksheet.clear()
            worksheet.append_row(test_data.columns.tolist())
            for _, row in test_data.iterrows():
                worksheet.append_row(row.tolist())

            st.success("✅ Datos guardados correctamente en tu Google Sheet!")
            st.info("🎉 El backup está funcionando. Revisá tu Google Drive.")
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
    st.metric("🔧 Método", "Sheet existente")
with col3:
    st.metric("📧 Email", "solpeschuk@gmail.com")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
    <strong>🔧 Google Drive Backup - Configuración Segura</strong><br>
    Email destino: solpeschuk@gmail.com
</div>
""", unsafe_allow_html=True)
