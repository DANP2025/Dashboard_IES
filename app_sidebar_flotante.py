import streamlit as st
import pandas as pd
from datetime import datetime
import os
from utils import DataManagement

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Gestión IES",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS para sidebar flotante visible en todos los dispositivos
sidebar_style = """
<style>
/* Hacer sidebar siempre visible y flotante */
.css-1d391kg {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    height: 100vh !important;
    width: 300px !important;
    background: white !important;
    border-right: 2px solid #f0f2f6 !important;
    box-shadow: 2px 0 10px rgba(0,0,0,0.1) !important;
    z-index: 999 !important;
    overflow-y: auto !important;
}

/* Ajustar contenido principal para no solaparse con sidebar */
.stMainBlockContainer {
    margin-left: 320px !important;
    padding: 20px !important;
}

/* Para móviles - hacer sidebar más pequeña pero visible */
@media (max-width: 768px) {
    .css-1d391kg {
        width: 250px !important;
        position: fixed !important;
        z-index: 9999 !important;
    }
    
    .stMainBlockContainer {
        margin-left: 270px !important;
        padding: 10px !important;
    }
    
    /* Hacer contenido responsive */
    .stSelectbox > div > div {
        font-size: 14px !important;
    }
    
    .stButton > button {
        font-size: 14px !important;
        padding: 8px !important;
        min-height: 40px !important;
    }
    
    .stTextInput > div > div > input {
        font-size: 14px !important;
        padding: 8px !important;
    }
    
    .stTextArea > div > div > textarea {
        font-size: 14px !important;
        padding: 8px !important;
    }
}

/* Para pantallas muy pequeñas */
@media (max-width: 480px) {
    .css-1d391kg {
        width: 200px !important;
    }
    
    .stMainBlockContainer {
        margin-left: 220px !important;
    }
}

/* Ocultar elementos de Streamlit no deseados */
#MainMenu {visibility: hidden !important;}
footer {visibility: hidden !important;}
header {visibility: hidden !important;}
.stAppDeployButton {display:none !important;}

/* Botón para toggle sidebar (opcional) */
.sidebar-toggle {
    position: fixed;
    top: 10px;
    left: 10px;
    z-index: 10000;
    background: #1f77b4;
    color: white;
    border: none;
    padding: 8px 12px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

.sidebar-toggle:hover {
    background: #17becf;
}
</style>

<!-- Botón de toggle para sidebar -->
<button class="sidebar-toggle" onclick="toggleSidebar()">☰</button>

<script>
function toggleSidebar() {
    var sidebar = document.querySelector('.css-1d391kg');
    var mainContent = document.querySelector('.stMainBlockContainer');
    
    if (sidebar.style.display === 'none') {
        sidebar.style.display = 'block';
        mainContent.style.marginLeft = '320px';
    } else {
        sidebar.style.display = 'none';
        mainContent.style.marginLeft = '20px';
    }
}
</script>
"""
st.markdown(sidebar_style, unsafe_allow_html=True)

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

# Título principal
st.markdown("# 📚 Dashboard de Gestión de Alumnos - IES")
st.markdown("---")

# Sidebar con filtros (ahora siempre visible)
st.sidebar.markdown("# 🔍 Filtros Principales")
st.sidebar.markdown("---")

# Filtro de cursos
cursos = ["Todos"] + dm.cursos
curso_seleccionado = st.sidebar.selectbox(
    "📚 Seleccionar Curso:",
    cursos,
    index=0
)

# Filtro de trimestres
trimestres = ["Todos"] + dm.trimestres
trimestre_seleccionado = st.sidebar.selectbox(
    "📅 Seleccionar Trimestre:",
    trimestres,
    index=0
)

# Filtro de alumnos (se carga dinámicamente)
alumnos = ["Todos"]
if curso_seleccionado != "Todos":
    alumnos.extend(dm.get_students_by_course(curso_seleccionado))
else:
    df = dm.load_data()
    if not df.empty:
        alumnos.extend(sorted(df["Apellido y Nombre"].unique()))

