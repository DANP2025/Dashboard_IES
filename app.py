import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

# Ocultar sidebar completamente
st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: block !important;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Sistema de Gestión Educativa",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("📚 Sistema de Gestión Educativa")
st.write("Dashboard completo para gestión de alumnos, asistencia y evaluaciones")

# Sidebar con filtros y acciones
st.sidebar.header("🔍 Filtros y Acciones")

# Filtro de cursos
cursos_disponibles = ["Todos", "EF 1A", "EF 2A", "EF 2A", "EF 1B", "EF 2B", "TD 2A", "TD 2B"]
curso_seleccionado = st.sidebar.selectbox("📂 Seleccionar Curso:", cursos_disponibles)

# Filtro de trimestres
trimestres_disponibles = ["Todos", "1 Trimestre", "2 Trimestre", "3 Trimestre"]
trimestre_seleccionado = st.sidebar.selectbox("📅 Seleccionar Trimestre:", trimestres_disponibles)

# Filtro de alumno
alumnos_disponibles = ["Todos", "Ana García", "Carlos López", "María Rodríguez", "Juan Martínez", "Laura Sánchez", "Pedro Fernández", "Sofía Martínez", "Lucas González"]
alumno_seleccionado = st.sidebar.selectbox("👤 Seleccionar Alumno:", alumnos_disponibles)

# Separador
st.sidebar.markdown("---")

# ACCIONES EN SIDEBAR
st.sidebar.subheader("✅ Acciones Rápidas")

# Sección de Evaluaciones en Sidebar
st.sidebar.markdown("### 📝 Agregar Evaluación")
with st.sidebar.form("evaluacion_sidebar"):
    eval_alumno = st.selectbox("👤 Alumno:", ["Ana García", "Carlos López", "María Rodríguez", "Juan Martínez", "Laura Sánchez", "Pedro Fernández", "Sofía Martínez", "Lucas González"], key="eval_alumno_sidebar")
    eval_tipo = st.selectbox("📋 Tipo:", ["Diagnóstico", "Físico", "Técnico", "Desempeño global"], key="eval_tipo_sidebar")
    eval_nombre = st.text_input("📝 Nombre Evaluación:", key="eval_nombre_sidebar")
    eval_calificacion = st.selectbox("📊 Calificación:", ["M", "R-", "R+", "B", "MB", "EX"], key="eval_calificacion_sidebar")
    
    if st.form_submit_button("📝 Agregar Evaluación", type="primary"):
        st.sidebar.success(f"✅ Evaluación '{eval_nombre}' agregada para {eval_alumno}")
        st.sidebar.info(f"📋 {eval_tipo} - Calificación: {eval_calificacion}")

# Separador
st.sidebar.markdown("---")

# Botón para limpiar datos de ejemplo
if st.sidebar.button("🗑️ Limpiar Datos de Ejemplo", type="secondary", help="Elimina todos los datos de ejemplo para empezar con datos reales"):
    st.sidebar.warning("⚠️ Esta función eliminará todos los datos de ejemplo")

# Sistema de navegación por pestañas principales
tab1, tab2, tab3 = st.tabs([
    "📊 Dashboard General", 
    "👥 Gestión de Alumnos", 
    "📋 Asistencia Interactiva"
])

