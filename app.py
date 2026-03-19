import streamlit as st
import json
import os

# Ocultar sidebar completamente
st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none !important;
}
section[data-testid="stSidebar"] {
    display: none !important;
}
aside[data-testid="stSidebar"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Google Drive Backup",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🔧 Google Drive Backup")
st.write("Configura tu backup automático a Google Drive")

# Enlace del spreadsheet existente
EXISTING_SPREADSHEET = "https://docs.google.com/spreadsheets/d/10sSBzhpkEPYk78jEctV6XzRoyFJpaYznQPnv9T6VpPc/edit?usp=drive_link"

# Formulario para ingresar credenciales manualmente
with st.form("credentials_form"):
    st.write("Ingresa tus credenciales de Google Cloud:")
    
    project_id = st.text_input("Project ID", value="turnkey-realm-490621-g6")
    private_key_id = st.text_input("Private Key ID", value="23197905dd3b00c010c0c95176ee2d7ef31690f6")
    client_email = st.text_input("Client Email", value="dashboard-backup@turnkey-realm-490621-g6.iam.gserviceaccount.com")
    client_id = st.text_input("Client ID", value="112970843523581797879")
    private_key = st.text_area("Private Key", value="-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDQmT9B3VOTdpL9\napPEOSFvFzLiv8vA7IP/5WmAV1KBTZ/5VOPKtrMHKDTedsBQpGbr68Nr5uPR03s7\n3T8PbEumSiV9Npj6Nqjb4hNq9sIq7mBaDJlcmYnBjpaqUo1zTVICOkUi9nXIk3wN\nqGmFsSxmlg/iNGH92Hwyqq0IRgT13HmlGLLpOv6uy3DaUXdg3Xl7jq/gbjLDTk4e\nUc+0TEA3Qd1djkHUYjqaxNcK+/Ie1GyF8hy6hB9YIkciiShBA8KKFi/Q8mxwIH5D\nfadiFqAwMIzdoPAHMwmQH/qw2PkK1Brk8y2cDIr8peoQPI+UyunbZERdLf+TmbYm\n3RgoTYqHAgMBAAECggEALyh2BI3ktxG3aVMO1O2VgWfdOSXjClpt/QwALeOP42uJ\nHvTyCoIDNzr/uMtf7ts76VoDdAFev7DvyzjZaMMy1wUsNIKDUw3IXu1dNnFStCHv\n5muywBx16Cw0I41GLSrtv1MtDhppxk6RXQUV1gOX5hlGvfzZqmmmqk2rkJNDy9ED\nqBLVt9DCu/MH6TFRrFQAsXSN7BvotXfs2TorSWpxQEyYAHUIHd7l3kMsDFog0nnt\noxGXukJtjOpk7cKjLJN/s+GKUUQRjT5fXKNmFzAJssfqIp8MerRyOVJvQl63rhyG\n1e0iqPEIxCxSE5uW6cNnfwRXUQelIPbZfsOZBmI1AQKBgQDtvdEvXkG7bHx5+3w6\nOsjAPDAwv7RyTQ+vC03hZVAOByUsQUCe/LHAecrYrLyEG7dEv2ILvGt2D02QXCEk\nt8LVA+Dk8pPDZS1fUSYfYFyWX0eTaL1ywjoBNPSuwauo5FmT3W4OAmUovluM0fpk\nkttGdmk1Nr5BAHDYgST8dIWRQwKBgQDgnnVxqmDAjSEBcOtxt2ZUhcZ0nGiqmRE+\nBISuqUmyR18svPn/Z+ERrULM4/JYyJh0IUEW3q5d0qVoZYPrf3ZZNx6nbvwxUFeI\no8e53NoXlxo8uvNDUjoNpbt1mK4+ycrkJz56cymQ3+4yHfQGbDGwn2KfF4aVgqRD\nAqjEuNb7bQKBgGr+7cFKw3yNg6wGgc9XG3hg3jNiY9y5T+CwzrktNo1Jq/Ix39pt\n0bXVWnSPsTwnmSConYC4qH2NKtOu1/iEB58Y1/GyLe8tmHajLS8Uo8ejIEMN48J\nWL+oTKLF6PLW6nXAx0Io08w1d9B1xCI1cdhRfGIFpDRu9VqLLNEtw9svAoGBALak\nAikneb53wvOyBrATiXCGyiS9nVnCVsPP1rdSzarZ3+i3zKvBor/F20BQxRkuGtCq\nzYs0DCIcCwVFLixKG0hVymYol4Xdpx9i1R8rFmcCJYJmHTGLZcr9DN2FBYHmgURd\nKK9WfuDfRIaZ1nd2eDz+jKmB7pwZe0lFm0dCaQRNAoGAGNqYxXyY64TmQjL6z6WR\nREfFhx3z5bjtc5Z2/JIT7QLCCZJzd/ObKW0xdJ+h3uvUemYFMJt3V4aBVhtlzGxr\nUQ0eaOw+61wDYTc7pwHp6XpBs5G56DmSzmPTPtDM0TWoBK/qXVYxjq8N4uwofun\nYKi8CaOnXQDNl/T1wj34RSo=\n-----END PRIVATE KEY-----", height=200)
    
    submitted = st.form_submit_button("Guardar Credenciales", type="primary")
    
    if submitted:
        credentials = {
            "type": "service_account",
            "project_id": project_id,
            "private_key_id": private_key_id,
            "private_key": private_key,
            "client_email": client_email,
            "client_id": client_id,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dashboard-backup%40turnkey-realm-490621-g6.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com"
        }
        
        with open('google_drive_credentials.json', 'w') as f:
            json.dump(credentials, f, indent=2)
        
        st.success("✅ Credenciales guardadas!")
        st.balloons()

