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

# CSS para hacer sidebar siempre visible sin JavaScript
sidebar_style = """
<style>
/* Forzar sidebar siempre visible */
.css-1d391kg {
    display: block !important;
    visibility: visible !important;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    height: 100vh !important;
    width: 280px !important;
    background: white !important;
    border-right: 2px solid #f0f2f6 !important;
    box-shadow: 2px 0 10px rgba(0,0,0,0.1) !important;
    z-index: 999 !important;
    overflow-y: auto !important;
    transition: all 0.3s ease !important;
}

/* Ajustar contenido principal */
.stMainBlockContainer {
    margin-left: 300px !important;
    padding: 20px !important;
    transition: all 0.3s ease !important;
}

/* Para móviles - sidebar más pequeña pero visible */
@media (max-width: 768px) {
    .css-1d391kg {
        width: 240px !important;
        min-width: 240px !important;
    }
    
    .stMainBlockContainer {
        margin-left: 260px !important;
        padding: 15px !important;
    }
    
    /* Asegurar que los elementos sean más grandes en móvil */
    .stSelectbox > div > div {
        font-size: 16px !important;
        min-height: 44px !important;
    }
    
    .stButton > button {
        font-size: 16px !important;
        padding: 12px !important;
        min-height: 44px !important;
        margin-bottom: 8px !important;
    }
    
    .stTextInput > div > div > input {
        font-size: 16px !important;
        padding: 12px !important;
        min-height: 44px !important;
    }
    
    .stTextArea > div > div > textarea {
        font-size: 16px !important;
        padding: 12px !important;
    }
    
    .stNumberInput > div > div > input {
        font-size: 16px !important;
        padding: 12px !important;
    }
}

/* Para pantallas muy pequeñas */
@media (max-width: 480px) {
    .css-1d391kg {
        width: 200px !important;
        min-width: 200px !important;
    }
    
    .stMainBlockContainer {
        margin-left: 220px !important;
        padding: 10px !important;
    }
}

/* Ocultar elementos de Streamlit no deseados */
#MainMenu {visibility: hidden !important;}
footer {visibility: hidden !important;}
header {visibility: hidden !important;}
.stAppDeployButton {display:none !important;}

/* Mejorar visibilidad de elementos en sidebar */
.css-1d391kg .element-container {
    padding: 10px !important;
}

.css-1d391kg .stSelectbox > div > div {
    background: #f8f9fa !important;
    border: 1px solid #e9ecef !important;
    border-radius: 5px !important;
    padding: 8px !important;
}

.css-1d391kg .stButton > button {
    background: #007bff !important;
    color: white !important;
    border: none !important;
    border-radius: 5px !important;
    font-weight: bold !important;
}

.css-1d391kg .stButton > button:hover {
    background: #0056b3 !important;
}

/* Indicador de sidebar activa */
.sidebar-indicator {
    position: fixed;
    top: 10px;
    right: 10px;
    background: #28a745;
    color: white;
    padding: 5px 10px;
    border-radius: 15px;
    font-size: 12px;
    z-index: 10000;
    font-weight: bold;
}

/* Animación de carga */
@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.7; }
    100% { opacity: 1; }
}

.loading {
    animation: pulse 1.5s infinite;
}
</style>

<!-- Indicador visual de sidebar activa -->
<div class="sidebar-indicator">
    📋 Sidebar Activa
</div>
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
st.markdown("### Sistema completo con sidebar siempre visible")
st.markdown("---")

# Sidebar con filtros (ahora siempre visible)
st.sidebar.markdown("# 📋 Panel de Control")
st.sidebar.markdown("---")

# Información de estado
st.sidebar.markdown("### 🟢 Estado del Sistema")
st.sidebar.success("✅ Sidebar Activa y Visible")
st.sidebar.info("📱 Funciona en todos los dispositivos")
st.sidebar.markdown("---")

# Filtro de cursos
st.sidebar.markdown("### 🔍 Filtros de Búsqueda")
cursos = ["Todos"] + dm.cursos
curso_seleccionado = st.sidebar.selectbox(
    "📚 Seleccionar Curso:",
    cursos,
    index=0,
    help="Filtra los alumnos por curso"
)

# Filtro de trimestres
trimestres = ["Todos"] + dm.trimestres
trimestre_seleccionado = st.sidebar.selectbox(
    "📅 Seleccionar Trimestre:",
    trimestres,
    index=0,
    help="Filtra por período académico"
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
    index=0,
    help="Busca un alumno específico"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🚀 Acciones Principales")

# Botones de acción principales con mejor feedback
col1, col2 = st.sidebar.columns(2)

with col1:
    if st.button("➕ Nuevo Alumno", use_container_width=True, type="primary", help="Registra un nuevo alumno"):
        st.session_state.show_new_student = True
        st.session_state.show_reports = False
        st.rerun()

with col2:
    if st.button("📊 Ver Reportes", use_container_width=True, help="Muestra estadísticas y reportes"):
        st.session_state.show_reports = True
        st.session_state.show_new_student = False
        st.rerun()

# Botón de actualización
if st.sidebar.button("🔄 Actualizar Página", use_container_width=True, help="Recarga todos los datos"):
    st.session_state.show_new_student = False
    st.session_state.show_reports = False
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 📱 Información de Acceso")
st.sidebar.markdown("""
**Link permanente:**
```
paolaies.streamlit.app
```

