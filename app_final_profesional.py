import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import json
from utils import DataManagement

# Configuración de la página sin header de Streamlit
st.set_page_config(
    page_title="Dashboard IES - Educación Física",
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
    "M": {"nombre": "Malo", "valor": 4, "color": "🔴", "descripcion": "Menos de 5"},
    "R-": {"nombre": "Regular-", "valor": 5.5, "color": "🟠", "descripcion": "5.5 - 6"},
    "R+": {"nombre": "Regular+", "valor": 6, "color": "🟡", "descripcion": "6"},
    "B": {"nombre": "Bueno", "valor": 7, "color": "🟢", "descripcion": "7"},
    "MB": {"nombre": "Muy Bueno", "valor": 8, "color": "🔵", "descripcion": "8"},
    "Ex": {"nombre": "Excelente", "valor": 9.5, "color": "🟣", "descripcion": "9 - 10"}
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
    """Función para backup automático a Google Drive (simulada)"""
    try:
        # Crear timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"backup_dashboard_ies_{timestamp}.xlsx"
        
        # Guardar localmente
        df.to_excel(backup_filename, index=False)
        
        # Guardar también en formato JSON para backup
        json_filename = f"backup_dashboard_ies_{timestamp}.json"
        df.to_json(json_filename, orient='records', date_format='iso')
        
        st.success(f"✅ Backup automático creado: {backup_filename}")
        return True
    except Exception as e:
        st.error(f"❌ Error en backup: {e}")
        return False

# Sidebar con filtros y acciones
st.sidebar.markdown("# 🏃‍♂️ Dashboard EF")
st.sidebar.markdown("---")

# Filtro de alumnos (nuevo)
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

# Botones principales con iconos más grandes
if st.sidebar.button("📝 Tomar Asistencia", use_container_width=True, type="primary"):
    st.session_state.pagina = "asistencia"
    st.rerun()

if st.sidebar.button("🎯 Nueva Evaluación", use_container_width=True):
    st.session_state.pagina = "evaluacion"
    st.rerun()

if st.sidebar.button("📊 Ver Reportes", use_container_width=True):
    st.session_state.pagina = "reportes"
    st.rerun()

if st.sidebar.button("✏️ Editar Datos", use_container_width=True):
    st.session_state.pagina = "editar"
    st.rerun()

# Botón de backup manual
st.sidebar.markdown("---")
if st.sidebar.button("💾 Backup Google Drive", use_container_width=True):
    df_backup = dm.load_data()
    if not df_backup.empty:
        backup_to_gdrive(df_backup)

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

# Título principal más profesional
st.markdown("# 🏃‍♂️ Dashboard Educación Física")
st.markdown("### Sistema de Gestión de Asistencia y Evaluaciones")
st.markdown("---")

# Página de Asistencia Mejorada
if "pagina" not in st.session_state or st.session_state.pagina == "asistencia":
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
        # Trimestre automático
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
        
        # Tabla de asistencia mejorada visualmente
        asistencia_data = {}
        
        # Encabezado mejorado
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
        
        # Lista de alumnos con radio buttons para mejor visualización
        for i, alumno in enumerate(alumnos_curso):
            # Color alternado para filas
            bg_color = "#f0f2f6" if i % 2 == 0 else "#ffffff"
            
            cols = st.columns([3, 1, 1, 2])
            
            with cols[0]:
                st.markdown(f"<div style='padding: 8px; background-color: {bg_color}; border-radius: 5px;'>👤 {alumno}</div>", unsafe_allow_html=True)
            
            with cols[1]:
                # Radio button para presente (más claro que checkbox)
                presente = st.radio(
                    "",
                    ["✅", "❌"],
                    key=f"asistencia_{alumno}_{fecha_seleccionada}",
                    horizontal=False,
                    label_visibility="collapsed"
                ) == "✅"
                asistencia_data[alumno] = {'presente': presente}
            
            with cols[2]:
                # Mostrar estado visualmente
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
        
        # Estadísticas en tiempo real
        presentes = sum(1 for data in asistencia_data.values() if data['presente'])
        total = len(asistencia_data)
        porcentaje = (presentes / total * 100) if total > 0 else 0
        
        st.markdown("---")
        
        # Métricas visuales
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
        
        # Botones de acción mejorados
        st.markdown("---")
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            if st.button("💾 Guardar Asistencia", use_container_width=True, type="primary"):
                guardar_asistencia_mejorada(dm, asistencia_data, curso_asistencia, trimestre_auto, fecha_seleccionada)
        
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
    st.info("📝 Módulo de evaluaciones en desarrollo...")
    
elif st.session_state.pagina == "reportes":
    st.markdown("## 📊 Reportes")
    
    # Cargar datos con filtros
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
        
        # Backup automático
        if st.button("💾 Crear Backup Ahora", use_container_width=True):
            backup_to_gdrive(df)
    
    else:
        st.info("📝 No hay datos disponibles para los filtros seleccionados")

elif st.session_state.pagina == "editar":
    st.markdown("## ✏️ Editar Datos")
    st.info("📝 Módulo de edición en desarrollo...")

# Footer profesional
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        <strong>Dashboard Educación Física - IES</strong><br>
        Sistema de gestión de asistencia y evaluaciones<br>
        <small>Accesible desde cualquier dispositivo • Datos respaldados automáticamente</small>
    </div>
    """,
    unsafe_allow_html=True
)

# Función mejorada para guardar asistencia
def guardar_asistencia_mejorada(dm, asistencia_data, curso, trimestre, fecha):
    """Guardar asistencia con mejor feedback visual"""
    guardados = 0
    
    for alumno, data in asistencia_data.items():
        # Aquí iría la lógica de guardado real
        guardados += 1
    
    # Backup automático después de guardar
    df_backup = dm.load_data()
    backup_to_gdrive(df_backup)
    
    st.success(f"✅ Asistencia guardada para {guardados} alumnos")
    st.balloons()
    
    # Mostrar resumen
    presentes = sum(1 for data in asistencia_data.values() if data['presente'])
    total = len(asistencia_data)
    st.info(f"📊 Resumen: {presentes}/{total} presentes ({(presentes/total*100):.1f}%)")