alumno_seleccionado = st.sidebar.selectbox(
    "👤 Seleccionar Alumno:",
    alumnos,
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("## 📝 Acciones Principales")

# Botones de acción principales
if st.sidebar.button("➕ Nuevo Alumno", use_container_width=True, type="primary"):
    st.session_state.show_new_student = True
    st.session_state.show_reports = False
    st.rerun()

if st.sidebar.button("📊 Ver Reportes", use_container_width=True):
    st.session_state.show_reports = True
    st.session_state.show_new_student = False
    st.rerun()

if st.sidebar.button("🔄 Actualizar Datos", use_container_width=True):
    st.session_state.show_new_student = False
    st.session_state.show_reports = False
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 📱 Información Útil")
st.sidebar.markdown("""
**Acceso Rápido:**
- Link permanente: `paolaies.streamlit.app`
- Agregar a pantalla de inicio móvil

**Atajos:**
- Click en ➕ para nuevo alumno
- Click en 📊 para ver reportes
- Usa filtros para buscar rápido
""")

# Sección de nuevo alumno
if "show_new_student" in st.session_state and st.session_state.show_new_student:
    st.subheader("➕ Registrar Nuevo Alumno")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        nuevo_curso = st.selectbox("📚 Curso:", dm.cursos)
        nuevo_trimestre = st.selectbox("📅 Trimestre:", dm.trimestres)
        nombre_alumno = st.text_input("👤 Apellido y Nombre del Alumno:")
    
    with col2:
        # Asistencia
        st.subheader("📋 Datos de Asistencia")
        asistencia_dias = st.number_input(
            "📅 Días de clase en el trimestre:",
            min_value=1,
            max_value=100,
            value=20
        )
        dias_presentes = st.number_input(
            "✅ Días presentes:",
            min_value=0,
            max_value=asistencia_dias,
            value=asistencia_dias
        )
        
        porcentaje_asistencia = (dias_presentes / asistencia_dias * 100) if asistencia_dias > 0 else 0
        st.info(f"📊 Porcentaje de asistencia: {porcentaje_asistencia:.1f}%")
        
        asistencia_estado, nota_asistencia = dm.calculate_attendance_grade(porcentaje_asistencia)
        st.success(f"✅ Nota de asistencia: {asistencia_estado} ({nota_asistencia})")
    
    # Evaluaciones
    st.subheader("📝 Evaluaciones del Alumno")
    
    tipo_evaluacion = st.selectbox("📝 Tipo de Evaluación:", dm.tipos_evaluacion)
    
    # Configurar evaluaciones
    evaluaciones = []
    calificaciones = []
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📋 Evaluaciones 1-3**")
        for i in range(1, 4):
            with st.expander(f"Evaluación {i}", expanded=True):
                nombre_eval = st.text_input(f"Nombre Evaluación {i}:", key=f"eval_{i}")
                calificacion = st.selectbox(
                    f"Calificación {i}:",
                    list(dm.calificaciones.keys()),
                    key=f"cal_{i}"
                )
                if nombre_eval:
                    evaluaciones.append(nombre_eval)
                    calificaciones.append(calificacion)
    
    with col2:
        st.write("**📋 Evaluaciones 4-6**")
        for i in range(4, 7):
            with st.expander(f"Evaluación {i}", expanded=True):
                nombre_eval = st.text_input(f"Nombre Evaluación {i}:", key=f"eval_{i}")
                calificacion = st.selectbox(
                    f"Calificación {i}:",
                    list(dm.calificaciones.keys()),
                    key=f"cal_{i}"
                )
                if nombre_eval:
                    evaluaciones.append(nombre_eval)
                    calificaciones.append(calificacion)
    
    # Calcular nota final
    if calificaciones:
        nota_final = dm.calculate_final_grade(calificaciones)
        st.success(f"📊 Nota Final del Alumno: {nota_final}")
    
    # Observaciones
    observaciones = st.text_area("📝 Observaciones sobre el alumno:", height=100)
    
    # Botones de guardado
    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("💾 Guardar Alumno", type="primary", use_container_width=True):
            if nombre_alumno and nuevo_curso and nuevo_trimestre:
                # Preparar datos para guardar
                student_data = {
                    "Curso": nuevo_curso,
                    "Trimestre": nuevo_trimestre,
                    "Apellido y Nombre": nombre_alumno,
                    "Asistencia": f"{dias_presentes}/{asistencia_dias}",
                    "Nota Asistencia": f"{asistencia_estado} ({nota_asistencia})",
                    "Evaluaciones": len(evaluaciones),
                    "Tipo Evaluación": tipo_evaluacion,
                    "Fecha Registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Observaciones": observaciones,
                    "Nota Final": nota_final
                }
                
                # Agregar evaluaciones y calificaciones
                for i, (eval_nombre, calificacion) in enumerate(zip(evaluaciones, calificaciones)):
                    student_data[f"Evaluación {i+1}"] = eval_nombre
                    student_data[f"Calificación {i+1}"] = calificacion
                
                # Rellenar campos vacíos
                for i in range(len(evaluaciones), 6):
                    student_data[f"Evaluación {i+1}"] = ""
                    student_data[f"Calificación {i+1}"] = ""
                
                if dm.save_student_data(student_data):
                    st.success("✅ Alumno guardado exitosamente!")
                    st.session_state.show_new_student = False
                    st.rerun()
                else:
                    st.error("❌ Error al guardar el alumno")
            else:
                st.error("❌ Por favor complete todos los campos obligatorios")
    
    with col2:
        if st.button("❌ Cancelar", use_container_width=True):
            st.session_state.show_new_student = False
            st.rerun()
    
    st.markdown("---")

# Sección de reportes
elif "show_reports" in st.session_state and st.session_state.show_reports:
    st.subheader("📊 Reportes y Estadísticas del Sistema")
    
    # Cargar datos filtrados
    df = dm.get_filtered_data(curso_seleccionado, trimestre_seleccionado, alumno_seleccionado)
    
    if not df.empty:
        # Estadísticas generales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 Total Alumnos", len(df))
        
        with col2:
            if "Nota Asistencia" in df.columns:
                promedio_asistencia = df["Nota Asistencia"].str.extract(r'(\d+)').astype(float).mean()
                if not pd.isna(promedio_asistencia):
                    st.metric("📊 Promedio Asistencia", f"{float(promedio_asistencia):.1f}")
                else:
                    st.metric("📊 Promedio Asistencia", "N/A")
        
        with col3:
            if "Nota Final" in df.columns:
                promedio_final = df["Nota Final"].mean()
                if not pd.isna(promedio_final):
                    st.metric("📈 Promedio Final", f"{float(promedio_final):.2f}")
                else:
                    st.metric("📈 Promedio Final", "N/A")
        
        with col4:
            if "Evaluaciones" in df.columns:
                total_evaluaciones = df["Evaluaciones"].sum()
                st.metric("📝 Total Evaluaciones", int(total_evaluaciones))
        
        # Tabla de datos detallados
        st.subheader("📋 Vista Detallada de Datos")
        
        # Resumen de filtros aplicados
        filtros_aplicados = []
        if curso_seleccionado != "Todos":
            filtros_aplicados.append(f"📚 Curso: {curso_seleccionado}")
        if trimestre_seleccionado != "Todos":
            filtros_aplicados.append(f"📅 Trimestre: {trimestre_seleccionado}")
        if alumno_seleccionado != "Todos":
            filtros_aplicados.append(f"👤 Alumno: {alumno_seleccionado}")
        
        if filtros_aplicados:
            st.info(f"🔍 Filtros aplicados: {' | '.join(filtros_aplicados)}")
        
        # Seleccionar columnas a mostrar
        columnas_mostrar = [
            "Apellido y Nombre", "Curso", "Trimestre", "Asistencia", 
            "Nota Asistencia", "Tipo Evaluación", "Nota Final", "Observaciones"
        ]
        
        # Agregar evaluaciones si existen
        for i in range(1, 7):
            if f"Evaluación {i}" in df.columns:
                columnas_mostrar.append(f"Evaluación {i}")
                columnas_mostrar.append(f"Calificación {i}")
        
        columnas_disponibles = [col for col in columnas_mostrar if col in df.columns]
        
        st.dataframe(
            df[columnas_disponibles].sort_values("Apellido y Nombre"),
            use_container_width=True,
            hide_index=True
        )
        
        # Gráficos
        if len(df) > 1:
            st.subheader("📈 Análisis Visual de Datos")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Distribución de notas finales
                if "Nota Final" in df.columns:
                    st.write("**📊 Distribución de Notas Finales**")
                    st.bar_chart(df["Nota Final"].value_counts().sort_index())
            
            with col2:
                # Distribución por curso
                if "Curso" in df.columns:
                    st.write("**📚 Distribución por Curso**")
                    st.bar_chart(df["Curso"].value_counts())
        
        # Exportación de datos
        st.subheader("💾 Exportar Datos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Exportar a Excel", use_container_width=True):
                # Crear nombre de archivo con timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"export_{timestamp}.xlsx"
                
                try:
                    df.to_excel(filename, index=False)
                    st.success(f"✅ Datos exportados a {filename}")
                    
                    # Botón de descarga
                    with open(filename, 'rb') as f:
                        st.download_button(
                            label="📄 Descargar Archivo Excel",
                            data=f.read(),
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                except Exception as e:
                    st.error(f"❌ Error al exportar: {e}")
        
        with col2:
            if st.button("🔄 Actualizar Datos", use_container_width=True):
                st.session_state.show_reports = False
                st.rerun()
    
    else:
        st.info("📝 No hay datos disponibles para los filtros seleccionados")
    
    if st.button("🔙 Volver al Inicio", use_container_width=True):
        st.session_state.show_reports = False
        st.rerun()
    
    st.markdown("---")

# Vista principal
if ("show_new_student" not in st.session_state or not st.session_state.show_new_student) and \
   ("show_reports" not in st.session_state or not st.session_state.show_reports):
    
    st.subheader("📋 Vista Principal de Alumnos")
    
    # Cargar datos con filtros
    df = dm.get_filtered_data(curso_seleccionado, trimestre_seleccionado, alumno_seleccionado)
    
    if not df.empty:
        # Resumen de filtros aplicados
        filtros_aplicados = []
        if curso_seleccionado != "Todos":
            filtros_aplicados.append(f"📚 Curso: {curso_seleccionado}")
        if trimestre_seleccionado != "Todos":
            filtros_aplicados.append(f"📅 Trimestre: {trimestre_seleccionado}")
        if alumno_seleccionado != "Todos":
            filtros_aplicados.append(f"👤 Alumno: {alumno_seleccionado}")
        
        if filtros_aplicados:
            st.info(f"🔍 Filtros aplicados: {' | '.join(filtros_aplicados)}")
        
        # Mostrar datos en tabla principal
        columnas_mostrar = [
            "Apellido y Nombre", "Curso", "Trimestre", "Asistencia", 
            "Nota Asistencia", "Tipo Evaluación", "Nota Final"
        ]
        
        columnas_disponibles = [col for col in columnas_mostrar if col in df.columns]
        
        st.dataframe(
            df[columnas_disponibles].sort_values("Apellido y Nombre"),
            use_container_width=True,
            hide_index=True
        )
        
        # Opciones adicionales
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📊 Total Registros", len(df))
        
        with col2:
            if "Nota Final" in df.columns:
                promedio = df["Nota Final"].mean()
                if not pd.isna(promedio):
                    st.metric("📈 Promedio General", f"{float(promedio):.2f}")
        
        with col3:
            if "Nota Asistencia" in df.columns:
                asistencia_counts = df["Nota Asistencia"].value_counts()
                excelentes = asistencia_counts.get("Ex (10)", 0)
                st.metric("🌟 Excelente Asistencia", excelentes)
    
    else:
        st.info("📝 No hay datos disponibles. Usa el botón '➕ Nuevo Alumno' para comenzar.")
        
        # Mostrar información del sistema
        st.subheader("ℹ️ Información del Sistema de Gestión")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**📚 Cursos Disponibles:**")
            for curso in dm.cursos:
                st.write(f"• {curso}")
        
        with col2:
            st.write("**📅 Trimestres Disponibles:**")
            for trimestre in dm.trimestres:
                st.write(f"• {trimestre}")
        
        with col3:
            st.write("**📝 Tipos de Evaluación:**")
            for tipo in dm.tipos_evaluacion:
                st.write(f"• {tipo}")
        
        st.subheader("📊 Sistema de Calificaciones")
        
        calificaciones_df = pd.DataFrame([
            {"Calificación": k, "Rango": v["rango"], "Valor": v["valor"]} 
            for k, v in dm.calificaciones.items()
        ])
        
        st.dataframe(calificaciones_df, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; padding: 20px;'>"
    "📚 Dashboard de Gestión IES - Desarrollado con Streamlit<br>"
    "Sistema completo de gestión de alumnos • Sidebar siempre visible"
    "</div>",
    unsafe_allow_html=True
)
