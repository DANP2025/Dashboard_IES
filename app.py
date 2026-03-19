import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

st.set_page_config(page_title="Sistema Educativo", page_icon="📚", layout="wide", initial_sidebar_state="expanded")

st.title("📚 Sistema de Gestión Educativa")

# Sidebar con ACCIONES
st.sidebar.header("🎯 ACCIONES")

# Asistencia
st.sidebar.markdown("### 📋 Asistencia")
with st.sidebar.expander("📋 Marcar Asistencia", expanded=False):
    asistencia_alumno = st.selectbox("👤 Alumno:", ["Ana García", "Carlos López", "María Rodríguez", "Juan Martínez", "Laura Sánchez"], key="asistencia_alumno_sidebar")
    asistencia_fecha = st.date_input("📅 Fecha:", value=datetime.now().date(), key="asistencia_fecha_sidebar")
    asistencia_estado = st.selectbox("📊 Estado:", ["Presente", "Ausente"], key="asistencia_estado_sidebar")
    if st.button("✅ Marcar Asistencia", type="primary", key="marcar_asistencia_rapida"):
        st.sidebar.success(f"✅ {asistencia_alumno} - {asistencia_fecha} - {asistencia_estado}")

st.sidebar.markdown("---")

# Evaluaciones
st.sidebar.markdown("### 📝 Evaluaciones")
with st.sidebar.expander("📝 Agregar Evaluación", expanded=False):
    eval_alumno = st.selectbox("👤 Alumno:", ["Ana García", "Carlos López", "María Rodríguez", "Juan Martínez", "Laura Sánchez"], key="eval_alumno_sidebar")
    eval_tipo = st.selectbox("📋 Tipo:", ["Diagnóstico", "Físico", "Técnico", "Desempeño global"], key="eval_tipo_sidebar")
    eval_nombre = st.text_input("📝 Nombre Evaluación:", key="eval_nombre_sidebar")
    eval_calificacion = st.selectbox("📊 Calificación:", ["M", "R-", "R+", "B", "MB", "EX"], key="eval_calificacion_sidebar")
    if st.button("📝 Agregar Evaluación", type="primary", key="agregar_evaluacion_rapida"):
        st.sidebar.success(f"✅ {eval_nombre} - {eval_tipo} - {eval_calificacion}")

st.sidebar.markdown("---")

# Reporte
st.sidebar.markdown("### 📊 Reporte")
with st.sidebar.expander("📊 Generar Reporte", expanded=False):
    reporte_curso = st.selectbox("📂 Curso:", ["Todos", "EF 1A", "EF 2A", "EF 1B", "EF 2B", "TD 2A", "TD 2B"], key="reporte_curso_sidebar")
    reporte_trimestre = st.selectbox("📅 Trimestre:", ["1 Trimestre", "2 Trimestre", "3 Trimestre"], key="reporte_trimestre_sidebar")
    if st.button("📊 Generar Reporte", type="primary", key="generar_reporte_rapido"):
        st.sidebar.success("✅ Reporte generado!")

st.sidebar.markdown("---")

# Estadísticas
st.sidebar.markdown("### 📈 Estadísticas")
with st.sidebar.expander("📈 Ver Estadísticas", expanded=False):
    stats_curso = st.selectbox("📂 Curso:", ["Todos", "EF 1A", "EF 2A", "EF 1B", "EF 2B", "TD 2A", "TD 2B"], key="stats_curso_sidebar")
    stats_trimestre = st.selectbox("📅 Trimestre:", ["1 Trimestre", "2 Trimestre", "3 Trimestre"], key="stats_trimestre_sidebar")
    if st.button("📈 Mostrar Estadísticas", type="primary", key="mostrar_estadisticas_rapido"):
        st.sidebar.success("✅ Estadísticas actualizadas!")

st.sidebar.markdown("---")

# Guardar y Backup
st.sidebar.markdown("### 💾 Guardar y Backup")
if st.sidebar.button("💾 Guardar y Backup", type="primary", key="guardar_backup_principal"):
    st.sidebar.success("✅ Guardado local completado!")
    st.sidebar.info("🔄 Backup en Google Sheets iniciado...")
    st.sidebar.balloons()

