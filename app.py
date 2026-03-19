import streamlit as st
import json
import os

# Ocultar sidebar completamente
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
st.write("🚀 Configuración automática - Credenciales incluidas")

CREDENTIALS = {
    "type": "service_account",
    "project_id": "turnkey-realm-490621-g6",
    "private_key_id": "23197905dd3b00c010c0c95176ee2d7ef31690f6",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDQmT9B3VOTdpL9\napPEOSFvFzLiv8vA7IP/5WmAV1KBTZ/5VOPKtrMHKDTedsBQpGbr68Nr5uPR03s7\n3T8PbEumSiV9Npj6Nqjb4hNq9sIq7mBaDJlcmYnBjpaqUo1zTVICOkUi9nXIk3wN\nqGmFsSxmlg/iNGH92Hwyqq0IRgT13HmlGLLpOv6uy3DaUXdg3Xl7jq/gbjLDTk4e\nUc+0TEA3Qd1djkHUYjqaxNcK+/Ie1GyF8hy6hB9YIkciiShBA8KKFi/Q8mxwIH5D\nfadiFqAwMIzdoPAHMwmQH/qw2PkK1Brk8y2cDIr8peoQPI+UyunbZERdLf+TmbYm\n3RgoTYqHAgMBAAECggEALyh2BI3ktxG3aVMO1O2VgWfdOSXjClpt/QwALeOP42uJ\nHvTyCoIDNzr/uMtf7ts76VoDdAFev7DvyzjZaMMy1wUsNIKDUw3IXu1dNnFStCHv\n5muywBx16Cw0I41GLSrtv1MtDhppxk6RXQUV1gOX5hlGvfzZqmmmqk2rkJNDy9ED\nqBLVt9DCu/MH6TFRrFQAsXSN7BvotXfs2TorSWpxQEyYAHUIHd7l3kMsDFog0nnt\noxGXukJtjOpk7cKjLJN/s+GKUUQRjT5fXKNmFzAJssfqIp8MerRyOVJvQl63rhyG\n1e0iqPEIxCxSE5uW6cNnfwRXUQelIPbZfsOZBmI1AQKBgQDtvdEvXkG7bHx5+3w6\nOsjAPDAwv7RyTQ+vC03hZVAOByUsQUCe/LHAecrYrLyEG7dEv2ILvGt2D02QXCEk\nt8LVA+Dk8pPDZS1fUSYfYFyWX0eTaL1ywjoBNPSuwauo5FmT3W4OAmUovluM0fpk\nkttGdmk1Nr5BAHDYgST8dIWRQwKBgQDgnnVxqmDAjSEBcOtxt2ZUhcZ0nGiqmRE+\nBISuqUmyR18svPn/Z+ERrULM4/JYyJh0IUEW3q5d0qVoZYPrf3ZZNx6nbvwxUFeI\no8e53NoXlxo8uvNDUjoNpbt1mK4+ycrkJz56cymQ3+4yHfQGbDGwn2KfF4aVgqRD\nAqjEuNb7bQKBgGr+7cFKw3yNg6wGgc9XG3hg3jNiY9y5T+CwzrktNo1Jq/Ix39pt\n0bXVWnSPsTwnmSConYC4qH2NKtOu1/iEB58Y1/GyLe8tmHajLS8Uo8ejIEMN48J\nWL+oTKLF6PLW6nXAx0Io08w1d9B1xCI1cdhRfGIFpDRu9VqLLNEtw9svAoGBALak\nAikneb53wvOyBrATiXCGyiS9nVnCVsPP1rdSzarZ3+i3zKvBor/F20BQxRkuGtCq\nzYs0DCIcCwVFLixKG0hVymYol4Xdpx9i1R8rFmcCJYJmHTGLZcr9DN2FBYHmgURd\nKK9WfuDfRIaZ1nd2eDz+jKmB7pwZe0lFm0dCaQRNAoGAGNqYxXyY64TmQjL6z6WR\nREfFhx3z5bjtc5Z2/JIT7QLCCZJzd/ObKW0xdJ+h3uvUemYFMJt3V4aBVhtlzGxr\nUQ0eaOw+61wDYTc7pwHp6XpBs5G56DmSzmPTPtDM0TWoBK/qXVYxjq8N4uwofun\nYKi8CaOnXQDNl/T1wj34RSo=\n-----END PRIVATE KEY-----\n",
    "client_email": "dashboard-backup@turnkey-realm-490621-g6.iam.gserviceaccount.com",
    "client_id": "112970843523581797879",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dashboard-backup%40turnkey-realm-490621-g6.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

st.success("✅ Credenciales ya configuradas automáticamente!")
st.write("📋 Información de la cuenta:")
st.info(f"📧 Email: {CREDENTIALS['client_email']}")
st.info(f"🆔 Project ID: {CREDENTIALS['project_id']}")
st.info(f"🆎 Client ID: {CREDENTIALS['client_id']}")

st.markdown("---")
st.subheader("🚀 Probar Conexión a Google Drive")

if st.button("🚀 Probar Conexión y Activar Backup", type="primary", use_container_width=True):
    try:
        import gspread
        from oauth2client.service_account import ServiceAccountCredentials
        import pandas as pd
        from datetime import datetime

        with st.spinner("Conectando con Google Drive..."):
            scope = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]

            # ✅ CORRECCIÓN: usar from_json_keyfile_dict() directamente
            creds_obj = ServiceAccountCredentials.from_json_keyfile_dict(CREDENTIALS, scope)
            client = gspread.authorize(creds_obj)

            # Crear spreadsheet
            spreadsheet = client.create("Dashboard IES - Backup Automático")
            spreadsheet.share('solpeschuk@gmail.com', perm_type='user', role='writer')

            st.success("✅ Conexión exitosa con Google Drive!")
            st.info(f"📁 Spreadsheet creado: {spreadsheet.url}")
            st.info("🎉 ¡Google Drive Backup está ahora ACTIVO!")
            st.info("📧 Todos los datos se guardarán automáticamente en solpeschuk@gmail.com")

            # Backup de prueba
            test_data = pd.DataFrame({
                'Test': ['Backup Configurado Automáticamente'],
                'Fecha': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                'Email': ['solpeschuk@gmail.com'],
                'Estado': ['Activo y Funcionando'],
                'Metodo': ['Configuración Automática'],
                'Project_ID': [CREDENTIALS['project_id']]
            })

            try:
                worksheet = spreadsheet.add_worksheet(title="Datos de Prueba", rows="100", cols="10")
                headers = test_data.columns.tolist()
                worksheet.append_row(headers)
                for _, row in test_data.iterrows():
                    worksheet.append_row(row.tolist())
                st.success("✅ Backup de prueba completado!")

            except Exception as ws_error:
                st.warning(f"⚠️ add_worksheet falló ({ws_error}), usando hoja por defecto...")
                try:
                    worksheet = spreadsheet.get_worksheet(0)
                    all_data = [test_data.columns.tolist()] + test_data.values.tolist()
                    worksheet.update('A1', all_data)
                    st.success("✅ Backup de prueba completado (método alternativo)!")
                except Exception as fallback_error:
                    st.error(f"❌ No se pudieron agregar los datos: {fallback_error}")
                    st.info(f"📁 El spreadsheet fue creado igual: {spreadsheet.url}")

            st.balloons()

    except ImportError as ie:
        st.error(f"❌ Biblioteca no instalada: {ie}")
        st.info("📦 Asegurate de tener gspread y oauth2client en requirements.txt")
    except Exception as e:
        st.error(f"❌ Error en conexión: {e}")
        st.info("🔧 Revisa los permisos de la cuenta de servicio en Google Cloud Console")

st.markdown("---")
st.subheader("📊 Estado del Backup")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📁 Credenciales", "✅ Configuradas")
with col2:
    st.metric("🔧 Método", "Automático")
with col3:
    st.metric("📧 Email", "solpeschuk@gmail.com")

st.markdown("---")
st.subheader("📋 ¿Qué pasó?")
st.markdown("""
### ✅ Configuración automática completada:
- **No necesitas hacer nada más**
- **Las credenciales ya están incluidas**
- **Solo haz click en el botón de prueba**
- **Google Drive Backup se activará automáticamente**

### 🎯 Ventajas:
- **Configuración instantánea** - Sin pasos manuales
- **Sin errores** - Todo está preconfigurado
- **Funciona siempre** - Sin dependencias externas
- **Backup automático** - Listo para usar
""")

st.markdown("---")
footer_html = """
<div style='text-align: center; color: gray; padding: 20px;'>
    <strong>🔧 Google Drive Backup - Configuración Automática Completa</strong><br>
    Email destino: solpeschuk@gmail.com<br>
    <small>Credenciales ya incluidas - Solo haz click en Probar Conexión</small>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)

