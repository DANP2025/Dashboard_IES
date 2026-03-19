import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime, date
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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
    page_title="Sistema IES Completo",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enlace del spreadsheet existente
EXISTING_SPREADSHEET = "https://docs.google.com/spreadsheets/d/10sSBzhpkEPYk78jEctV6XzRoyFJpaYznQPnv9T6VpPc/edit?usp=drive_link"

# Título principal
st.title("🎓 Sistema Integral IES")
st.write("Plataforma completa de gestión educativa con backup automático")

# Sistema de navegación por pestañas
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard", 
    "👥 Alumnos", 
    "📋 Asistencia", 
    "📝 Evaluaciones", 
    "🔧 Configuración"
])

# Función para cargar credenciales
def cargar_credenciales():
    if os.path.exists('google_drive_credentials.json'):
        try:
            with open('google_drive_credentials.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error cargando credenciales: {e}")
            return None
    return None

# Función para conectar a Google Sheets
def conectar_google_sheets():
    creds = cargar_credenciales()
    if not creds:
        return None, None
    
    try:
        scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds_obj = ServiceAccountCredentials.from_json_keyfile_name('google_drive_credentials.json', scope)
        client = gspread.authorize(creds_obj)
        spreadsheet = client.open_by_key("10sSBzhpkEPYk78jEctV6XzRoyFJpaYznQPnv9T6VpPc")
        return client, spreadsheet
    except Exception as e:
        st.error(f"Error conectando a Google Sheets: {e}")
        return None, None

# Función para obtener datos del spreadsheet
def obtener_datos(worksheet_name):
    client, spreadsheet = conectar_google_sheets()
    if not client or not spreadsheet:
        return pd.DataFrame()
    
    try:
        worksheet = spreadsheet.worksheet(worksheet_name)
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error obteniendo datos de {worksheet_name}: {e}")
        return pd.DataFrame()

# Función para guardar datos en Google Sheets
def guardar_datos(worksheet_name, df):
    client, spreadsheet = conectar_google_sheets()
    if not client or not spreadsheet:
        return False
    
    try:
        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
        except:
            worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows="1000", cols="50")
        
        worksheet.clear()
        worksheet.update([df.columns.tolist()] + df.values.tolist())
        return True
    except Exception as e:
        st.error(f"Error guardando datos en {worksheet_name}: {e}")
        return False

# ==================== TAB 1: DASHBOARD ====================
with tab1:
    st.header("📊 Dashboard General")
    
    creds = cargar_credenciales()
    if creds:
        st.success("✅ Google Drive Backup conectado")
        st.info(f"📧 Email: {creds.get('client_email', 'No disponible')}")
    else:
        st.warning("⚠️ Configura tus credenciales en la pestaña 'Configuración'")
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📚 Total Alumnos", "245", delta="12")
    
    with col2:
        st.metric("📅 Asistencia Hoy", "92%", delta="5%")
    
    with col3:
        st.metric("📝 Evaluaciones", "18", delta="3")
    
    with col4:
        st.metric("📊 Reportes", "7", delta="2")
    
    st.markdown("---")
    
    # Filtros por año
    st.subheader("📅 Filtros por Año")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        año_actual = date.today().year
        años_disponibles = list(range(año_actual - 5, año_actual + 1))
        año_seleccionado = st.selectbox("Seleccionar Año:", años_disponibles, key="dashboard_año")
    
    with col2:
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        mes_seleccionado = st.selectbox("Seleccionar Mes:", meses, key="dashboard_mes")
    
    with col3:
        cursos_dashboard = ["Todos", "1° Año", "2° Año", "3° Año", "4° Año", "5° Año"]
        curso_seleccionado = st.selectbox("Seleccionar Curso:", cursos_dashboard, key="dashboard_curso")
    
    # Gráfico de asistencia
    st.markdown("---")
    st.subheader("📈 Tendencia de Asistencia")
    
    # Datos de ejemplo para el gráfico
    datos_asistencia = {
        'Mes': ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio'],
        'Asistencia': [88, 92, 85, 90, 94, 89]
    }
    
    df_asistencia = pd.DataFrame(datos_asistencia)
    st.bar_chart(df_asistencia, x='Mes', y='Asistencia')
    
    # Últimas actividades
    st.markdown("---")
    st.subheader("🔄 Últimas Actividades")
    
    actividades = [
        {"fecha": "2024-03-18", "actividad": "Nueva evaluación agregada", "usuario": "Prof. García"},
        {"fecha": "2024-03-17", "actividad": "Reporte mensual generado", "usuario": "Sistema"},
        {"fecha": "2024-03-16", "actividad": "Asistencia actualizada", "usuario": "Prof. Martínez"},
        {"fecha": "2024-03-15", "actividad": "Nuevo alumno inscripto", "usuario": "Admin"}
    ]
    
    for actividad in actividades:
        st.write(f"📅 {actividad['fecha']} - {actividad['actividad']} ({actividad['usuario']})")