# Función para crear/leer Excel
def crear_excel_si_no_existe():
    archivo_excel = "sistema_educativo.xlsx"
    
    if not os.path.exists(archivo_excel):
        # Crear workbook
        wb = openpyxl.Workbook()
        
        # Eliminar hoja por defecto
        wb.remove(wb.active)
        
        # Crear hojas para cada trimestre
        for trimestre in ["1 Trimestre", "2 Trimestre", "3 Trimestre"]:
            ws = wb.create_sheet(title=trimestre)
            
            # Encabezados
            headers = [
                "Apellido y Nombre", "Curso", 
                # Asistencia diaria (marzo-mayo para 1 trimestre)
                "Mar-01", "Mar-02", "Mar-03", "Mar-04", "Mar-05", "Mar-06", "Mar-07", "Mar-08", "Mar-09", "Mar-10",
                "Mar-11", "Mar-12", "Mar-13", "Mar-14", "Mar-15", "Mar-16", "Mar-17", "Mar-18", "Mar-19", "Mar-20",
                "Mar-21", "Mar-22", "Mar-23", "Mar-24", "Mar-25", "Mar-26", "Mar-27", "Mar-28", "Mar-29", "Mar-30", "Mar-31",
                "Abr-01", "Abr-02", "Abr-03", "Abr-04", "Abr-05", "Abr-06", "Abr-07", "Abr-08", "Abr-09", "Abr-10",
                "Abr-11", "Abr-12", "Abr-13", "Abr-14", "Abr-15", "Abr-16", "Abr-17", "Abr-18", "Abr-19", "Abr-20",
                "Abr-21", "Abr-22", "Abr-23", "Abr-24", "Abr-25", "Abr-26", "Abr-27", "Abr-28", "Abr-29", "Abr-30",
                "May-01", "May-02", "May-03", "May-04", "May-05", "May-06", "May-07", "May-08", "May-09", "May-10",
                "May-11", "May-12", "May-13", "May-14", "May-15", "May-16", "May-17", "May-18", "May-19", "May-20",
                "May-21", "May-22", "May-23", "May-24", "May-25", "May-26", "May-27", "May-28", "May-29", "May-30", "May-31",
                "Nota Asistencia",
                # Evaluaciones
                "Tipo Evaluación", "Eval 1", "Calif 1", "Eval 2", "Calif 2", "Eval 3", "Calif 3", 
                "Eval 4", "Calif 4", "Eval 5", "Calif 5", "Eval 6", "Calif 6",
                "Nota Final Evaluaciones", "Observaciones"
            ]
            
            # Escribir encabezados
            for col_num, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col_num, value=header)
                cell.font = Font(bold=True)
                cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
                cell.alignment = Alignment(horizontal="center")
        
        # Guardar archivo
        wb.save(archivo_excel)
        st.success(f"✅ Archivo Excel creado: {archivo_excel}")
    
    return archivo_excel

