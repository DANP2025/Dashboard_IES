import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
import random

st.set_page_config(page_title="Sistema Educativo", page_icon="📚", layout="wide", initial_sidebar_state="expanded")

GOOGLE_SHEETS_DISPONIBLE = False
try:
    if "gcp_service_account" in st.secrets:
        GOOGLE_SHEETS_DISPONIBLE = True
except Exception:
    GOOGLE_SHEETS_DISPONIBLE = False

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
                cell.fill = PatternFill(start_color="DDDDDD", end_color="DDDDDD", fill_type="solid")
                cell.alignment = Alignment(horizontal="center")
        wb.save(archivo_excel)
    return archivo_excel

def calcular_nota_asistencia(presentes, totales):
    if totales == 0:
        return 0
    porcentaje = (presentes / totales) * 100
    if porcentaje >= 90:
        return 10
    elif porcentaje >= 80:
        return 8
    else:
        return 5

def calificacion_a_numero(calif):
    try:
        calificaciones = {"M": 2, "R-": 4, "R+": 5, "B": 6, "MB": 8, "EX": 10}
        return calificaciones.get(calif, 0)
    except:
        return 0

def guardar_datos_excel(df, sheet_name, archivo_excel="sistema_educativo.xlsx"):
    """Función para guardar datos en Excel con manejo de errores"""
    try:
        with pd.ExcelWriter(archivo_excel, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        return True
    except Exception as e:
        st.error(f"Error guardando en Excel: {e}")
        return False

def generar_backup_detalles():
    """Generar backup detallado en Excel con todas las columnas solicitadas"""
    try:
        archivo_excel = "sistema_educativo.xlsx"
        if not os.path.exists(archivo_excel):
            return False
        
        backup_filename = f"backup_detalles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        wb_backup = openpyxl.Workbook()
        wb_backup.remove(wb_backup.active)
        
        for trimestre_num in range(1, 4):
            nombre_trimestre = f"{trimestre_num} Trimestre"
            ws_backup = wb_backup.create_sheet(title=nombre_trimestre)
            
            headers_backup = [
                "Fecha y Hora Backup", "Alumno", "Curso", "Trimestre",
                "Asistencia", "Evaluación", "Tipo Evaluación", "Calificación"
            ]
            
            for col_num, header in enumerate(headers_backup, 1):
                cell = ws_backup.cell(row=1, column=col_num, value=header)
                cell.font = Font(bold=True)
                cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
                cell.alignment = Alignment(horizontal="center")
            
            df_trimestre = pd.read_excel(archivo_excel, sheet_name=nombre_trimestre)
            
            if not df_trimestre.empty:
                row_num = 2
                for idx, row in df_trimestre.iterrows():
                    if pd.notna(row["Apellido y Nombre"]):
                        columnas_asistencia = [col for col in df_trimestre.columns if any(mes in col for mes in ["Mar-", "Abr-", "May-"])]
                        presentes = sum(1 for col in columnas_asistencia if pd.notna(row[col]) and row[col] == "Presente")
                        totales = sum(1 for col in columnas_asistencia if pd.notna(row[col]))
                        porcentaje_asistencia = (presentes / totales * 100) if totales > 0 else 0
                        
                        ws_backup.cell(row=row_num, column=1, value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        ws_backup.cell(row=row_num, column=2, value=row["Apellido y Nombre"])
                        ws_backup.cell(row=row_num, column=3, value=row["Curso"])
                        ws_backup.cell(row=row_num, column=4, value=nombre_trimestre)
                        ws_backup.cell(row=row_num, column=5, value=f"{presentes}/{totales} ({porcentaje_asistencia:.1f}%)")
                        ws_backup.cell(row=row_num, column=6, value="")
                        ws_backup.cell(row=row_num, column=7, value="")
                        ws_backup.cell(row=row_num, column=8, value="")
                        row_num += 1
                        
                        for j in range(1, 7):
                            eval_col = f"Eval {j}"
                            calif_col = f"Calif {j}"
                            
                            if pd.notna(row[eval_col]) and pd.notna(row[calif_col]):
                                ws_backup.cell(row=row_num, column=1, value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                ws_backup.cell(row=row_num, column=2, value=row["Apellido y Nombre"])
                                ws_backup.cell(row=row_num, column=3, value=row["Curso"])
                                ws_backup.cell(row=row_num, column=4, value=nombre_trimestre)
                                ws_backup.cell(row=row_num, column=5, value="")
                                ws_backup.cell(row=row_num, column=6, value=row[eval_col])
                                ws_backup.cell(row=row_num, column=7, value=row.get("Tipo Evaluación", ""))
                                ws_backup.cell(row=row_num, column=8, value=row[calif_col])
                                row_num += 1
        
        wb_backup.save(backup_filename)
        return True
    except Exception as e:
        st.error(f"Error generando backup: {e}")
        return False

def cargar_datos_desde_sheets(nombre_trimestre):
    """Carga datos desde Google Sheets si no existe el Excel local"""
    try:
        import gspread
        from google.oauth2.service_account import Credentials

        if not GOOGLE_SHEETS_DISPONIBLE:
            return None

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

        SPREADSHEET_ID = st.secrets["gcp_service_account"]["sheet_id"]
        spreadsheet = client.open_by_key(SPREADSHEET_ID)

        try:
            ws = spreadsheet.worksheet(nombre_trimestre)
            data = ws.get_all_values()
            if len(data) <= 1:
                return None
            
            headers = data[0]
            rows = data[1:]
            
            df = pd.DataFrame(rows, columns=headers)
            return df
        except Exception:
            return None
    except Exception:
        return None

def sincronizar_google_sheets():
    """Sincroniza todos los datos con Google Sheets de forma legible"""
    try:
        import gspread
        from google.oauth2.service_account import Credentials

        if not GOOGLE_SHEETS_DISPONIBLE:
            return False, "Secrets de Google no configurados"

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

        SPREADSHEET_ID = st.secrets["gcp_service_account"]["sheet_id"]
        spreadsheet = client.open_by_key(SPREADSHEET_ID)

        archivo_excel = "sistema_educativo.xlsx"
        if not os.path.exists(archivo_excel):
            return False, "No existe el archivo Excel local. Primero agregá datos simulados."

        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")

        headers = [
            "Última Actualización",
            "Apellido y Nombre",
            "Curso",
            "Trimestre",
            "Días Presentes",
            "Días Ausentes",
            "% Asistencia",
            "Nota Asistencia",
            "Eval 1 — Nombre",
            "Eval 1 — Calif",
            "Eval 2 — Nombre",
            "Eval 2 — Calif",
            "Eval 3 — Nombre",
            "Eval 3 — Calif",
            "Eval 4 — Nombre",
            "Eval 4 — Calif",
            "Eval 5 — Nombre",
            "Eval 5 — Calif",
            "Eval 6 — Nombre",
            "Eval 6 — Calif",
            "Promedio Final"
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
                presentes = sum(
                    1 for col in columnas_asistencia
                    if pd.notna(row.get(col)) and row.get(col) == "Presente"
                )
                totales = sum(
                    1 for col in columnas_asistencia
                    if pd.notna(row.get(col))
                )
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
                "backgroundColor": {"red": 0.118, "green": 0.227, "blue": 0.373},
                "textFormat": {
                    "bold": True,
                    "fontSize": 10,
                    "foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}
                },
                "horizontalAlignment": "CENTER"
            })

            if len(rows_data) > 1:
                rango_datos = f"A2:U{len(rows_data)}"
                ws.format(rango_datos, {
                    "textFormat": {"fontSize": 10},
                    "horizontalAlignment": "LEFT"
                })

        return True, f"Sincronizado el {timestamp}"

    except Exception as e:
        return False, str(e)

def restaurar_desde_sheets_si_vacio():
    """Si el Excel local está vacío, restaura desde Google Sheets"""
    try:
        if not GOOGLE_SHEETS_DISPONIBLE:
            return False
        wb_check = openpyxl.load_workbook(archivo_excel)
        ws_check = wb_check["1 Trimestre"]
        tiene_datos = ws_check.max_row > 1
        wb_check.close()
        if tiene_datos:
            return False

        restaurado = False
        for trimestre_num in range(1, 4):
            nombre_trimestre = f"{trimestre_num} Trimestre"
            df_sheets = cargar_datos_desde_sheets(nombre_trimestre)
            if df_sheets is not None and not df_sheets.empty:
                guardar_datos_excel(df_sheets, nombre_trimestre, archivo_excel)
                restaurado = True
        return restaurado
    except Exception:
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
                
                df_trimestre = pd.read_excel(archivo_excel, sheet_name=nombre_trimestre)
                
                for curso in cursos:
                    alumnos_curso = [n for n in nombres_femeninos if curso in n] + [n for n in nombres_adicionales_ef1a if curso in n]
                    if curso == "EF 1A":
                        alumnos_curso = alumnos_curso[:5]
                    elif curso == "EF 2A":
                        alumnos_curso = alumnos_curso[:5]
                    
                    for alumno in alumnos_curso:
                        if alumno not in df_trimestre["Apellido y Nombre"].values:
                            nueva_fila = {
                                "Apellido y Nombre": alumno,
                                "Curso": curso,
                                "Tipo Evaluación": "Diagnóstico"
                            }
                            
                            for mes in range(1, 32):
                                fecha_col = f"Mar-{mes:02d}"
                                if fecha_col not in df_trimestre.columns:
                                    df_trimestre[fecha_col] = "Ausente"
                                nueva_fila[fecha_col] = "Ausente" if random.random() > 0.15 else "Presente"
                            
                            for mes in range(1, 31):
                                fecha_col = f"Abr-{mes:02d}"
                                if fecha_col not in df_trimestre.columns:
                                    df_trimestre[fecha_col] = "Ausente"
                                nueva_fila[fecha_col] = "Ausente" if random.random() > 0.15 else "Presente"
                            
                            for mes in range(1, 32):
                                fecha_col = f"May-{mes:02d}"
                                if fecha_col not in df_trimestre.columns:
                                    df_trimestre[fecha_col] = "Ausente"
                                nueva_fila[fecha_col] = "Ausente" if random.random() > 0.15 else "Presente"
                            
                            evaluaciones = [
                                "Test de Velocidad", "Test de Resistencia", "Test de Flexibilidad",
                                "Test de Fuerza", "Test de Coordinación", "Test de Agilidad"
                            ]
                            calificaciones = ["B", "MB", "EX", "R+", "R-", "M"]
                            
                            for i in range(1, 7):
                                nueva_fila[f"Eval {i}"] = random.choice(evaluaciones)
                                nueva_fila[f"Calif {i}"] = random.choice(calificaciones)
                            
                            df_trimestre = pd.concat([df_trimestre, pd.DataFrame([nueva_fila])], ignore_index=True)
                
                guardar_datos_excel(df_trimestre, nombre_trimestre, archivo_excel)
            return True
        except Exception as e:
            st.error(f"Error generando datos simulados: {e}")
            return False
    return False

def agregar_nuevo_alumno(nombre, curso):
    archivo_excel = "sistema_educativo.xlsx"
    try:
        for trimestre_num in range(1, 4):
            nombre_trimestre = f"{trimestre_num} Trimestre"
            df_trimestre = pd.read_excel(archivo_excel, sheet_name=nombre_trimestre)
            
            nueva_fila = {
                "Apellido y Nombre": nombre,
                "Curso": curso,
                "Tipo Evaluación": "Diagnóstico"
            }
            
            columnas_asistencia = [col for col in df_trimestre.columns if any(mes in col for mes in ["Mar-", "Abr-", "May-"])]
            for col in columnas_asistencia:
                nueva_fila[col] = "Ausente"
            
            for i in range(1, 7):
                nueva_fila[f"Eval {i}"] = ""
                nueva_fila[f"Calif {i}"] = ""
            
            df_trimestre = pd.concat([df_trimestre, pd.DataFrame([nueva_fila])], ignore_index=True)
            guardar_datos_excel(df_trimestre, nombre_trimestre, archivo_excel)
        
        return True
    except Exception as e:
        st.error(f"Error agregando alumno: {e}")
        return False

def obtener_alumnos_disponibles():
    archivo_excel = "sistema_educativo.xlsx"
    try:
        df_1t = pd.read_excel(archivo_excel, sheet_name="1 Trimestre")
        alumnos = df_1t["Apellido y Nombre"].dropna().tolist()
        return ["Todos"] + sorted(alumnos)
    except Exception:
        return ["Todos"]

def crear_grafico_asistencia(presentes, ausentes, nombre_alumno):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 4))
    labels = ['Presentes', 'Ausentes']
    sizes = [presentes, ausentes]
    colors = ['#2ecc71', '#e74c3c']
    explode = (0.1, 0)
    
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    plt.title(f'Asistencia - {nombre_alumno}', fontsize=14, fontweight='bold')
    
    return fig