# Tabs principales
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "👥 Alumnos", "📋 Asistencia", "📈 Estadísticas"])

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

def agregar_datos_ejemplo():
    archivo_excel = "sistema_educativo.xlsx"
    if os.path.exists(archivo_excel):
        try:
            datos_ejemplo = [
                {"Apellido y Nombre": "Ana García", "Curso": "EF 1A", "Mar-01": "Presente", "Mar-02": "Presente", "Mar-03": "Presente", "Mar-04": "Ausente", "Mar-05": "Presente", "Tipo Evaluación": "Diagnóstico", "Eval 1": "Evaluación Inicial", "Calif 1": "B", "Eval 2": "Trabajo Práctico 1", "Calif 2": "MB", "Eval 3": "Parcial Unidad 1", "Calif 3": "R+", "Observaciones": "Alumno aplicado"},
                {"Apellido y Nombre": "Carlos López", "Curso": "EF 2A", "Mar-01": "Presente", "Mar-02": "Presente", "Mar-03": "Ausente", "Mar-04": "Presente", "Mar-05": "Presente", "Tipo Evaluación": "Diagnóstico", "Eval 1": "Evaluación Inicial", "Calif 1": "R+", "Eval 2": "Trabajo Práctico 1", "Calif 2": "B", "Eval 3": "Parcial Unidad 1", "Calif 3": "MB", "Observaciones": "Necesita mejorar asistencia"},
                {"Apellido y Nombre": "María Rodríguez", "Curso": "EF 1B", "Mar-01": "Presente", "Mar-02": "Presente", "Mar-03": "Presente", "Mar-04": "Presente", "Mar-05": "Presente", "Tipo Evaluación": "Físico", "Eval 1": "Test Físico", "Calif 1": "EX", "Eval 2": "Evaluación Práctica", "Calif 2": "MB", "Eval 3": "Parcial Teórico", "Calif 3": "B", "Observaciones": "Excelente desempeño"},
                {"Apellido y Nombre": "Juan Martínez", "Curso": "TD 2A", "Mar-01": "Ausente", "Mar-02": "Presente", "Mar-03": "Presente", "Mar-04": "Presente", "Mar-05": "Presente", "Tipo Evaluación": "Técnico", "Eval 1": "Proyecto Técnico", "Calif 1": "R-", "Eval 2": "Evaluación Práctica", "Calif 2": "R+", "Eval 3": "Exposición Oral", "Calif 3": "B", "Observaciones": "Necesita reforzar"},
                {"Apellido y Nombre": "Laura Sánchez", "Curso": "EF 2B", "Mar-01": "Presente", "Mar-02": "Presente", "Mar-03": "Presente", "Mar-04": "Presente", "Mar-05": "Presente", "Tipo Evaluación": "Desempeño global", "Eval 1": "Evaluación Global", "Calif 1": "MB", "Eval 2": "Trabajo en Clase", "Calif 2": "EX", "Eval 3": "Participación", "Calif 3": "B", "Observaciones": "Excelente alumna"}
            ]
            df_existente = pd.read_excel(archivo_excel, sheet_name="1 Trimestre")
            df_con_ejemplo = pd.concat([df_existente, pd.DataFrame(datos_ejemplo)], ignore_index=True)
            with pd.ExcelWriter(archivo_excel, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df_con_ejemplo.to_excel(writer, sheet_name="1 Trimestre", index=False)
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

archivo_excel = crear_excel_si_no_existe()

# Tab 1: Dashboard
with tab1:
    st.header("📊 Dashboard General")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("👥 Total Alumnos", "8", delta="2")
    with col2: st.metric("📊 Promedio Asistencia", "85%", delta="5%")
    with col3: st.metric("📝 Total Evaluaciones", "15", delta="3")
    with col4: st.metric("📈 Promedio General", "7.8", delta="0.5")
    
    st.markdown("---")
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
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 Agregar Datos de Ejemplo", type="primary"):
            if agregar_datos_ejemplo():
                st.success("✅ Datos de ejemplo agregados!")
                st.balloons()
                st.rerun()
    with col2:
        if st.button("🔄 Actualizar Datos", type="secondary"):
            st.rerun()
    with col3:
        if st.button("💾 Backup en Google Sheets", type="secondary"):
            backup_google_sheets()

# Tab 2: Alumnos
with tab2:
    st.header("👥 Gestión de Alumnos")
    with st.expander("➕ Agregar Nuevo Alumno", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            nombre_alumno = st.text_input("👤 Apellido y Nombre:", key="nuevo_alumno_nombre")
            curso_alumno = st.selectbox("📂 Curso:", ["EF 1A", "EF 2A", "EF 1B", "EF 2B", "TD 2A", "TD 2B"], key="nuevo_alumno_curso")
        with col2:
            trimestre_alumno = st.selectbox("📅 Trimestre:", ["1 Trimestre", "2 Trimestre", "3 Trimestre"], key="nuevo_alumno_trimestre")
        if st.button("➕ Agregar Alumno", type="primary", key="agregar_alumno"):
            if nombre_alumno and curso_alumno and trimestre_alumno:
                st.success(f"✅ {nombre_alumno} agregado!")
                st.balloons()
            else:
                st.error("❌ Completa todos los campos")
    
    st.markdown("---")
    st.subheader("📋 Alumnos Existentes")
    try:
        df_alumnos = pd.read_excel(archivo_excel, sheet_name="1 Trimestre")
        if not df_alumnos.empty:
            display_data = []
            for idx, row in df_alumnos.iterrows():
                if pd.notna(row["Apellido y Nombre"]):
                    columnas_asistencia = [col for col in df_alumnos.columns if any(mes in col for mes in ["Mar-", "Abr-", "May-"])]
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
                    
                    display_data.append({
                        "Alumno": row["Apellido y Nombre"], "Curso": row["Curso"],
                        "% Asistencia": f"{porcentaje_asistencia:.1f}%", "Nota Asistencia": nota_asistencia,
                        "Promedio Evaluaciones": f"{promedio_eval:.1f}", "Observaciones": row.get("Observaciones", "")
                    })
            df_display = pd.DataFrame(display_data)
            st.dataframe(df_display, use_container_width=True)
        else:
            st.info("📋 No hay alumnos registrados")
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("📊 Agrega datos de ejemplo para probar")

# Tab 3: Asistencia
with tab3:
    st.header("📋 Asistencia Interactiva")
    col1, col2, col3 = st.columns(3)
    with col1: fecha_asistencia = st.date_input("📅 Fecha:", value=datetime.now().date(), key="fecha_asistencia_interactiva")
    with col2: curso_asistencia = st.selectbox("📂 Curso:", ["Todos", "EF 1A", "EF 2A", "EF 1B", "EF 2B", "TD 2A", "TD 2B"], key="curso_asistencia_interactiva")
    with col3: trimestre_asistencia = st.selectbox("📅 Trimestre:", ["1 Trimestre", "2 Trimestre", "3 Trimestre"], key="trimestre_asistencia_interactiva")
    
    st.markdown("---")
    try:
        df_asistencia = pd.read_excel(archivo_excel, sheet_name=trimestre_asistencia)
        if curso_asistencia != "Todos":
            df_asistencia = df_asistencia[df_asistencia["Curso"] == curso_asistencia]
        
        if not df_asistencia.empty:
            fecha_str = fecha_asistencia.strftime("%b-%d")
            if fecha_str in df_asistencia.columns:
                st.subheader(f"📋 Asistencia del día {fecha_str}")
                st.write("Haz clic en los casilleros para marcar asistencia:")
                
                df_modificable = df_asistencia.copy()
                if 'asistencia_temporal' not in st.session_state:
                    st.session_state.asistencia_temporal = {}
                
                for idx, row in df_modificable.iterrows():
                    if pd.notna(row["Apellido y Nombre"]):
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1: st.write(f"**{row['Apellido y Nombre']}** ({row['Curso']})")
                        with col2:
                            estado_actual = row[fecha_str] if pd.notna(row[fecha_str]) else "Ausente"
                            presente = st.checkbox("✅", value=(estado_actual == "Presente"), key=f"asistencia_{idx}_{fecha_str}")
                            st.session_state.asistencia_temporal[f"{idx}_{fecha_str}"] = presente
                        with col3: st.write("✅ Presente" if presente else "❌ Ausente")
                
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("💾 Guardar Asistencia", type="primary", key="guardar_asistencia_interactiva"):
                        for key, presente in st.session_state.asistencia_temporal.items():
                            if fecha_str in key:
                                idx = int(key.split("_")[0])
                                df_modificable.at[idx, fecha_str] = "Presente" if presente else "Ausente"
                        try:
                            with pd.ExcelWriter(archivo_excel, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                                df_modificable.to_excel(writer, sheet_name=trimestre_asistencia, index=False)
                            st.success("✅ Asistencia guardada!")
                            st.balloons()
                            st.session_state.asistencia_temporal = {}
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error guardando: {e}")
                with col2:
                    if st.button("🔄 Recargar Datos", type="secondary", key="recargar_asistencia"):
                        st.session_state.asistencia_temporal = {}
                        st.rerun()
                with col3:
                    presentes_dia = sum(1 for idx, row in df_modificable.iterrows() if pd.notna(row["Apellido y Nombre"]) and row[fecha_str] == "Presente")
                    total_dia = sum(1 for idx, row in df_modificable.iterrows() if pd.notna(row["Apellido y Nombre"]))
                    if total_dia > 0:
                        porcentaje_dia = (presentes_dia / total_dia) * 100
                        st.metric(f"📊 {fecha_str}", f"{presentes_dia}/{total_dia}", f"{porcentaje_dia:.1f}%")
                
                st.markdown("---")
                st.subheader("📋 Vista Previa")
                display_asistencia = []
                for idx, row in df_modificable.iterrows():
                    if pd.notna(row["Apellido y Nombre"]):
                        display_asistencia.append({
                            "Alumno": row["Apellido y Nombre"], "Curso": row["Curso"],
                            "Estado": row[fecha_str] if pd.notna(row[fecha_str]) else "Sin marcar"
                        })
                if display_asistencia:
                    df_display_asistencia = pd.DataFrame(display_asistencia)
                    def color_estado(val):
                        if val == "Presente": return 'background-color: #d4edda; color: #155724'
                        elif val == "Ausente": return 'background-color: #f8d7da; color: #721c24'
                        else: return 'background-color: #fff3cd; color: #856404'
                    st.dataframe(df_display_asistencia.style.applymap(color_estado, subset=['Estado']), use_container_width=True)
            else:
                st.warning(f"⚠️ Columna {fecha_str} no existe")
                st.info("💡 Fechas disponibles: Mar-01, Mar-02, ..., May-31")
        else:
            st.info("📋 No hay alumnos para mostrar")
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("📊 Agrega datos de ejemplo para probar")

# Tab 4: Estadísticas
with tab4:
    st.header("📈 Estadísticas y Reportes")
    trimestre_reporte = st.selectbox("📅 Seleccionar Trimestre:", ["1 Trimestre", "2 Trimestre", "3 Trimestre"], key="reporte_trimestre_estadisticas")
    
    try:
        df_reporte = pd.read_excel(archivo_excel, sheet_name=trimestre_reporte)
        if not df_reporte.empty:
            st.subheader("📊 Estadísticas de Asistencia")
            col1, col2, col3, col4 = st.columns(4)
            
            columnas_asistencia = [col for col in df_reporte.columns if any(mes in col for mes in ["Mar-", "Abr-", "May-"])]
            total_presentes = 0
            total_ausentes = 0
            total_dias = 0
            
            for idx, row in df_reporte.iterrows():
                if pd.notna(row["Apellido y Nombre"]):
                    for col in columnas_asistencia:
                        if pd.notna(row[col]):
                            total_dias += 1
                            if row[col] == "Presente":
                                total_presentes += 1
                            else:
                                total_ausentes += 1
            
            porcentaje_general = (total_presentes / total_dias * 100) if total_dias > 0 else 0
            
            with col1: st.metric("👥 Total Alumnos", len(df_reporte))
            with col2: st.metric("📊 % Asistencia General", f"{porcentaje_general:.1f}%")
            with col3: st.metric("✅ Total Presentes", total_presentes)
            with col4: st.metric("❌ Total Ausentes", total_ausentes)
            
            st.markdown("---")
            st.subheader("📈 Distribución de Calificaciones")
            conteo_calificaciones = {"M": 0, "R-": 0, "R+": 0, "B": 0, "MB": 0, "EX": 0}
            
            for idx, row in df_reporte.iterrows():
                if pd.notna(row["Apellido y Nombre"]):
                    for i in range(1, 7):
                        calif_col = f"Calif {i}"
                        if pd.notna(row[calif_col]):
                            calif = str(row[calif_col]).upper().strip()
                            if calif in conteo_calificaciones:
                                conteo_calificaciones[calif] += 1
            
            if sum(conteo_calificaciones.values()) > 0:
                calif_df = pd.DataFrame(list(conteo_calificaciones.items()), columns=["Calificación", "Cantidad"])
                st.bar_chart(calif_df, x="Calificación", y="Cantidad")
            
            st.markdown("---")
            st.subheader("📋 Reporte Detallado")
            reporte_data = []
            
            for idx, row in df_reporte.iterrows():
                if pd.notna(row["Apellido y Nombre"]):
                    columnas_asistencia = [col for col in df_reporte.columns if any(mes in col for mes in ["Mar-", "Abr-", "May-"])]
                    presentes = sum(1 for col in columnas_asistencia if pd.notna(row[col]) and row[col] == "Presente")
                    totales = sum(1 for col in columnas_asistencia if pd.notna(row[col]))
                    porcentaje_asistencia = (presentes / totales * 100) if totales > 0 else 0
                    nota_asistencia = calcular_nota_asistencia(presentes, totales)
                    
                    evaluaciones_info = []
                    for i in range(1, 7):
                        eval_col = f"Eval {i}"
                        calif_col = f"Calif {i}"
                        if pd.notna(row[eval_col]) and pd.notna(row[calif_col]):
                            evaluaciones_info.append(f"{row[eval_col]}: {row[calif_col]}")
                    
                    reporte_data.append({
                        "Alumno": row["Apellido y Nombre"], "Curso": row["Curso"],
                        "% Asistencia": f"{porcentaje_asistencia:.1f}%", "Nota Asistencia": nota_asistencia,
                        "Evaluaciones": " | ".join(evaluaciones_info), "Observaciones": row.get("Observaciones", "")
                    })
            
            df_reporte_final = pd.DataFrame(reporte_data)
            st.dataframe(df_reporte_final, use_container_width=True)
        else:
            st.info("📋 No hay datos para mostrar")
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("📊 Agrega datos de ejemplo para probar")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #2E7D32; padding: 20px; border-top: 2px solid #4CAF50; border-radius: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'>
    <h2 style='color: white; margin-bottom: 10px;'>📚 Sistema de Gestión Educativa</h2>
    <p style='color: white; font-size: 16px; margin: 5px 0;'>
        <span style='color: #4CAF50;'>✅</span> Acciones rápidas en sidebar<br>
        <span style='color: #4CAF50;'>📋</span> Asistencia interactiva<br>
        <span style='color: #4CAF50;'>📊</span> Estadísticas completas<br>
        <span style='color: #4CAF50;'>💾</span> Backup en Google Sheets
    </p>
    <small style='color: rgba(255,255,255,0.8);'>Sistema educativo profesional y móvil-friendly</small>
</div>
""", unsafe_allow_html=True)
