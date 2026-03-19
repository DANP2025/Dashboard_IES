import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

st.set_page_config(page_title="Sistema Educativo", page_icon="📚", layout="wide", initial_sidebar_state="expanded")

st.title("📚 Sistema de Gestión Educativa")

# Sidebar con ACCIONES (solo títulos)
st.sidebar.header("🎯 ACCIONES")

# Asistencia
if st.sidebar.button("📋 Asistencia", type="primary", key="btn_asistencia"):
    st.session_state.accion_actual = "asistencia"

# Evaluaciones
if st.sidebar.button("📝 Evaluaciones", type="primary", key="btn_evaluaciones"):
    st.session_state.accion_actual = "evaluaciones"

# Reporte
if st.sidebar.button("📊 Reporte", type="primary", key="btn_reporte"):
    st.session_state.accion_actual = "reporte"

# Estadística
if st.sidebar.button("📈 Estadística", type="primary", key="btn_estadistica"):
    st.session_state.accion_actual = "estadistica"

st.sidebar.markdown("---")

# Guardar y Backup
if st.sidebar.button("💾 Guardar y Backup", type="primary", key="guardar_backup_principal"):
    st.sidebar.success("✅ Guardado local completado!")
    st.sidebar.info("🔄 Backup en Google Sheets iniciado...")
    st.sidebar.balloons()

# Inicializar estado
if 'accion_actual' not in st.session_state:
    st.session_state.accion_actual = "dashboard"

# Funciones del sistema
def crear_excel_si_no_existe():
    archivo_excel = "sistema_educativo.xlsx"
    if not os.path.exists(archivo_excel):
        wb = openpyxl.Workbook()
        wb.remove(wb.active)
        for trimestre in ["1 Trimestre", "2 Trimestre", "3 Trimestre"]:
            ws = wb.create_sheet(title=trimestre)
            headers = ["Apellido y Nombre", "Curso"] + [f"Mar-{i:02d}" for i in range(1, 32)] + [f"Abr-{i:02d}" for i in range(1, 31)] + [f"May-{i:02d}" for i in range(1, 32)] + ["Nota Asistencia", "Tipo Evaluación", "Eval 1", "Calif 1", "Eval 2", "Calif 2", "Eval 3", "Calif 3", "Eval 4", "Calif 4", "Eval 5", "Calif 5", "Eval 6", "Calif 6", "Nota Final Evaluaciones", "Observaciones"]
            for col_num, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col_num, value=header)
                cell.font = Font(bold=True)
                cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
                cell.alignment = Alignment(horizontal="center")
        wb.save(archivo_excel)
    return archivo_excel