def crear_grafico_evaluaciones(evaluaciones_data, nombre_alumno):
    import matplotlib.pyplot as plt
    if not evaluaciones_data:
        return None
    
    df_grafico = pd.DataFrame(evaluaciones_data)
    if not df_grafico.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(df_grafico['Evaluación'], df_grafico['Valor Numérico'], color='#3498db')
        ax.set_xlabel('Evaluaciones', fontsize=12)
        ax.set_ylabel('Calificación', fontsize=12)
        ax.set_title(f'Rendimiento en Evaluaciones - {nombre_alumno}', fontsize=14, fontweight='bold')
        ax.set_ylim(0, 10.5)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        return fig
    return None

# Inicializar estado
if 'accion_actual' not in st.session_state:
    st.session_state.accion_actual = "dashboard"
if 'nuevas_evaluaciones' not in st.session_state:
    st.session_state.nuevas_evaluaciones = []

# Sidebar con botones de navegación
st.sidebar.markdown("# 📚 Sistema Educativo")
st.sidebar.markdown("---")

if st.sidebar.button("📊 Dashboard", type="primary", key="btn_dashboard"):
    st.session_state.accion_actual = "dashboard"
if st.sidebar.button("📋 Asistencia", type="primary", key="btn_asistencia"):
    st.session_state.accion_actual = "asistencia"
