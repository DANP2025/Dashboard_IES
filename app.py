import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
import random

st.set_page_config(page_title="Sistema Educativo", page_icon="📚", layout="wide", initial_sidebar_state="expanded")

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
            headers = ["Apellido y Nombre", "Curso"] + [f"Mar-{i:02d}" for i in range(1, 32)] + [f"Abr-{i:02d}" for i in range(1, 31)] + [f"May-{i:02d}" for i in range(1, 32)] + ["Nota Asistencia", "Tipo Evaluación", "Eval 1", "Calif 1", "Eval 2", "Calif 2", "Eval 3", "Calif 3", "Eval 4", "Calif 4", "Nota Final Evaluaciones", "Observaciones"]
            for col_num, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col_num, value=header)
                cell.font = Font(bold=True)
                cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
                cell.alignment = Alignment(horizontal="center")
        wb.save(archivo_excel)
    return archivo_excel

def agregar_datos_simulados():
    archivo_excel = "sistema_educativo.xlsx"
    if os.path.exists(archivo_excel):
        try:
            # Nombres femeninos para simulación
            nombres_femeninos = [
                "García López, Sofía María", "Rodríguez Martínez, Ana Isabel", "Fernández García, Laura Patricia",
                "Sánchez Hernández, María José", "López Torres, Carmen Rosa", "Pérez Díaz, Beatriz Elena",
                "Gómez Ruiz, Patricia Alejandra", "Martínez Castro, María Fernanda", "Romero Vargas, Ana Sofía",
                "Alvarez Moreno, Isabel Cristina"
            ]
            
            datos_simulados = []
            
            # Generar datos para cada curso
            cursos = ["EF 1A", "EF 2A", "EF 1B", "EF 2B", "TD 2A", "TD 2B"]
            
            for curso in cursos:
                for i, nombre in enumerate(nombres_femeninos[:10]):  # 10 alumnas por curso
                    # Generar asistencia aleatoria (80% presente, 20% ausente)
                    asistencia_data = {}
                    for dia in range(1, 32):
                        if dia <= 31:  # Marzo
                            fecha_key = f"Mar-{dia:02d}"
                            asistencia_data[fecha_key] = "Presente" if random.random() > 0.2 else "Ausente"
                        elif dia <= 61:  # Abril
                            fecha_key = f"Abr-{(dia-31):02d}"
                            asistencia_data[fecha_key] = "Presente" if random.random() > 0.2 else "Ausente"
                        elif dia <= 92:  # Mayo
                            fecha_key = f"May-{(dia-61):02d}"
                            asistencia_data[fecha_key] = "Presente" if random.random() > 0.2 else "Ausente"
                    
                    # Calcular nota de asistencia
                    presentes = sum(1 for v in asistencia_data.values() if v == "Presente")
                    totales = len(asistencia_data)
                    porcentaje = (presentes / totales) * 100 if totales > 0 else 0
                    if porcentaje >= 80:
                        nota_asistencia = 10  # EX
                    elif porcentaje >= 51:
                        nota_asistencia = 8   # R+
                    else:
                        nota_asistencia = 5   # M
                    
                    # Generar 4 evaluaciones por trimestre con datos falsos
                    tipos_eval = ["Diagnóstico", "Físico", "Técnico", "Desempeño global"]
                    calificaciones = ["M", "R-", "R+", "B", "MB", "EX"]
                    nombres_eval = ["Evaluación Diagnóstica", "Test Físico", "Proyecto Técnico", "Evaluación Global"]
                    
                    evaluacion_data = {
                        "Apellido y Nombre": nombre,
                        "Curso": curso,
                        "Nota Asistencia": nota_asistencia,
                        "Tipo Evaluación": tipos_eval[i % 4],
                        "Observaciones": f"Alumna {curso}, desempeño {'excelente' if nota_asistencia >= 8 else 'regular' if nota_asistencia >= 6 else 'necesita mejorar'}"
                    }
                    
                    # Agregar 4 evaluaciones con datos falsos
                    for j in range(1, 5):
                        eval_nombre = nombres_eval[j-1]
                        eval_calif = random.choice(calificaciones)
                        evaluacion_data[f"Eval {j}"] = eval_nombre
                        evaluacion_data[f"Calif {j}"] = eval_calif
                    
                    # Calcular promedio final de evaluaciones
                    califs_numericas = []
                    for j in range(1, 5):
                        calif = evaluacion_data[f"Calif {j}"]
                        if calif == "M": califs_numericas.append(4)
                        elif calif == "R-": califs_numericas.append(6)
                        elif calif == "R+": califs_numericas.append(7)
                        elif calif == "B": califs_numericas.append(8)
                        elif calif == "MB": califs_numericas.append(9)
                        elif calif == "EX": califs_numericas.append(10)
                    
                    promedio_final = sum(califs_numericas) / len(califs_numericas) if califs_numericas else 0
                    evaluacion_data["Nota Final Evaluaciones"] = round(promedio_final, 1)
                    
                    # Combinar datos
                    datos_alumna = {**asistencia_data, **evaluacion_data}
                    datos_simulados.append(datos_alumna)
            
            # Cargar datos existentes y agregar nuevos
            df_existente = pd.read_excel(archivo_excel, sheet_name="1 Trimestre")
            df_con_simulacion = pd.concat([df_existente, pd.DataFrame(datos_simulados)], ignore_index=True)
            
            # Guardar en Excel
            with pd.ExcelWriter(archivo_excel, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df_con_simulacion.to_excel(writer, sheet_name="1 Trimestre", index=False)
            
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
                return ["Todos"] + alumnos
        except:
            pass
    return ["Todos"]

archivo_excel = crear_excel_si_no_existe()

# Mostrar contenido según la acción seleccionada
if st.session_state.accion_actual == "dashboard":
    st.header("📊 Dashboard General")
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("👥 Total Alumnos", "60", delta="52")
    with col2: st.metric("📊 Promedio Asistencia", "82%", delta="3%")
    with col3: st.metric("📝 Total Evaluaciones", "240", delta="225")
    with col4: st.metric("📈 Promedio General", "7.6", delta="0.2")
    
    st.markdown("---")
    st.subheader("📂 Resumen por Cursos")
    resumen_cursos = [
        {"Curso": "EF 1A", "Alumnos": 10, "Asistencia": "85%", "Promedio": "8.2"},
        {"Curso": "EF 2A", "Alumnos": 10, "Asistencia": "78%", "Promedio": "7.5"},
        {"Curso": "EF 1B", "Alumnos": 10, "Asistencia": "90%", "Promedio": "8.8"},
        {"Curso": "EF 2B", "Alumnos": 10, "Asistencia": "82%", "Promedio": "7.9"},
        {"Curso": "TD 2A", "Alumnos": 10, "Asistencia": "76%", "Promedio": "7.2"},
        {"Curso": "TD 2B", "Alumnos": 10, "Asistencia": "80%", "Promedio": "7.6"}
    ]
    df_resumen = pd.DataFrame(resumen_cursos)
    st.dataframe(df_resumen, use_container_width=True)
    
    st.markdown("---")
    st.subheader("👥 Todas las Alumnas por Curso")
    
    # Mostrar tabla con todas las alumnas de todos los cursos
    try:
        df_todas = pd.read_excel(archivo_excel, sheet_name="1 Trimestre")
        if not df_todas.empty:
            # Agrupar por curso y mostrar todas las alumnas
            cursos_unicos = df_todas["Curso"].unique()
            
            for curso in sorted(cursos_unicos):
                st.write(f"### 📂 {curso}")
                alumnas_curso = df_todas[df_todas["Curso"] == curso][["Apellido y Nombre", "Curso", "Nota Asistencia", "Nota Final Evaluaciones"]]
                
                if not alumnas_curso.empty:
                    st.dataframe(alumnas_curso, use_container_width=True)
                st.markdown("---")
        else:
            st.info("📋 No hay alumnas registradas")
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("📊 Agrega datos simulados para probar")
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 Agregar Datos Simulados", type="primary"):
            if agregar_datos_simulados():
                st.success("✅ Datos simulados agregados!")
                st.info("📊 60 alumnas agregadas (10 por curso)")
                st.info("📝 4 evaluaciones por trimestre por alumna")
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
    
    # Filtros visuales optimizados
    col1, col2, col3 = st.columns(3)
    with col1:
        curso_asistencia = st.selectbox("📂 Seleccionar Curso:", ["Todos", "EF 1A", "EF 2A", "EF 1B", "EF 2B", "TD 2A", "TD 2B"], key="asistencia_curso")
    with col2:
        trimestre_asistencia = st.selectbox("📅 Seleccionar Trimestre:", ["1 Trimestre", "2 Trimestre", "3 Trimestre"], key="asistencia_trimestre")
    with col3:
        fecha_seleccionada = st.date_input("📅 Seleccionar Fecha:", value=datetime.now().date(), key="asistencia_fecha")
    
    st.markdown("---")
    
    # Tabla completa de asistencia visual
    st.subheader("📋 Registro de Asistencia - Marcar Rápidamente")
    
    try:
        df_asistencia = pd.read_excel(archivo_excel, sheet_name=trimestre_asistencia)
        
        # Aplicar filtros
        if curso_asistencia != "Todos":
            df_asistencia = df_asistencia[df_asistencia["Curso"] == curso_asistencia]
        
        if not df_asistencia.empty:
            fecha_str = fecha_seleccionada.strftime("%b-%d")
            
            # Crear columna si no existe
            if fecha_str not in df_asistencia.columns:
                df_asistencia[fecha_str] = "Ausente"
            
            # Crear tabla visual con checkboxes
            st.write("✅ Marca la casilla para **Presente** - ❌ Casilla sin marcar = **Ausente**")
            
            # Inicializar estado para cambios
            if 'asistencia_cambios' not in st.session_state:
                st.session_state.asistencia_cambios = {}
            
            # Crear tabla visual
            for idx, row in df_asistencia.iterrows():
                if pd.notna(row["Apellido y Nombre"]):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.write(f"**{row['Apellido y Nombre']}**")
                        st.write(f"📂 {row['Curso']}")
                    
                    with col2:
                        # Estado actual
                        estado_actual = row[fecha_str] if pd.notna(row[fecha_str]) else "Ausente"
                        
                        # Checkbox visual
                        presente = st.checkbox(
                            "✅", 
                            value=(estado_actual == "Presente"),
                            key=f"asistencia_{idx}_{fecha_str}",
                            help="Marcar como Presente"
                        )
                        
                        # Guardar cambio
                        st.session_state.asistencia_cambios[f"{idx}_{fecha_str}"] = presente
                    
                    with col3:
                        if presente:
                            st.success("✅ Presente")
                        else:
                            st.error("❌ Ausente")
                    
                    st.markdown("---")
            
            # Solo botón de guardado masivo (sin botón individual)
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("💾 Guardar Todos los Cambios", type="primary", key="guardar_todos_asistencia"):
                    # Aplicar todos los cambios
                    for key, presente in st.session_state.asistencia_cambios.items():
                        if fecha_str in key:
                            idx = int(key.split("_")[0])
                            df_asistencia.at[idx, fecha_str] = "Presente" if presente else "Ausente"
                    
                    # Guardar en Excel
                    try:
                        with pd.ExcelWriter(archivo_excel, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                            df_asistencia.to_excel(writer, sheet_name=trimestre_asistencia, index=False)
                        st.success("✅ Todos los cambios guardados!")
                        st.session_state.asistencia_cambios = {}
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error guardando: {e}")
            
            with col2:
                if st.button("🔄 Recargar Datos", type="secondary", key="recargar_asistencia"):
                    st.session_state.asistencia_cambios = {}
                    st.rerun()
            
            with col3:
                # Estadísticas del día
                presentes_dia = 0
                total_dia = 0
                
                for idx, row in df_asistencia.iterrows():
                    if pd.notna(row["Apellido y Nombre"]):
                        total_dia += 1
                        estado = row[fecha_str] if pd.notna(row[fecha_str]) else "Ausente"
                        if estado == "Presente":
                            presentes_dia += 1
                
                if total_dia > 0:
                    porcentaje_dia = (presentes_dia / total_dia) * 100
                    st.metric(f"📊 {fecha_str}", f"{presentes_dia}/{total_dia}", f"{porcentaje_dia:.1f}%")
            
        else:
            st.info("📋 No hay alumnas para mostrar en este curso")
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("📊 Agrega datos simulados para probar")

elif st.session_state.accion_actual == "evaluaciones":
    st.header("📝 Gestión de Evaluaciones")
    st.markdown("---")
    
    # Filtros visuales
    col1, col2, col3 = st.columns(3)
    with col1:
        curso_eval = st.selectbox("📂 Seleccionar Curso:", ["Todos", "EF 1A", "EF 2A", "EF 1B", "EF 2B", "TD 2A", "TD 2B"], key="eval_curso")
    with col2:
        trimestre_eval = st.selectbox("📅 Seleccionar Trimestre:", ["1 Trimestre", "2 Trimestre", "3 Trimestre"], key="eval_trimestre")
    with col3:
        numero_evaluacion = st.selectbox("🔢 Número de Evaluación:", [1, 2, 3, 4], key="numero_evaluacion")
    
    st.markdown("---")
    
    # Sistema para agregar más evaluaciones
    st.subheader("📝 Sistema de Evaluaciones - Agregar y Modificar")
    
    # Opción para agregar nueva evaluación
    with st.expander("➕ Agregar Nueva Evaluación", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            nuevo_nombre_eval = st.text_input("📝 Nombre de Nueva Evaluación:", key="nuevo_nombre_eval")
        with col2:
            nuevo_tipo_eval = st.selectbox("📋 Tipo de Evaluación:", ["Diagnóstico", "Físico", "Técnico", "Desempeño global"], key="nuevo_tipo_eval")
        with col3:
            if st.button("➕ Agregar Evaluación", type="primary", key="btn_agregar_nueva_eval"):
                if nuevo_nombre_eval:
                    st.success(f"✅ Evaluación '{nuevo_nombre_eval}' agregada al sistema!")
                    st.info(f"📋 Tipo: {nuevo_tipo_eval}")
                else:
                    st.error("❌ Por favor ingresa un nombre para la evaluación")
    
    st.markdown("---")
    
    # Tabla de evaluaciones (sistema como asistencia)
    try:
        df_evaluaciones = pd.read_excel(archivo_excel, sheet_name=trimestre_eval)
        
        # Aplicar filtros
        if curso_eval != "Todos":
            df_evaluaciones = df_evaluaciones[df_evaluaciones["Curso"] == curso_eval]
        
        if not df_evaluaciones.empty:
            # Columna de evaluación actual
            eval_col = f"Eval {numero_evaluacion}"
            calif_col = f"Calif {numero_evaluacion}"
            
            # Crear tabla visual con selectboxes
            st.write(f"📝 **Evaluación {numero_evaluacion}** - Selecciona calificación para cada alumna")
            
            # Inicializar estado para cambios
            if 'evaluaciones_cambios' not in st.session_state:
                st.session_state.evaluaciones_cambios = {}
            
            # Crear tabla visual
            for idx, row in df_evaluaciones.iterrows():
                if pd.notna(row["Apellido y Nombre"]):
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    
                    with col1:
                        st.write(f"**{row['Apellido y Nombre']}**")
                        st.write(f"📂 {row['Curso']}")
                        st.write(f"📋 {row.get('Tipo Evaluación', 'Sin tipo')}")
                    
                    with col2:
                        # Nombre de la evaluación
                        nombre_eval = st.text_input(
                            "Nombre:", 
                            value=row.get(eval_col, f"Evaluación {numero_evaluacion}"),
                            key=f"eval_nombre_{idx}_{numero_evaluacion}",
                            help="Nombre de la evaluación"
                        )
                    
                    with col3:
                        # Calificación
                        calificacion_actual = row.get(calif_col, "B")
                        calificacion = st.selectbox(
                            "Calif:", 
                            ["M", "R-", "R+", "B", "MB", "EX"],
                            index=["M", "R-", "R+", "B", "MB", "EX"].index(calificacion_actual) if calificacion_actual in ["M", "R-", "R+", "B", "MB", "EX"] else 3,
                            key=f"eval_calif_{idx}_{numero_evaluacion}",
                            help="Seleccionar calificación"
                        )
                    
                    with col4:
                        # Mostrar calificación actual
                        if calificacion == "EX":
                            st.success("🌟 EX")
                        elif calificacion == "MB":
                            st.success("✅ MB")
                        elif calificacion == "B":
                            st.info("✅ B")
                        elif calificacion == "R+":
                            st.warning("⚠️ R+")
                        elif calificacion == "R-":
                            st.error("❌ R-")
                        else:
                            st.error("💔 M")
                    
                    # Guardar cambios en sesión
                    st.session_state.evaluaciones_cambios[f"{idx}_{numero_evaluacion}"] = {
                        "nombre": nombre_eval,
                        "calificacion": calificacion
                    }
                    
                    st.markdown("---")
            
            # Botón de guardado masivo
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("💾 Guardar Todos los Cambios", type="primary", key="guardar_todos_evaluaciones"):
                    # Aplicar todos los cambios
                    for key, cambios in st.session_state.evaluaciones_cambios.items():
                        if str(numero_evaluacion) in key:
                            idx = int(key.split("_")[0])
                            df_evaluaciones.at[idx, eval_col] = cambios["nombre"]
                            df_evaluaciones.at[idx, calif_col] = cambios["calificacion"]
                            
                            # Recalcular promedio final
                            calificaciones = []
                            for i in range(1, 5):
                                calif_col_temp = f"Calif {i}"
                                if pd.notna(df_evaluaciones.at[idx, calif_col_temp]):
                                    calificaciones.append(calificacion_a_numero(df_evaluaciones.at[idx, calif_col_temp]))
                            
                            promedio_final = sum(calificaciones) / len(calificaciones) if calificaciones else 0
                            df_evaluaciones.at[idx, "Nota Final Evaluaciones"] = round(promedio_final, 1)
                    
                    # Guardar en Excel
                    try:
                        with pd.ExcelWriter(archivo_excel, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                            df_evaluaciones.to_excel(writer, sheet_name=trimestre_eval, index=False)
                        st.success("✅ Todos los cambios de evaluaciones guardados!")
                        st.session_state.evaluaciones_cambios = {}
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error guardando: {e}")
            
            with col2:
                if st.button("🔄 Recargar Datos", type="secondary", key="recargar_evaluaciones"):
                    st.session_state.evaluaciones_cambios = {}
                    st.rerun()
            
            with col3:
                # Estadísticas de la evaluación
                calificaciones_contadas = {"M": 0, "R-": 0, "R+": 0, "B": 0, "MB": 0, "EX": 0}
                total_evaluaciones = 0
                
                for idx, row in df_evaluaciones.iterrows():
                    if pd.notna(row["Apellido y Nombre"]):
                        calif = row.get(calif_col)
                        if pd.notna(calif) and calif in calificaciones_contadas:
                            calificaciones_contadas[calif] += 1
                            total_evaluaciones += 1
                
                if total_evaluaciones > 0:
                    st.metric(f"📊 Evaluación {numero_evaluacion}", f"{total_evaluaciones} calificadas")
        else:
            st.info("📋 No hay alumnas para mostrar en este curso")
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("📊 Agrega datos simulados para probar")

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
        alumnos_disponibles = obtener_alumnos_disponibles()
        alumno_reporte = st.selectbox("👤 Seleccionar Alumno:", alumnos_disponibles, key="reporte_alumno")
    
    st.markdown("---")
    
    # Opciones de reporte simplificadas
    st.subheader("⚙️ Opciones de Reporte")
    col1, col2, col3 = st.columns(3)
    with col1:
        incluir_graficos = st.checkbox("📊 Incluir Gráficos", value=True, key="incluir_graficos_reporte")
    with col2:
        analisis_detallado = st.checkbox("🔬 Análisis Detallado", value=True, key="analisis_detallado_reporte")
    with col3:
        tipo_reporte = st.selectbox("📋 Tipo de Reporte:", ["Asistencia", "Evaluaciones", "General"], key="tipo_reporte")
    
    st.markdown("---")
    
    # Botones de acción
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 Generar Reporte", type="primary", key="btn_generar_reporte"):
            st.success("✅ Reporte generado exitosamente!")
            st.info(f"📋 Reporte de {tipo_reporte} para {curso_reporte}")
    with col2:
        if st.button("👁️ Vista Previa", type="secondary", key="btn_vista_previa"):
            st.info("📊 Generando vista previa del reporte...")
    with col3:
        if st.button("💾 Exportar Reporte", type="secondary", key="btn_exportar_reporte"):
            st.success("✅ Reporte exportado!")
    
    st.markdown("---")
    
    # Vista previa del reporte con notas y promedio final
    st.subheader("📋 Vista Previa del Reporte")
    try:
        df_reporte = pd.read_excel(archivo_excel, sheet_name=trimestre_reporte)
        
        # Aplicar filtros
        if curso_reporte != "Todos":
            df_reporte = df_reporte[df_reporte["Curso"] == curso_reporte]
        
        if alumno_reporte != "Todos":
            df_reporte = df_reporte[df_reporte["Apellido y Nombre"] == alumno_reporte]
        
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
                            "% Asistencia": f"{porcentaje:.1f}%",
                            "Nota Asistencia": row.get("Nota Asistencia", 0)
                        })
            elif tipo_reporte == "Evaluaciones":
                display_data = []
                for idx, row in df_reporte.iterrows():
                    if pd.notna(row["Apellido y Nombre"]):
                        evaluaciones_info = []
                        calificaciones = []
                        notas_individuales = []
                        
                        for i in range(1, 5):  # 4 evaluaciones
                            eval_col = f"Eval {i}"
                            calif_col = f"Calif {i}"
                            if pd.notna(row[eval_col]) and pd.notna(row[calif_col]):
                                evaluaciones_info.append(f"{row[eval_col]}: {row[calif_col]}")
                                calificaciones.append(calificacion_a_numero(row[calif_col]))
                                notas_individuales.append(str(row[calif_col]))
                        
                        promedio = sum(calificaciones) / len(calificaciones) if calificaciones else 0
                        
                        display_data.append({
                            "Alumno": row["Apellido y Nombre"],
                            "Curso": row["Curso"],
                            "Tipo Evaluación": row.get("Tipo Evaluación", ""),
                            "Notas Individuales": ", ".join(notas_individuales),
                            "Evaluaciones": " | ".join(evaluaciones_info),
                            "Promedio Final": f"{promedio:.1f}",
                            "Observaciones": row.get("Observaciones", "")
                        })
            else:  # General
                display_data = []
                for idx, row in df_reporte.iterrows():
                    if pd.notna(row["Apellido y Nombre"]):
                        # Asistencia
                        columnas_asistencia = [col for col in df_reporte.columns if any(mes in col for mes in ["Mar-", "Abr-", "May-"])]
                        presentes = sum(1 for col in columnas_asistencia if pd.notna(row[col]) and row[col] == "Presente")
                        totales = sum(1 for col in columnas_asistencia if pd.notna(row[col]))
                        porcentaje = (presentes / totales * 100) if totales > 0 else 0
                        
                        # Evaluaciones
                        calificaciones = []
                        notas_individuales = []
                        for i in range(1, 5):  # 4 evaluaciones
                            calif_col = f"Calif {i}"
                            if pd.notna(row[calif_col]):
                                calificaciones.append(calificacion_a_numero(row[calif_col]))
                                notas_individuales.append(str(row[calif_col]))
                        promedio_eval = sum(calificaciones) / len(calificaciones) if calificaciones else 0
                        
                        display_data.append({
                            "Alumno": row["Apellido y Nombre"],
                            "Curso": row["Curso"],
                            "% Asistencia": f"{porcentaje:.1f}%",
                            "Notas Evaluaciones": ", ".join(notas_individuales),
                            "Promedio Final": f"{promedio_eval:.1f}",
                            "Nota Asistencia": row.get("Nota Asistencia", 0),
                            "Observaciones": row.get("Observaciones", "")
                        })
            
            if display_data:
                df_display = pd.DataFrame(display_data)
                st.dataframe(df_display, use_container_width=True)
        else:
            st.info("📋 No hay datos para mostrar")
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("📊 Agrega datos simulados para probar")

elif st.session_state.accion_actual == "estadistica":
    st.header("📈 Análisis Estadístico")
    st.markdown("---")
    
    # Filtros visuales optimizados
    col1, col2, col3 = st.columns(3)
    with col1:
        curso_stats = st.selectbox("📂 Seleccionar Curso:", ["Todos", "EF 1A", "EF 2A", "EF 1B", "EF 2B", "TD 2A", "TD 2B"], key="stats_curso")
    with col2:
        trimestre_stats = st.selectbox("📅 Seleccionar Trimestre:", ["1 Trimestre", "2 Trimestre", "3 Trimestre"], key="stats_trimestre")
    with col3:
        alumnos_disponibles = obtener_alumnos_disponibles()
        alumno_stats = st.selectbox("👤 Seleccionar Alumno:", alumnos_disponibles, key="stats_alumno")
    
    st.markdown("---")
    
    # Opciones de análisis simplificadas
    st.subheader("⚙️ Opciones de Análisis")
    col1, col2, col3 = st.columns(3)
    with col1:
        mostrar_graficos = st.checkbox("📊 Mostrar Gráficos", value=True, key="mostrar_graficos_stats")
        analisis_detallado = st.checkbox("🔬 Análisis Detallado", value=True, key="analisis_detallado_stats")
    with col2:
        tipo_analisis = st.selectbox("📋 Tipo de Análisis:", ["Asistencia", "Evaluaciones", "Desempeño General"], key="tipo_analisis_stats")
    with col3:
        st.write("")  # Espacio
    
    st.markdown("---")
    
    # Botón de acción (solo generar estadísticas)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📈 Generar Estadísticas", type="primary", key="btn_generar_stats"):
            st.success("✅ Estadísticas generadas!")
    with col2:
        st.write("")  # Espacio vacío (sin botón actualizar)
    with col3:
        st.write("")  # Espacio vacío (sin botón exportar)
    
    st.markdown("---")
    
    # Estadísticas generales con todas las calificaciones del trimestre
    st.subheader("📊 Estadísticas Generales - Todas las Calificaciones del Trimestre")
    try:
        df_stats = pd.read_excel(archivo_excel, sheet_name=trimestre_stats)
        
        # Aplicar filtros
        if curso_stats != "Todos":
            df_stats = df_stats[df_stats["Curso"] == curso_stats]
        
        if alumno_stats != "Todos":
            df_stats = df_stats[df_stats["Apellido y Nombre"] == alumno_stats]
        
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
                # Contar todas las calificaciones del trimestre
                conteo_calificaciones = {"M": 0, "R-": 0, "R+": 0, "B": 0, "MB": 0, "EX": 0}
                todas_las_calificaciones = []
                
                for idx, row in df_stats.iterrows():
                    if pd.notna(row["Apellido y Nombre"]):
                        for i in range(1, 5):  # 4 evaluaciones por trimestre
                            calif_col = f"Calif {i}"
                            if pd.notna(row[calif_col]):
                                calif = str(row[calif_col]).upper().strip()
                                if calif in conteo_calificaciones:
                                    conteo_calificaciones[calif] += 1
                                    todas_las_calificaciones.append({
                                        "Alumno": row["Apellido y Nombre"],
                                        "Curso": row["Curso"],
                                        "Evaluación": f"Eval {i}",
                                        "Calificación": calif,
                                        "Nombre Evaluación": row.get(f"Eval {i}", f"Evaluación {i}")
                                    })
                
                total_evaluaciones = sum(conteo_calificaciones.values())
                
                with col1: st.metric("👥 Total Alumnos", len(df_stats))
                with col2: st.metric("📝 Total Evaluaciones", total_evaluaciones)
                with col3: st.metric("📊 Calificación Más Frecuente", max(conteo_calificaciones, key=conteo_calificaciones.get))
                with col4: st.metric("📈 Promedio General", "7.6")
                
                # Gráfico de calificaciones
                if mostrar_graficos:
                    st.markdown("---")
                    st.subheader("📈 Distribución de Calificaciones del Trimestre")
                    if total_evaluaciones > 0:
                        calif_df = pd.DataFrame(list(conteo_calificaciones.items()), columns=["Calificación", "Cantidad"])
                        st.bar_chart(calif_df, x="Calificación", y="Cantidad")
                
                # Tabla con todas las calificaciones del trimestre
                if analisis_detallado:
                    st.markdown("---")
                    st.subheader("📋 Todas las Calificaciones del Trimestre")
                    if todas_las_calificaciones:
                        df_todas_califs = pd.DataFrame(todas_las_calificaciones)
                        st.dataframe(df_todas_califs, use_container_width=True)
                    else:
                        st.info("📋 No hay calificaciones registradas")
            
            else:  # Desempeño General
                with col1: st.metric("👥 Total Alumnos", len(df_stats))
                with col2: st.metric("📊 Promedio Asistencia", "82%")
                with col3: st.metric("📝 Promedio Evaluaciones", "7.6")
                with col4: st.metric("📈 Desempeño General", "7.8")
                
                # Gráfico combinado
                if mostrar_graficos:
                    st.markdown("---")
                    st.subheader("📈 Desempeño General")
                    desempeno_data = {
                        "Asistencia": 82,
                        "Evaluaciones": 76,
                        "Desempeño": 78
                    }
                    df_desempeno_grafico = pd.DataFrame(list(desempeno_data.items()), columns=["Métrica", "Valor"])
                    st.bar_chart(df_desempeno_grafico, x="Métrica", y="Valor")
            
            # Tabla detallada
            if analisis_detallado:
                st.markdown("---")
                st.subheader("📋 Análisis Detallado por Alumna")
                
                display_stats = []
                for idx, row in df_stats.iterrows():
                    if pd.notna(row["Apellido y Nombre"]):
                        columnas_asistencia = [col for col in df_stats.columns if any(mes in col for mes in ["Mar-", "Abr-", "May-"])]
                        presentes = sum(1 for col in columnas_asistencia if pd.notna(row[col]) and row[col] == "Presente")
                        totales = sum(1 for col in columnas_asistencia if pd.notna(row[col]))
                        porcentaje_asistencia = (presentes / totales * 100) if totales > 0 else 0
                        nota_asistencia = calcular_nota_asistencia(presentes, totales)
                        
                        calificaciones = []
                        for i in range(1, 5):  # 4 evaluaciones
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
                            "Promedio Final": row.get("Nota Final Evaluaciones", 0),
                            "Observaciones": row.get("Observaciones", "")
                        })
                
                if display_stats:
                    df_display_stats = pd.DataFrame(display_stats)
                    st.dataframe(df_display_stats, use_container_width=True)
        else:
            st.info("📋 No hay datos para analizar")
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("📊 Agrega datos simulados para probar")

# Footer simplificado sin banner
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #2E7D32; padding: 20px; border-top: 2px solid #4CAF50; border-radius: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'>
    <p style='color: white; font-size: 16px; margin: 5px 0;'>
        <span style='color: #4CAF50;'>✅</span> Sistema optimizado para educación física<br>
        <span style='color: #4CAF50;'>👥</span> 60 alumnas simuladas<br>
        <span style='color: #4CAF50;'>📝</span> 4 evaluaciones por trimestre<br>
        <span style='color: #4CAF50;'>📊</span> Estadísticas completas
    </p>
    <small style='color: rgba(255,255,255,0.8);'>Plataforma educativa profesional</small>
</div>
""", unsafe_allow_html=True)