**Para agregar a inicio:**
1. Abrir en teléfono
2. Compartir → Agregar a inicio
3. Listo! 🎉

**Atajos de teclado:**
- Tab: Navegar elementos
- Enter: Confirmar selección
- Esc: Cerrar diálogos
""")

# Sección de nuevo alumno
if "show_new_student" in st.session_state and st.session_state.show_new_student:
    st.markdown("## ➕ Registrar Nuevo Alumno")
    st.markdown("### Complete todos los datos del alumno")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📋 Información Básica")
        nuevo_curso = st.selectbox("📚 Curso:", dm.cursos, help="Selecciona el curso del alumno")
        nuevo_trimestre = st.selectbox("📅 Trimestre:", dm.trimestres, help="Período académico")
        nombre_alumno = st.text_input("👤 Apellido y Nombre:", placeholder="Ej: García López, María", help="Nombre completo del alumno")
    
    with col2:
        st.markdown("#### 📊 Datos de Asistencia")
        asistencia_dias = st.number_input(
            "📅 Total días de clase:",
            min_value=1,
            max_value=100,
            value=20,
            help="Total de días en el trimestre"
        )
        dias_presentes = st.number_input(
            "✅ Días presentes:",
            min_value=0,
            max_value=asistencia_dias,
            value=asistencia_dias,
            help="Días que el alumno asistió"
        )
        
        porcentaje_asistencia = (dias_presentes / asistencia_dias * 100) if asistencia_dias > 0 else 0
        st.info(f"📊 Porcentaje: {porcentaje_asistencia:.1f}%")
        
        asistencia_estado, nota_asistencia = dm.calculate_attendance_grade(porcentaje_asistencia)
        st.success(f"✅ Nota asistencia: {asistencia_estado} ({nota_asistencia})")
    
    # Evaluaciones
    st.markdown("#### 📝 Evaluaciones del Alumno")
    
    tipo_evaluacion = st.selectbox("📝 Tipo de Evaluación:", dm.tipos_evaluacion, help="Categoría de evaluación")
    
    # Configurar evaluaciones
    evaluaciones = []
    calificaciones = []
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📋 Evaluaciones 1-3**")
        for i in range(1, 4):
            with st.expander(f"Evaluación {i}", expanded=True):
                nombre_eval = st.text_input(f"Nombre:", key=f"eval_{i}", placeholder=f"Ej: Test de Resistencia")
                calificacion = st.selectbox(
                    f"Calificación:",
                    list(dm.calificaciones.keys()),
                    key=f"cal_{i}",
                    help="Seleccione la calificación correspondiente"
                )
                if nombre_eval:
                    evaluaciones.append(nombre_eval)
                    calificaciones.append(calificacion)
    
    with col2:
        st.write("**📋 Evaluaciones 4-6**")
        for i in range(4, 7):
            with st.expander(f"Evaluación {i}", expanded=True):
                nombre_eval = st.text_input(f"Nombre:", key=f"eval_{i}", placeholder=f"Ej: Test de Fuerza")
                calificacion = st.selectbox(
                    f"Calificación:",
                    list(dm.calificaciones.keys()),
                    key=f"cal_{i}",
                    help="Seleccione la calificación correspondiente"
                )
                if nombre_eval:
                    evaluaciones.append(nombre_eval)
                    calificaciones.append(calificacion)
    
    # Calcular nota final
    if calificaciones:
        nota_final = dm.calculate_final_grade(calificaciones)
        st.success(f"📊 Nota Final: {nota_final}")
    
    # Observaciones
    st.markdown("#### 📝 Observaciones")
    observaciones = st.text_area("Observaciones sobre el alumno:", height=100, placeholder="Comentarios adicionales sobre el rendimiento del alumno...")
    
    # Botones de guardado
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 Guardar Alumno", type="primary", use_container_width=True, help="Guarda todos los datos del alumno"):
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
                    st.balloons()
                    st.session_state.show_new_student = False
                    st.rerun()
                else:
                    st.error("❌ Error al guardar el alumno")
            else:
                st.error("❌ Por favor complete todos los campos obligatorios")
    
    with col2:
        if st.button("❌ Cancelar", use_container_width=True, help="Cancela y vuelve al inicio"):
            st.session_state.show_new_student = False
            st.rerun()
    
    st.markdown("---")

# Sección de reportes
elif "show_reports" in st.session_state and st.session_state.show_reports:
    st.markdown("## 📊 Reportes y Estadísticas")
    st.markdown("### Análisis completo de los datos del sistema")
    
    # Cargar datos filtrados
    df = dm.get_filtered_data(curso_seleccionado, trimestre_seleccionado, alumno_seleccionado)
    
    if not df.empty:
        # Estadísticas generales
        st.markdown("#### 📈 Métricas Principales")
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
        st.markdown("#### 📋 Vista Detallada de Datos")
        
        # Resumen de filtros aplicados
        filtros_aplicados = []
        if curso_seleccionado != "Todos":
            filtros_aplicados.append(f"📚 Curso: {curso_seleccionado}")
        if trimestre_seleccionado != "Todos":
            filtros_aplicados.append(f"📅 Trimestre: {trimestre_seleccionado}")
        if alumno_seleccionado != "Todos":
            filtros_aplicados.append(f"👤 Alumno: {alumno_seleccionado}")
        
        if filtros_aplicados:
            st.info(f"🔍 Filtros activos: {' | '.join(filtros_aplicados)}")
        
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
            st.markdown("#### 📈 Análisis Visual")
            
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
        st.markdown("#### 💾 Exportar Datos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Exportar a Excel", use_container_width=True, help="Descarga todos los datos filtrados"):
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
            if st.button("🔄 Actualizar Datos", use_container_width=True, help="Recarga la página"):
                st.session_state.show_reports = False
                st.rerun()
    
    else:
        st.info("📝 No hay datos disponibles para los filtros seleccionados")
    
    if st.button("🔙 Volver al Inicio", use_container_width=True, help="Vuelve a la vista principal"):
        st.session_state.show_reports = False
        st.rerun()
    
    st.markdown("---")

# Vista principal
if ("show_new_student" not in st.session_state or not st.session_state.show_new_student) and \
   ("show_reports" not in st.session_state or not st.session_state.show_reports):
    
    st.markdown("## 📋 Vista Principal de Alumnos")
    st.markdown("### Listado completo con filtros aplicados")
    
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
            st.info(f"🔍 Filtros activos: {' | '.join(filtros_aplicados)}")
        
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
        st.markdown("#### 📊 Resumen Rápido")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📋 Total Registros", len(df))
        
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
        st.markdown("#### ℹ️ Información del Sistema")
        
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
        
        st.markdown("#### 📊 Sistema de Calificaciones")
        
        calificaciones_df = pd.DataFrame([
            {"Calificación": k, "Rango": v["rango"], "Valor": v["valor"]} 
            for k, v in dm.calificaciones.items()
        ])
        
        st.dataframe(calificaciones_df, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 20px;'>
        <strong>📚 Dashboard de Gestión IES</strong><br>
        Sistema completo con sidebar siempre visible • Funciona en todos los dispositivos<br>
        <small>Link permanente: paolaies.streamlit.app</small>
    </div>
    """,
    unsafe_allow_html=True
)