if st.sidebar.button("📝 Evaluaciones", type="primary", key="btn_evaluaciones"):
    st.session_state.accion_actual = "evaluaciones"
if st.sidebar.button("👤 Agregar Alumno", type="primary", key="btn_agregar_alumno"):
    st.session_state.accion_actual = "agregar_alumno"
if st.sidebar.button("📈 Estadística", type="primary", key="btn_estadistica"):
    st.session_state.accion_actual = "estadistica"
if st.sidebar.button("📊 Reporte", type="primary", key="btn_reporte"):
    st.session_state.accion_actual = "reporte"

st.sidebar.markdown("---")

# Guardar y Backup
if st.sidebar.button("💾 Guardar y Backup", type="primary", key="guardar_backup_principal"):
    try:
        if generar_backup_detalles():
            st.sidebar.success("✅ Backup Excel generado!")
        else:
            st.sidebar.error("❌ Error generando backup Excel")
    except Exception as e:
        st.sidebar.error(f"❌ Error Excel: {e}")

    with st.sidebar:
        with st.spinner("Sincronizando Google Sheets..."):
            ok, mensaje = sincronizar_google_sheets()
            if ok:
                st.sidebar.success(f"✅ Google Sheets: {mensaje}")
            else:
                st.sidebar.error(f"❌ Google Sheets: {mensaje}")

# Inicializar estado
if 'accion_actual' not in st.session_state:
    st.session_state.accion_actual = "dashboard"
if 'nuevas_evaluaciones' not in st.session_state:
    st.session_state.nuevas_evaluaciones = []

archivo_excel = crear_excel_si_no_existe()