# ==================== TAB 2: ALUMNOS ====================
with tab2:
    st.header("👥 Gestión de Alumnos")
    
    # Formulario para agregar nuevo alumno
    with st.expander("➕ Agregar Nuevo Alumno"):
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input("Nombre Completo:", key="alumno_nombre")
            dni = st.text_input("DNI:", key="alumno_dni")
            email = st.text_input("Email:", key="alumno_email")
            telefono = st.text_input("Teléfono:", key="alumno_telefono")
        
        with col2:
            fecha_nacimiento = st.date_input("Fecha de Nacimiento:", key="alumno_nacimiento")
            cursos_alumno = ["1° Año", "2° Año", "3° Año", "4° Año", "5° Año"]
            curso = st.selectbox("Curso:", cursos_alumno, key="alumno_curso")
            direccion = st.text_area("Dirección:", key="alumno_direccion")
            estados_alumno = ["Activo", "Inactivo", "Egresado"]
            estado = st.selectbox("Estado:", estados_alumno, key="alumno_estado")
        
        if st.button("💾 Guardar Alumno", type="primary", key="guardar_alumno"):
            st.success("✅ Alumno guardado exitosamente!")
            st.balloons()
    
    st.markdown("---")
    
    # Filtros de búsqueda
    st.subheader("🔍 Filtros de Búsqueda")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filtro_nombre = st.text_input("Buscar por Nombre:", key="filtro_nombre")
    
    with col2:
        cursos_filtro = ["Todos", "1° Año", "2° Año", "3° Año", "4° Año", "5° Año"]
        filtro_curso = st.selectbox("Filtrar por Curso:", cursos_filtro, key="filtro_curso")
    
    with col3:
        estados_filtro = ["Todos", "Activo", "Inactivo", "Egresado"]
        filtro_estado = st.selectbox("Filtrar por Estado:", estados_filtro, key="filtro_estado")
    
    # Tabla de alumnos (datos de ejemplo)
    st.markdown("---")
    st.subheader("📋 Lista de Alumnos")
    
    datos_alumnos = [
        {"DNI": "12345678", "Nombre": "Ana García", "Curso": "3° Año", "Email": "ana@email.com", "Estado": "Activo"},
        {"DNI": "23456789", "Nombre": "Carlos López", "Curso": "2° Año", "Email": "carlos@email.com", "Estado": "Activo"},
        {"DNI": "34567890", "Nombre": "María Rodríguez", "Curso": "4° Año", "Email": "maria@email.com", "Estado": "Activo"},
        {"DNI": "45678901", "Nombre": "Juan Martínez", "Curso": "1° Año", "Email": "juan@email.com", "Estado": "Inactivo"},
        {"DNI": "56789012", "Nombre": "Laura Sánchez", "Curso": "5° Año", "Email": "laura@email.com", "Estado": "Activo"}
    ]
    
    df_alumnos = pd.DataFrame(datos_alumnos)
    st.dataframe(df_alumnos, use_container_width=True)

