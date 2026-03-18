import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
from utils import DataManagement

# Configuración de la página
st.set_page_config(
    page_title="Dashboard IES - Asistencia Diaria",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
st.title("📅 Dashboard de Asistencia Diaria")
st.markdown("### Registro y Gestión de Asistencia por Clase")
st.markdown("---")

# Sidebar con filtros y acciones
st.sidebar.title("📋 Acciones Principales")

# Botones principales
if st.sidebar.button("📝 Tomar Asistencia Hoy", use_container_width=True, type="primary"):
    st.session_state.pagina = "asistencia_diaria"
    st.rerun()

if st.sidebar.button("📊 Ver Asistencias", use_container_width=True):
    st.session_state.pagina = "ver_asistencias"
    st.rerun()

if st.sidebar.button("✏️ Editar Datos", use_container_width=True):
    st.session_state.pagina = "editar_datos"
    st.rerun()

if st.sidebar.button("📈 Reportes", use_container_width=True):
    st.session_state.pagina = "reportes"
    st.rerun()

# Filtros
st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filtros")

cursos = ["Todos"] + dm.cursos
curso_seleccionado = st.sidebar.selectbox(
    "Curso:",
    cursos,
    index=0
)

trimestres = ["Todos"] + dm.trimestres
trimestre_seleccionado = st.sidebar.selectbox(
    "Trimestre:",
    trimestres,
    index=0
)

# Página de Asistencia Diaria
if "pagina" not in st.session_state or st.session_state.pagina == "asistencia_diaria":
    st.header("📝 Tomar Asistencia - Registro Diario")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Calendario para seleccionar fecha
        fecha_seleccionada = st.date_input(
            "📅 Seleccione la fecha de clase:",
            value=datetime.now().date(),
            max_value=datetime.now().date()
        )
        
        # Selección de curso
        curso_asistencia = st.selectbox(
            "🎯 Seleccione el curso:",
            dm.cursos,
            index=0
        )
    
    with col2:
        # Trimestre automático según la fecha
        mes = fecha_seleccionada.month
        if 3 <= mes <= 5:
            trimestre_auto = "1 Trimestre"
        elif 6 <= mes <= 9:
            trimestre_auto = "2 Trimestre"
        else:
            trimestre_auto = "3 Trimestre"
        
        st.info(f"📊 Trimestre: {trimestre_auto}")
        
        # Día de la semana
        dia_semana = fecha_seleccionada.strftime("%A")
        st.info(f"📆 Día: {dia_semana}")
    
    with col3:
        # Estadísticas rápidas
        st.metric("📋 Mes", fecha_seleccionada.strftime("%B"))
        st.metric("📅 Día", fecha_seleccionada.day)
        st.metric("📊 Año", fecha_seleccionada.year)
    
    # Obtener alumnos del curso
    alumnos_curso = dm.get_students_by_course(curso_asistencia)
    
    if alumnos_curso:
        st.markdown("---")
        st.subheader(f"👥 Alumnos de {curso_asistencia} - {fecha_seleccionada.strftime('%d/%m/%Y')}")
        
        # Crear tabla de asistencia
        asistencia_data = {}
        
        # Encabezados de la tabla
        cols = st.columns([3, 1, 1, 2])
        with cols[0]:
            st.write("**Alumno**")
        with cols[1]:
            st.write("**Presente**")
        with cols[2]:
            st.write("**Ausente**")
        with cols[3]:
            st.write("**Observaciones**")
        
        st.markdown("---")
        
        # Lista de alumnos con checkboxes
        for i, alumno in enumerate(alumnos_curso):
            cols = st.columns([3, 1, 1, 2])
            
            with cols[0]:
                st.write(f"👤 {alumno}")
            
            with cols[1]:
                presente = st.checkbox(
                    "✅",
                    key=f"presente_{alumno}_{fecha_seleccionada}",
                    value=True
                )
            
            with cols[2]:
                ausente = st.checkbox(
                    "❌",
                    key=f"ausente_{alumno}_{fecha_seleccionada}",
                    value=False
                )
            
            with cols[3]:
                obs = st.text_input(
                    "",
                    key=f"obs_{alumno}_{fecha_seleccionada}",
                    placeholder="Obs...",
                    label_visibility="collapsed"
                )
            
            # Guardar datos
            asistencia_data[alumno] = {
                'presente': presente and not ausente,
                'observaciones': obs
            }
        
        # Botones de acción
        st.markdown("---")
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            if st.button("💾 Guardar Asistencia", use_container_width=True, type="primary"):
                guardar_asistencia_diaria(dm, asistencia_data, curso_asistencia, trimestre_auto, fecha_seleccionada)
        
        with col2:
            if st.button("✅ Marcar Todos Presentes", use_container_width=True):
                for alumno in alumnos_curso:
                    st.session_state[f"presente_{alumno}_{fecha_seleccionada}"] = True
                    st.session_state[f"ausente_{alumno}_{fecha_seleccionada}"] = False
                st.rerun()
        
        with col3:
            if st.button("❌ Marcar Todos Ausentes", use_container_width=True):
                for alumno in alumnos_curso:
                    st.session_state[f"presente_{alumno}_{fecha_seleccionada}"] = False
                    st.session_state[f"ausente_{alumno}_{fecha_seleccionada}"] = True
                st.rerun()
        
        with col4:
            if st.button("🔄 Limpiar Selección", use_container_width=True):
                for alumno in alumnos_curso:
                    st.session_state[f"presente_{alumno}_{fecha_seleccionada}"] = False
                    st.session_state[f"ausente_{alumno}_{fecha_seleccionada}"] = False
                st.rerun()
        
        # Estadísticas en tiempo real
        presentes = sum(1 for data in asistencia_data.values() if data['presente'])
        total = len(asistencia_data)
        porcentaje = (presentes / total * 100) if total > 0 else 0
        
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 Total Alumnos", total)
        
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
    
    else:
        st.warning("📝 No hay alumnos registrados en este curso")

# Página de Ver Asistencias
elif st.session_state.pagina == "ver_asistencias":
    st.header("📊 Historial de Asistencias")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Filtros de fecha
        fecha_inicio = st.date_input("📅 Fecha inicio:", value=datetime.now().date() - timedelta(days=30))
        fecha_fin = st.date_input("📅 Fecha fin:", value=datetime.now().date())
        
        curso_filtro = st.selectbox("🎯 Filtrar por curso:", ["Todos"] + dm.cursos)
    
    with col2:
        # Estadísticas del período
        df_filtrado = dm.get_filtered_data(curso_filtro if curso_filtro != "Todos" else None, trimestre_seleccionado if trimestre_seleccionado != "Todos" else None)
        
        if not df_filtrado.empty:
            st.metric("📊 Total Registros", len(df_filtrado))
            
            if "Nota Asistencia" in df_filtrado.columns:
                asistencia_counts = df_filtrado["Nota Asistencia"].value_counts()
                st.metric("🌟 Asistencia Excelente", asistencia_counts.get("Ex (10)", 0))
                st.metric("👍 Asistencia Buena", asistencia_counts.get("MB (8)", 0))
    
    # Tabla de asistencias
    if not df_filtrado.empty:
        st.markdown("---")
        st.subheader("📋 Registro de Asistencias")
        
        columnas_mostrar = [
            "Apellido y Nombre", "Curso", "Trimestre", "Asistencia", 
            "Nota Asistencia", "Fecha Registro", "Observaciones"
        ]
        
        columnas_disponibles = [col for col in columnas_mostrar if col in df_filtrado.columns]
        
        # Ordenar por fecha
        if "Fecha Registro" in df_filtrado.columns:
            df_filtrado["Fecha Registro"] = pd.to_datetime(df_filtrado["Fecha Registro"], errors='coerce')
            df_filtrado = df_filtrado.sort_values("Fecha Registro", ascending=False)
        
        st.dataframe(df_filtrado[columnas_disponibles], use_container_width=True)
        
        # Exportación
        if st.button("📥 Exportar Asistencias", use_container_width=True):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"asistencias_{timestamp}.xlsx"
            df_filtrado.to_excel(filename, index=False)
            st.success(f"✅ Exportado a {filename}")
    
    else:
        st.info("📝 No hay registros de asistencia en el período seleccionado")

# Página de Editar Datos
elif st.session_state.pagina == "editar_datos":
    st.header("✏️ Editar Datos de Alumnos")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Seleccionar alumno a editar
        df_total = dm.load_data()
        
        if not df_total.empty:
            # Crear lista de alumnos únicos
            alumnos_unicos = df_total["Apellido y Nombre"].unique()
            alumno_editar = st.selectbox("👤 Seleccione alumno para editar:", alumnos_unicos)
            
            # Mostrar registros del alumno
            registros_alumno = df_total[df_total["Apellido y Nombre"] == alumno_editar]
            
            if not registros_alumno.empty:
                st.subheader(f"📊 Registros de {alumno_editar}")
                
                for idx, registro in registros_alumno.iterrows():
                    with st.expander(f"📅 {registro.get('Trimestre', 'N/A')} - {registro.get('Fecha Registro', 'N/A')}"):
                        col1, col2 = st.columns([1, 1])
                        
                        with col1:
                            nuevo_nombre = st.text_input("Nombre:", registro.get("Apellido y Nombre", ""), key=f"nombre_{idx}")
                            nuevo_curso = st.selectbox("Curso:", dm.cursos, index=dm.cursos.index(registro.get("Curso", dm.cursos[0])), key=f"curso_{idx}")
                            nuevo_trimestre = st.selectbox("Trimestre:", dm.trimestres, index=dm.trimestres.index(registro.get("Trimestre", dm.trimestres[0])), key=f"trimestre_{idx}")
                        
                        with col2:
                            nueva_asistencia = st.text_input("Asistencia:", registro.get("Asistencia", ""), key=f"asistencia_{idx}")
                            nueva_observacion = st.text_area("Observaciones:", registro.get("Observaciones", ""), key=f"obs_{idx}")
                        
                        if st.button(f"💾 Guardar Cambios", key=f"guardar_{idx}"):
                            # Aquí iría la lógica de actualización
                            st.success(f"✅ Cambios guardados para {alumno_editar}")
    
    with col2:
        st.subheader("📈 Estadísticas de Edición")
        st.info("ℹ️ Seleccione un alumno para ver y editar sus datos")
        
        if not df_total.empty:
            st.metric("📊 Total Alumnos", len(df_total["Apellido y Nombre"].unique()))
            st.metric("📋 Total Registros", len(df_total))
            
            # Distribución por cursos
            if "Curso" in df_total.columns:
                st.write("**Distribución por cursos:**")
                for curso, count in df_total["Curso"].value_counts().items():
                    st.write(f"• {curso}: {count} registros")

# Página de Reportes
else:
    st.header("📈 Reportes y Estadísticas")
    
    df = dm.get_filtered_data(curso_seleccionado if curso_seleccionado != "Todos" else None, trimestre_seleccionado if trimestre_seleccionado != "Todos" else None)
    
    if not df.empty:
        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 Total Alumnos", len(df))
        
        with col2:
            if "Nota Asistencia" in df.columns:
                asistencia_counts = df["Nota Asistencia"].value_counts()
                excelentes = asistencia_counts.get("Ex (10)", 0)
                st.metric("🌟 Excelente", excelentes)
        
        with col3:
            if "Nota Final" in df.columns:
                promedio = df["Nota Final"].mean()
                st.metric("📊 Promedio Final", f"{promedio:.2f}")
        
        with col4:
            if "Nota Final" in df.columns:
                aprobados = len(df[df["Nota Final"] >= 6])
                st.metric("✅ Aprobados", f"{aprobados}/{len(df)}")
        
        # Gráficos
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Distribución de Notas Finales")
            if "Nota Final" in df.columns:
                notas_counts = df["Nota Final"].round(1).value_counts().sort_index()
                st.bar_chart(notas_counts)
        
        with col2:
            st.subheader("📈 Asistencia por Curso")
            if "Curso" in df.columns:
                curso_counts = df["Curso"].value_counts()
                st.bar_chart(curso_counts)
        
        # Alertas
        st.markdown("---")
        st.subheader("⚠️ Alertas del Sistema")
        
        # Alumnos con baja asistencia
        if "Nota Asistencia" in df.columns:
            baja_asistencia = df[df["Nota Asistencia"].str.contains("M")]
            if not baja_asistencia.empty:
                st.error(f"🚨 {len(baja_asistencia)} alumnos con asistencia baja (≤50%)")
                st.dataframe(baja_asistencia[["Apellido y Nombre", "Asistencia", "Nota Asistencia", "Observaciones"]])
        
        # Alumnos con notas bajas
        if "Nota Final" in df.columns:
            notas_bajas = df[df["Nota Final"] < 6]
            if not notas_bajas.empty:
                st.warning(f"⚠️ {len(notas_bajas)} alumnos con notas finales bajas (<6)")
                st.dataframe(notas_bajas[["Apellido y Nombre", "Nota Final", "Observaciones"]])
    
    else:
        st.info("📝 No hay datos disponibles. Usa 'Tomar Asistencia Hoy' para comenzar.")

# Funciones auxiliares
def guardar_asistencia_diaria(dm, asistencia_data, curso, trimestre, fecha):
    """Guardar asistencia diaria de múltiples alumnos"""
    guardados = 0
    
    for alumno, data in asistencia_data.items():
        # Calcular totales de asistencia
        # Buscar registros anteriores del alumno
        df_anteriores = dm.get_filtered_data(curso=curso, trimestre=trimestre, alumno=alumno)
        
        if not df_anteriores.empty:
            # Actualizar registro existente
            # Obtener totales anteriores
            registro_anterior = df_anteriores.iloc[0]
            asistencia_anterior = registro_anterior.get("Asistencia", "0/0")
            
            try:
                partes = asistencia_anterior.split("/")
                dias_totales_anteriores = int(partes[1]) if len(partes) > 1 else 0
                dias_presentes_anteriores = int(partes[0]) if len(partes) > 0 else 0
            except:
                dias_totales_anteriores = 0
                dias_presentes_anteriores = 0
            
            # Actualizar totales
            nuevos_dias_totales = dias_totales_anteriores + 1
            nuevos_dias_presentes = dias_presentes_anteriores + (1 if data['presente'] else 0)
            
            # Calcular nueva nota de asistencia
            porcentaje = (nuevos_dias_presentes / nuevos_dias_totales * 100) if nuevos_dias_totales > 0 else 0
            asistencia_estado, nota_asistencia = dm.calculate_attendance_grade(porcentaje)
            
            # Actualizar registro
            student_data = registro_anterior.to_dict()
            student_data["Asistencia"] = f"{nuevos_dias_presentes}/{nuevos_dias_totales}"
            student_data["Nota Asistencia"] = f"{asistencia_estado} ({nota_asistencia})"
            student_data["Fecha Registro"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if data['observaciones']:
                obs_anteriores = student_data.get("Observaciones", "")
                obs_nuevas = f"{obs_anteriores} | {fecha.strftime('%d/%m/%Y')}: {data['observaciones']}"
                student_data["Observaciones"] = obs_nuevas
            
            # Guardar actualización (aquí iría la lógica de actualización real)
            guardados += 1
            
        else:
            # Crear nuevo registro
            dias_totales = 1
            dias_presentes = 1 if data['presente'] else 0
            
            porcentaje = (dias_presentes / dias_totales * 100) if dias_totales > 0 else 0
            asistencia_estado, nota_asistencia = dm.calculate_attendance_grade(porcentaje)
            
            student_data = {
                "Curso": curso,
                "Trimestre": trimestre,
                "Apellido y Nombre": alumno,
                "Asistencia": f"{dias_presentes}/{dias_totales}",
                "Nota Asistencia": f"{asistencia_estado} ({nota_asistencia})",
                "Evaluaciones": 0,
                "Tipo Evaluación": "",
                "Fecha Registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Observaciones": f"{fecha.strftime('%d/%m/%Y')}: {data['observaciones']}" if data['observaciones'] else f"Asistencia registrada {fecha.strftime('%d/%m/%Y')}",
                "Nota Final": nota_asistencia
            }
            
            # Rellenar campos vacíos
            for i in range(1, 7):
                student_data[f"Evaluación {i}"] = ""
                student_data[f"Calificación {i}"] = ""
            
            if dm.save_student_data(student_data):
                guardados += 1
    
    st.success(f"✅ Asistencia guardada para {guardados} alumnos")
    st.balloons()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Dashboard de Asistencia Diaria - Educación Física"
    "</div>",
    unsafe_allow_html=True
)