# Restaurar desde Google Sheets si Streamlit reinició y perdió los datos
if GOOGLE_SHEETS_DISPONIBLE:
    try:
        if restaurar_desde_sheets_si_vacio():
            st.toast("✅ Datos restaurados desde Google Sheets", icon="☁️")
    except Exception:
        pass

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
    
    resumen_cursos = [
        {"Curso": "EF 1A", "Alumnos": 10, "Asistencia": "85%", "Promedio": "7.8"},
        {"Curso": "EF 2A", "Alumnos": 10, "Asistencia": "78%", "Promedio": "7.2"},
        {"Curso": "EF 1B", "Alumnos": 10, "Asistencia": "82%", "Promedio": "7.5"},
        {"Curso": "EF 2B", "Alumnos": 10, "Asistencia": "80%", "Promedio": "7.6"},
        {"Curso": "TD 2A", "Alumnos": 10, "Asistencia": "76%", "Promedio": "7.2"},
        {"Curso": "TD 2B", "Alumnos": 10, "Asistencia": "80%", "Promedio": "7.6"}
    ]
    df_resumen = pd.DataFrame(resumen_cursos)
    st.dataframe(df_resumen, use_container_width=True)
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 Agregar Datos Simulados Completos", type="primary"):
            with st.spinner("Generando datos..."):
                try:
                    if agregar_datos_simulados_completos():
                        st.success("✅ Datos simulados agregados!")
                        st.info("📊 10 alumnos por curso, 6 cursos")
                        st.info("📝 6 evaluaciones por trimestre")
                        st.info("📅 Datos para los 3 trimestres")
                        with st.spinner("Sincronizando con Google Sheets..."):
                            ok, mensaje = sincronizar_google_sheets()
                            if ok:
                                st.success("✅ Google Sheets actualizado!")
                            else:
                                st.warning(f"⚠️ Sheets: {mensaje}")
                        st.rerun()
                    else:
                        st.error("❌ Error generando datos")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
    with col2:
        if st.button("🔄 Actualizar Datos", type="secondary"):
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
        # Intentar leer desde Excel local
        df_asistencia = pd.read_excel(archivo_excel, sheet_name=trimestre_asistencia)
        # Si está vacío, intentar desde Sheets
        if df_asistencia.empty and GOOGLE_SHEETS_DISPONIBLE:
            df_sheets = cargar_datos_desde_sheets(trimestre_asistencia)
            if df_sheets is not None and not df_sheets.empty:
                guardar_datos_excel(df_sheets, trimestre_asistencia, archivo_excel)
                df_asistencia = df_sheets
    except Exception:
        df_asistencia = pd.DataFrame()
        if GOOGLE_SHEETS_DISPONIBLE:
            df_sheets = cargar_datos_desde_sheets(trimestre_asistencia)
            if df_sheets is not None and not df_sheets.empty:
                df_asistencia = df_sheets
        
        if curso_asistencia != "Todos":
            df_asistencia = df_asistencia[df_asistencia["Curso"] == curso_asistencia]
        
        if not df_asistencia.empty:
            meses_es = {
                "Jan": "Jan", "Feb": "Feb", "Mar": "Mar", "Apr": "Abr",
                "May": "May", "Jun": "Jun", "Jul": "Jul", "Aug": "Ago",
                "Sep": "Sep", "Oct": "Oct", "Nov": "Nov", "Dec": "Dic"
            }
            mes_en = fecha_seleccionada.strftime("%b")
            mes = meses_es.get(mes_en, mes_en)
            fecha_str = f"{mes}-{fecha_seleccionada.strftime('%d')}"
            
            if fecha_str not in df_asistencia.columns:
                df_asistencia[fecha_str] = "Ausente"
            
            st.write("✅ Marca la casilla para **Presente** - ❌ Casilla sin marcar = **Ausente**")
            
            if 'asistencia_cambios' not in st.session_state:
                st.session_state.asistencia_cambios = {}
            
            for idx, row in df_asistencia.iterrows():
                if pd.notna(row["Apellido y Nombre"]):
                    st.write(f"### **{row['Apellido y Nombre']}** - 📂 {row['Curso']}")
                    
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
                        
                        if presente != (estado_actual == "Presente"):
                            st.session_state.asistencia_cambios[f"{idx}_{fecha_str}"] = "Presente" if presente else "Ausente"
                    
                    with col3:
                        if pd.notna(row[fecha_str]):
                            if row[fecha_str] == "Presente":
                                st.success("✅ Presente")
                            else:
                                st.error("❌ Ausente")
                        else:
                            st.warning("⚠️ Sin dato")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("💾 Guardar Asistencia", type="primary", key="guardar_todos_asistencia"):
                    with st.spinner("Guardando asistencia..."):
                        try:
                            cambios_guardados = 0
                            for key, presente in st.session_state.asistencia_cambios.items():
                                if fecha_str in key:
                                    idx = int(key.split("_")[0])
                                    df_asistencia.at[idx, fecha_str] = "Presente" if presente else "Ausente"
                                    cambios_guardados += 1

                            # Recalcular nota asistencia
                            columnas_asistencia = [col for col in df_asistencia.columns if any(mes in col for mes in ["Mar-", "Abr-", "May-"])]
                            for idx, row in df_asistencia.iterrows():
                                if pd.notna(row["Apellido y Nombre"]):
                                    presentes = sum(1 for col in columnas_asistencia if pd.notna(row[col]) and row[col] == "Presente")
                                    totales = sum(1 for col in columnas_asistencia if pd.notna(row[col]))
                                    df_asistencia.at[idx, "Nota Asistencia"] = calcular_nota_asistencia(presentes, totales)

                            # Guardar Excel local
                            if guardar_datos_excel(df_asistencia, trimestre_asistencia, archivo_excel):
                                st.success(f"✅ Asistencia del {fecha_seleccionada.strftime('%d/%m/%Y')} guardada — {cambios_guardados} registros")
                                st.session_state.asistencia_cambios = {}
                            else:
                                st.error("❌ Error guardando Excel local")
                                st.stop()

                            # Sincronizar con Google Sheets
                            with st.spinner("Sincronizando con Google Sheets..."):
                                ok, mensaje = sincronizar_google_sheets()
                                if ok:
                                    st.success("✅ Google Sheets actualizado!")
                                else:
                                    st.warning(f"⚠️ Excel guardado pero Sheets falló: {mensaje}")

                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
            with col2:
                if st.button("🔄 Recargar Datos", type="secondary", key="recargar_asistencia"):
                    st.session_state.asistencia_cambios = {}
                    st.rerun()
            with col3:
                st.write("")
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("📊 Agrega datos simulados para probar")