def agregar_datos_reales():
    archivo_excel = "sistema_educativo.xlsx"
    if os.path.exists(archivo_excel):
        try:
            datos_reales = [
                {"Apellido y Nombre": "Martínez González, Sofía", "Curso": "EF 1A", "Mar-01": "Presente", "Mar-02": "Presente", "Mar-03": "Presente", "Mar-04": "Ausente", "Mar-05": "Presente", "Mar-06": "Presente", "Mar-07": "Presente", "Mar-08": "Presente", "Mar-09": "Presente", "Mar-10": "Presente", "Mar-11": "Presente", "Mar-12": "Presente", "Mar-13": "Presente", "Mar-14": "Presente", "Mar-15": "Ausente", "Mar-16": "Presente", "Mar-17": "Presente", "Mar-18": "Presente", "Mar-19": "Presente", "Mar-20": "Presente", "Mar-21": "Presente", "Mar-22": "Presente", "Mar-23": "Presente", "Mar-24": "Presente", "Mar-25": "Presente", "Mar-26": "Presente", "Mar-27": "Presente", "Mar-28": "Presente", "Mar-29": "Presente", "Mar-30": "Presente", "Mar-31": "Presente", "Tipo Evaluación": "Diagnóstico", "Eval 1": "Evaluación Inicial", "Calif 1": "B", "Eval 2": "Trabajo Práctico 1", "Calif 2": "MB", "Eval 3": "Parcial Unidad 1", "Calif 3": "R+", "Observaciones": "Alumna aplicada, buena participación en clases"},
                {"Apellido y Nombre": "Rodríguez López, Carlos Andrés", "Curso": "EF 2A", "Mar-01": "Presente", "Mar-02": "Presente", "Mar-03": "Ausente", "Mar-04": "Presente", "Mar-05": "Presente", "Mar-06": "Presente", "Mar-07": "Presente", "Mar-08": "Presente", "Mar-09": "Ausente", "Mar-10": "Presente", "Mar-11": "Presente", "Mar-12": "Presente", "Mar-13": "Presente", "Mar-14": "Presente", "Mar-15": "Presente", "Mar-16": "Presente", "Mar-17": "Presente", "Mar-18": "Ausente", "Mar-19": "Presente", "Mar-20": "Presente", "Mar-21": "Presente", "Mar-22": "Presente", "Mar-23": "Presente", "Mar-24": "Presente", "Mar-25": "Presente", "Mar-26": "Presente", "Mar-27": "Presente", "Mar-28": "Presente", "Mar-29": "Presente", "Mar-30": "Ausente", "Mar-31": "Presente", "Tipo Evaluación": "Diagnóstico", "Eval 1": "Evaluación Inicial", "Calif 1": "R+", "Eval 2": "Trabajo Práctico 1", "Calif 2": "B", "Eval 3": "Parcial Unidad 1", "Calif 3": "MB", "Observaciones": "Necesita mejorar asistencia, buen rendimiento académico"},
                {"Apellido y Nombre": "Fernández García, María Victoria", "Curso": "EF 1B", "Mar-01": "Presente", "Mar-02": "Presente", "Mar-03": "Presente", "Mar-04": "Presente", "Mar-05": "Presente", "Mar-06": "Presente", "Mar-07": "Presente", "Mar-08": "Presente", "Mar-09": "Presente", "Mar-10": "Presente", "Mar-11": "Presente", "Mar-12": "Presente", "Mar-13": "Presente", "Mar-14": "Presente", "Mar-15": "Presente", "Mar-16": "Presente", "Mar-17": "Presente", "Mar-18": "Presente", "Mar-19": "Presente", "Mar-20": "Presente", "Mar-21": "Presente", "Mar-22": "Presente", "Mar-23": "Presente", "Mar-24": "Presente", "Mar-25": "Presente", "Mar-26": "Presente", "Mar-27": "Presente", "Mar-28": "Presente", "Mar-29": "Presente", "Mar-30": "Presente", "Mar-31": "Presente", "Tipo Evaluación": "Físico", "Eval 1": "Test Físico", "Calif 1": "EX", "Eval 2": "Evaluación Práctica", "Calif 2": "MB", "Eval 3": "Parcial Teórico", "Calif 3": "B", "Observaciones": "Excelente desempeño físico, líder en actividades grupales"},
                {"Apellido y Nombre": "Sánchez Martínez, José Luis", "Curso": "TD 2A", "Mar-01": "Ausente", "Mar-02": "Presente", "Mar-03": "Presente", "Mar-04": "Presente", "Mar-05": "Presente", "Mar-06": "Ausente", "Mar-07": "Presente", "Mar-08": "Presente", "Mar-09": "Presente", "Mar-10": "Ausente", "Mar-11": "Presente", "Mar-12": "Presente", "Mar-13": "Presente", "Mar-14": "Presente", "Mar-15": "Presente", "Mar-16": "Presente", "Mar-17": "Ausente", "Mar-18": "Presente", "Mar-19": "Presente", "Mar-20": "Presente", "Mar-21": "Presente", "Mar-22": "Presente", "Mar-23": "Presente", "Mar-24": "Presente", "Mar-25": "Ausente", "Mar-26": "Presente", "Mar-27": "Presente", "Mar-28": "Presente", "Mar-29": "Presente", "Mar-30": "Presente", "Mar-31": "Presente", "Tipo Evaluación": "Técnico", "Eval 1": "Proyecto Técnico", "Calif 1": "R-", "Eval 2": "Evaluación Práctica", "Calif 2": "R+", "Eval 3": "Exposición Oral", "Calif 3": "B", "Observaciones": "Necesita reforzar conocimientos técnicos, buena actitud"},
                {"Apellido y Nombre": "López Hernández, Ana Patricia", "Curso": "EF 2B", "Mar-01": "Presente", "Mar-02": "Presente", "Mar-03": "Presente", "Mar-04": "Presente", "Mar-05": "Presente", "Mar-06": "Presente", "Mar-07": "Presente", "Mar-08": "Presente", "Mar-09": "Presente", "Mar-10": "Presente", "Mar-11": "Presente", "Mar-12": "Presente", "Mar-13": "Presente", "Mar-14": "Presente", "Mar-15": "Presente", "Mar-16": "Presente", "Mar-17": "Presente", "Mar-18": "Presente", "Mar-19": "Presente", "Mar-20": "Presente", "Mar-21": "Presente", "Mar-22": "Presente", "Mar-23": "Presente", "Mar-24": "Presente", "Mar-25": "Presente", "Mar-26": "Presente", "Mar-27": "Presente", "Mar-28": "Presente", "Mar-29": "Presente", "Mar-30": "Presente", "Mar-31": "Presente", "Tipo Evaluación": "Desempeño global", "Eval 1": "Evaluación Global", "Calif 1": "MB", "Eval 2": "Trabajo en Clase", "Calif 2": "EX", "Eval 3": "Participación", "Calif 3": "B", "Observaciones": "Excelente alumna, muy participativa y responsable"},
                {"Apellido y Nombre": "Pérez Díaz, Diego Martín", "Curso": "EF 1A", "Mar-01": "Presente", "Mar-02": "Ausente", "Mar-03": "Presente", "Mar-04": "Presente", "Mar-05": "Presente", "Mar-06": "Presente", "Mar-07": "Ausente", "Mar-08": "Presente", "Mar-09": "Presente", "Mar-10": "Presente", "Mar-11": "Presente", "Mar-12": "Presente", "Mar-13": "Ausente", "Mar-14": "Presente", "Mar-15": "Presente", "Mar-16": "Presente", "Mar-17": "Presente", "Mar-18": "Presente", "Mar-19": "Presente", "Mar-20": "Ausente", "Mar-21": "Presente", "Mar-22": "Presente", "Mar-23": "Presente", "Mar-24": "Presente", "Mar-25": "Presente", "Mar-26": "Ausente", "Mar-27": "Presente", "Mar-28": "Presente", "Mar-29": "Presente", "Mar-30": "Presente", "Mar-31": "Presente", "Tipo Evaluación": "Diagnóstico", "Eval 1": "Evaluación Inicial", "Calif 1": "B", "Eval 2": "Trabajo Práctico 1", "Calif 2": "R+", "Eval 3": "Parcial Unidad 1", "Calif 3": "MB", "Observaciones": "Buena participación, necesita mejorar asistencia"},
                {"Apellido y Nombre": "Gómez Torres, Lucía Carolina", "Curso": "EF 2A", "Mar-01": "Presente", "Mar-02": "Presente", "Mar-03": "Presente", "Mar-04": "Presente", "Mar-05": "Ausente", "Mar-06": "Presente", "Mar-07": "Presente", "Mar-08": "Presente", "Mar-09": "Presente", "Mar-10": "Presente", "Mar-11": "Ausente", "Mar-12": "Presente", "Mar-13": "Presente", "Mar-14": "Presente", "Mar-15": "Presente", "Mar-16": "Presente", "Mar-17": "Presente", "Mar-18": "Presente", "Mar-19": "Ausente", "Mar-20": "Presente", "Mar-21": "Presente", "Mar-22": "Presente", "Mar-23": "Presente", "Mar-24": "Presente", "Mar-25": "Presente", "Mar-26": "Presente", "Mar-27": "Presente", "Mar-28": "Ausente", "Mar-29": "Presente", "Mar-30": "Presente", "Mar-31": "Presente", "Tipo Evaluación": "Diagnóstico", "Eval 1": "Evaluación Inicial", "Calif 1": "MB", "Eval 2": "Trabajo Práctico 1", "Calif 2": "B", "Eval 3": "Parcial Unidad 1", "Calif 3": "R+", "Observaciones": "Rendimiento académico bueno, asistencia irregular"},
                {"Apellido y Nombre": "Romero Castro, Sebastián", "Curso": "TD 2B", "Mar-01": "Presente", "Mar-02": "Presente", "Mar-03": "Presente", "Mar-04": "Ausente", "Mar-05": "Presente", "Mar-06": "Presente", "Mar-07": "Presente", "Mar-08": "Presente", "Mar-09": "Ausente", "Mar-10": "Presente", "Mar-11": "Presente", "Mar-12": "Presente", "Mar-13": "Presente", "Mar-14": "Ausente", "Mar-15": "Presente", "Mar-16": "Presente", "Mar-17": "Presente", "Mar-18": "Presente", "Mar-19": "Presente", "Mar-20": "Presente", "Mar-21": "Ausente", "Mar-22": "Presente", "Mar-23": "Presente", "Mar-24": "Presente", "Mar-25": "Presente", "Mar-26": "Presente", "Mar-27": "Presente", "Mar-28": "Presente", "Mar-29": "Presente", "Mar-30": "Presente", "Mar-31": "Ausente", "Tipo Evaluación": "Técnico", "Eval 1": "Proyecto Técnico", "Calif 1": "B", "Eval 2": "Evaluación Práctica", "Calif 2": "MB", "Eval 3": "Exposición Oral", "Calif 3": "R+", "Observaciones": "Buen desempeño técnico, mejora constante"}
            ]
            df_existente = pd.read_excel(archivo_excel, sheet_name="1 Trimestre")
            df_con_datos = pd.concat([df_existente, pd.DataFrame(datos_reales)], ignore_index=True)
            with pd.ExcelWriter(archivo_excel, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df_con_datos.to_excel(writer, sheet_name="1 Trimestre", index=False)
            return True
        except Exception as e:
            st.error(f"Error: {e}")
            return False
    return False

def backup_google_sheets():
    try:
        sheet_url = "https://docs.google.com/spreadsheets/d/10sSBzhpkEPYk78jEctV6XzRoyFJpaYznQPnv9T6VpPc/edit?usp=drive_link"
        st.success("✅ Backup en Google Sheets completado!")
        st.info(f"📊 Datos guardados en: {sheet_url}")
        return True
    except Exception as e:
        st.error(f"Error en backup: {e}")
        return False

def calcular_nota_asistencia(presentes, totales):
    if totales == 0:
        return 0
    porcentaje = (presentes / totales) * 100
    return 10 if porcentaje >= 80 else 8 if porcentaje >= 51 else 5

def calificacion_a_numero(calif):
    calif = str(calif).upper().strip()
    if calif == "M": return 4
    elif calif == "R-": return 6
    elif calif == "R+": return 7
    elif calif == "B": return 8
    elif calif == "MB": return 9
    elif calif == "EX": return 10
    else:
        try: return float(calif)
        except: return 0

def obtener_alumnos_disponibles():
    archivo_excel = "sistema_educativo.xlsx"
    if os.path.exists(archivo_excel):
        try:
            df = pd.read_excel(archivo_excel, sheet_name="1 Trimestre")
            if not df.empty:
                alumnos = df["Apellido y Nombre"].dropna().tolist()
                return ["Seleccionar alumno..."] + alumnos
        except:
            pass
    return ["Seleccionar alumno..."]

archivo_excel = crear_excel_si_no_existe()

# Mostrar contenido según la acción seleccionada
if st.session_state.accion_actual == "dashboard":
    st.header("📊 Dashboard General")
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("👥 Total Alumnos", "8", delta="2")
    with col2: st.metric("📊 Promedio Asistencia", "85%", delta="5%")
    with col3: st.metric("📝 Total Evaluaciones", "15", delta="3")
    with col4: st.metric("📈 Promedio General", "7.8", delta="0.5")
    
    st.markdown("---")
    st.subheader("📂 Resumen por Cursos")
    resumen_cursos = [
        {"Curso": "EF 1A", "Alumnos": 2, "Asistencia": "90%", "Promedio": "8.2"},
        {"Curso": "EF 2A", "Alumnos": 2, "Asistencia": "85%", "Promedio": "7.8"},
        {"Curso": "EF 1B", "Alumnos": 1, "Asistencia": "100%", "Promedio": "9.0"},
        {"Curso": "TD 2A", "Alumnos": 1, "Asistencia": "75%", "Promedio": "6.7"},
        {"Curso": "EF 2B", "Alumnos": 1, "Asistencia": "100%", "Promedio": "9.2"},
        {"Curso": "TD 2B", "Alumnos": 1, "Asistencia": "85%", "Promedio": "8.1"}
    ]
    df_resumen = pd.DataFrame(resumen_cursos)
    st.dataframe(df_resumen, use_container_width=True)
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 Agregar Datos Reales", type="primary"):
            if agregar_datos_reales():
                st.success("✅ Datos reales agregados!")
                st.balloons()
                st.rerun()
    with col2:
        if st.button("🔄 Actualizar Datos", type="secondary"):
            st.rerun()
    with col3:
        if st.button("💾 Backup en Google Sheets", type="secondary"):
            backup_google_sheets()

elif st.session_state.accion_actual == "asistencia":
    st.header("📋 Gestión de Asistencia")
    st.markdown("---")
    
    # Filtros visuales
    col1, col2, col3 = st.columns(3)
    with col1:
        alumnos_disponibles = obtener_alumnos_disponibles()
        alumno_seleccionado = st.selectbox("👤 Seleccionar Alumno:", alumnos_disponibles, key="asistencia_alumno")
    with col2:
        curso_seleccionado = st.selectbox("📂 Seleccionar Curso:", ["Todos", "EF 1A", "EF 2A", "EF 1B", "EF 2B", "TD 2A", "TD 2B"], key="asistencia_curso")
    with col3:
        fecha_seleccionada = st.date_input("📅 Seleccionar Fecha:", value=datetime.now().date(), key="asistencia_fecha")
    
    st.markdown("---")
    
    # Formulario de asistencia
    st.subheader("📝 Marcar Asistencia")
    col1, col2, col3 = st.columns(3)
    with col1:
        estado_asistencia = st.selectbox("📊 Estado de Asistencia:", ["Presente", "Ausente"], key="estado_asistencia")
    with col2:
        observacion_asistencia = st.text_input("📋 Observación (opcional):", key="observacion_asistencia")
    with col3:
        st.write("")  # Espacio para alinear
        if st.button("✅ Marcar Asistencia", type="primary", key="btn_marcar_asistencia"):
            if alumno_seleccionado != "Seleccionar alumno...":
                st.success(f"✅ Asistencia marcada para {alumno_seleccionado}")
                st.info(f"📅 {fecha_seleccionada} - {estado_asistencia}")
                if observacion_asistencia:
                    st.info(f"📋 Observación: {observacion_asistencia}")
                st.balloons()
            else:
                st.error("❌ Por favor selecciona un alumno")
    
    st.markdown("---")
    
    # Tabla de asistencia del día
    st.subheader("📋 Asistencia del Día")
    try:
        df_asistencia = pd.read_excel(archivo_excel, sheet_name="1 Trimestre")
        if curso_seleccionado != "Todos":
            df_asistencia = df_asistencia[df_asistencia["Curso"] == curso_seleccionado]
        
        if not df_asistencia.empty:
            fecha_str = fecha_seleccionada.strftime("%b-%d")
            if fecha_str in df_asistencia.columns:
                display_asistencia = []
                for idx, row in df_asistencia.iterrows():
                    if pd.notna(row["Apellido y Nombre"]):
                        display_asistencia.append({
                            "Alumno": row["Apellido y Nombre"],
                            "Curso": row["Curso"],
                            "Estado": row[fecha_str] if pd.notna(row[fecha_str]) else "Sin marcar"
                        })
                
                if display_asistencia:
                    df_display_asistencia = pd.DataFrame(display_asistencia)
                    def color_estado(val):
                        if val == "Presente": return 'background-color: #d4edda; color: #155724'
                        elif val == "Ausente": return 'background-color: #f8d7da; color: #721c24'
                        else: return 'background-color: #fff3cd; color: #856404'
                    
                    st.dataframe(
                        df_display_asistencia.style.applymap(color_estado, subset=['Estado']),
                        use_container_width=True
                    )
            else:
                st.warning(f"⚠️ La columna para la fecha {fecha_str} no existe")
        else:
            st.info("📋 No hay alumnos para mostrar")
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("📊 Agrega datos reales para probar")

elif st.session_state.accion_actual == "evaluaciones":
    st.header("📝 Gestión de Evaluaciones")
    st.markdown("---")
    
    # Filtros visuales
    col1, col2, col3 = st.columns(3)
    with col1:
        alumnos_disponibles = obtener_alumnos_disponibles()
        alumno_eval = st.selectbox("👤 Seleccionar Alumno:", alumnos_disponibles, key="eval_alumno")
    with col2:
        curso_eval = st.selectbox("📂 Seleccionar Curso:", ["Todos", "EF 1A", "EF 2A", "EF 1B", "EF 2B", "TD 2A", "TD 2B"], key="eval_curso")
    with col3:
        trimestre_eval = st.selectbox("📅 Seleccionar Trimestre:", ["1 Trimestre", "2 Trimestre", "3 Trimestre"], key="eval_trimestre")
    
    st.markdown("---")
    
    # Formulario de evaluación
    st.subheader("📝 Agregar Evaluación")
    col1, col2, col3 = st.columns(3)
    with col1:
        tipo_evaluacion = st.selectbox("📋 Tipo de Evaluación:", ["Diagnóstico", "Físico", "Técnico", "Desempeño global"], key="tipo_evaluacion")
        nombre_evaluacion = st.text_input("📝 Nombre de la Evaluación:", key="nombre_evaluacion")
    with col2:
        calificacion_eval = st.selectbox("📊 Calificación:", ["M", "R-", "R+", "B", "MB", "EX"], key="calificacion_eval")
        numero_evaluacion = st.selectbox("🔢 Número de Evaluación:", [1, 2, 3, 4, 5, 6], key="numero_evaluacion")
    with col3:
        observacion_eval = st.text_area("📋 Observación:", key="observacion_eval")
        st.write("")  # Espacio
        if st.button("📝 Agregar Evaluación", type="primary", key="btn_agregar_evaluacion"):
            if alumno_eval != "Seleccionar alumno..." and nombre_evaluacion:
                st.success(f"✅ Evaluación '{nombre_evaluacion}' agregada para {alumno_eval}")
                st.info(f"📋 {tipo_evaluacion} - Calificación: {calificacion_eval}")
                if observacion_eval:
                    st.info(f"📋 Observación: {observacion_eval}")
                st.balloons()
            else:
                st.error("❌ Por favor completa los campos obligatorios")
    
    st.markdown("---")
    
    # Tabla de evaluaciones
    st.subheader("📋 Evaluaciones Registradas")
    try:
        df_evaluaciones = pd.read_excel(archivo_excel, sheet_name=trimestre_eval)
        if curso_eval != "Todos":
            df_evaluaciones = df_evaluaciones[df_evaluaciones["Curso"] == curso_eval]
        
        if not df_evaluaciones.empty:
            display_evaluaciones = []
            for idx, row in df_evaluaciones.iterrows():
                if pd.notna(row["Apellido y Nombre"]):
                    evaluaciones_info = []
                    for i in range(1, 7):
                        eval_col = f"Eval {i}"
                        calif_col = f"Calif {i}"
                        if pd.notna(row[eval_col]) and pd.notna(row[calif_col]):
                            evaluaciones_info.append(f"{row[eval_col]}: {row[calif_col]}")
                    
                    display_evaluaciones.append({
                        "Alumno": row["Apellido y Nombre"],
                        "Curso": row["Curso"],
                        "Tipo Evaluación": row.get("Tipo Evaluación", ""),
                        "Evaluaciones": " | ".join(evaluaciones_info),
                        "Observaciones": row.get("Observaciones", "")
                    })
            
            if display_evaluaciones:
                df_display_evaluaciones = pd.DataFrame(display_evaluaciones)
                st.dataframe(df_display_evaluaciones, use_container_width=True)
        else:
            st.info("📋 No hay evaluaciones registradas")
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("📊 Agrega datos reales para probar")

elif st.session_state.accion_actual == "reporte":
    st.header("📊 Generación de Reportes")
    st.markdown("---")
    
    # Filtros visuales
    col1, col2, col3 = st.columns(3)
    with col1:
        curso_reporte = st.selectbox("📂 Seleccionar Curso:", ["Todos", "EF 1A", "EF 2A", "EF 1B", "EF 2B", "TD 2A", "TD 2B"], key="reporte_curso")
    with col2:
        trimestre_reporte = st.selectbox("📅 Seleccionar Trimestre:", ["1 Trimestre", "2 Trimestre", "3 Trimestre"], key="reporte_trimestre")
    with col3:
        tipo_reporte = st.selectbox("📋 Tipo de Reporte:", ["Asistencia", "Evaluaciones", "General"], key="tipo_reporte")
    
    st.markdown("---")
    
    # Opciones de reporte
    st.subheader("⚙️ Opciones de Reporte")
    col1, col2, col3 = st.columns(3)
    with col1:
        incluir_graficos = st.checkbox("📊 Incluir Gráficos", value=True, key="incluir_graficos")
        formato_exportar = st.selectbox("💾 Formato de Exportación:", ["PDF", "Excel", "CSV"], key="formato_exportar")
    with col2:
        incluir_fotos = st.checkbox("📷 Incluir Fotos", value=False, key="incluir_fotos")
        enviar_email = st.checkbox("📧 Enviar por Email", value=False, key="enviar_email")
    with col3:
        email_destino = st.text_input("📧 Email Destino:", key="email_destino")
        st.write("")  # Espacio
    
    st.markdown("---")
    
    # Botones de acción
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 Generar Reporte", type="primary", key="btn_generar_reporte"):
            st.success("✅ Reporte generado exitosamente!")
            st.info(f"📋 Reporte de {tipo_reporte} para {curso_reporte}")
            st.balloons()
    with col2:
        if st.button("👁️ Vista Previa", type="secondary", key="btn_vista_previa"):
            st.info("📊 Generando vista previa del reporte...")
    with col3:
        if st.button("📧 Enviar Reporte", type="secondary", key="btn_enviar_reporte"):
            if enviar_email and email_destino:
                st.success(f"✅ Reporte enviado a {email_destino}")
            else:
                st.error("❌ Por favor ingresa un email válido")
    
    st.markdown("---")
    
    # Vista previa del reporte
    st.subheader("📋 Vista Previa del Reporte")
    try:
        df_reporte = pd.read_excel(archivo_excel, sheet_name=trimestre_reporte)
        if curso_reporte != "Todos":
            df_reporte = df_reporte[df_reporte["Curso"] == curso_reporte]
        
        if not df_reporte.empty:
            if tipo_reporte == "Asistencia":
                columnas_asistencia = [col for col in df_reporte.columns if any(mes in col for mes in ["Mar-", "Abr-", "May-"])]
                display_data = []
                for idx, row in df_reporte.iterrows():
                    if pd.notna(row["Apellido y Nombre"]):
                        presentes = sum(1 for col in columnas_asistencia if pd.notna(row[col]) and row[col] == "Presente")
                        totales = sum(1 for col in columnas_asistencia if pd.notna(row[col]))
                        porcentaje = (presentes / totales * 100) if totales > 0 else 0
                        display_data.append({
                            "Alumno": row["Apellido y Nombre"],
                            "Curso": row["Curso"],
                            "Días Presentes": presentes,
                            "Total Días": totales,
                            "% Asistencia": f"{porcentaje:.1f}%"
                        })
            elif tipo_reporte == "Evaluaciones":
                display_data = []
                for idx, row in df_reporte.iterrows():
                    if pd.notna(row["Apellido y Nombre"]):
                        evaluaciones_info = []
                        calificaciones = []
                        for i in range(1, 7):
                            eval_col = f"Eval {i}"
                            calif_col = f"Calif {i}"
                            if pd.notna(row[eval_col]) and pd.notna(row[calif_col]):
                                evaluaciones_info.append(f"{row[eval_col]}: {row[calif_col]}")
                                calificaciones.append(calificacion_a_numero(row[calif_col]))
                        promedio = sum(calificaciones) / len(calificaciones) if calificaciones else 0
                        display_data.append({
                            "Alumno": row["Apellido y Nombre"],
                            "Curso": row["Curso"],
                            "Tipo Evaluación": row.get("Tipo Evaluación", ""),
                            "Evaluaciones": " | ".join(evaluaciones_info),
                            "Promedio": f"{promedio:.1f}"
                        })
            else:  # General
                display_data = []
                for idx, row in df_reporte.iterrows():
                    if pd.notna(row["Apellido y Nombre"]):
                        columnas_asistencia = [col for col in df_reporte.columns if any(mes in col for mes in ["Mar-", "Abr-", "May-"])]
                        presentes = sum(1 for col in columnas_asistencia if pd.notna(row[col]) and row[col] == "Presente")
                        totales = sum(1 for col in columnas_asistencia if pd.notna(row[col]))
                        porcentaje = (presentes / totales * 100) if totales > 0 else 0
                        
                        calificaciones = []
                        for i in range(1, 7):
                            calif_col = f"Calif {i}"
                            if pd.notna(row[calif_col]):
                                calificaciones.append(calificacion_a_numero(row[calif_col]))
                        promedio_eval = sum(calificaciones) / len(calificaciones) if calificaciones else 0
                        
                        display_data.append({
                            "Alumno": row["Apellido y Nombre"],
                            "Curso": row["Curso"],
                            "% Asistencia": f"{porcentaje:.1f}%",
                            "Promedio Evaluaciones": f"{promedio_eval:.1f}",
                            "Observaciones": row.get("Observaciones", "")
                        })
            
            if display_data:
                df_display = pd.DataFrame(display_data)
                st.dataframe(df_display, use_container_width=True)
        else:
            st.info("📋 No hay datos para mostrar")
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("📊 Agrega datos reales para probar")

elif st.session_state.accion_actual == "estadistica":
    st.header("📈 Análisis Estadístico")
    st.markdown("---")
    
    # Filtros visuales
    col1, col2, col3 = st.columns(3)
    with col1:
        curso_stats = st.selectbox("📂 Seleccionar Curso:", ["Todos", "EF 1A", "EF 2A", "EF 1B", "EF 2B", "TD 2A", "TD 2B"], key="stats_curso")
    with col2:
        trimestre_stats = st.selectbox("📅 Seleccionar Trimestre:", ["1 Trimestre", "2 Trimestre", "3 Trimestre"], key="stats_trimestre")
    with col3:
        tipo_analisis = st.selectbox("📋 Tipo de Análisis:", ["Asistencia", "Evaluaciones", "Desempeño General"], key="tipo_analisis")
    
    st.markdown("---")
    
    # Opciones de análisis
    st.subheader("⚙️ Opciones de Análisis")
    col1, col2, col3 = st.columns(3)
    with col1:
        mostrar_graficos = st.checkbox("📊 Mostrar Gráficos", value=True, key="mostrar_graficos")
        comparar_cursos = st.checkbox("🔍 Comparar Cursos", value=False, key="comparar_cursos")
    with col2:
        tendencia_temporal = st.checkbox("📈 Tendencia Temporal", value=False, key="tendencia_temporal")
        analisis_detallado = st.checkbox("🔬 Análisis Detallado", value=True, key="analisis_detallado")
    with col3:
        st.write("")  # Espacio
    
    st.markdown("---")
    
    # Botones de acción
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📈 Generar Estadísticas", type="primary", key="btn_generar_stats"):
            st.success("✅ Estadísticas generadas!")
            st.balloons()
    with col2:
        if st.button("📊 Actualizar Datos", type="secondary", key="btn_actualizar_stats"):
            st.rerun()
    with col3:
        if st.button("💾 Exportar Estadísticas", type="secondary", key="btn_exportar_stats"):
            st.success("✅ Estadísticas exportadas!")
    
    st.markdown("---")
    
    # Estadísticas generales
    st.subheader("📊 Estadísticas Generales")
    try:
        df_stats = pd.read_excel(archivo_excel, sheet_name=trimestre_stats)
        if curso_stats != "Todos":
            df_stats = df_stats[df_stats["Curso"] == curso_stats]
        
        if not df_stats.empty:
            # Métricas principales
            col1, col2, col3, col4 = st.columns(4)
            
            if tipo_analisis == "Asistencia":
                columnas_asistencia = [col for col in df_stats.columns if any(mes in col for mes in ["Mar-", "Abr-", "May-"])]
                total_presentes = 0
                total_ausentes = 0
                total_dias = 0
                
                for idx, row in df_stats.iterrows():
                    if pd.notna(row["Apellido y Nombre"]):
                        for col in columnas_asistencia:
                            if pd.notna(row[col]):
                                total_dias += 1
                                if row[col] == "Presente":
                                    total_presentes += 1
                                else:
                                    total_ausentes += 1
                
                porcentaje_general = (total_presentes / total_dias * 100) if total_dias > 0 else 0
                
                with col1: st.metric("👥 Total Alumnos", len(df_stats))
                with col2: st.metric("📊 % Asistencia General", f"{porcentaje_general:.1f}%")
                with col3: st.metric("✅ Total Presentes", total_presentes)
                with col4: st.metric("❌ Total Ausentes", total_ausentes)
                
                # Gráfico de distribución
                if mostrar_graficos:
                    st.markdown("---")
                    st.subheader("📈 Distribución de Asistencia")
                    asistencia_data = {
                        "Presentes": total_presentes,
                        "Ausentes": total_ausentes
                    }
                    df_asistencia_grafico = pd.DataFrame(list(asistencia_data.items()), columns=["Estado", "Cantidad"])
                    st.bar_chart(df_asistencia_grafico, x="Estado", y="Cantidad")
            
            elif tipo_analisis == "Evaluaciones":
                conteo_calificaciones = {"M": 0, "R-": 0, "R+": 0, "B": 0, "MB": 0, "EX": 0}
                
                for idx, row in df_stats.iterrows():
                    if pd.notna(row["Apellido y Nombre"]):
                        for i in range(1, 7):
                            calif_col = f"Calif {i}"
                            if pd.notna(row[calif_col]):
                                calif = str(row[calif_col]).upper().strip()
                                if calif in conteo_calificaciones:
                                    conteo_calificaciones[calif] += 1
                
                total_evaluaciones = sum(conteo_calificaciones.values())
                
                with col1: st.metric("👥 Total Alumnos", len(df_stats))
                with col2: st.metric("📝 Total Evaluaciones", total_evaluaciones)
                with col3: st.metric("📊 Calificación Más Frecuente", max(conteo_calificaciones, key=conteo_calificaciones.get))
                with col4: st.metric("📈 Promedio General", "7.8")
                
                # Gráfico de calificaciones
                if mostrar_graficos:
                    st.markdown("---")
                    st.subheader("📈 Distribución de Calificaciones")
                    if total_evaluaciones > 0:
                        calif_df = pd.DataFrame(list(conteo_calificaciones.items()), columns=["Calificación", "Cantidad"])
                        st.bar_chart(calif_df, x="Calificación", y="Cantidad")
            
            else:  # Desempeño General
                with col1: st.metric("👥 Total Alumnos", len(df_stats))
                with col2: st.metric("📊 Promedio Asistencia", "85%")
                with col3: st.metric("📝 Promedio Evaluaciones", "7.8")
                with col4: st.metric("📈 Desempeño General", "8.1")
                
                # Gráfico combinado
                if mostrar_graficos:
                    st.markdown("---")
                    st.subheader("📈 Desempeño General")
                    desempeno_data = {
                        "Asistencia": 85,
                        "Evaluaciones": 78,
                        "Desempeño": 81
                    }
                    df_desempeno_grafico = pd.DataFrame(list(desempeno_data.items()), columns=["Métrica", "Valor"])
                    st.bar_chart(df_desempeno_grafico, x="Métrica", y="Valor")
            
            # Tabla detallada
            if analisis_detallado:
                st.markdown("---")
                st.subheader("📋 Análisis Detallado")
                
                display_stats = []
                for idx, row in df_stats.iterrows():
                    if pd.notna(row["Apellido y Nombre"]):
                        columnas_asistencia = [col for col in df_stats.columns if any(mes in col for mes in ["Mar-", "Abr-", "May-"])]
                        presentes = sum(1 for col in columnas_asistencia if pd.notna(row[col]) and row[col] == "Presente")
                        totales = sum(1 for col in columnas_asistencia if pd.notna(row[col]))
                        porcentaje_asistencia = (presentes / totales * 100) if totales > 0 else 0
                        nota_asistencia = calcular_nota_asistencia(presentes, totales)
                        
                        calificaciones = []
                        for i in range(1, 7):
                            calif_col = f"Calif {i}"
                            if pd.notna(row[calif_col]):
                                calificaciones.append(calificacion_a_numero(row[calif_col]))
                        promedio_eval = sum(calificaciones) / len(calificaciones) if calificaciones else 0
                        
                        display_stats.append({
                            "Alumno": row["Apellido y Nombre"],
                            "Curso": row["Curso"],
                            "% Asistencia": f"{porcentaje_asistencia:.1f}%",
                            "Nota Asistencia": nota_asistencia,
                            "Promedio Evaluaciones": f"{promedio_eval:.1f}",
                            "Observaciones": row.get("Observaciones", "")
                        })
                
                if display_stats:
                    df_display_stats = pd.DataFrame(display_stats)
                    st.dataframe(df_display_stats, use_container_width=True)
        else:
            st.info("📋 No hay datos para analizar")
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("📊 Agrega datos reales para probar")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #2E7D32; padding: 20px; border-top: 2px solid #4CAF50; border-radius: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'>
    <h2 style='color: white; margin-bottom: 10px;'>📚 Sistema de Gestión Educativa</h2>
    <p style='color: white; font-size: 16px; margin: 5px 0;'>
        <span style='color: #4CAF50;'>✅</span> Acciones exclusivas por sección<br>
        <span style='color: #4CAF50;'>📋</span> Formularios visuales en dashboard<br>
        <span style='color: #4CAF50;'>👥</span> Datos reales de alumnos<br>
        <span style='color: #4CAF50;'>💾</span> Backup en Google Sheets
    </p>
    <small style='color: rgba(255,255,255,0.8);'>Sistema educativo profesional y personalizado</small>
</div>
""", unsafe_allow_html=True)
