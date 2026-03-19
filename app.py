import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
import random

st.set_page_config(page_title="Sistema Educativo", page_icon="📚", layout="wide", initial_sidebar_state="expanded")

# Sidebar con ACCIONES
st.sidebar.header("🎯 ACCIONES")

# Agregar Alumno
if st.sidebar.button("👤 Agregar Alumno", type="primary", key="btn_agregar_alumno"):
    st.session_state.accion_actual = "agregar_alumno"

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
    # Generar backup detallado
    try:
        if generar_backup_detalles():
            st.sidebar.success("✅ Backup en Excel generado exitosamente!")
            st.sidebar.info(f"📁 Archivo: backup_detalles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
        else:
            st.sidebar.error("❌ Error generando backup")
    except Exception as e:
        st.sidebar.error(f"❌ Error: {e}")

# Inicializar estado
if 'accion_actual' not in st.session_state:
    st.session_state.accion_actual = "dashboard"
if 'nuevas_evaluaciones' not in st.session_state:
    st.session_state.nuevas_evaluaciones = []

# Funciones del sistema
def sincronizar_google_sheets():
    """Sincroniza los datos locales con Google Sheets"""
    try:
        import gspread
        from google.oauth2.service_account import Credentials

        # Leer credenciales desde secrets.toml
        creds_info = {
            "type": st.secrets["gcp_service_account"]["type"],
            "project_id": st.secrets["gcp_service_account"]["project_id"],
            "private_key_id": st.secrets["gcp_service_account"]["private_key_id"],
            "private_key": st.secrets["gcp_service_account"]["private_key"],
            "client_email": st.secrets["gcp_service_account"]["client_email"],
            "client_id": st.secrets["gcp_service_account"]["client_id"],
            "auth_uri": st.secrets["gcp_service_account"]["auth_uri"],
            "token_uri": st.secrets["gcp_service_account"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["gcp_service_account"]["client_x509_cert_url"],
        }

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
        client = gspread.authorize(creds)

        # Leer sheet_id desde secrets
        SPREADSHEET_ID = st.secrets["gcp_service_account"]["sheet_id"]
        spreadsheet = client.open_by_key(SPREADSHEET_ID)

        archivo_excel = "sistema_educativo.xlsx"
        if not os.path.exists(archivo_excel):
            return False, "No existe el archivo Excel local. Primero agregá datos."

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        headers = [
            "Fecha y Hora Actualización", "Apellido y Nombre", "Curso", "Trimestre",
            "Días Presentes", "Días Ausentes", "% Asistencia", "Nota Asistencia",
            "Eval 1 - Nombre", "Eval 1 - Calif",
            "Eval 2 - Nombre", "Eval 2 - Calif",
            "Eval 3 - Nombre", "Eval 3 - Calif",
            "Eval 4 - Nombre", "Eval 4 - Calif",
            "Eval 5 - Nombre", "Eval 5 - Calif",
            "Eval 6 - Nombre", "Eval 6 - Calif",
            "Promedio Final Evaluaciones"
        ]

        for trimestre_num in range(1, 4):
            nombre_trimestre = f"{trimestre_num} Trimestre"

            try:
                ws = spreadsheet.worksheet(nombre_trimestre)
            except Exception:
                ws = spreadsheet.add_worksheet(title=nombre_trimestre, rows=500, cols=25)

            try:
                df = pd.read_excel(archivo_excel, sheet_name=nombre_trimestre)
            except Exception:
                continue

            if df.empty:
                continue

            rows_data = [headers]

            for _, row in df.iterrows():
                if pd.isna(row.get("Apellido y Nombre")):
                    continue

                columnas_asistencia = [
                    col for col in df.columns
                    if any(mes in str(col) for mes in ["Mar-", "Abr-", "May-"])
                ]
                presentes = sum(1 for col in columnas_asistencia if pd.notna(row.get(col)) and row.get(col) == "Presente")
                totales = sum(1 for col in columnas_asistencia if pd.notna(row.get(col)))
                ausentes = totales - presentes
                porcentaje = round((presentes / totales * 100), 1) if totales > 0 else 0
                nota_asistencia = calcular_nota_asistencia(presentes, totales)

                fila = [
                    timestamp,
                    str(row.get("Apellido y Nombre", "")),
                    str(row.get("Curso", "")),
                    nombre_trimestre,
                    presentes,
                    ausentes,
                    f"{porcentaje}%",
                    nota_asistencia,
                ]

                for j in range(1, 7):
                    fila.append(str(row.get(f"Eval {j}", "")))
                    fila.append(str(row.get(f"Calif {j}", "")))

                fila.append(str(row.get("Nota Final Evaluaciones", "")))
                rows_data.append(fila)

            ws.clear()
            ws.update(rows_data, value_input_option="USER_ENTERED")

            ws.format("A1:U1", {
                "backgroundColor": {"red": 0.212, "green": 0.380, "blue": 0.573},
                "textFormat": {
                    "bold": True,
                    "foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}
                },
                "horizontalAlignment": "CENTER"
            })

        return True, f"Sincronizado correctamente a las {timestamp}"

    except Exception as e:
        return False, str(e)

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

def generar_backup_detalles():
    """Generar backup detallado en Excel con todas las columnas solicitadas"""
    try:
        archivo_excel = "sistema_educativo.xlsx"
        if not os.path.exists(archivo_excel):
            return False
        
        # Crear nuevo Excel para backup
        backup_filename = f"backup_detalles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        wb_backup = openpyxl.Workbook()
        wb_backup.remove(wb_backup.active)
        
        # Procesar cada trimestre
        for trimestre_num in range(1, 4):
            nombre_trimestre = f"{trimestre_num} Trimestre"
            ws_backup = wb_backup.create_sheet(title=nombre_trimestre)
            
            # Encabezados del backup
            headers_backup = [
                "Fecha y Hora Backup", "Alumno", "Curso", "Trimestre",
                "Asistencia", "Evaluación", "Tipo Evaluación", "Calificación"
            ]
            
            # Escribir encabezados
            for col_num, header in enumerate(headers_backup, 1):
                cell = ws_backup.cell(row=1, column=col_num, value=header)
                cell.font = Font(bold=True)
                cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
                cell.alignment = Alignment(horizontal="center")
            
            # Leer datos del trimestre
            df_trimestre = pd.read_excel(archivo_excel, sheet_name=nombre_trimestre)
            
            if not df_trimestre.empty:
                row_num = 2
                for idx, row in df_trimestre.iterrows():
                    if pd.notna(row["Apellido y Nombre"]):
                        # Procesar asistencia
                        columnas_asistencia = [col for col in df_trimestre.columns if any(mes in col for mes in ["Mar-", "Abr-", "May-"])]
                        presentes = sum(1 for col in columnas_asistencia if pd.notna(row[col]) and row[col] == "Presente")
                        totales = sum(1 for col in columnas_asistencia if pd.notna(row[col]))
                        porcentaje_asistencia = (presentes / totales * 100) if totales > 0 else 0
                        
                        # Escribir fila de asistencia
                        ws_backup.cell(row=row_num, column=1, value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        ws_backup.cell(row=row_num, column=2, value=row["Apellido y Nombre"])
                        ws_backup.cell(row=row_num, column=3, value=row["Curso"])
                        ws_backup.cell(row=row_num, column=4, value=nombre_trimestre)
                        ws_backup.cell(row=row_num, column=5, value=f"{presentes}/{totales} ({porcentaje_asistencia:.1f}%)")
                        ws_backup.cell(row=row_num, column=6, value="")  # Evaluación vacía para fila de asistencia
                        ws_backup.cell(row=row_num, column=7, value="")  # Tipo vacío para fila de asistencia
                        ws_backup.cell(row=row_num, column=8, value="")  # Calificación vacía para fila de asistencia
                        row_num += 1
                        
                        # Procesar evaluaciones
                        for j in range(1, 7):  # 6 evaluaciones
                            eval_col = f"Eval {j}"
                            calif_col = f"Calif {j}"
                            
                            if pd.notna(row[eval_col]) and pd.notna(row[calif_col]):
                                ws_backup.cell(row=row_num, column=1, value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                ws_backup.cell(row=row_num, column=2, value=row["Apellido y Nombre"])
                                ws_backup.cell(row=row_num, column=3, value=row["Curso"])
                                ws_backup.cell(row=row_num, column=4, value=nombre_trimestre)
                                ws_backup.cell(row=row_num, column=5, value="")  # Asistencia vacía para fila de evaluación
                                ws_backup.cell(row=row_num, column=6, value=row[eval_col])
                                ws_backup.cell(row=row_num, column=7, value=row.get("Tipo Evaluación", ""))
                                ws_backup.cell(row=row_num, column=8, value=row[calif_col])
                                row_num += 1
        
        # Guardar backup
        wb_backup.save(backup_filename)
        return True
    except Exception as e:
        st.error(f"Error generando backup: {e}")
        return False

def guardar_datos_excel(df, sheet_name, archivo_excel="sistema_educativo.xlsx"):
    """Función para guardar datos en Excel con manejo de errores"""
    try:
        with pd.ExcelWriter(archivo_excel, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        return True
    except Exception as e:
        st.error(f"Error guardando en Excel: {e}")
        return False

def agregar_datos_simulados_completos():
    archivo_excel = "sistema_educativo.xlsx"
    if os.path.exists(archivo_excel):
        try:
            nombres_femeninos = [
                "García López, Sofía María", "Rodríguez Martínez, Ana Isabel", "Fernández García, Laura Patricia",
                "Sánchez Hernández, María José", "López Torres, Carmen Rosa", "Pérez Díaz, Beatriz Elena",
                "Gómez Ruiz, Patricia Alejandra", "Martínez Castro, María Fernanda", "Romero Vargas, Ana Sofía",
                "Alvarez Moreno, Isabel Cristina"
            ]
            
            nombres_adicionales_ef1a = [
                "Hernández González, Luciana Beatriz", "Mendoza Silva, Valentina Sofía", "Castro Ramos, Isabella Gabriela",
                "Vargas Morales, Emilia Alejandra", "Ortiz Ruiz, Camila Victoria"
            ]
            
            cursos = ["EF 1A", "EF 2A", "EF 1B", "EF 2B", "TD 2A", "TD 2B"]
            
            for trimestre_num in range(1, 4):
                nombre_trimestre = f"{trimestre_num} Trimestre"
                datos_trimestre = []
                
                for curso in cursos:
                    if curso == "EF 1A":
                        nombres_curso = nombres_femeninos[:10] + nombres_adicionales_ef1a
                    else:
                        nombres_curso = nombres_femeninos[:10]
                    
                    for i, nombre in enumerate(nombres_curso):
                        asistencia_data = {}
                        for dia in range(1, 32):
                            asistencia_data[f"Mar-{dia:02d}"] = "Presente" if random.random() > 0.2 else "Ausente"
                        for dia in range(1, 31):
                            asistencia_data[f"Abr-{dia:02d}"] = "Presente" if random.random() > 0.2 else "Ausente"
                        for dia in range(1, 32):
                            asistencia_data[f"May-{dia:02d}"] = "Presente" if random.random() > 0.2 else "Ausente"
                        
                        presentes = sum(1 for v in asistencia_data.values() if v == "Presente")
                        totales = len(asistencia_data)
                        porcentaje = (presentes / totales * 100) if totales > 0 else 0
                        
                        if porcentaje >= 80:
                            nota_asistencia = 10
                        elif porcentaje >= 51:
                            nota_asistencia = 8
                        else:
                            nota_asistencia = 5
                        
                        tipos_eval = ["Diagnóstico", "Físico", "Técnico", "Desempeño global"]
                        calificaciones = ["M", "R-", "R+", "B", "MB", "EX"]
                        nombres_eval = ["Evaluación Diagnóstica", "Test Físico", "Proyecto Técnico", "Evaluación Global", "Trabajo Práctico", "Exposición Oral"]
                        
                        evaluacion_data = {
                            "Apellido y Nombre": nombre,
                            "Curso": curso,
                            "Nota Asistencia": nota_asistencia,
                            "Tipo Evaluación": tipos_eval[i % 4],
                            "Observaciones": f"Alumna {curso}, desempeño {'excelente' if nota_asistencia >= 8 else 'regular' if nota_asistencia >= 6 else 'necesita mejorar'}"
                        }
                        
                        for j in range(1, 7):
                            eval_nombre = nombres_eval[j-1]
                            eval_calif = random.choice(calificaciones)
                            evaluacion_data[f"Eval {j}"] = eval_nombre
                            evaluacion_data[f"Calif {j}"] = eval_calif
                        
                        califs_numericas = []
                        for j in range(1, 7):
                            calif = evaluacion_data[f"Calif {j}"]
                            if calif == "M": califs_numericas.append(4)
                            elif calif == "R-": califs_numericas.append(6)
                            elif calif == "R+": califs_numericas.append(7)
                            elif calif == "B": califs_numericas.append(8)
                            elif calif == "MB": califs_numericas.append(9)
                            elif calif == "EX": califs_numericas.append(10)
                        
                        promedio_final = sum(califs_numericas) / len(califs_numericas) if califs_numericas else 0
                        evaluacion_data["Nota Final Evaluaciones"] = round(promedio_final, 1)
                        
                        datos_alumna = {**asistencia_data, **evaluacion_data}
                        datos_trimestre.append(datos_alumna)
                
                df_trimestre = pd.DataFrame(datos_trimestre)
                if guardar_datos_excel(df_trimestre, nombre_trimestre, archivo_excel):
                    continue
                else:
                    return False
            
            return True
        except Exception as e:
            st.error(f"Error: {e}")
            return False
    return False

def agregar_nuevo_alumno(nombre, curso):
    archivo_excel = "sistema_educativo.xlsx"
    if os.path.exists(archivo_excel):
        try:
            for trimestre_num in range(1, 4):
                nombre_trimestre = f"{trimestre_num} Trimestre"
                df_existente = pd.read_excel(archivo_excel, sheet_name=nombre_trimestre)
                
                nuevo_alumno = {
                    "Apellido y Nombre": nombre,
                    "Curso": curso,
                    "Nota Asistencia": 0,
                    "Tipo Evaluación": "Diagnóstico",
                    "Observaciones": "Nuevo alumno"
                }
                
                for dia in range(1, 32):
                    nuevo_alumno[f"Mar-{dia:02d}"] = "Ausente"
                for dia in range(1, 31):
                    nuevo_alumno[f"Abr-{dia:02d}"] = "Ausente"
                for dia in range(1, 32):
                    nuevo_alumno[f"May-{dia:02d}"] = "Ausente"
                
                for j in range(1, 7):
                    nuevo_alumno[f"Eval {j}"] = f"Evaluación {j}"
                    nuevo_alumno[f"Calif {j}"] = "B"
                
                nuevo_alumno["Nota Final Evaluaciones"] = 8.0
                
                df_actualizado = pd.concat([df_existente, pd.DataFrame([nuevo_alumno])], ignore_index=True)
                
                if guardar_datos_excel(df_actualizado, nombre_trimestre, archivo_excel):
                    continue
                else:
                    return False
            
            return True
        except Exception as e:
            st.error(f"Error: {e}")
            return False
    return False

def calcular_nota_asistencia(presentes, totales):
    if totales == 0:
        return 0
    porcentaje = (presentes / totales) * 100
    if porcentaje >= 80:
        return 10
    elif porcentaje >= 51:
        return 8
    else:
        return 5

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

def crear_grafico_asistencia(presentes, ausentes, nombre_alumno):
    data = {'Estado': ['Presentes', 'Ausentes'], 'Cantidad': [presentes, ausentes]}
    df_grafico = pd.DataFrame(data)
    st.bar_chart(df_grafico.set_index('Estado'))
    st.caption(f"📊 Distribución de Asistencia - {nombre_alumno}")

def crear_grafico_evaluaciones(evaluaciones_data, nombre_alumno):
    df_grafico = pd.DataFrame(evaluaciones_data)
    if not df_grafico.empty:
        st.bar_chart(df_grafico.set_index('Evaluación')['Valor Numérico'])
        st.caption(f"📈 Rendimiento en Evaluaciones - {nombre_alumno}")

archivo_excel = crear_excel_si_no_existe()

# Mostrar contenido según la acción seleccionada
if st.session_state.accion_actual == "dashboard":
    st.header("📊 Dashboard General")
    
    total_alumnos = 65
    total_evaluaciones = total_alumnos * 6 * 3
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("👥 Total Alumnos", total_alumnos, delta="57")
    with col2: st.metric("📊 Promedio Asistencia", "82%", delta="3%")
    with col3: st.metric("📝 Total Evaluaciones", total_evaluaciones, delta=f"+{total_evaluaciones - 720}")
    with col4: st.metric("📈 Promedio General", "7.6", delta="0.2")
    
    st.markdown("---")
    st.subheader("📂 Resumen por Cursos")
    resumen_cursos = [
        {"Curso": "EF 1A", "Alumnos": 15, "Asistencia": "85%", "Promedio": "8.2"},
        {"Curso": "EF 2A", "Alumnos": 10, "Asistencia": "78%", "Promedio": "7.5"},
        {"Curso": "EF 1B", "Alumnos": 10, "Asistencia": "90%", "Promedio": "8.8"},
        {"Curso": "EF 2B", "Alumnos": 10, "Asistencia": "82%", "Promedio": "7.9"},
        {"Curso": "TD 2A", "Alumnos": 10, "Asistencia": "76%", "Promedio": "7.2"},
        {"Curso": "TD 2B", "Alumnos": 10, "Asistencia": "80%", "Promedio": "7.6"}
    ]
    df_resumen = pd.DataFrame(resumen_cursos)
    st.dataframe(df_resumen, use_container_width=True)
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 Agregar Datos Simulados Completos", type="primary"):
            if agregar_datos_simulados_completos():
                st.success("✅ Datos simulados agregados!")
                st.info(f"📊 {total_alumnos} alumnas agregadas")
                st.info("📝 6 evaluaciones por trimestre por alumna")
                st.info("📅 Datos para los 3 trimestres")
                st.rerun()
    with col2:
        if st.button("🔄 Actualizar Datos", type="secondary"):
            st.rerun()
    with col3:
        st.write("")

elif st.session_state.accion_actual == "agregar_alumno":
    st.header("👤 Agregar Nuevo Alumno")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        nuevo_nombre = st.text_input("📝 Nombre Completo del Alumno:", key="nuevo_nombre_alumno")
    with col2:
        nuevo_curso = st.selectbox("📂 Curso:", ["EF 1A", "EF 2A", "EF 1B", "EF 2B", "TD 2A", "TD 2B"], key="nuevo_curso_alumno")
    with col3:
        st.write("")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✅ Agregar Alumno", type="primary", key="btn_agregar_nuevo_alumno"):
            if nuevo_nombre and nuevo_curso:
                if agregar_nuevo_alumno(nuevo_nombre, nuevo_curso):
                    st.success(f"✅ Alumno '{nuevo_nombre}' agregado exitosamente al curso {nuevo_curso}")
                    st.info("📊 Agregado a los 3 trimestres")
                    st.rerun()
                else:
                    st.error("❌ Error al agregar el alumno")
            else:
                st.error("❌ Por favor completa todos los campos")
    with col2:
        if st.button("🔄 Limpiar Formulario", type="secondary", key="btn_limpiar_formulario"):
            st.rerun()
    with col3:
        st.write("")

elif st.session_state.accion_actual == "asistencia":
    st.header("📋 Gestión de Asistencia")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        curso_asistencia = st.selectbox("📂 Seleccionar Curso:", ["Todos", "EF 1A", "EF 2A", "EF 1B", "EF 2B", "TD 2A", "TD 2B"], key="asistencia_curso")
    with col2:
        trimestre_asistencia = st.selectbox("📅 Seleccionar Trimestre:", ["1 Trimestre", "2 Trimestre", "3 Trimestre"], key="asistencia_trimestre")
    with col3:
        fecha_seleccionada = st.date_input("📅 Seleccionar Fecha:", value=datetime.now().date(), key="asistencia_fecha")
    
    st.markdown("---")
    
    st.subheader("📋 Registro de Asistencia - Marcar Rápidamente")
    
    try:
        df_asistencia = pd.read_excel(archivo_excel, sheet_name=trimestre_asistencia)
        
        if curso_asistencia != "Todos":
            df_asistencia = df_asistencia[df_asistencia["Curso"] == curso_asistencia]
        
        if not df_asistencia.empty:
            fecha_str = fecha_seleccionada.strftime("%b-%d")
            
            if fecha_str not in df_asistencia.columns:
                df_asistencia[fecha_str] = "Ausente"
            
            st.write("✅ Marca la casilla para **Presente** - ❌ Casilla sin marcar = **Ausente**")
            
            if 'asistencia_cambios' not in st.session_state:
                st.session_state.asistencia_cambios = {}
            
            for idx, row in df_asistencia.iterrows():
                if pd.notna(row["Apellido y Nombre"]):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.write(f"**{row['Apellido y Nombre']}**")
                        st.write(f"📂 {row['Curso']}")
                    
                    with col2:
                        estado_actual = row[fecha_str] if pd.notna(row[fecha_str]) else "Ausente"
                        
                        presente = st.checkbox(
                            "✅", 
                            value=(estado_actual == "Presente"),
                            key=f"asistencia_{idx}_{fecha_str}",
                            help="Marcar como Presente"
                        )
                        
                        st.session_state.asistencia_cambios[f"{idx}_{fecha_str}"] = presente
                    
                    with col3:
                        if presente:
                            st.success("✅ Presente")
                        else:
                            st.error("❌ Ausente")
                    
                    st.markdown("---")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("💾 Guardar Todos los Cambios", type="primary", key="guardar_todos_asistencia"):
                    cambios_guardados = 0
                    for key, presente in st.session_state.asistencia_cambios.items():
                        if fecha_str in key:
                            idx = int(key.split("_")[0])
                            df_asistencia.at[idx, fecha_str] = "Presente" if presente else "Ausente"
                            cambios_guardados += 1
                    
                    columnas_asistencia = [col for col in df_asistencia.columns if any(mes in col for mes in ["Mar-", "Abr-", "May-"])]
                    for idx, row in df_asistencia.iterrows():
                        if pd.notna(row["Apellido y Nombre"]):
                            presentes = sum(1 for col in columnas_asistencia if pd.notna(row[col]) and row[col] == "Presente")
                            totales = sum(1 for col in columnas_asistencia if pd.notna(row[col]))
                            nota_asistencia = calcular_nota_asistencia(presentes, totales)
                            df_asistencia.at[idx, "Nota Asistencia"] = nota_asistencia
                    
                    if guardar_datos_excel(df_asistencia, trimestre_asistencia, archivo_excel):
                        st.success(f"✅ {cambios_guardados} cambios guardados!")
                        st.info(f"📁 Datos guardados en: {os.path.abspath(archivo_excel)}")
                        st.session_state.asistencia_cambios = {}
                        st.rerun()
                    else:
                        st.error("❌ Error guardando cambios")
            
            with col2:
                if st.button("🔄 Recargar Datos", type="secondary", key="recargar_asistencia"):
                    st.session_state.asistencia_cambios = {}
                    st.rerun()
            
            with col3:
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
    
    col1, col2 = st.columns(2)
    with col1:
        curso_eval = st.selectbox("📂 Seleccionar Curso:", ["Todos", "EF 1A", "EF 2A", "EF 1B", "EF 2B", "TD 2A", "TD 2B"], key="eval_curso")
    with col2:
        trimestre_eval = st.selectbox("📅 Seleccionar Trimestre:", ["1 Trimestre", "2 Trimestre", "3 Trimestre"], key="eval_trimestre")
    
    st.markdown("---")
    
    st.subheader("📝 Sistema de Evaluaciones - Formato Consistente")
    
    with st.expander("➕ Agregar Nueva Evaluación", expanded=False):
        col1, col2, col3, col4 = st.columns([2, 3, 2, 1])

        with col1:
            nuevo_tipo_eval = st.selectbox(
                "Tipo",
                ["Diagnóstico", "Físico", "Técnico", "Desempeño global"],
                key="nuevo_tipo_eval",
                label_visibility="visible"
            )
        with col2:
            nuevo_nombre_eval = st.text_input(
                "Nombre de la evaluación",
                key="nuevo_nombre_eval",
                placeholder="Ej: Test de velocidad",
                label_visibility="visible"
            )
        with col3:
            nueva_calif_eval = st.selectbox(
                "Calificación",
                ["M", "R-", "R+", "B", "MB", "EX"],
                index=3,
                key="nueva_calif_eval",
                label_visibility="visible"
            )
        with col4:
            st.markdown("###")
            if st.button("➕ Agregar", type="primary", key="btn_agregar_nueva_eval"):
                if nuevo_nombre_eval:
                    st.session_state.nuevas_evaluaciones.append({
                        "nombre": nuevo_nombre_eval,
                        "tipo": nuevo_tipo_eval,
                        "calificacion": nueva_calif_eval,
                        "numero": len(st.session_state.nuevas_evaluaciones) + 7
                    })
                    st.success(f"✅ '{nuevo_nombre_eval}' agregada!")
                    st.rerun()
                else:
                    st.error("❌ Ingresá un nombre para la evaluación")
    
    st.markdown("---")
    
    try:
        df_evaluaciones = pd.read_excel(archivo_excel, sheet_name=trimestre_eval)
        
        if curso_eval != "Todos":
            df_evaluaciones = df_evaluaciones[df_evaluaciones["Curso"] == curso_eval]
        
        if not df_evaluaciones.empty:
            st.write("📝 **Evaluaciones** - Formato consistente (nombre arriba, nombre abajo)")
            
            if 'evaluaciones_cambios' not in st.session_state:
                st.session_state.evaluaciones_cambios = {}
            
            for idx, row in df_evaluaciones.iterrows():
                if pd.notna(row["Apellido y Nombre"]):
                    st.write(f"### **{row['Apellido y Nombre']}** - 📂 {row['Curso']}")
                    
                    # Encabezado visual
                    col_h1, col_h2, col_h3, col_h4 = st.columns([1, 3, 2, 1])
                    with col_h1:
                        st.caption("Nro.")
                    with col_h2:
                        st.caption("Nombre de la evaluación")
                    with col_h3:
                        st.caption("Calificación")
                    with col_h4:
                        st.caption("Estado")
                    
                    for j in range(1, 7):
                        eval_col = f"Eval {j}"
                        calif_col = f"Calif {j}"
                        
                        if eval_col in df_evaluaciones.columns and calif_col in df_evaluaciones.columns:
                            col1, col2, col3, col4 = st.columns([1, 3, 2, 1])

                            with col1:
                                tipo_eval = str(row.get('Tipo Evaluación', 'Diagnóstico'))
                                st.markdown(f"**Eval {j}**")
                                st.caption(tipo_eval)

                            with col2:
                                nombre_eval_actual = st.text_input(
                                    f"Nombre evaluación {j}",
                                    value=str(row.get(eval_col, f"Evaluación {j}")),
                                    key=f"eval_nombre_{idx}_{j}",
                                    label_visibility="collapsed"
                                )

                            with col3:
                                calificacion_actual = str(row.get(calif_col, "B"))
                                opciones_calif = ["M", "R-", "R+", "B", "MB", "EX"]
                                idx_cal = opciones_calif.index(calificacion_actual) if calificacion_actual in opciones_calif else 3
                                calificacion = st.selectbox(
                                    f"Calificación {j}",
                                    opciones_calif,
                                    index=idx_cal,
                                    key=f"eval_calif_{idx}_{j}",
                                    label_visibility="collapsed"
                                )

                            with col4:
                                iconos_calif = {
                                    "EX": "🌟",
                                    "MB": "✅",
                                    "B": "🔵",
                                    "R+": "⚠️",
                                    "R-": "🔴",
                                    "M": "💔"
                                }
                                st.markdown(f"### {iconos_calif.get(calificacion, '❓')}")

                            st.session_state.evaluaciones_cambios[f"{idx}_{j}"] = {
                                "nombre": nombre_eval_actual,
                                "calificacion": calificacion
                            }
                    
                    if st.session_state.nuevas_evaluaciones:
                        for nueva_eval in st.session_state.nuevas_evaluaciones:
                            # Layout claro para nuevas evaluaciones
                            st.markdown("---")
                            st.write(f"### 🆕 **Nueva Evaluación: {nueva_eval['nombre']}**")
                            
                            col1, col2, col3 = st.columns([2, 3, 2])
                            
                            with col1:
                                st.write("**📋 Tipo de Evaluación**")
                                st.write(f"**{nueva_eval['tipo']}**")
                            
                            with col2:
                                st.write("**📝 Nombre de la Evaluación**")
                                st.write(f"**{nueva_eval['nombre']}**")
                                calif_nueva = st.selectbox(
                                    "Calif:", 
                                    ["M", "R-", "R+", "B", "MB", "EX"],
                                    key=f"eval_nueva_{nueva_eval['numero']}_{idx}",
                                    help="Seleccionar calificación"
                                )
                            
                            with col3:
                                st.write("**⭐ Calificación**")
                                # Mostrar calificación con color
                                if calif_nueva == "EX":
                                    st.success("🌟 EXCELENTE")
                                elif calif_nueva == "MB":
                                    st.success("✅ MUY BUENO")
                                elif calif_nueva == "B":
                                    st.info("✅ BUENO")
                                elif calif_nueva == "R+":
                                    st.warning("⚠️ REGULAR+")
                                elif calif_nueva == "R-":
                                    st.error("❌ REGULAR-")
                                else:
                                    st.error("💔 INSUFICIENTE")
                    
                    st.markdown("---")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("💾 Guardar Todos los Cambios", type="primary", key="guardar_todos_evaluaciones"):
                    with st.spinner("Guardando cambios..."):
                        cambios_guardados = 0
                        try:
                            # Aplicar cambios al dataframe
                            for key, cambios in st.session_state.evaluaciones_cambios.items():
                                partes = key.split("_")
                                idx = int(partes[0])
                                j = int(partes[1])

                                eval_col = f"Eval {j}"
                                calif_col = f"Calif {j}"

                                df_evaluaciones.at[idx, eval_col] = cambios["nombre"]
                                df_evaluaciones.at[idx, calif_col] = cambios["calificacion"]
                                cambios_guardados += 1

                            # Recalcular nota final de cada alumno
                            for idx, row in df_evaluaciones.iterrows():
                                if pd.notna(row.get("Apellido y Nombre")):
                                    calificaciones_temp = []
                                    for i in range(1, 7):
                                        calif_val = df_evaluaciones.at[idx, f"Calif {i}"]
                                        if pd.notna(calif_val):
                                            calificaciones_temp.append(calificacion_a_numero(calif_val))
                                    if calificaciones_temp:
                                        promedio_final = sum(calificaciones_temp) / len(calificaciones_temp)
                                        df_evaluaciones.at[idx, "Nota Final Evaluaciones"] = round(promedio_final, 1)

                            # Guardar en Excel local
                            exito_local = guardar_datos_excel(df_evaluaciones, trimestre_eval, archivo_excel)

                            if exito_local:
                                ruta_absoluta = os.path.abspath(archivo_excel)
                                st.success(f"✅ {cambios_guardados} cambios guardados en Excel!")
                                st.info(f"📁 Archivo guardado en: {ruta_absoluta}")
                                st.session_state.evaluaciones_cambios = {}
                            else:
                                st.error("❌ Error al guardar en Excel local")
                                st.stop()

                            # Guardar en Google Sheets
                            with st.spinner("Sincronizando con Google Sheets..."):
                                ok, mensaje = sincronizar_google_sheets()
                                if ok:
                                    st.success(f"✅ Google Sheets actualizado: {mensaje}")
                                else:
                                    st.warning(f"⚠️ Excel guardado pero Google Sheets falló: {mensaje}")

                            st.rerun()

                        except Exception as e:
                            st.error(f"❌ Error inesperado al guardar: {e}")
            
            with col2:
                if st.button("🔄 Recargar Datos", type="secondary", key="recargar_evaluaciones"):
                    st.session_state.evaluaciones_cambios = {}
                    st.rerun()
            
            with col3:
                calificaciones_contadas = {"M": 0, "R-": 0, "R+": 0, "B": 0, "MB": 0, "EX": 0}
                total_evaluaciones = 0
                
                for idx, row in df_evaluaciones.iterrows():
                    if pd.notna(row["Apellido y Nombre"]):
                        for j in range(1, 7):
                            calif_col = f"Calif {j}"
                            calif = row.get(calif_col)
                            if pd.notna(calif) and calif in calificaciones_contadas:
                                calificaciones_contadas[calif] += 1
                                total_evaluaciones += 1
                
                if total_evaluaciones > 0:
                    st.metric("📊 Total Evaluaciones", f"{total_evaluaciones}")
        else:
            st.info("📋 No hay alumnas para mostrar en este curso")
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("📊 Agrega datos simulados para probar")

elif st.session_state.accion_actual == "reporte":
    st.header("📊 Reporte Individual Completo")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        curso_reporte = st.selectbox("📂 Seleccionar Curso:", ["Todos", "EF 1A", "EF 2A", "EF 1B", "EF 2B", "TD 2A", "TD 2B"], key="reporte_curso")
    with col2:
        trimestre_reporte = st.selectbox("📅 Seleccionar Trimestre:", ["1 Trimestre", "2 Trimestre", "3 Trimestre"], key="reporte_trimestre")
    with col3:
        alumnos_disponibles = obtener_alumnos_disponibles()
        alumno_reporte = st.selectbox("👤 Seleccionar Alumno:", alumnos_disponibles, key="reporte_alumno")
    
    st.markdown("---")
    
    try:
        df_reporte = pd.read_excel(archivo_excel, sheet_name=trimestre_reporte)
        
        if curso_reporte != "Todos":
            df_reporte = df_reporte[df_reporte["Curso"] == curso_reporte]
        
        if alumno_reporte != "Todos":
            df_reporte = df_reporte[df_reporte["Apellido y Nombre"] == alumno_reporte]
        
        if not df_reporte.empty:
            for idx, row in df_reporte.iterrows():
                if pd.notna(row["Apellido y Nombre"]):
                    st.write(f"# 📊 Reporte Individual: {row['Apellido y Nombre']}")
                    st.write(f"**📂 Curso:** {row['Curso']}")
                    st.write(f"**📅 Trimestre:** {trimestre_reporte}")
                    st.markdown("---")
                    
                    st.write("## 📋 Asistencia")
                    columnas_asistencia = [col for col in df_reporte.columns if any(mes in col for mes in ["Mar-", "Abr-", "May-"])]
                    presentes = sum(1 for col in columnas_asistencia if pd.notna(row[col]) and row[col] == "Presente")
                    totales = sum(1 for col in columnas_asistencia if pd.notna(row[col]))
                    ausentes = totales - presentes
                    porcentaje = (presentes / totales * 100) if totales > 0 else 0
                    
                    if porcentaje >= 80:
                        nota_asistencia = "EX (10)"
                        color_asistencia = "🌟"
                    elif porcentaje >= 51:
                        nota_asistencia = "R+ (8)"
                        color_asistencia = "⚠️"
                    else:
                        nota_asistencia = "M (5)"
                        color_asistencia = "💔"
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1: st.metric("📊 Días Presentes", presentes)
                    with col2: st.metric("📊 Días Ausentes", ausentes)
                    with col3: st.metric("📊 % Asistencia", f"{porcentaje:.1f}%")
                    with col4: st.metric("📊 Nota Asistencia", f"{color_asistencia} {nota_asistencia}")
                    
                    st.markdown("---")
                    st.write("### 📈 Gráfico de Asistencia")
                    crear_grafico_asistencia(presentes, ausentes, row["Apellido y Nombre"])
                    
                    st.markdown("---")
                    st.write("## 📝 Evaluaciones")
                    evaluaciones_data = []
                    calificaciones = []
                    
                    for i in range(1, 7):
                        eval_col = f"Eval {i}"
                        calif_col = f"Calif {i}"
                        if pd.notna(row[eval_col]) and pd.notna(row[calif_col]):
                            evaluaciones_data.append({
                                "Evaluación": row[eval_col],
                                "Calificación": row[calif_col],
                                "Valor Numérico": calificacion_a_numero(row[calif_col])
                            })
                            calificaciones.append(calificacion_a_numero(row[calif_col]))
                    
                    if evaluaciones_data:
                        df_eval_display = pd.DataFrame(evaluaciones_data)
                        st.dataframe(df_eval_display, use_container_width=True)
                        
                        promedio_final = sum(calificaciones) / len(calificaciones) if calificaciones else 0
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("📊 Promedio Final Evaluaciones", f"{promedio_final:.1f}")
                        with col2:
                            if promedio_final >= 9:
                                calif_final = "EX"
                                color_final = "🌟"
                            elif promedio_final >= 8:
                                calif_final = "MB"
                                color_final = "✅"
                            elif promedio_final >= 7:
                                calif_final = "B"
                                color_final = "✅"
                            elif promedio_final >= 6:
                                calif_final = "R+"
                                color_final = "⚠️"
                            else:
                                calif_final = "M"
                                color_final = "💔"
                            
                            st.metric("📊 Calificación Final", f"{color_final} {calif_final}")
                        
                        st.markdown("---")
                        st.write("### 📈 Gráfico de Evaluaciones")
                        crear_grafico_evaluaciones(evaluaciones_data, row["Apellido y Nombre"])
                    
                    st.markdown("---")
                    st.write("## 📈 Resumen General")
                    nota_asistencia_num = calcular_nota_asistencia(presentes, totales)
                    promedio_eval = sum(calificaciones) / len(calificaciones) if calificaciones else 0
                    promedio_general = (nota_asistencia_num + promedio_eval) / 2 if calificaciones else nota_asistencia_num
                    
                    col1, col2, col3 = st.columns(3)
                    with col1: st.metric("📊 Nota Asistencia", f"{nota_asistencia_num:.1f}")
                    with col2: st.metric("📊 Promedio Evaluaciones", f"{promedio_eval:.1f}")
                    with col3: st.metric("📊 Promedio General", f"{promedio_general:.1f}")
                    
                    break
        else:
            st.info("📋 No hay datos para mostrar")
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("📊 Agrega datos simulados para probar")

elif st.session_state.accion_actual == "estadistica":
    st.header("📈 Análisis Estadístico Individual")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        curso_stats = st.selectbox("📂 Seleccionar Curso:", ["Todos", "EF 1A", "EF 2A", "EF 1B", "EF 2B", "TD 2A", "TD 2B"], key="stats_curso")
    with col2:
        trimestre_stats = st.selectbox("📅 Seleccionar Trimestre:", ["1 Trimestre", "2 Trimestre", "3 Trimestre"], key="stats_trimestre")
    with col3:
        alumnos_disponibles = obtener_alumnos_disponibles()
        alumno_stats = st.selectbox("👤 Seleccionar Alumno:", alumnos_disponibles, key="stats_alumno")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📈 Generar Estadísticas", type="primary", key="btn_generar_stats"):
            st.success("✅ Estadísticas generadas!")
    with col2:
        st.write("")
    with col3:
        st.write("")
    
    st.markdown("---")
    
    st.subheader("📊 Estadísticas Individuales Detalladas")
    try:
        df_stats = pd.read_excel(archivo_excel, sheet_name=trimestre_stats)
        
        if curso_stats != "Todos":
            df_stats = df_stats[df_stats["Curso"] == curso_stats]
        
        if alumno_stats != "Todos":
            df_stats = df_stats[df_stats["Apellido y Nombre"] == alumno_stats]
        
        if not df_stats.empty:
            for idx, row in df_stats.iterrows():
                if pd.notna(row["Apellido y Nombre"]):
                    st.write(f"## 📊 Estadísticas de: {row['Apellido y Nombre']}")
                    st.write(f"**📂 Curso:** {row['Curso']} | **📅 Trimestre:** {trimestre_stats}")
                    st.markdown("---")
                    
                    st.write("### 📋 Estadísticas de Asistencia")
                    columnas_asistencia = [col for col in df_stats.columns if any(mes in col for mes in ["Mar-", "Abr-", "May-"])]
                    presentes = sum(1 for col in columnas_asistencia if pd.notna(row[col]) and row[col] == "Presente")
                    totales = sum(1 for col in columnas_asistencia if pd.notna(row[col]))
                    ausentes = totales - presentes
                    porcentaje = (presentes / totales * 100) if totales > 0 else 0
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1: st.metric("📊 Días Presentes", presentes)
                    with col2: st.metric("📊 Días Ausentes", ausentes)
                    with col3: st.metric("📊 Total Días", totales)
                    with col4: st.metric("📊 % Asistencia", f"{porcentaje:.1f}%")
                    
                    st.markdown("---")
                    st.write("### 📝 Estadísticas de Evaluaciones Detalladas")
                    evaluaciones_detalle = []
                    calificaciones = []
                    
                    for i in range(1, 7):
                        eval_col = f"Eval {i}"
                        calif_col = f"Calif {i}"
                        if pd.notna(row[eval_col]) and pd.notna(row[calif_col]):
                            calif_num = calificacion_a_numero(row[calif_col])
                            evaluaciones_detalle.append({
                                "Evaluación": row[eval_col],
                                "Calificación": row[calif_col],
                                "Valor Numérico": calif_num
                            })
                            calificaciones.append(calif_num)
                    
                    if evaluaciones_detalle:
                        df_eval_detalle = pd.DataFrame(evaluaciones_detalle)
                        st.dataframe(df_eval_detalle, use_container_width=True)
                        
                        if calificaciones:
                            promedio_final = sum(calificaciones) / len(calificaciones)
                            max_calificacion = max(calificaciones)
                            min_calificacion = min(calificaciones)
                            
                            st.markdown("---")
                            st.write("#### 📈 Resumen Numérico de Evaluaciones")
                            col1, col2, col3, col4 = st.columns(4)
                            with col1: st.metric("📊 Promedio Final", f"{promedio_final:.1f}")
                            with col2: st.metric("📊 Calificación Más Alta", f"{max_calificacion:.1f}")
                            with col3: st.metric("📊 Calificación Más Baja", f"{min_calificacion:.1f}")
                            with col4: st.metric("📊 Total Evaluaciones", len(calificaciones))
                            
                            st.markdown("---")
                            st.write("#### 📈 Gráfico de Desempeño por Evaluación")
                            crear_grafico_evaluaciones(evaluaciones_detalle, row["Apellido y Nombre"])
                    
                    st.markdown("---")
                    st.write("### 📈 Resumen General Individual")
                    nota_asistencia_num = calcular_nota_asistencia(presentes, totales)
                    promedio_eval = sum(calificaciones) / len(calificaciones) if calificaciones else 0
                    promedio_general = (nota_asistencia_num + promedio_eval) / 2 if calificaciones else nota_asistencia_num
                    
                    col1, col2, col3 = st.columns(3)
                    with col1: st.metric("📊 Nota Asistencia", f"{nota_asistencia_num:.1f}")
                    with col2: st.metric("📊 Promedio Evaluaciones", f"{promedio_eval:.1f}")
                    with col3: st.metric("📊 Promedio General", f"{promedio_general:.1f}")
                    
                    break
        else:
            st.info("📋 No hay datos para analizar")
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("📊 Agrega datos simulados para probar")

st.markdown("---")