elif st.session_state.accion_actual == "evaluaciones":
    st.header("📝 Gestión de Evaluaciones")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        curso_eval = st.selectbox(
            "📂 Seleccionar Curso:",
            ["Todos", "EF 1A", "EF 2A", "EF 1B", "EF 2B", "TD 2A", "TD 2B"],
            key="eval_curso"
        )
    with col2:
        trimestre_eval = st.selectbox(
            "📅 Seleccionar Trimestre:",
            ["1 Trimestre", "2 Trimestre", "3 Trimestre"],
            key="eval_trimestre"
        )
    with col3:
        fecha_evaluacion = st.date_input(
            "📅 Fecha de Evaluación:",
            value=datetime.now().date(),
            key="eval_fecha"
        )
    
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
        # Intentar leer desde Excel local
        df_evaluaciones = pd.read_excel(archivo_excel, sheet_name=trimestre_eval)
        # Si está vacío, intentar desde Sheets
        if df_evaluaciones.empty and GOOGLE_SHEETS_DISPONIBLE:
            df_sheets = cargar_datos_desde_sheets(trimestre_eval)
            if df_sheets is not None and not df_sheets.empty:
                guardar_datos_excel(df_sheets, trimestre_eval, archivo_excel)
                df_evaluaciones = df_sheets
    except Exception:
        df_evaluaciones = pd.DataFrame()
        if GOOGLE_SHEETS_DISPONIBLE:
            df_sheets = cargar_datos_desde_sheets(trimestre_eval)
            if df_sheets is not None and not df_sheets.empty:
                df_evaluaciones = df_sheets
        
        if curso_eval != "Todos":
            df_evaluaciones = df_evaluaciones[df_evaluaciones["Curso"] == curso_eval]
        
        if not df_evaluaciones.empty:
            # Resumen de evaluaciones cargadas
            total_alumnos_eval = len(df_evaluaciones[df_evaluaciones["Apellido y Nombre"].notna()])
            total_evals = 0
            for _, row in df_evaluaciones.iterrows():
                for j in range(1, 7):
                    if pd.notna(row.get(f"Eval {j}")) and pd.notna(row.get(f"Calif {j}")):
                        total_evals += 1

            col_i1, col_i2, col_i3 = st.columns(3)
            with col_i1:
                st.metric("👥 Alumnos cargados", total_alumnos_eval)
            with col_i2:
                st.metric("📝 Evaluaciones totales", total_evals)
            with col_i3:
                st.metric("📅 Trimestre activo", trimestre_eval)
            st.markdown("---")
            
            st.write("📝 **Evaluaciones** - Formato consistente (nombre arriba, nombre abajo)")
            
            if 'evaluaciones_cambios' not in st.session_state:
                st.session_state.evaluaciones_cambios = {}
            
            for idx, row in df_evaluaciones.iterrows():
                if pd.notna(row["Apellido y Nombre"]):
                    st.write(f"### **{row['Apellido y Nombre']}** - 📂 {row['Curso']}")
                    
                    # Encabezado visual
                    col_h1, col_h2, col_h3, col_h4, col_h5 = st.columns([1, 3, 2, 2, 1])
                    with col_h1:
                        st.caption("Nro.")
                    with col_h2:
                        st.caption("Nombre de la evaluación")
                    with col_h3:
                        st.caption("Calificación")
                    with col_h4:
                        st.caption(f"📅 {fecha_evaluacion.strftime('%d/%m/%Y')}")
                    with col_h5:
                        st.caption("Estado")
                    
                    for j in range(1, 7):
                        eval_col = f"Eval {j}"
                        calif_col = f"Calif {j}"
                        
                        if eval_col in df_evaluaciones.columns and calif_col in df_evaluaciones.columns:
                            col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2, 1])

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
                                st.caption(f"📅 {fecha_evaluacion.strftime('%d/%m/%Y')}")

                            with col5:
                                iconos_calif = {"EX": "🌟", "MB": "✅", "B": "🔵", "R+": "⚠️", "R-": "🔴", "M": "💔"}
                                st.markdown(f"### {iconos_calif.get(calificacion, '❓')}")

                            st.session_state.evaluaciones_cambios[f"{idx}_{j}"] = {
                                "nombre": nombre_eval_actual,
                                "calificacion": calificacion,
                                "fecha": fecha_evaluacion.strftime("%d/%m/%Y")
                            }
                    
                    st.markdown("---")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("💾 Guardar Evaluaciones", type="primary", key="guardar_todos_evaluaciones"):
                    with st.spinner("Guardando evaluaciones..."):
                        try:
                            cambios_guardados = 0
                            for key, cambios in st.session_state.evaluaciones_cambios.items():
                                partes = key.split("_")
                                idx = int(partes[0])
                                j = int(partes[1])

                                eval_col = f"Eval {j}"
                                calif_col = f"Calif {j}"

                                df_evaluaciones.at[idx, eval_col] = cambios["nombre"]
                                df_evaluaciones.at[idx, calif_col] = cambios["calificacion"]
                                cambios_guardados += 1

                            # Recalcular nota final
                            for idx, row in df_evaluaciones.iterrows():
                                if pd.notna(row.get("Apellido y Nombre")):
                                    califs = []
                                    for i in range(1, 7):
                                        v = df_evaluaciones.at[idx, f"Calif {i}"]
                                        if pd.notna(v):
                                            califs.append(calificacion_a_numero(v))
                                    if califs:
                                        promedio_final = sum(califs) / len(califs)
                                        df_evaluaciones.at[idx, "Nota Final Evaluaciones"] = round(promedio_final, 1)

                            # Guardar Excel local
                            if guardar_datos_excel(df_evaluaciones, trimestre_eval, archivo_excel):
                                st.success(f"✅ {cambios_guardados} evaluaciones guardadas correctamente!")
                                st.session_state.evaluaciones_cambios = {}
                            else:
                                st.error("❌ Error guardando Excel local")
                                st.stop()

                            # Sincronizar con Google Sheets
                            with st.spinner("Sincronizando con Google Sheets..."):
                                ok, mensaje = sincronizar_google_sheets()
                                if ok:
                                    st.success("✅ Google Sheets actualizado!")
                                else:
                                    st.warning(f"⚠️ Excel guardado pero Sheets falló: {mensaje}")

                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error inesperado: {e}")
            with col2:
                if st.button("🔄 Recargar Datos", type="secondary", key="recargar_evaluaciones"):
                    st.session_state.evaluaciones_cambios = {}
                    st.rerun()
            with col3:
                calificaciones_contadas = {"M": 0, "R-": 0, "R+": 0, "B": 0, "MB": 0, "EX": 0}
                total_evaluaciones = 0
                
                for _, row in df_evaluaciones.iterrows():
                    if pd.notna(row["Apellido y Nombre"]):
                        for i in range(1, 7):
                            calif = df_evaluaciones.at[row.name, f"Calif {i}"]
                            if pd.notna(calif):
                                calificaciones_contadas[calif] += 1
                                total_evaluaciones += 1
                
                if total_evaluaciones > 0:
                    st.write("#### 📈 Distribución de Calificaciones")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write("📈 **Distribución calificaciones:**")
                        for calif, cantidad in calificaciones_contadas.items():
                            st.write(f"- {calif}: {cantidad}")
                    with col2:
                        st.write(f"📊 **Total evaluaciones:** {total_evaluaciones}")
                    with col3:
                        st.write(f"📈 **Promedio general:** {total_evaluaciones/6:.1f}")
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("📊 Agrega datos simulados para probar")

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
        if st.button("➕ Agregar Alumno", type="primary", key="btn_agregar_alumno_def"):
            if nuevo_nombre and nuevo_curso:
                if agregar_nuevo_alumno(nuevo_nombre, nuevo_curso):
                    st.success(f"✅ '{nuevo_nombre}' agregado a {nuevo_curso}")
                    st.rerun()
                else:
                    st.error("❌ Error agregando alumno")
            else:
                st.error("❌ Completá todos los campos")
    with col2:
        st.write("")
    with col3:
        st.write("")
    
    st.markdown("---")
    st.write("📋 **Alumnos Actuales:**")
    try:
        df_alumnos = pd.read_excel(archivo_excel, sheet_name="1 Trimestre")
        if not df_alumnos.empty:
            for idx, row in df_alumnos.iterrows():
                if pd.notna(row["Apellido y Nombre"]):
                    st.write(f"👤 {row['Apellido y Nombre']} - 📂 {row['Curso']}")
    except Exception as e:
        st.error(f"Error: {e}")