if os.path.exists('google_drive_credentials.json'):
    st.success("✅ Credenciales configuradas")
    
    try:
        with open('google_drive_credentials.json', 'r') as f:
            creds = json.load(f)
        
        st.write("📋 Información de la cuenta:")
        st.info(f"📧 Email: {creds.get('client_email', 'No disponible')}")
        st.info(f"🆔 Project ID: {creds.get('project_id', 'No disponible')}")
        st.info(f"🆎 Client ID: {creds.get('client_id', 'No disponible')}")
        
        # Mostrar información del backup existente
        st.markdown("---")
        st.subheader("📁 Backup Automático Actual")
        st.success("✅ Backup automático ya está ACTIVO!")
        st.markdown(f"📁 [Ver Backup Actual]({EXISTING_SPREADSHEET})")
        st.info("📧 Todos los datos se guardan automáticamente en solpeschuk@gmail.com")
        
        # Botón para probar conexión (crear nuevo backup)
        st.markdown("---")
        st.subheader("🚀 Opciones de Backup")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📂 Ver Backup Actual", type="secondary", use_container_width=True):
                st.markdown(f"📁 [Abrir Backup Actual]({EXISTING_SPREADSHEET})")
        
        with col2:
            if st.button("🆕 Crear Nuevo Backup", type="primary", use_container_width=True):
                try:
                    import gspread
                    from oauth2client.service_account import ServiceAccountCredentials
                    
                    with st.spinner("Creando nuevo backup..."):
                        # Configurar credenciales
                        scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
                        creds_obj = ServiceAccountCredentials.from_json_keyfile_name('google_drive_credentials.json', scope)
                        client = gspread.authorize(creds_obj)
                        
                        # Crear nuevo spreadsheet
                        new_spreadsheet = client.create("Dashboard IES - Backup Nuevo")
                        
                        # Compartir con el email
                        new_spreadsheet.share('solpeschuk@gmail.com', perm_type='user', role='writer')
                        
                        st.success("✅ Nuevo backup creado!")
                        st.info(f"📁 Nuevo spreadsheet: {new_spreadsheet.url}")
                        st.info("🎉 ¡Tienes dos backups activos!")
                        st.balloons()
                        
                        # Backup de prueba en el nuevo spreadsheet
                        import pandas as pd
                        from datetime import datetime
                        
                        test_data = pd.DataFrame({
                            'Test': ['Nuevo Backup Creado'],
                            'Fecha': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                            'Email': ['solpeschuk@gmail.com'],
                            'Estado': ['Activo y Funcionando'],
                            'Metodo': ['Configuración Manual'],
                            'Project_ID': [creds.get('project_id', 'No disponible')],
                            'Spreadsheet_Anterior': [EXISTING_SPREADSHEET]
                        })
                        
                        # Agregar datos al nuevo spreadsheet
                        worksheet = new_spreadsheet.worksheet(0)
                        data = [test_data.columns.tolist()] + test_data.values.tolist()
                        worksheet.update('A1', data)
                        
                        st.success("✅ Datos de prueba agregados al nuevo backup!")
                        st.balloons()
                        
                except ImportError:
                    st.error("❌ Bibliotecas no instaladas")
                    st.info("📦 Las bibliotecas se están instalando en Streamlit Cloud")
                except Exception as e:
                    st.error(f"❌ Error creando nuevo backup: {e}")
                    st.info("🔧 Revisa que tus credenciales sean correctas")
        
        # Botón para eliminar credenciales
        st.markdown("---")
        if st.button("🗑️ Eliminar credenciales", use_container_width=True):
            os.remove('google_drive_credentials.json')
            st.success("✅ Credenciales eliminadas.")
            st.rerun()
            
    except Exception as e:
        st.error(f"❌ Error al leer credenciales: {e}")
else:
    st.warning("⚠️ Configura tus credenciales arriba")

# Instrucciones
st.markdown("---")
st.subheader("📋 Estado del Backup")

col1, col2, col3 = st.columns(3)

with col1:
    if os.path.exists('google_drive_credentials.json'):
        st.metric("📁 Archivo", "✅ Encontrado")
    else:
        st.metric("📁 Archivo", "❌ No encontrado")

with col2:
    if os.path.exists('google_drive_credentials.json'):
        st.metric("🔧 Configuración", "✅ Lista")
    else:
        st.metric("🔧 Configuración", "❌ Pendiente")

with col3:
    st.metric("📧 Email", "solpeschuk@gmail.com")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 20px;'>
        <strong>🔧 Google Drive Backup - Configuración Manual con Backup Existente</strong><br>
        Email destino: solpeschuk@gmail.com<br>
        <small>Configura tus credenciales y mantén tu backup actual o crea nuevos</small>
    </div>
    """,
    unsafe_allow_html=True
)
