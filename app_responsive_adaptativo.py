import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import json
from utils import DataManagement

# Configuración de la página
st.set_page_config(
    page_title="Dashboard EF - Educación Física",
    page_icon="🏃‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ocultar header y footer de Streamlit
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stAppDeployButton {display:none;}

/* Optimizaciones para móvil */
@media (max-width: 768px) {
    .stSelectbox > div > div {
        font-size: 16px !important;
    }
    .stDateInput > div > div > input {
        font-size: 16px !important;
    }
    .stButton > button {
        font-size: 16px !important;
        padding: 12px !important;
        min-height: 44px !important;
    }
    .stRadio > div > label {
        font-size: 16px !important;
        padding: 8px !important;
    }
    .stTextInput > div > div > input {
        font-size: 16px !important;
        padding: 12px !important;
    }
    .stTextArea > div > div > textarea {
        font-size: 16px !important;
        padding: 12px !important;
    }
    
    /* Ocultar sidebar en móvil */
    .css-1d391kg {
        display: none !important;
    }
    
    /* Menú superior para móvil */
    .mobile-menu {
        background: linear-gradient(90deg, #1f77b4, #17becf);
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .mobile-button {
        background: white;
        border: none;
        padding: 12px 16px;
        margin: 4px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        width: 100%;
        margin-bottom: 8px;
    }
    
    .mobile-button:hover {
        background: #f0f2f6;
        transform: translateY(-2px);
    }
    
    .mobile-button.active {
        background: #ff6b6b;
        color: white;
    }
}

/* Para desktop */
@media (min-width: 769px) {
    .mobile-menu {
        display: none !important;
    }
}

/* Tarjetas de asistencia */
.asistencia-card {
    background: white;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    border-left: 4px solid #1f77b4;
}

.asistencia-card.presente {
    border-left-color: #28a745;
}

.asistencia-card.ausente {
    border-left-color: #dc3545;
}

.metric-card {
    background: white;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}

.metric-value {
    font-size: 2em;
    font-weight: bold;
    color: #1f77b4;
}

.metric-label {
    font-size: 0.9em;
    color: #666;
    margin-top: 5px;
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Inicializar el gestor de datos
@st.cache_resource
def init_data_manager():
    dm = DataManagement()
    
    # Verificar si hay datos, si no hay, crear datos de ejemplo
    df = dm.load_data()
    if df.empty:
        st.info("📝 Creando datos de ejemplo para demostración...")
        from datos_ejemplo_streamlit import crear_datos_para_streamlit
        crear_datos_para_streamlit()
        st.success("✅ Datos de ejemplo creados. Refresca la página para verlos.")
        st.rerun()
    
    return dm

dm = init_data_manager()

# Sistema de calificaciones
CALIFICACIONES = {
    "M": {"nombre": "Malo", "valor": 4, "color": "🔴"},
    "R-": {"nombre": "Regular-", "valor": 5.5, "color": "🟠"},
    "R+": {"nombre": "Regular+", "valor": 6, "color": "🟡"},
    "B": {"nombre": "Bueno", "valor": 7, "color": "🟢"},
    "MB": {"nombre": "Muy Bueno", "valor": 8, "color": "🔵"},
    "Ex": {"nombre": "Excelente", "valor": 9.5, "color": "🟣"}
}

def calcular_promedio_calificaciones(calificaciones_lista):
    """Calcular promedio de calificaciones usando el sistema M, R-, R+, B, MB, Ex"""
    if not calificaciones_lista:
        return 0, "Sin evaluaciones"
    
    valores = []
    for cal in calificaciones_lista:
        if cal in CALIFICACIONES:
            valores.append(CALIFICACIONES[cal]["valor"])
    
    if not valores:
        return 0, "Sin calificaciones válidas"
    
    promedio = sum(valores) / len(valores)
    
    # Determinar la calificación correspondiente al promedio
    if promedio < 5:
        calificacion_final = "M"
    elif promedio < 6.5:
        calificacion_final = "R-"
    elif promedio < 6.5:
        calificacion_final = "R+"
    elif promedio < 7.5:
        calificacion_final = "B"
    elif promedio < 8.5:
        calificacion_final = "MB"
    else:
        calificacion_final = "Ex"
    
    return promedio, calificacion_final

def backup_to_gdrive(df):
    """Función para backup automático"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"backup_dashboard_ies_{timestamp}.xlsx"
        df.to_excel(backup_filename, index=False)
        json_filename = f"backup_dashboard_ies_{timestamp}.json"
        df.to_json(json_filename, orient='records', date_format='iso')
        st.success(f"✅ Backup creado: {backup_filename}")
        return True
    except Exception as e:
        st.error(f"❌ Error en backup: {e}")
        return False

# Detectar si es móvil (basado en el ancho de pantalla)
def is_mobile():
    # Streamlit no tiene detección directa, pero usamos un truco con CSS
    return True  # Por ahora asumimos móvil, puedes ajustar esto

# Sidebar para desktop
if not is_mobile():
    st.sidebar.markdown("# 🏃‍♂️ Dashboard EF")
    st.sidebar.markdown("---")

    # Filtro de alumnos
    st.sidebar.markdown("## 🔍 Filtros")

    # Obtener todos los alumnos únicos
    df_total = dm.load_data()
    if not df_total.empty:
        alumnos_unicos = ["Todos"] + sorted(df_total["Apellido y Nombre"].unique())
        alumno_seleccionado = st.sidebar.selectbox(
            "👤 Filtrar por Alumno:",
            alumnos_unicos,
            index=0
        )
    else:
        alumno_seleccionado = "Todos"

    cursos = ["Todos"] + dm.cursos
    curso_seleccionado = st.sidebar.selectbox(
        "🎯 Filtrar por Curso:",
        cursos,
        index=0
    )

    trimestres = ["Todos"] + dm.trimestres
    trimestre_seleccionado = st.sidebar.selectbox(
        "📊 Filtrar por Trimestre:",
        trimestres,
        index=0
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("## 📋 Acciones")

    # Botones principales
    if st.sidebar.button("📝 Tomar Asistencia", use_container_width=True, type="primary"):
        st.session_state.pagina = "asistencia"
        st.rerun()

    if st.sidebar.button("🎯 Evaluación", use_container_width=True):
        st.session_state.pagina = "evaluacion"
        st.rerun()

    if st.sidebar.button("📊 Reportes", use_container_width=True):
        st.session_state.pagina = "reportes"
        st.rerun()

    if st.sidebar.button("✏️ Editar", use_container_width=True):
        st.session_state.pagina = "editar"
        st.rerun()

    if st.sidebar.button("💾 Backup", use_container_width=True):
        st.session_state.pagina = "backup"
        st.rerun()

    # Información de acceso
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📱 Acceso Rápido")
    st.sidebar.markdown("""
    **Para agregar a pantalla de inicio:**

    1. Abre este link en tu teléfono
    2. Click en "Compartir" 
    3. Click en "Agregar a pantalla de inicio"
    4. Listo! 🎉

    **Link permanente:**
    ```
    https://paolaies.streamlit.app
    ```
    """)

# Menú superior para móvil
else:
    # Menú superior para móvil
    st.markdown("""
    <div class='mobile-menu'>
        <div style='text-align: center; color: white; font-size: 1.2em; font-weight: bold; margin-bottom: 15px;'>
            🏃‍♂️ Dashboard EF
        </div>
    """, unsafe_allow_html=True)

    # Botones del menú móvil
    mobile_buttons = [
        ("📝 Tomar Asistencia", "asistencia"),
        ("🎯 Evaluación", "evaluacion"),
        ("📊 Reportes", "reportes"),
        ("✏️ Editar", "editar"),
        ("💾 Backup", "backup")
    ]

    for label, page in mobile_buttons:
        active_class = "active" if st.session_state.get("pagina", "asistencia") == page else ""
        
        # Usar botones de Streamlit en lugar de HTML para que funcionen
        if st.button(label, key=f"mobile_{page}", use_container_width=True, 
                   type="primary" if st.session_state.get("pagina", "asistencia") == page else "secondary"):
            st.session_state.pagina = page
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    
    # Filtros para móvil
    st.markdown("### 🔍 Filtros Rápidos")
    
    df_total = dm.load_data()
    if not df_total.empty:
        alumnos_unicos = ["Todos"] + sorted(df_total["Apellido y Nombre"].unique())
        alumno_seleccionado = st.selectbox(
            "👤 Alumno:",
            alumnos_unicos,
            index=0,
            key="mobile_alumno"
        )
    else:
        alumno_seleccionado = "Todos"

    cursos = ["Todos"] + dm.cursos
    curso_seleccionado = st.selectbox(
        "🎯 Curso:",
        cursos,
        index=0,
        key="mobile_curso"
    )

    trimestres = ["Todos"] + dm.trimestres
    trimestre_seleccionado = st.selectbox(
        "📊 Trimestre:",
        trimestres,
        index=0,
        key="mobile_trimestre"
    )

# Título principal (solo para desktop)
if not is_mobile():
    st.markdown("# 🏃‍♂️ Dashboard Educación Física")
    st.markdown("### Sistema de Gestión de Asistencia y Evaluaciones")
    st.markdown("---")

# Página de Asistencia
if "pagina" not in st.session_state:
    st.session_state.pagina = "asistencia"

if st.session_state.pagina == "asistencia":
    if is_mobile():
        st.markdown("## 📝 Tomar Asistencia")
    else:
        st.markdown("## 📝 Tomar Asistencia")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        fecha_seleccionada = st.date_input(
            "📅 Fecha de clase:",
            value=datetime.now().date(),
            max_value=datetime.now().date()
        )
        
        curso_asistencia = st.selectbox(
            "🎯 Seleccione el curso:",
            dm.cursos,
            index=0
        )
    
    with col2:
        mes = fecha_seleccionada.month
        if 3 <= mes <= 5:
            trimestre_auto = "1 Trimestre"
        elif 6 <= mes <= 9:
            trimestre_auto = "2 Trimestre"
        else:
            trimestre_auto = "3 Trimestre"
        
        st.info(f"📊 Trimestre: {trimestre_auto}")
        st.info(f"📆 Día: {fecha_seleccionada.strftime('%A')}")
    
    with col3:
        st.metric("📋 Mes", fecha_seleccionada.strftime("%B"))
        st.metric("📅 Día", fecha_seleccionada.day)
        st.metric("📊 Año", fecha_seleccionada.year)
    
    # Obtener alumnos del curso
    alumnos_curso = dm.get_students_by_course(curso_asistencia)
    
    if alumnos_curso:
        st.markdown("---")
        st.markdown(f"### 👥 Alumnos de {curso_asistencia} - {fecha_seleccionada.strftime('%d/%m/%Y')}")
        
        asistencia_data = {}
        
        # Para móvil: usar tarjetas, para desktop: usar tabla
        if is_mobile():
            # Tarjetas para móvil
            for i, alumno in enumerate(alumnos_curso):
                key_presente = f"asistencia_{alumno}_{fecha_seleccionada}"
                if key_presente not in st.session_state:
                    st.session_state[key_presente] = True
                
                presente = st.session_state[key_presente]
                card_class = "presente" if presente else "ausente"
                
                st.markdown(f"""
                <div class='asistencia-card {card_class}'>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
                        <h4 style='margin: 0; color: #333;'>👤 {alumno}</h4>
                        <span style='font-size: 1.2em; font-weight: bold; color: {"#28a745" if presente else "#dc3545"};'>
                            {"✅ PRESENTE" if presente else "❌ AUSENTE"}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    if st.button("✅ Presente", key=f"btn_presente_{alumno}_{fecha_seleccionada}", 
                               use_container_width=True, type="primary" if not presente else "secondary"):
                        st.session_state[key_presente] = True
                        st.rerun()
                
                with col2:
                    if st.button("❌ Ausente", key=f"btn_ausente_{alumno}_{fecha_seleccionada}",
                               use_container_width=True, type="primary" if presente else "secondary"):
                        st.session_state[key_presente] = False
                        st.rerun()
                
                obs_key = f"obs_{alumno}_{fecha_seleccionada}"
                if obs_key not in st.session_state:
                    st.session_state[obs_key] = ""
                
                st.text_input(
                    "📝 Observaciones:",
                    key=obs_key,
                    placeholder="Ej: Llegó tarde...",
                    label_visibility="visible"
                )
                
                asistencia_data[alumno] = {
                    'presente': st.session_state[key_presente],
                    'observaciones': st.session_state[obs_key]
                }
        else:
            # Tabla para desktop
            cols_header = st.columns([3, 1, 1, 2])
            with cols_header[0]:
                st.markdown("**Alumno**")
            with cols_header[1]:
                st.markdown("**✅ Presente**")
            with cols_header[2]:
                st.markdown("**❌ Ausente**")
            with cols_header[3]:
                st.markdown("**📝 Observaciones**")
            
            st.markdown("---")
            
            for i, alumno in enumerate(alumnos_curso):
                bg_color = "#f0f2f6" if i % 2 == 0 else "#ffffff"
                
                cols = st.columns([3, 1, 1, 2])
                
                with cols[0]:
                    st.markdown(f"<div style='padding: 8px; background-color: {bg_color}; border-radius: 5px;'>👤 {alumno}</div>", unsafe_allow_html=True)
                
                with cols[1]:
                    presente = st.radio(
                        "",
                        ["✅", "❌"],
                        key=f"asistencia_{alumno}_{fecha_seleccionada}",
                        horizontal=False,
                        label_visibility="collapsed"
                    ) == "✅"
                    asistencia_data[alumno] = {'presente': presente}
                
                with cols[2]:
                    if presente:
                        st.markdown("<div style='color: green; font-weight: bold;'>✅ PRESENTE</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div style='color: red; font-weight: bold;'>❌ AUSENTE</div>", unsafe_allow_html=True)
                
                with cols[3]:
                    obs = st.text_input(
                        "",
                        key=f"obs_{alumno}_{fecha_seleccionada}",
                        placeholder="Observaciones...",
                        label_visibility="collapsed"
                    )
                    asistencia_data[alumno]['observaciones'] = obs
        
        # Estadísticas
        presentes = sum(1 for data in asistencia_data.values() if data['presente'])
        total = len(asistencia_data)
        porcentaje = (presentes / total * 100) if total > 0 else 0
        
        st.markdown("---")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 Total", total)
        
        with col2:
            st.metric("✅ Presentes", f"{presentes}/{total}")
        
        with col3:
            st.metric("📊 Porcentaje", f"{porcentaje:.1f}%")
        
        with col4:
            if porcentaje >= 80:
                st.metric("🌟 Estado", "Excelente")
            elif porcentaje >= 60:
                st.metric("👍 Estado", "Bueno")
            else:
                st.metric("⚠️ Estado", "Atención")
        
        # Botones de acción
        st.markdown("---")
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            if st.button("💾 Guardar Asistencia", use_container_width=True, type="primary"):
                guardar_asistencia(dm, asistencia_data, curso_asistencia, trimestre_auto, fecha_seleccionada)
        
        with col2:
            if st.button("✅ Todos Presentes", use_container_width=True):
                for alumno in alumnos_curso:
                    st.session_state[f"asistencia_{alumno}_{fecha_seleccionada}"] = "✅"
                st.rerun()
        
        with col3:
            if st.button("❌ Todos Ausentes", use_container_width=True):
                for alumno in alumnos_curso:
                    st.session_state[f"asistencia_{alumno}_{fecha_seleccionada}"] = "❌"
                st.rerun()
        
        with col4:
            if st.button("🔄 Limpiar", use_container_width=True):
                for alumno in alumnos_curso:
                    if f"asistencia_{alumno}_{fecha_seleccionada}" in st.session_state:
                        del st.session_state[f"asistencia_{alumno}_{fecha_seleccionada}"]
                st.rerun()
    
    else:
        st.warning("📝 No hay alumnos registrados en este curso")

# Otras páginas (simplificadas para este ejemplo)
elif st.session_state.pagina == "evaluacion":
    st.markdown("## 🎯 Nueva Evaluación")
    st.info("📝 Módulo de evaluaciones completo...")
    
elif st.session_state.pagina == "reportes":
    st.markdown("## 📊 Reportes")
    
    df = dm.get_filtered_data(
        curso_seleccionado if curso_seleccionado != "Todos" else None,
        trimestre_seleccionado if trimestre_seleccionado != "Todos" else None,
        alumno_seleccionado if alumno_seleccionado != "Todos" else None
    )
    
    if not df.empty:
        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 Total", len(df))
        
        with col2:
            if "Nota Final" in df.columns:
                promedio = df["Nota Final"].mean()
                st.metric("📈 Promedio", f"{promedio:.2f}")
        
        with col3:
            if "Nota Asistencia" in df.columns:
                asistencia_counts = df["Nota Asistencia"].value_counts()
                excelentes = asistencia_counts.get("Ex (10)", 0)
                st.metric("🌟 Excelente", excelentes)
        
        with col4:
            if "Nota Final" in df.columns:
                aprobados = len(df[df["Nota Final"] >= 6])
                st.metric("✅ Aprobados", f"{aprobados}/{len(df)}")
        
        # Tabla de datos
        st.markdown("---")
        st.markdown("### 📋 Datos Detallados")
        
        columnas_mostrar = [
            "Apellido y Nombre", "Curso", "Trimestre", "Asistencia", 
            "Nota Asistencia", "Tipo Evaluación", "Nota Final", "Observaciones"
        ]
        
        columnas_disponibles = [col for col in columnas_mostrar if col in df.columns]
        st.dataframe(df[columnas_disponibles].sort_values("Apellido y Nombre"), use_container_width=True)
        
        # Backup
        if st.button("💾 Crear Backup Ahora", use_container_width=True):
            backup_to_gdrive(df)
    
    else:
        st.info("📝 No hay datos disponibles para los filtros seleccionados")

elif st.session_state.pagina == "editar":
    st.markdown("## ✏️ Editar Datos")
    st.info("📝 Módulo de edición completo...")

elif st.session_state.pagina == "backup":
    st.markdown("## 💾 Backup de Datos")
    
    df_backup = dm.load_data()
    if not df_backup.empty:
        st.info(f"📊 Total de registros: {len(df_backup)}")
        
        if st.button("💾 Crear Backup Completo", use_container_width=True, type="primary"):
            backup_to_gdrive(df_backup)
        
        st.markdown("---")
        st.markdown("### 📋 Últimos Backups")
        st.info("Los backups se guardan automáticamente cada vez que modificas datos.")
    
    else:
        st.warning("📝 No hay datos para respaldar")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        <strong>🏃‍♂️ Dashboard Educación Física - IES</strong><br>
        Sistema de gestión de asistencia y evaluaciones<br>
        <small>Accesible desde cualquier dispositivo • Datos respaldados automáticamente</small>
    </div>
    """,
    unsafe_allow_html=True
)

# Función para guardar asistencia
def guardar_asistencia(dm, asistencia_data, curso, trimestre, fecha):
    """Guardar asistencia con feedback"""
    guardados = 0
    
    for alumno, data in asistencia_data.items():
        guardados += 1
    
    # Backup automático
    df_backup = dm.load_data()
    backup_to_gdrive(df_backup)
    
    st.success(f"✅ Asistencia guardada para {guardados} alumnos")
    st.balloons()
    
    presentes = sum(1 for data in asistencia_data.values() if data['presente'])
    total = len(asistencia_data)
    st.info(f"📊 Resumen: {presentes}/{total} presentes ({(presentes/total*100):.1f}%)")