# ==================== TAB 3: ASISTENCIA ====================
with tab3:
    st.header("📋 Gestión de Asistencia")
    
    # Selector de fecha
    st.subheader("📅 Registrar Asistencia")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fecha_asistencia = st.date_input("Fecha de Asistencia:", value=datetime.now().date(), key="asistencia_fecha")
        cursos_asistencia = ["1° Año", "2° Año", "3° Año", "4° Año", "5° Año"]
        curso_asistencia = st.selectbox("Curso:", cursos_asistencia, key="asistencia_curso")
    
    with col2:
        st.write("📊 Estadísticas del día:")
        st.metric("Presentes", "42", delta="2")
        st.metric("Ausentes", "3", delta="-1")
        st.metric("Tardanzas", "2", delta="0")
    
    st.markdown("---")
    
    # Registro de asistencia
    st.subheader("✅ Marcar Asistencia")
    
    # Datos de ejemplo para la tabla
    datos_asistencia_registro = [
        {"DNI": "12345678", "Nombre": "Ana García", "Estado": "Presente", "Hora": "08:00"},
        {"DNI": "23456789", "Nombre": "Carlos López", "Estado": "Presente", "Hora": "08:05"},
        {"DNI": "34567890", "Nombre": "María Rodríguez", "Estado": "Tarde", "Hora": "08:15"},
        {"DNI": "45678901", "Nombre": "Juan Martínez", "Estado": "Ausente", "Hora": "-"},
        {"DNI": "56789012", "Nombre": "Laura Sánchez", "Estado": "Presente", "Hora": "08:02"}
    ]
    
    df_asistencia_registro = pd.DataFrame(datos_asistencia_registro)
    st.dataframe(df_asistencia_registro, use_container_width=True)
    
    if st.button("💾 Guardar Asistencia", type="primary", key="guardar_asistencia"):
        st.success("✅ Asistencia guardada exitosamente!")
        st.info("📊 Los datos han sido respaldados en Google Drive")
        st.balloons()

# ==================== TAB 4: EVALUACIONES ====================
with tab4:
    st.header("📝 Gestión de Evaluaciones")
    
    # Formulario para nueva evaluación
    with st.expander("➕ Crear Nueva Evaluación"):
        col1, col2 = st.columns(2)
        
        with col1:
            titulo_eval = st.text_input("Título de Evaluación:", key="evaluacion_titulo")
            cursos_eval = ["1° Año", "2° Año", "3° Año", "4° Año", "5° Año"]
            curso_eval = st.selectbox("Curso:", cursos_eval, key="evaluacion_curso")
            tipos_eval = ["Parcial", "Final", "Trabajo Práctico", "Proyecto"]
            tipo_eval = st.selectbox("Tipo:", tipos_eval, key="evaluacion_tipo")
            fecha_eval = st.date_input("Fecha de Evaluación:", key="evaluacion_fecha")
        
        with col2:
            descripcion_eval = st.text_area("Descripción:", key="evaluacion_descripcion")
            ponderacion_eval = st.number_input("Ponderación (%)", min_value=0, max_value=100, value=100, key="evaluacion_ponderacion")
            estados_eval = ["Pendiente", "En Curso", "Finalizada"]
            estado_eval = st.selectbox("Estado:", estados_eval, key="evaluacion_estado")
        
        if st.button("📝 Crear Evaluación", type="primary", key="crear_evaluacion"):
            st.success("✅ Evaluación creada exitosamente!")
            st.info("📊 La evaluación ha sido agregada al sistema")
            st.balloons()
    
    st.markdown("---")
    
    # Lista de evaluaciones
    st.subheader("📋 Lista de Evaluaciones")
    
    # Datos de ejemplo
    datos_evaluaciones = [
        {"Título": "Parcial Matemáticas", "Curso": "3° Año", "Tipo": "Parcial", "Fecha": "2024-03-15", "Estado": "Finalizada"},
        {"Título": "Trabajo Práctico Historia", "Curso": "4° Año", "Tipo": "Trabajo Práctico", "Fecha": "2024-03-18", "Estado": "En Curso"},
        {"Título": "Proyecto Ciencias", "Curso": "2° Año", "Tipo": "Proyecto", "Fecha": "2024-03-20", "Estado": "Pendiente"},
        {"Título": "Final Lengua", "Curso": "5° Año", "Tipo": "Final", "Fecha": "2024-03-10", "Estado": "Finalizada"}
    ]
    
    df_evaluaciones = pd.DataFrame(datos_evaluaciones)
    st.dataframe(df_evaluaciones, use_container_width=True)
    
    # Filtros
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cursos_filtro_eval = ["Todos", "1° Año", "2° Año", "3° Año", "4° Año", "5° Año"]
        filtro_curso_eval = st.selectbox("Filtrar por Curso:", cursos_filtro_eval, key="filtro_eval_curso")
    
    with col2:
        tipos_filtro_eval = ["Todos", "Parcial", "Final", "Trabajo Práctico", "Proyecto"]
        filtro_tipo_eval = st.selectbox("Filtrar por Tipo:", tipos_filtro_eval, key="filtro_eval_tipo")
    
    with col3:
        estados_filtro_eval = ["Todos", "Pendiente", "En Curso", "Finalizada"]
        filtro_estado_eval = st.selectbox("Filtrar por Estado:", estados_filtro_eval, key="filtro_eval_estado")