# Función para agregar datos de ejemplo
def agregar_datos_ejemplo():
    archivo_excel = "sistema_educativo.xlsx"
    
    if os.path.exists(archivo_excel):
        try:
            # Datos de ejemplo para 1 Trimestre
            datos_ejemplo = [
                {
                    "Apellido y Nombre": "Ana García", "Curso": "EF 1A",
                    "Mar-01": "Presente", "Mar-02": "Presente", "Mar-03": "Presente", "Mar-04": "Ausente", "Mar-05": "Presente",
                    "Mar-06": "Presente", "Mar-07": "Presente", "Mar-08": "Presente", "Mar-09": "Presente", "Mar-10": "Presente",
                    "Mar-11": "Presente", "Mar-12": "Presente", "Mar-13": "Presente", "Mar-14": "Presente", "Mar-15": "Ausente",
                    "Mar-16": "Presente", "Mar-17": "Presente", "Mar-18": "Presente", "Mar-19": "Presente", "Mar-20": "Presente",
                    "Mar-21": "Presente", "Mar-22": "Presente", "Mar-23": "Presente", "Mar-24": "Presente", "Mar-25": "Presente",
                    "Mar-26": "Presente", "Mar-27": "Presente", "Mar-28": "Presente", "Mar-29": "Presente", "Mar-30": "Presente",
                    "Mar-31": "Presente",
                    "Tipo Evaluación": "Diagnóstico",
                    "Eval 1": "Evaluación Inicial", "Calif 1": "B",
                    "Eval 2": "Trabajo Práctico 1", "Calif 2": "MB",
                    "Eval 3": "Parcial Unidad 1", "Calif 3": "R+",
                    "Observaciones": "Alumno aplicado, buena participación"
                },
                {
                    "Apellido y Nombre": "Carlos López", "Curso": "EF 2A",
                    "Mar-01": "Presente", "Mar-02": "Presente", "Mar-03": "Ausente", "Mar-04": "Presente", "Mar-05": "Presente",
                    "Mar-06": "Presente", "Mar-07": "Presente", "Mar-08": "Presente", "Mar-09": "Ausente", "Mar-10": "Presente",
                    "Mar-11": "Presente", "Mar-12": "Presente", "Mar-13": "Presente", "Mar-14": "Presente", "Mar-15": "Presente",
                    "Mar-16": "Presente", "Mar-17": "Presente", "Mar-18": "Ausente", "Mar-19": "Presente", "Mar-20": "Presente",
                    "Mar-21": "Presente", "Mar-22": "Presente", "Mar-23": "Presente", "Mar-24": "Presente", "Mar-25": "Presente",
                    "Mar-26": "Presente", "Mar-27": "Presente", "Mar-28": "Presente", "Mar-29": "Presente", "Mar-30": "Ausente",
                    "Mar-31": "Presente",
                    "Tipo Evaluación": "Diagnóstico",
                    "Eval 1": "Evaluación Inicial", "Calif 1": "R+",
                    "Eval 2": "Trabajo Práctico 1", "Calif 2": "B",
                    "Eval 3": "Parcial Unidad 1", "Calif 3": "MB",
                    "Observaciones": "Necesita mejorar asistencia"
                },
                {
                    "Apellido y Nombre": "María Rodríguez", "Curso": "EF 1B",
                    "Mar-01": "Presente", "Mar-02": "Presente", "Mar-03": "Presente", "Mar-04": "Presente", "Mar-05": "Presente",
                    "Mar-06": "Presente", "Mar-07": "Presente", "Mar-08": "Presente", "Mar-09": "Presente", "Mar-10": "Presente",
                    "Mar-11": "Presente", "Mar-12": "Presente", "Mar-13": "Presente", "Mar-14": "Presente", "Mar-15": "Presente",
                    "Mar-16": "Presente", "Mar-17": "Presente", "Mar-18": "Presente", "Mar-19": "Presente", "Mar-20": "Presente",
                    "Mar-21": "Presente", "Mar-22": "Presente", "Mar-23": "Presente", "Mar-24": "Presente", "Mar-25": "Presente",
                    "Mar-26": "Presente", "Mar-27": "Presente", "Mar-28": "Presente", "Mar-29": "Presente", "Mar-30": "Presente",
                    "Mar-31": "Presente",
                    "Tipo Evaluación": "Físico",
                    "Eval 1": "Test Físico", "Calif 1": "EX",
                    "Eval 2": "Evaluación Práctica", "Calif 2": "MB",
                    "Eval 3": "Parcial Teórico", "Calif 3": "B",
                    "Observaciones": "Excelente desempeño físico"
                },
                {
                    "Apellido y Nombre": "Juan Martínez", "Curso": "TD 2A",
                    "Mar-01": "Ausente", "Mar-02": "Presente", "Mar-03": "Presente", "Mar-04": "Presente", "Mar-05": "Presente",
                    "Mar-06": "Ausente", "Mar-07": "Presente", "Mar-08": "Presente", "Mar-09": "Presente", "Mar-10": "Ausente",
                    "Mar-11": "Presente", "Mar-12": "Presente", "Mar-13": "Presente", "Mar-14": "Presente", "Mar-15": "Presente",
                    "Mar-16": "Presente", "Mar-17": "Ausente", "Mar-18": "Presente", "Mar-19": "Presente", "Mar-20": "Presente",
                    "Mar-21": "Presente", "Mar-22": "Presente", "Mar-23": "Presente", "Mar-24": "Presente", "Mar-25": "Ausente",
                    "Mar-26": "Presente", "Mar-27": "Presente", "Mar-28": "Presente", "Mar-29": "Presente", "Mar-30": "Presente",
                    "Mar-31": "Presente",
                    "Tipo Evaluación": "Técnico",
                    "Eval 1": "Proyecto Técnico", "Calif 1": "R-",
                    "Eval 2": "Evaluación Práctica", "Calif 2": "R+",
                    "Eval 3": "Exposición Oral", "Calif 3": "B",
                    "Observaciones": "Necesita reforzar conocimientos técnicos"
                },
                {
                    "Apellido y Nombre": "Laura Sánchez", "Curso": "EF 2B",
                    "Mar-01": "Presente", "Mar-02": "Presente", "Mar-03": "Presente", "Mar-04": "Presente", "Mar-05": "Presente",
                    "Mar-06": "Presente", "Mar-07": "Presente", "Mar-08": "Presente", "Mar-09": "Presente", "Mar-10": "Presente",
                    "Mar-11": "Presente", "Mar-12": "Presente", "Mar-13": "Presente", "Mar-14": "Presente", "Mar-15": "Presente",
                    "Mar-16": "Presente", "Mar-17": "Presente", "Mar-18": "Presente", "Mar-19": "Presente", "Mar-20": "Presente",
                    "Mar-21": "Presente", "Mar-22": "Presente", "Mar-23": "Presente", "Mar-24": "Presente", "Mar-25": "Presente",
                    "Mar-26": "Presente", "Mar-27": "Presente", "Mar-28": "Presente", "Mar-29": "Presente", "Mar-30": "Presente",
                    "Mar-31": "Presente",
                    "Tipo Evaluación": "Desempeño global",
                    "Eval 1": "Evaluación Global", "Calif 1": "MB",
                    "Eval 2": "Trabajo en Clase", "Calif 2": "EX",
                    "Eval 3": "Participación", "Calif 3": "B",
                    "Observaciones": "Excelente alumna, muy participativa"
                }
            ]
            
            # Cargar el DataFrame existente
            df_existente = pd.read_excel(archivo_excel, sheet_name="1 Trimestre")
            
            # Agregar datos de ejemplo al DataFrame existente
            df_con_ejemplo = pd.concat([df_existente, pd.DataFrame(datos_ejemplo)], ignore_index=True)
            
            # Guardar en Excel
            with pd.ExcelWriter(archivo_excel, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df_con_ejemplo.to_excel(writer, sheet_name="1 Trimestre", index=False)
            
            return True
        except Exception as e:
            st.error(f"Error agregando datos de ejemplo: {e}")
            return False
    return False

# Función para calcular nota de asistencia
def calcular_nota_asistencia(presentes, totales):
    if totales == 0:
        return 0
    porcentaje = (presentes / totales) * 100
    if porcentaje >= 80:
        return 10  # Ex
    elif porcentaje >= 51:
        return 8   # R+
    else:
        return 5   # M

# Función para convertir calificación a número
def calificacion_a_numero(calif):
    calif = str(calif).upper().strip()
    if calif == "M":
        return 4
    elif calif == "R-":
        return 6
    elif calif == "R+":
        return 7
    elif calif == "B":
        return 8
    elif calif == "MB":
        return 9
    elif calif == "EX":
        return 10
    else:
        try:
            return float(calif)
        except:
            return 0

# Crear archivo Excel si no existe
archivo_excel = crear_excel_si_no_existe()

# ==================== TAB 1: DASHBOARD GENERAL ====================
with tab1:
    st.header("📊 Dashboard General")
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Total Alumnos", "8", delta="2")
    
    with col2:
        st.metric("📊 Promedio Asistencia", "85%", delta="5%")
    
    with col3:
        st.metric("📝 Total Evaluaciones", "15", delta="3")
    
    with col4:
        st.metric("📈 Promedio General", "7.8", delta="0.5")
    
    st.markdown("---")
    
    # Resumen por cursos
    st.subheader("📂 Resumen por Cursos")
    
    resumen_cursos = [
        {"Curso": "EF 1A", "Alumnos": 2, "Asistencia": "90%", "Promedio": "8.2"},
        {"Curso": "EF 2A", "Alumnos": 1, "Asistencia": "85%", "Promedio": "7.8"},
        {"Curso": "EF 1B", "Alumnos": 1, "Asistencia": "100%", "Promedio": "9.0"},
        {"Curso": "TD 2A", "Alumnos": 1, "Asistencia": "75%", "Promedio": "6.7"},
        {"Curso": "EF 2B", "Alumnos": 1, "Asistencia": "100%", "Promedio": "9.2"}
    ]
    
    df_resumen = pd.DataFrame(resumen_cursos)
    st.dataframe(df_resumen, use_container_width=True)
    
    # Botón para agregar datos de ejemplo
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Agregar Datos de Ejemplo", type="primary", help="Agrega datos de ejemplo para probar el sistema"):
            if agregar_datos_ejemplo():
                st.success("✅ Datos de ejemplo agregados exitosamente!")
                st.balloons()
                st.rerun()
    
    with col2:
        if st.button("🔄 Actualizar Dashboard", type="secondary"):
            st.rerun()
    
    with col3:
        st.info("📁 Archivo: sistema_educativo.xlsx")

# ==================== TAB 2: GESTIÓN DE ALUMNOS ====================
with tab2:
    st.header("👥 Gestión de Alumnos")
    
    # Formulario para agregar nuevo alumno
    with st.expander("➕ Agregar Nuevo Alumno"):
        col1, col2 = st.columns(2)
        
        with col1:
            nombre_alumno = st.text_input("👤 Apellido y Nombre:", key="nuevo_alumno_nombre")
            curso_alumno = st.selectbox("📂 Curso:", ["EF 1A", "EF 2A", "EF 2A", "EF 1B", "EF 2B", "TD 2A", "TD 2B"], key="nuevo_alumno_curso")
        
        with col2:
            trimestre_alumno = st.selectbox("📅 Trimestre:", ["1 Trimestre", "2 Trimestre", "3 Trimestre"], key="nuevo_alumno_trimestre")
        
        if st.button("➕ Agregar Alumno", type="primary", key="agregar_alumno"):
            if nombre_alumno and curso_alumno and trimestre_alumno:
                st.success(f"✅ Alumno {nombre_alumno} agregado exitosamente!")
                st.balloons()
            else:
                st.error("❌ Por favor completa todos los campos")
    
    # Mostrar alumnos existentes
    st.markdown("---")
    st.subheader("📋 Alumnos Existentes")
    
    # Leer datos del Excel
    try:
        df_alumnos = pd.read_excel(archivo_excel, sheet_name="1 Trimestre")
        
        # Aplicar filtros
        if curso_seleccionado != "Todos":
            df_alumnos = df_alumnos[df_alumnos["Curso"] == curso_seleccionado]
        
        if alumno_seleccionado != "Todos":
            df_alumnos = df_alumnos[df_alumnos["Apellido y Nombre"] == alumno_seleccionado]
        
        # Mostrar tabla de alumnos con datos clave
        if not df_alumnos.empty:
            # Calcular asistencia y notas para cada alumno
            display_data = []
            
            for idx, row in df_alumnos.iterrows():
                if pd.notna(row["Apellido y Nombre"]):
                    # Calcular asistencia
                    columnas_asistencia = [col for col in df_alumnos.columns if any(mes in col for mes in ["Mar-", "Abr-", "May-"])]
                    presentes = 0
                    totales = 0
                    
                    for col in columnas_asistencia:
                        if pd.notna(row[col]):
                            totales += 1
                            if row[col] == "Presente":
                                presentes += 1
                    
                    porcentaje_asistencia = (presentes / totales * 100) if totales > 0 else 0
                    nota_asistencia = calcular_nota_asistencia(presentes, totales)
                    
                    # Calcular promedio de evaluaciones
                    calificaciones = []
                    for i in range(1, 7):
                        calif_col = f"Calif {i}"
                        if pd.notna(row[calif_col]):
                            calificaciones.append(calificacion_a_numero(row[calif_col]))
                    
                    promedio_eval = sum(calificaciones) / len(calificaciones) if calificaciones else 0
                    
                    display_data.append({
                        "Alumno": row["Apellido y Nombre"],
                        "Curso": row["Curso"],
                        "% Asistencia": f"{porcentaje_asistencia:.1f}%",
                        "Nota Asistencia": nota_asistencia,
                        "Promedio Evaluaciones": f"{promedio_eval:.1f}",
                        "Tipo Evaluación": row.get("Tipo Evaluación", ""),
                        "Observaciones": row.get("Observaciones", "")
                    })
            
            df_display = pd.DataFrame(display_data)
            st.dataframe(df_display, use_container_width=True)
            
        else:
            st.info("📋 No hay alumnos que coincidan con los filtros seleccionados")
            
    except Exception as e:
        st.error(f"Error leyendo datos: {e}")
        st.info("📊 Haz clic en 'Agregar Datos de Ejemplo' para probar el sistema")

# ==================== TAB 3: ASISTENCIA INTERACTIVA ====================
with tab3:
    st.header("📋 Asistencia Interactiva")
    
    # Seleccionar fecha y curso
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fecha_asistencia = st.date_input("📅 Fecha de Asistencia:", value=datetime.now().date(), key="fecha_asistencia_interactiva")
    
    with col2:
        curso_asistencia = st.selectbox("📂 Curso:", ["Todos", "EF 1A", "EF 2A", "EF 2A", "EF 1B", "EF 2B", "TD 2A", "TD 2B"], key="curso_asistencia_interactiva")
    
    with col3:
        trimestre_asistencia = st.selectbox("📅 Trimestre:", ["1 Trimestre", "2 Trimestre", "3 Trimestre"], key="trimestre_asistencia_interactiva")
    
    st.markdown("---")
    
    # Leer datos del Excel
    try:
        df_asistencia = pd.read_excel(archivo_excel, sheet_name=trimestre_asistencia)
        
        # Aplicar filtros
        if curso_asistencia != "Todos":
            df_asistencia = df_asistencia[df_asistencia["Curso"] == curso_asistencia]
        
        if not df_asistencia.empty:
            # Obtener la columna de fecha actual
            fecha_str = fecha_asistencia.strftime("%b-%d")
            
            # Verificar si la columna existe
            if fecha_str in df_asistencia.columns:
                st.subheader(f"📋 Asistencia del día {fecha_str}")
                
                # Crear tabla interactiva
                st.write("Haz clic en los casilleros para marcar asistencia:")
                
                # Crear una copia para modificar
                df_modificable = df_asistencia.copy()
                
                # Inicializar session state para almacenar cambios
                if 'asistencia_temporal' not in st.session_state:
                    st.session_state.asistencia_temporal = {}
                
                # Crear tabla con checkboxes
                for idx, row in df_modificable.iterrows():
                    if pd.notna(row["Apellido y Nombre"]):
                        col1, col2, col3 = st.columns([3, 1, 1])
                        
                        with col1:
                            st.write(f"**{row['Apellido y Nombre']}** ({row['Curso']})")
                        
                        with col2:
                            # Obtener estado actual
                            estado_actual = row[fecha_str] if pd.notna(row[fecha_str]) else "Ausente"
                            
                            # Crear checkbox para cambiar estado
                            presente = st.checkbox(
                                "✅", 
                                value=(estado_actual == "Presente"),
                                key=f"asistencia_{idx}_{fecha_str}",
                                help="Marcar como Presente"
                            )
                            
                            # Guardar en session state
                            st.session_state.asistencia_temporal[f"{idx}_{fecha_str}"] = presente
                        
                        with col3:
                            if not presente:
                                st.write("❌ Ausente")
                            else:
                                st.write("✅ Presente")
                
                # Botón para guardar cambios
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("💾 Guardar Asistencia", type="primary", key="guardar_asistencia_interactiva"):
                        # Aplicar cambios al DataFrame
                        for key, presente in st.session_state.asistencia_temporal.items():
                            if fecha_str in key:
                                idx = int(key.split("_")[0])
                                df_modificable.at[idx, fecha_str] = "Presente" if presente else "Ausente"
                        
                        # Guardar en Excel
                        try:
                            with pd.ExcelWriter(archivo_excel, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                                df_modificable.to_excel(writer, sheet_name=trimestre_asistencia, index=False)
                            
                            st.success("✅ Asistencia guardada exitosamente!")
                            st.balloons()
                            
                            # Limpiar session state
                            st.session_state.asistencia_temporal = {}
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"Error guardando asistencia: {e}")
                
                with col2:
                    if st.button("🔄 Recargar Datos", type="secondary", key="recargar_asistencia"):
                        st.session_state.asistencia_temporal = {}
                        st.rerun()
                
                with col3:
                    # Calcular estadísticas del día
                    presentes_dia = 0
                    total_dia = 0
                    
                    for idx, row in df_modificable.iterrows():
                        if pd.notna(row["Apellido y Nombre"]):
                            total_dia += 1
                            if row[fecha_str] == "Presente":
                                presentes_dia += 1
                    
                    if total_dia > 0:
                        porcentaje_dia = (presentes_dia / total_dia) * 100
                        st.metric(f"📊 {fecha_str}", f"{presentes_dia}/{total_dia}", f"{porcentaje_dia:.1f}%")
                
                # Mostrar tabla actual
                st.markdown("---")
                st.subheader("📋 Vista Previa de Asistencia")
                
                # Preparar datos para mostrar
                display_asistencia = []
                for idx, row in df_modificable.iterrows():
                    if pd.notna(row["Apellido y Nombre"]):
                        display_asistencia.append({
                            "Alumno": row["Apellido y Nombre"],
                            "Curso": row["Curso"],
                            "Estado": row[fecha_str] if pd.notna(row[fecha_str]) else "Sin marcar"
                        })
                
                if display_asistencia:
                    df_display_asistencia = pd.DataFrame(display_asistencia)
                    
                    # Colorear según estado
                    def color_estado(val):
                        if val == "Presente":
                            return 'background-color: #d4edda; color: #155724'
                        elif val == "Ausente":
                            return 'background-color: #f8d7da; color: #721c24'
                        else:
                            return 'background-color: #fff3cd; color: #856404'
                    
                    st.dataframe(
                        df_display_asistencia.style.applymap(color_estado, subset=['Estado']),
                        use_container_width=True
                    )
                
            else:
                st.warning(f"⚠️ La columna para la fecha {fecha_str} no existe en el Excel")
                st.info("💡 Las fechas disponibles son: Mar-01, Mar-02, ..., May-31")
                
        else:
            st.info("📋 No hay alumnos para mostrar con los filtros seleccionados")
            
    except Exception as e:
        st.error(f"Error cargando datos de asistencia: {e}")
        st.info("📊 Haz clic en 'Agregar Datos de Ejemplo' para probar el sistema")

# Información del sistema
st.markdown("---")
st.subheader("📁 Información del Sistema")

col1, col2, col3 = st.columns(3)

with col1:
    if os.path.exists("sistema_educativo.xlsx"):
        st.success("✅ Archivo Excel creado")
        st.info("📁 Nombre: sistema_educativo.xlsx")
    else:
        st.warning("⚠️ Archivo no encontrado")

with col2:
    st.info("📂 Ubicación: Carpeta actual")
    st.info("🔄 Auto-backup: Activo")

with col3:
    st.info("📊 Total trimestres: 3")
    st.info("📅 Periodo: Mar-Dic")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #2E7D32; padding: 20px; border-top: 2px solid #4CAF50; border-radius: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'>
    <h2 style='color: white; margin-bottom: 10px;'>📚 Sistema de Gestión Educativa</h2>
    <p style='color: white; font-size: 16px; margin: 5px 0;'>
        <span style='color: #4CAF50;'>✅</span> Gestión completa con sidebar<br>
        <span style='color: #4CAF50;'>📋</span> Asistencia interactiva con checkboxes<br>
        <span style='color: #4CAF50;'>📊</span> Evaluaciones rápidas<br>
        <span style='color: #4CAF50;'>📁</span> Excel local con datos reales
    </p>
    <small style='color: rgba(255,255,255,0.8);'>Sistema educativo profesional y funcional</small>
</div>
""", unsafe_allow_html=True)