elif st.session_state.accion_actual == "estadistica":
    st.header("📈 Análisis Estadístico Individual")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        curso_stats = st.selectbox(
            "📂 Curso:",
            ["Todos", "EF 1A", "EF 2A", "EF 1B", "EF 2B", "TD 2A", "TD 2B"],
            key="stats_curso"
        )
    with col2:
        trimestre_stats = st.selectbox(
            "📅 Trimestre:",
            ["1 Trimestre", "2 Trimestre", "3 Trimestre"],
            key="stats_trimestre"
        )
    with col3:
        alumnos_disponibles = obtener_alumnos_disponibles()
        alumno_stats = st.selectbox(
            "👤 Alumno:",
            alumnos_disponibles,
            key="stats_alumno"
        )

    st.markdown("---")

    try:
        # Intentar leer desde Excel local
        df_stats = pd.read_excel(archivo_excel, sheet_name=trimestre_stats)
        # Si está vacío, intentar desde Sheets
        if df_stats.empty and GOOGLE_SHEETS_DISPONIBLE:
            df_sheets = cargar_datos_desde_sheets(trimestre_stats)
            if df_sheets is not None and not df_sheets.empty:
                guardar_datos_excel(df_sheets, trimestre_stats, archivo_excel)
                df_stats = df_sheets

        if curso_stats != "Todos":
            df_stats = df_stats[df_stats["Curso"] == curso_stats]
        if alumno_stats != "Todos":
            df_stats = df_stats[df_stats["Apellido y Nombre"] == alumno_stats]

        if not df_stats.empty:
            for idx, row in df_stats.iterrows():
                if pd.notna(row.get("Apellido y Nombre")):

                    # Encabezado del alumno
                    st.markdown(f"""
                    <div style='background:linear-gradient(135deg,#1e3a5f,#2d6a9f);
                    padding:16px 20px;border-radius:12px;margin-bottom:16px;'>
                        <div style='font-size:20px;font-weight:700;color:white;'>
                            👤 {row['Apellido y Nombre']}
                        </div>
                        <div style='color:#a8c8e8;font-size:14px;margin-top:4px;'>
                            📂 {row['Curso']} &nbsp;|&nbsp; 📅 {trimestre_stats}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # ── ASISTENCIA ──────────────────────────
                    st.markdown('<div class="seccion-titulo">📋 ASISTENCIA</div>', unsafe_allow_html=True)

                    columnas_asistencia = [
                        col for col in df_stats.columns
                        if any(mes in str(col) for mes in ["Mar-", "Abr-", "May-"])
                    ]
                    presentes = sum(
                        1 for col in columnas_asistencia
                        if pd.notna(row.get(col)) and row.get(col) == "Presente"
                    )
                    totales = sum(
                        1 for col in columnas_asistencia
                        if pd.notna(row.get(col))
                    )
                    ausentes = totales - presentes
                    porcentaje = round((presentes / totales * 100), 1) if totales > 0 else 0
                    nota_asistencia = calcular_nota_asistencia(presentes, totales)

                    # Badge de calificación asistencia
                    if nota_asistencia == 10:
                        badge_asist = '<span class="badge-ex">EX — 10</span>'
                        color_asist = "#1a7a4a"
                    elif nota_asistencia == 8:
                        badge_asist = '<span class="badge-b">B — 8</span>'
                        color_asist = "#4a90d9"
                    else:
                        badge_asist = '<span class="badge-m">M — 5</span>'
                        color_asist = "#c0392b"

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.markdown(f"""<div class="stat-card">
                            <div class="stat-title">Días Presentes</div>
                            <div class="stat-value">{presentes}</div>
                            <div class="stat-sub">de {totales} clases</div>
                        </div>""", unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"""<div class="stat-card">
                            <div class="stat-title">Días Ausentes</div>
                            <div class="stat-value">{ausentes}</div>
                            <div class="stat-sub">faltas registradas</div>
                        </div>""", unsafe_allow_html=True)
                    with col3:
                        st.markdown(f"""<div class="stat-card">
                            <div class="stat-title">% Asistencia</div>
                            <div class="stat-value">{porcentaje}%</div>
                            <div class="stat-sub">{"✅ Regular" if porcentaje >= 80 else "⚠️ Irregular"}</div>
                        </div>""", unsafe_allow_html=True)
                    with col4:
                        st.markdown(f"""<div class="stat-card">
                            <div class="stat-title">Calif. Asistencia</div>
                            <div class="stat-value">{nota_asistencia}</div>
                            <div class="stat-sub">{badge_asist}</div>
                        </div>""", unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)

                    # ── EVALUACIONES ────────────────────────
                    st.markdown('<div class="seccion-titulo">📝 EVALUACIONES</div>', unsafe_allow_html=True)

                    evaluaciones_detalle = []
                    calificaciones = []

                    for i in range(1, 7):
                        eval_col = f"Eval {i}"
                        calif_col = f"Calif {i}"
                        if pd.notna(row.get(eval_col)) and pd.notna(row.get(calif_col)):
                            calif_val = str(row.get(calif_col))
                            calif_num = calificacion_a_numero(calif_val)
                            evaluaciones_detalle.append({
                                "N°": i,
                                "Evaluación": str(row.get(eval_col)),
                                "Calificación": calif_val,
                                "Valor": calif_num
                            })
                            calificaciones.append(calif_num)

                    if evaluaciones_detalle:
                        # Tabla estilizada
                        for ev in evaluaciones_detalle:
                            calif = ev["Calificación"]
                            badges = {
                                "EX": "badge-ex", "MB": "badge-mb",
                                "B": "badge-b", "R+": "badge-rp",
                                "R-": "badge-rm", "M": "badge-m"
                            }
                            badge_class = badges.get(calif, "badge-b")
                            col1, col2, col3 = st.columns([1, 5, 2])
                            with col1:
                                st.markdown(
                                    f"<div style='padding:8px;text-align:center;"
                                    f"font-weight:700;color:#1e3a5f;'>#{ev['N°']}</div>",
                                    unsafe_allow_html=True
                                )
                            with col2:
                                st.markdown(
                                    f"<div style='padding:8px;color:#2c3e50;"
                                    f"font-size:15px;'>{ev['Evaluación']}</div>",
                                    unsafe_allow_html=True
                                )
                            with col3:
                                st.markdown(
                                    f"<div style='padding:8px;text-align:center;'>"
                                    f"<span class='{badge_class}'>"
                                    f"{calif} — {ev['Valor']}</span></div>",
                                    unsafe_allow_html=True
                                )

                        st.markdown("<br>", unsafe_allow_html=True)

                        promedio_eval = sum(calificaciones) / len(calificaciones)
                        max_cal = max(calificaciones)
                        min_cal = min(calificaciones)

                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown(f"""<div class="stat-card">
                                <div class="stat-title">Promedio Evaluaciones</div>
                                <div class="stat-value">{promedio_eval:.1f}</div>
                                <div class="stat-sub">sobre 10 puntos</div>
                            </div>""", unsafe_allow_html=True)
                        with col2:
                            st.markdown(f"""<div class="stat-card">
                                <div class="stat-title">Calificación Más Alta</div>
                                <div class="stat-value">{max_cal}</div>
                                <div class="stat-sub">mejor resultado</div>
                            </div>""", unsafe_allow_html=True)
                        with col3:
                            st.markdown(f"""<div class="stat-card">
                                <div class="stat-title">Calificación Más Baja</div>
                                <div class="stat-value">{min_cal}</div>
                                <div class="stat-sub">resultado a mejorar</div>
                            </div>""", unsafe_allow_html=True)

                        st.markdown("<br>", unsafe_allow_html=True)

                        # ── RESUMEN GENERAL ──────────────────
                        st.markdown('<div class="seccion-titulo">🏆 RESUMEN GENERAL</div>', unsafe_allow_html=True)

                        promedio_general = (nota_asistencia + promedio_eval) / 2

                        if promedio_general >= 9:
                            color_gral = "#1a7a4a"
                            texto_gral = "Rendimiento Excelente"
                        elif promedio_general >= 8:
                            color_gral = "#2d6a9f"
                            texto_gral = "Muy Buen Rendimiento"
                        elif promedio_general >= 7:
                            color_gral = "#4a90d9"
                            texto_gral = "Buen Rendimiento"
                        elif promedio_general >= 6:
                            color_gral = "#e8a020"
                            texto_gral = "Rendimiento Regular"
                        else:
                            color_gral = "#c0392b"
                            texto_gral = "Necesita Mejorar"

                        st.markdown(f"""
                        <div style='background:linear-gradient(135deg,{color_gral},{color_gral}cc);
                        padding:20px;border-radius:12px;text-align:center;margin:10px 0;'>
                            <div style='font-size:36px;font-weight:800;color:white;'>
                                {promedio_general:.1f}
                            </div>
                            <div style='font-size:16px;color:rgba(255,255,255,0.9);
                            font-weight:600;margin-top:4px;'>
                                {texto_gral}
                            </div>
                            <div style='font-size:12px;color:rgba(255,255,255,0.7);
                            margin-top:6px;'>
                                Asistencia {nota_asistencia} + 
                                Evaluaciones {promedio_eval:.1f} ÷ 2
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    break
        else:
            st.info("📋 No hay datos para analizar. Seleccioná un alumno.")
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("📊 Primero agregá datos simulados desde el Dashboard.")

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
        # Intentar leer desde Excel local
        df_reporte = pd.read_excel(archivo_excel, sheet_name=trimestre_reporte)
        # Si está vacío, intentar desde Sheets
        if df_reporte.empty and GOOGLE_SHEETS_DISPONIBLE:
            df_sheets = cargar_datos_desde_sheets(trimestre_reporte)
            if df_sheets is not None and not df_sheets.empty:
                guardar_datos_excel(df_sheets, trimestre_reporte, archivo_excel)
                df_reporte = df_sheets

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
                    
                    st.write("## 📋 Asistencia Detallada")
                    columnas_asistencia = [col for col in df_reporte.columns if any(mes in col for mes in ["Mar-", "Abr-", "May-"])]
                    asistencia_data = []
                    presentes = 0
                    ausentes = 0
                    
                    for col in columnas_asistencia:
                        if pd.notna(row[col]):
                            estado = row[col]
                            asistencia_data.append({
                                "Fecha": col,
                                "Estado": estado
                            })
                            if estado == "Presente":
                                presentes += 1
                            else:
                                ausentes += 1
                    
                    if asistencia_data:
                        df_asistencia = pd.DataFrame(asistencia_data)
                        st.dataframe(df_asistencia, use_container_width=True)
                        
                        total_dias = presentes + ausentes
                        porcentaje = (presentes / total_dias * 100) if total_dias > 0 else 0
                        nota_asistencia = calcular_nota_asistencia(presentes, total_dias)
                        
                        st.write(f"**📊 Resumen:** {presentes} presentes, {ausentes} ausentes ({porcentaje:.1f}%)")
                        st.write(f"**📊 Nota Asistencia:** {nota_asistencia}")
                    
                    st.markdown("---")
                    st.write("## 📝 Evaluaciones Detalladas")
                    evaluaciones_data = []
                    calificaciones = []
                    
                    for i in range(1, 7):
                        eval_col = f"Eval {i}"
                        calif_col = f"Calif {i}"
                        if pd.notna(row[eval_col]) and pd.notna(row[calif_col]):
                            calif_num = calificacion_a_numero(row[calif_col])
                            evaluaciones_data.append({
                                "Evaluación": row[eval_col],
                                "Calificación": row[calif_col],
                                "Valor Numérico": calif_num
                            })
                            calificaciones.append(calif_num)
                    
                    if evaluaciones_data:
                        df_evaluaciones = pd.DataFrame(evaluaciones_data)
                        st.dataframe(df_evaluaciones, use_container_width=True)
                        
                        if calificaciones:
                            promedio_eval_num = sum(calificaciones) / len(calificaciones)
                            max_calificacion = max(calificaciones)
                            min_calificacion = min(calificaciones)
                            
                            st.write(f"**📊 Promedio Evaluaciones:** {promedio_eval_num:.1f}")
                            st.write(f"**📊 Calificación Más Alta:** {max_calificacion}")
                            st.write(f"**📊 Calificación Más Baja:** {min_calificacion}")
                            
                            st.markdown("---")
                            st.write("#### 📈 Gráfico de Desempeño")
                            crear_grafico_evaluaciones(evaluaciones_data, row["Apellido y Nombre"])
                    
                    st.markdown("---")
                    st.write("## 📈 Resumen General del Alumno")
                    nota_asistencia_num = calcular_nota_asistencia(presentes, total_dias)
                    promedio_eval_num = sum(calificaciones) / len(calificaciones) if calificaciones else 0
                    promedio_general_num = (nota_asistencia_num + promedio_eval_num) / 2 if calificaciones else nota_asistencia_num
                    
                    st.write(f"**📊 Nota Final Asistencia:** {nota_asistencia_num}")
                    st.write(f"**📊 Promedio Final Evaluaciones:** {promedio_eval_num}")
                    st.write(f"**📈 Promedio General Final:** {promedio_general_num:.1f}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("📊 Nota Final Asistencia", nota_asistencia_num)
                    with col2:
                        st.metric("📈 Promedio Final Evaluaciones", promedio_eval_num)
                    
                    st.markdown("---")
                    st.metric("📈 Promedio General Final", promedio_general_num)
                    
                    break
        else:
            st.info("📋 No hay datos para mostrar")
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("📊 Agrega datos simulados para probar")
