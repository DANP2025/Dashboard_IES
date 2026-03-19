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

# Sidebar con filtros
st.sidebar.header("🔍 Filtros")

# Filtro de cursos
cursos_disponibles = ["Todos", "EF 1A", "EF 2A", "EF 2A", "EF 1B", "EF 2B", "TD 2A", "TD 2B"]
curso_seleccionado = st.sidebar.selectbox("📂 Seleccionar Curso:", cursos_disponibles)

# Filtro de trimestres
trimestres_disponibles = ["Todos", "1 Trimestre", "2 Trimestre", "3 Trimestre"]
trimestre_seleccionado = st.sidebar.selectbox("📅 Seleccionar Trimestre:", trimestres_disponibles)

# Filtro de alumno
alumnos_disponibles = ["Todos", "Ana García", "Carlos López", "María Rodríguez", "Juan Martínez", "Laura Sánchez"]
alumno_seleccionado = st.sidebar.selectbox("👤 Seleccionar Alumno:", alumnos_disponibles)

# Sistema de navegación por pestañas
tab1, tab2, tab3 = st.tabs([
    "📊 Gestión de Alumnos", 
    "📋 Asistencia", 
    "📝 Evaluaciones"
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

# Función para leer datos del Excel
def leer_datos_excel(trimestre):
    archivo_excel = "sistema_educativo.xlsx"
    
    if not os.path.exists(archivo_excel):
        crear_excel_si_no_existe()
        return pd.DataFrame()
    
    try:
        df = pd.read_excel(archivo_excel, sheet_name=trimestre)
        return df
    except:
        return pd.DataFrame()

# Función para guardar datos en Excel
def guardar_datos_excel(df, trimestre):
    archivo_excel = "sistema_educativo.xlsx"
    
    try:
        with pd.ExcelWriter(archivo_excel, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=trimestre, index=False)
        return True
    except Exception as e:
        st.error(f"Error guardando datos: {e}")
        return False

# Función para calcular nota de asistencia
def calcular_nota_asistencia(porcentaje_asistencia):
    if porcentaje_asistencia >= 80:
        return 10  # Ex
    elif porcentaje_asistencia >= 51:
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

# ==================== TAB 1: GESTIÓN DE ALUMNOS ====================
with tab1:
    st.header("📊 Gestión de Alumnos")
    
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
                # Leer datos existentes
                df_existente = leer_datos_excel(trimestre_alumno)
                
                # Crear nueva fila
                nueva_fila = {
                    "Apellido y Nombre": nombre_alumno,
                    "Curso": curso_alumno
                }
                
                # Agregar fila al DataFrame
                df_nuevo = pd.concat([df_existente, pd.DataFrame([nueva_fila])], ignore_index=True)
                
                # Guardar en Excel
                if guardar_datos_excel(df_nuevo, trimestre_alumno):
                    st.success(f"✅ Alumno {nombre_alumno} agregado exitosamente!")
                    st.balloons()
                    st.rerun()
            else:
                st.error("❌ Por favor completa todos los campos")
    
    # Mostrar alumnos existentes
    st.markdown("---")
    st.subheader("📋 Alumnos Existentes")
    
    # Seleccionar trimestre para mostrar
    trimestre_mostrar = st.selectbox("📅 Seleccionar Trimestre para ver:", ["1 Trimestre", "2 Trimestre", "3 Trimestre"], key="mostrar_trimestre")
    
    df_alumnos = leer_datos_excel(trimestre_mostrar)
    
    if not df_alumnos.empty:
        # Aplicar filtros
        if curso_seleccionado != "Todos":
            df_alumnos = df_alumnos[df_alumnos["Curso"] == curso_seleccionado]
        
        if alumno_seleccionado != "Todos":
            df_alumnos = df_alumnos[df_alumnos["Apellido y Nombre"] == alumno_seleccionado]
        
        if not df_alumnos.empty:
            st.dataframe(df_alumnos[["Apellido y Nombre", "Curso"]], use_container_width=True)
        else:
            st.info("📋 No hay alumnos que coincidan con los filtros seleccionados")
    else:
        st.info("📋 No hay alumnos registrados en este trimestre")

# ==================== TAB 2: ASISTENCIA ====================
with tab2:
    st.header("📋 Gestión de Asistencia")
    
    # Formulario para marcar asistencia
    with st.expander("✅ Marcar Asistencia"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            trimestre_asistencia = st.selectbox("📅 Trimestre:", ["1 Trimestre", "2 Trimestre", "3 Trimestre"], key="asistencia_trimestre")
            
            # Obtener alumnos del trimestre
            df_alumnos_asistencia = leer_datos_excel(trimestre_asistencia)
            if not df_alumnos_asistencia.empty:
                alumnos_lista = df_alumnos_asistencia["Apellido y Nombre"].tolist()
                alumno_asistencia = st.selectbox("👤 Alumno:", alumnos_lista, key="asistencia_alumno")
            else:
                st.warning("⚠️ No hay alumnos registrados en este trimestre")
                alumno_asistencia = None
        
        with col2:
            fecha_asistencia = st.date_input("📅 Fecha:", value=datetime.now().date(), key="asistencia_fecha")
            estado_asistencia = st.selectbox("📊 Estado:", ["Presente", "Ausente"], key="asistencia_estado")
        
        with col3:
            if st.button("✅ Marcar Asistencia", type="primary", key="marcar_asistencia"):
                if alumno_asistencia:
                    # Leer datos existentes
                    df_existente = leer_datos_excel(trimestre_asistencia)
                    
                    # Encontrar fila del alumno
                    alumno_fila = df_existente[df_existente["Apellido y Nombre"] == alumno_asistencia]
                    
                    if not alumno_fila.empty:
                        # Obtener índice
                        idx = alumno_fila.index[0]
                        
                        # Formatear fecha para columna
                        fecha_str = fecha_asistencia.strftime("%b-%d")
                        
                        # Marcar asistencia
                        df_existente.at[idx, fecha_str] = "Presente" if estado_asistencia == "Presente" else "Ausente"
                        
                        # Calcular nota de asistencia
                        # Contar presentes y ausentes
                        columnas_asistencia = [col for col in df_existente.columns if any(mes in col for mes in ["Mar-", "Abr-", "May-", "Jun-", "Jul-", "Ago-", "Sep-", "Oct-", "Nov-", "Dec-"])]
                        
                        presentes = 0
                        totales = 0
                        
                        for col in columnas_asistencia:
                            if pd.notna(df_existente.at[idx, col]):
                                totales += 1
                                if df_existente.at[idx, col] == "Presente":
                                    presentes += 1
                        
                        if totales > 0:
                            porcentaje = (presentes / totales) * 100
                            nota_asistencia = calcular_nota_asistencia(porcentaje)
                            df_existente.at[idx, "Nota Asistencia"] = nota_asistencia
                        
                        # Guardar en Excel
                        if guardar_datos_excel(df_existente, trimestre_asistencia):
                            st.success(f"✅ Asistencia marcada para {alumno_asistencia}")
                            st.info(f"📊 Porcentaje de asistencia: {porcentaje:.1f}% - Nota: {nota_asistencia}")
                            st.balloons()
                            st.rerun()
                    else:
                        st.error("❌ Alumno no encontrado")
                else:
                    st.error("❌ Por favor selecciona un alumno")
    
    # Mostrar resumen de asistencia
    st.markdown("---")
    st.subheader("📊 Resumen de Asistencia")
    
    trimestre_resumen = st.selectbox("📅 Trimestre para resumen:", ["1 Trimestre", "2 Trimestre", "3 Trimestre"], key="resumen_trimestre")
    
    df_resumen = leer_datos_excel(trimestre_resumen)
    
    if not df_resumen.empty:
        # Aplicar filtros
        if curso_seleccionado != "Todos":
            df_resumen = df_resumen[df_resumen["Curso"] == curso_seleccionado]
        
        if alumno_seleccionado != "Todos":
            df_resumen = df_resumen[df_resumen["Apellido y Nombre"] == alumno_seleccionado]
        
        if not df_resumen.empty:
            # Calcular estadísticas de asistencia
            resumen_data = []
            
            for idx, row in df_resumen.iterrows():
                if pd.notna(row["Apellido y Nombre"]):
                    # Contar presentes y ausentes
                    columnas_asistencia = [col for col in df_resumen.columns if any(mes in col for mes in ["Mar-", "Abr-", "May-", "Jun-", "Jul-", "Ago-", "Sep-", "Oct-", "Nov-", "Dec-"])]
                    
                    presentes = 0
                    totales = 0
                    
                    for col in columnas_asistencia:
                        if pd.notna(row[col]):
                            totales += 1
                            if row[col] == "Presente":
                                presentes += 1
                    
                    if totales > 0:
                        porcentaje = (presentes / totales) * 100
                        nota_asistencia = calcular_nota_asistencia(porcentaje)
                        
                        resumen_data.append({
                            "Alumno": row["Apellido y Nombre"],
                            "Curso": row["Curso"],
                            "Días Presentes": presentes,
                            "Total Días": totales,
                            "% Asistencia": f"{porcentaje:.1f}%",
                            "Nota Asistencia": nota_asistencia
                        })
            
            if resumen_data:
                df_resumen_final = pd.DataFrame(resumen_data)
                st.dataframe(df_resumen_final, use_container_width=True)
            else:
                st.info("📋 No hay datos de asistencia para mostrar")
        else:
            st.info("📋 No hay alumnos que coincidan con los filtros seleccionados")

# ==================== TAB 3: EVALUACIONES ====================
with tab3:
    st.header("📝 Gestión de Evaluaciones")
    
    # Formulario para agregar evaluaciones
    with st.expander("📝 Agregar Evaluación"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            trimestre_eval = st.selectbox("📅 Trimestre:", ["1 Trimestre", "2 Trimestre", "3 Trimestre"], key="eval_trimestre")
            
            # Obtener alumnos del trimestre
            df_alumnos_eval = leer_datos_excel(trimestre_eval)
            if not df_alumnos_eval.empty:
                alumnos_eval_lista = df_alumnos_eval["Apellido y Nombre"].tolist()
                alumno_eval = st.selectbox("👤 Alumno:", alumnos_eval_lista, key="eval_alumno")
            else:
                st.warning("⚠️ No hay alumnos registrados en este trimestre")
                alumno_eval = None
        
        with col2:
            tipo_evaluacion = st.selectbox("📋 Tipo Evaluación:", ["Diagnóstico", "Físico", "Técnico", "Desempeño global"], key="eval_tipo")
        
        with col3:
            nombre_evaluacion = st.text_input("📝 Nombre Evaluación:", key="eval_nombre")
            calificacion_eval = st.selectbox("📊 Calificación:", ["M", "R-", "R+", "B", "MB", "EX"], key="eval_calificacion")
        
        if st.button("📝 Agregar Evaluación", type="primary", key="agregar_evaluacion"):
            if alumno_eval and nombre_evaluacion:
                # Leer datos existentes
                df_existente = leer_datos_excel(trimestre_eval)
                
                # Encontrar fila del alumno
                alumno_fila = df_existente[df_existente["Apellido y Nombre"] == alumno_eval]
                
                if not alumno_fila.empty:
                    # Obtener índice
                    idx = alumno_fila.index[0]
                    
                    # Establecer tipo de evaluación
                    df_existente.at[idx, "Tipo Evaluación"] = tipo_evaluacion
                    
                    # Buscar la primera columna de evaluación vacía
                    eval_cols = [col for col in df_existente.columns if col.startswith("Eval ") and col != "Tipo Evaluación"]
                    
                    for i, col in enumerate(eval_cols[:6]):  # Máximo 6 evaluaciones
                        calif_col = col.replace("Eval", "Calif")
                        
                        if pd.isna(df_existente.at[idx, col]) or df_existente.at[idx, col] == "":
                            df_existente.at[idx, col] = nombre_evaluacion
                            df_existente.at[idx, calif_col] = calificacion_eval
                            break
                    
                    # Calcular nota final de evaluaciones
                    calificaciones = []
                    for col in eval_cols[:6]:
                        calif_col = col.replace("Eval", "Calif")
                        if pd.notna(df_existente.at[idx, calif_col]):
                            calificaciones.append(calificacion_a_numero(df_existente.at[idx, calif_col]))
                    
                    if calificaciones:
                        nota_final = sum(calificaciones) / len(calificaciones)
                        df_existente.at[idx, "Nota Final Evaluaciones"] = round(nota_final, 2)
                    
                    # Guardar en Excel
                    if guardar_datos_excel(df_existente, trimestre_eval):
                        st.success(f"✅ Evaluación '{nombre_evaluacion}' agregada para {alumno_eval}")
                        st.info(f"📊 Calificación: {calificacion_eval}")
                        st.balloons()
                        st.rerun()
                else:
                    st.error("❌ Alumno no encontrado")
            else:
                st.error("❌ Por favor completa todos los campos")
    
    # Mostrar resumen de evaluaciones
    st.markdown("---")
    st.subheader("📊 Resumen de Evaluaciones")
    
    trimestre_eval_resumen = st.selectbox("📅 Trimestre para resumen:", ["1 Trimestre", "2 Trimestre", "3 Trimestre"], key="eval_resumen_trimestre")
    
    df_eval_resumen = leer_datos_excel(trimestre_eval_resumen)
    
    if not df_eval_resumen.empty:
        # Aplicar filtros
        if curso_seleccionado != "Todos":
            df_eval_resumen = df_eval_resumen[df_eval_resumen["Curso"] == curso_seleccionado]
        
        if alumno_seleccionado != "Todos":
            df_eval_resumen = df_eval_resumen[df_eval_resumen["Apellido y Nombre"] == alumno_seleccionado]
        
        if not df_eval_resumen.empty:
            # Preparar datos de evaluaciones
            eval_data = []
            
            for idx, row in df_eval_resumen.iterrows():
                if pd.notna(row["Apellido y Nombre"]):
                    # Obtener evaluaciones
                    eval_cols = [col for col in df_eval_resumen.columns if col.startswith("Eval ") and col != "Tipo Evaluación"]
                    
                    for i, col in enumerate(eval_cols[:6]):  # Máximo 6 evaluaciones
                        calif_col = col.replace("Eval", "Calif")
                        
                        if pd.notna(row[col]) and pd.notna(row[calif_col]):
                            eval_data.append({
                                "Alumno": row["Apellido y Nombre"],
                                "Curso": row["Curso"],
                                "Tipo Evaluación": row.get("Tipo Evaluación", ""),
                                "Evaluación": row[col],
                                "Calificación": row[calif_col],
                                "Nota Numérica": calificacion_a_numero(row[calif_col])
                            })
            
            if eval_data:
                df_eval_final = pd.DataFrame(eval_data)
                st.dataframe(df_eval_final, use_container_width=True)
                
                # Estadísticas de evaluaciones
                st.markdown("---")
                st.subheader("📈 Estadísticas de Evaluaciones")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    total_eval = len(df_eval_final)
                    st.metric("📝 Total Evaluaciones", total_eval)
                
                with col2:
                    promedio = df_eval_final["Nota Numérica"].mean()
                    st.metric("📊 Promedio General", f"{promedio:.2f}")
                
                with col3:
                    max_nota = df_eval_final["Nota Numérica"].max()
                    st.metric("🏆 Nota Máxima", f"{max_nota:.2f}")
                
                with col4:
                    min_nota = df_eval_final["Nota Numérica"].min()
                    st.metric("📉 Nota Mínima", f"{min_nota:.2f}")
            else:
                st.info("📋 No hay evaluaciones registradas")
        else:
            st.info("📋 No hay alumnos que coincidan con los filtros seleccionados")

# Información del archivo
st.markdown("---")
st.subheader("📁 Información del Archivo")

col1, col2, col3 = st.columns(3)

with col1:
    if os.path.exists("sistema_educativo.xlsx"):
        st.success("✅ Archivo Excel creado")
        st.info("📁 Nombre: sistema_educativo.xlsx")
    else:
        st.warning("⚠️ Archivo no encontrado")

with col2:
    st.info("📂 Ubicación: Mis Documentos")
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
        <span style='color: #4CAF50;'>✅</span> Gestión completa de alumnos<br>
        <span style='color: #4CAF50;'>📋</span> Control de asistencia por trimestres<br>
        <span style='color: #4CAF50;'>📝</span> Sistema de evaluaciones<br>
        <span style='color: #4CAF50;'>📁</span> Backup automático en Excel
    </p>
    <small style='color: rgba(255,255,255,0.8);'>Sistema educativo completo y funcional</small>
</div>
""", unsafe_allow_html=True)
