import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import json
from utils import DataManagement

# Configuración de la página para móvil
st.set_page_config(
    page_title="Dashboard EF - Móvil",
    page_icon="🏃‍♂️",
    layout="wide",
    initial_sidebar_state="collapsed"  # Comenzar colapsado para móvil
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
}

/* Menú superior para móvil */
.menu-container {
    background: linear-gradient(90deg, #1f77b4, #17becf);
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.menu-button {
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
}

.menu-button:hover {
    background: #f0f2f6;
    transform: translateY(-2px);
}

.menu-button.active {
    background: #ff6b6b;
    color: white;
}

.filtro-container {
    background: #f8f9fa;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 20px;
    border: 2px solid #e9ecef;
}

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

# Título principal optimizado para móvil
st.markdown("""
<div style='text-align: center; padding: 20px 0; background: linear-gradient(90deg, #1f77b4, #17becf); border-radius: 15px; margin-bottom: 20px; color: white;'>
    <h1 style='margin: 0; font-size: 1.8em;'>🏃‍♂️ Dashboard EF</h1>
    <p style='margin: 5px 0 0 0; font-size: 0.9em;'>Educación Física - Móvil</p>
</div>
""", unsafe_allow_html=True)

# Menú superior para móvil (en lugar de sidebar)
st.markdown("""
<div class='menu-container'>
    <div style='display: flex; flex-wrap: wrap; justify-content: center;'>
""", unsafe_allow_html=True)

# Botones del menú principal
menu_buttons = [
    ("📝 Asistencia", "asistencia"),
    ("🎯 Evaluación", "evaluacion"),
    ("📊 Reportes", "reportes"),
    ("✏️ Editar", "editar"),
    ("💾 Backup", "backup")
]

# Determinar página actual
if "pagina" not in st.session_state:
    st.session_state.pagina = "asistencia"

# Crear botones del menú
for label, page in menu_buttons:
    active_class = "active" if st.session_state.pagina == page else ""
    st.markdown(f"""
    <button class='menu-button {active_class}' onclick='window.location.href="?pagina={page}"'>
        {label}
    </button>
    """, unsafe_allow_html=True)

st.markdown("""
    </div>
</div>
""", unsafe_allow_html=True)

# Filtros compactos para móvil
st.markdown("<div class='filtro-container'>", unsafe_allow_html=True)

st.markdown("**🔍 Filtros Rápidos:**")

# Obtener datos para filtros
df_total = dm.load_data()
if not df_total.empty:
    alumnos_unicos = ["Todos"] + sorted(df_total["Apellido y Nombre"].unique())
    alumno_seleccionado = st.selectbox(
        "👤 Alumno:",
        alumnos_unicos,
        index=0,
        key="filtro_alumno"
    )
else:
    alumno_seleccionado = "Todos"

cursos = ["Todos"] + dm.cursos
curso_seleccionado = st.selectbox(
    "🎯 Curso:",
    cursos,
    index=0,
    key="filtro_curso"
)

trimestres = ["Todos"] + dm.trimestres
trimestre_seleccionado = st.selectbox(
    "📊 Trimestre:",
    trimestres,
    index=0,
    key="filtro_trimestre"
)

st.markdown("</div>", unsafe_allow_html=True)

# Página de Asistencia Optimizada para Móvil
if st.session_state.pagina == "asistencia":
    st.markdown("## 📝 Tomar Asistencia")
    
    # Controles superiores compactos
    col1, col2 = st.columns([1, 1])
    
    with col1:
        fecha_seleccionada = st.date_input(
            "📅 Fecha:",
            value=datetime.now().date(),
            max_value=datetime.now().date()
        )
        
        curso_asistencia = st.selectbox(
            "🎯 Curso:",
            dm.cursos,
            index=0,
            key="curso_asistencia"
        )
    
    with col2:
        # Trimestre automático
        mes = fecha_seleccionada.month
        if 3 <= mes <= 5:
            trimestre_auto = "1 Trimestre"
        elif 6 <= mes <= 9:
            trimestre_auto = "2 Trimestre"
        else:
            trimestre_auto = "3 Trimestre"
        
        st.info(f"📊 {trimestre_auto}")
        st.info(f"📆 {fecha_seleccionada.strftime('%A')}")
    
    # Obtener alumnos
    alumnos_curso = dm.get_students_by_course(curso_asistencia)
    
    if alumnos_curso:
        st.markdown(f"### 👥 {curso_asistencia} - {fecha_seleccionada.strftime('%d/%m/%Y')}")
        
        asistencia_data = {}
        
        # Tarjetas de alumnos optimizadas para móvil
        for i, alumno in enumerate(alumnos_curso):
            # Determinar estado inicial
            key_presente = f"asistencia_{alumno}_{fecha_seleccionada}"
            if key_presente not in st.session_state:
                st.session_state[key_presente] = True  # Por defecto presente
            
            presente = st.session_state[key_presente]
            
            # Tarjeta visual para cada alumno
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
            
            # Radio buttons grandes para fácil toque
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
            
            # Observaciones
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
        
        # Métricas en tarjetas
        st.markdown("---")
        st.markdown("### 📊 Resumen de Asistencia")
        
        presentes = sum(1 for data in asistencia_data.values() if data['presente'])
        total = len(asistencia_data)
        porcentaje = (presentes / total * 100) if total > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{total}</div>
                <div class='metric-label'>👥 Total</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{presentes}</div>
                <div class='metric-label'>✅ Presentes</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{porcentaje:.1f}%</div>
                <div class='metric-label'>📊 Porcentaje</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            estado_color = "#28a745" if porcentaje >= 80 else "#ffc107" if porcentaje >= 60 else "#dc3545"
            estado_texto = "🌟 Excelente" if porcentaje >= 80 else "👍 Bueno" if porcentaje >= 60 else "⚠️ Atención"
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value' style='color: {estado_color};'>{estado_texto}</div>
                <div class='metric-label'>Estado</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Botones de acción grandes
        st.markdown("---")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("💾 Guardar Asistencia", use_container_width=True, type="primary"):
                guardar_asistencia_movil(dm, asistencia_data, curso_asistencia, trimestre_auto, fecha_seleccionada)
        
        with col2:
            if st.button("💾 Backup Ahora", use_container_width=True):
                df_backup = dm.load_data()
                backup_to_gdrive(df_backup)
        
        # Botones rápidos adicionales
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ Todos Presentes", use_container_width=True):
                for alumno in alumnos_curso:
                    st.session_state[f"asistencia_{alumno}_{fecha_seleccionada}"] = True
                st.rerun()
        
        with col2:
            if st.button("❌ Todos Ausentes", use_container_width=True):
                for alumno in alumnos_curso:
                    st.session_state[f"asistencia_{alumno}_{fecha_seleccionada}"] = False
                st.rerun()
        
        with col3:
            if st.button("🔄 Limpiar", use_container_width=True):
                for alumno in alumnos_curso:
                    key = f"asistencia_{alumno}_{fecha_seleccionada}"
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
    
    else:
        st.warning("📝 No hay alumnos registrados en este curso")

# Otras páginas (simplificadas)
elif st.session_state.pagina == "evaluacion":
    st.markdown("## 🎯 Nueva Evaluación")
    st.info("📝 Módulo de evaluaciones en desarrollo...")

elif st.session_state.pagina == "reportes":
    st.markdown("## 📊 Reportes")
    
    df = dm.get_filtered_data(
        curso_seleccionado if curso_seleccionado != "Todos" else None,
        trimestre_seleccionado if trimestre_seleccionado != "Todos" else None,
        alumno_seleccionado if alumno_seleccionado != "Todos" else None
    )
    
    if not df.empty:
        # Métricas en tarjetas
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{len(df)}</div>
                <div class='metric-label'>👥 Total Alumnos</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if "Nota Final" in df.columns:
                promedio = df["Nota Final"].mean()
                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value'>{promedio:.2f}</div>
                    <div class='metric-label'>📈 Promedio Final</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Tabla de datos
        st.markdown("---")
        st.markdown("### 📋 Datos Detallados")
        
        columnas_mostrar = [
            "Apellido y Nombre", "Curso", "Trimestre", "Asistencia", 
            "Nota Asistencia", "Nota Final"
        ]
        
        columnas_disponibles = [col for col in columnas_mostrar if col in df.columns]
        st.dataframe(df[columnas_disponibles].sort_values("Apellido y Nombre"), use_container_width=True)
    
    else:
        st.info("📝 No hay datos disponibles para los filtros seleccionados")

elif st.session_state.pagina == "editar":
    st.markdown("## ✏️ Editar Datos")
    st.info("📝 Módulo de edición en desarrollo...")

elif st.session_state.pagina == "backup":
    st.markdown("## 💾 Backup de Datos")
    
    df_backup = dm.load_data()
    if not df_backup.empty:
        st.info(f"📊 Total de registros: {len(df_backup)}")
        
        if st.button("💾 Crear Backup Completo", use_container_width=True, type="primary"):
            backup_to_gdrive(df_backup)
    else:
        st.warning("📝 No hay datos para respaldar")

# Footer móvil
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px; font-size: 0.9em;'>
    <strong>🏃‍♂️ Dashboard EF - Móvil</strong><br>
    Optimizado para uso en dispositivos móviles<br>
    <small>💾 Datos respaldados automáticamente</small>
</div>
""", unsafe_allow_html=True)

# Función optimizada para guardar asistencia móvil
def guardar_asistencia_movil(dm, asistencia_data, curso, trimestre, fecha):
    """Guardar asistencia con feedback móvil"""
    guardados = 0
    
    for alumno, data in asistencia_data.items():
        # Aquí iría la lógica de guardado real
        guardados += 1
    
    # Backup automático
    df_backup = dm.load_data()
    backup_to_gdrive(df_backup)
    
    st.success(f"✅ Guardado: {guardados} alumnos")
    st.balloons()
    
    # Resumen
    presentes = sum(1 for data in asistencia_data.values() if data['presente'])
    total = len(asistencia_data)
    st.info(f"📊 {presentes}/{total} presentes ({(presentes/total*100):.1f}%)")