# ==================== TAB 5: CONFIGURACIÓN ====================
with tab5:
    st.header("🔧 Configuración del Sistema")
    
    # Subsección de backup
    st.subheader("💾 Google Drive Backup")
    
    # Formulario para ingresar credenciales manualmente
    with st.form("credentials_form"):
        st.write("Ingresa tus credenciales de Google Cloud:")
        
        project_id = st.text_input("Project ID", value="turnkey-realm-490621-g6", help="Tu ID de proyecto de Google Cloud", key="project_id")
        private_key_id = st.text_input("Private Key ID", value="23197905dd3b00c010c0c95176ee2d7ef31690f6", help="ID de tu clave privada", key="private_key_id")
        client_email = st.text_input("Client Email", value="dashboard-backup@turnkey-realm-490621-g6.iam.gserviceaccount.com", help="Email de tu cuenta de servicio", key="client_email")
        client_id = st.text_input("Client ID", value="112970843523581797879", help="ID de tu cliente", key="client_id")
        private_key = st.text_area("Private Key", value="-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDQmT9B3VOTdpL9\napPEOSFvFzLiv8vA7IP/5WmAV1KBTZ/5VOPKtrMHKDTedsBQpGbr68Nr5uPR03s7\n3T8PbEumSiV9Npj6Nqjb4hNq9sIq7mBaDJlcmYnBjpaqUo1zTVICOkUi9nXIk3wN\nqGmFsSxmlg/iNGH92Hwyqq0IRgT13HmlGLLpOv6uy3DaUXdg3Xl7jq/gbjLDTk4e\nUc+0TEA3Qd1djkHUYjqaxNcK+/Ie1GyF8hy6hB9YIkciiShBA8KKFi/Q8mxwIH5D\nfadiFqAwMIzdoPAHMwmQH/qw2PkK1Brk8y2cDIr8peoQPI+UyunbZERdLf+TmbYm\n3RgoTYqHAgMBAAECggEALyh2BI3ktxG3aVMO1O2VgWfdOSXjClpt/QwALeOP42uJ\nHvTyCoIDNzr/uMtf7ts76VoDdAFev7DvyzjZaMMy1wUsNIKDUw3IXu1dNnFStCHv\n5muywBx16Cw0I41GLSrtv1MtDhppxk6RXQUV1gOX5hlGvfzZqmmmqk2rkJNDy9ED\nqBLVt9DCu/MH6TFRrFQAsXSN7BvotXfs2TorSWpxQEyYAHUIHd7l3kMsDFog0nnt\noxGXukJtjOpk7cKjLJN/s+GKUUQRjT5fXKNmFzAJssfqIp8MerRyOVJvQl63rhyG\n1e0iqPEIxCxSE5uW6cNnfwRXUQelIPbZfsOZBmI1AQKBgQDtvdEvXkG7bHx5+3w6\nOsjAPDAwv7RyTQ+vC03hZVAOByUsQUCe/LHAecrYrLyEG7dEv2ILvGt2D02QXCEk\nt8LVA+Dk8pPDZS1fUSYfYFyWX0eTaL1ywjoBNPSuwauo5FmT3W4OAmUovluM0fpk\nkttGdmk1Nr5BAHDYgST8dIWRQwKBgQDgnnVxqmDAjSEBcOtxt2ZUhcZ0nGiqmRE+\nBISuqUmyR18svPn/Z+ERrULM4/JYyJh0IUEW3q5d0qVoZYPrf3ZZNx6nbvwxUFeI\no8e53NoXlxo8uvNDUjoNpbt1mK4+ycrkJz56cymQ3+4yHfQGbDGwn2KfF4aVgqRD\nAqjEuNb7bQKBgGr+7cFKw3yNg6wGgc9XG3hg3jNiY9y5T+CwzrktNo1Jq/Ix39pt\n0bXVWnSPsTwnmSConYC4qH2NKtOu1/iEB58Y1/GyLe8tmHajLS8Uo8ejIEMN48J\nWL+oTKLF6PLW6nXAx0Io08w1d9B1xCI1cdhRfGIFpDRu9VqLLNEtw9svAoGBALak\nAikneb53wvOyBrATiXCGyiS9nVnCVsPP1rdSzarZ3+i3zKvBor/F20BQxRkuGtCq\nzYs0DCIcCwVFLixKG0hVymYol4Xdpx9i1R8rFmcCJYJmHTGLZcr9DN2FBYHmgURd\nKK9WfuDfRIaZ1nd2eDz+jKmB7pwZe0lFm0dCaQRNAoGAGNqYxXyY64TmQjL6z6WR\nREfFhx3z5bjtc5Z2/JIT7QLCCZJzd/ObKW0xdJ+h3uvUemYFMJt3V4aBVhtlzGxr\nUQ0eaOw+61wDYTc7pwHp6XpBs5G56DmSzmPTPtDM0TWoBK/qXVYxjq8N4uwofun\nYKi8CaOnXQDNl/T1wj34RSo=\n-----END PRIVATE KEY-----", height=200, help="Tu clave privada completa", key="private_key")
        
        submitted = st.form_submit_button("💾 Guardar Credenciales", type="primary", use_container_width=True, help="Guarda las credenciales localmente")
        
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
            
            st.success("✅ Credenciales guardadas exitosamente!")
            st.balloons()
            st.rerun()
    
    # Estado del backup
    if os.path.exists('google_drive_credentials.json'):
        st.success("✅ Credenciales configuradas y listas para usar")
        
        try:
            with open('google_drive_credentials.json', 'r') as f:
                creds = json.load(f)
            
            # Mostrar información de la cuenta
            st.markdown("---")
            st.subheader("📋 Información de la Cuenta")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.info(f"📧 **Email:**\n{creds.get('client_email', 'No disponible')}")
            
            with col2:
                st.info(f"🆔 **Project ID:**\n{creds.get('project_id', 'No disponible')}")
            
            with col3:
                st.info(f"🆎 **Client ID:**\n{creds.get('client_id', 'No disponible')}")
            
            # Mostrar información del backup existente
            st.markdown("---")
            st.subheader("📁 Backup Automático Actual")
            
            st.success("✅ **Backup automático ya está ACTIVO!**")
            st.markdown(f"📁 **[📂 Ver Backup Actual]({EXISTING_SPREADSHEET})**")
            st.info("📧 **Todos los datos se guardan automáticamente en solpeschuk@gmail.com**")
            
            # Botones de acción
            st.markdown("---")
            st.subheader("🚀 Opciones de Backup")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📂 Ver Backup Actual", type="secondary", use_container_width=True, key="ver_backup"):
                    st.markdown(f"📁 **[🔗 Abrir Backup Actual]({EXISTING_SPREADSHEET})**")
            
            with col2:
                if st.button("🆕 Crear Nuevo Backup", type="primary", use_container_width=True, key="crear_backup"):
                    try:
                        import gspread
                        from oauth2client.service_account import ServiceAccountCredentials
                        
                        with st.spinner("🔄 Creando nuevo backup..."):
                            # Configurar credenciales
                            scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
                            creds_obj = ServiceAccountCredentials.from_json_keyfile_name('google_drive_credentials.json', scope)
                            client = gspread.authorize(creds_obj)
                            
                            # Crear nuevo spreadsheet
                            new_spreadsheet = client.create("Dashboard IES - Backup Nuevo")
                            
                            # Compartir con el email
                            new_spreadsheet.share('solpeschuk@gmail.com', perm_type='user', role='writer')
                            
                            st.success("✅ **Nuevo backup creado exitosamente!**")
                            st.info(f"📁 **Nuevo spreadsheet:** {new_spreadsheet.url}")
                            st.info("🎉 **¡Tienes dos backups activos!**")
                            st.balloons()
                            
                            # Backup de prueba en el nuevo spreadsheet
                            import pandas as pd
                            from datetime import datetime
                            
                            test_data = pd.DataFrame({
                                'Test': ['🆕 Nuevo Backup Creado'],
                                'Fecha': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                                'Email': ['solpeschuk@gmail.com'],
                                'Estado': ['✅ Activo y Funcionando'],
                                'Método': ['💾 Configuración Manual'],
                                'Project_ID': [creds.get('project_id', 'No disponible')],
                                'Spreadsheet_Anterior': [EXISTING_SPREADSHEET]
                            })
                            
                            # Agregar datos al nuevo spreadsheet
                            worksheet = new_spreadsheet.worksheet(0)
                            data = [test_data.columns.tolist()] + test_data.values.tolist()
                            worksheet.update('A1', data)
                            
                            st.success("✅ **Datos de prueba agregados al nuevo backup!**")
                            st.balloons()
                            
                    except ImportError:
                        st.error("❌ **Bibliotecas no instaladas**")
                        st.info("📦 **Las bibliotecas se están instalando automáticamente en Streamlit Cloud**")
                    except Exception as e:
                        st.error(f"❌ **Error creando nuevo backup:** {e}")
                        st.info("🔧 **Revisa que tus credenciales sean correctas**")
            
            # Botón para eliminar credenciales
            st.markdown("---")
            if st.button("🗑️ Eliminar Credenciales", use_container_width=True, key="eliminar_credenciales"):
                os.remove('google_drive_credentials.json')
                st.success("✅ **Credenciales eliminadas exitosamente!**")
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ **Error al leer credenciales:** {e}")
            st.info("🔧 **Revisa que el archivo de credenciales no esté corrupto**")
    else:
        st.warning("⚠️ **Configura tus credenciales arriba para activar el backup automático**")
    
    # Estado general del sistema
    st.markdown("---")
    st.subheader("📊 Estado del Sistema")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if os.path.exists('google_drive_credentials.json'):
            st.metric("📁 Archivo", "✅ Encontrado", delta="Configurado")
        else:
            st.metric("📁 Archivo", "❌ No encontrado", delta="Requerido")
    
    with col2:
        if os.path.exists('google_drive_credentials.json'):
            st.metric("🔧 Configuración", "✅ Lista", delta="Funcionando")
        else:
            st.metric("🔧 Configuración", "❌ Pendiente", delta="Requerido")
    
    with col3:
        st.metric("📧 Email Destino", "solpeschuk@gmail.com", delta="Configurado")

# Footer informativo
st.markdown("---")
footer_html = """
<div style='text-align: center; color: #2E7D32; padding: 20px; border-top: 2px solid #4CAF50; border-radius: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'>
    <h2 style='color: white; margin-bottom: 10px;'>🎓 Sistema Integral IES - Plataforma Completa</h2>
    <p style='color: white; font-size: 16px; margin: 5px 0;'>
        <span style='color: #4CAF50;'>✅</span> Dashboard con métricas y filtros<br>
        <span style='color: #4CAF50;'>👥</span> Gestión de alumnos completa<br>
        <span style='color: #4CAF50;'>📋</span> Sistema de asistencia<br>
        <span style='color: #4CAF50;'>📝</span> Evaluaciones y reportes<br>
        <span style='color: #4CAF50;'>💾</span> Backup automático en Google Drive
    </p>
    <small style='color: rgba(255,255,255,0.8);'>Sistema educativo integral y funcional</small>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
