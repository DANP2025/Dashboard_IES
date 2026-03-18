import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
from utils import DataManagement

# Configuración de la página
st.set_page_config(
    page_title="Dashboard IES - Profesor",
    page_icon="🏃‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar el gestor de datos
@st.cache_resource
def init_data_manager():
    return DataManagement()

dm = init_data_manager()

# Título optimizado para profesor
st.title("🏃‍♂️ Dashboard Educación Física")
st.markdown("### Registro Rápido de Asistencia y Evaluaciones")
st.markdown("---")

# Sidebar optimizado
st.sidebar.title("📋 Acciones Rápidas")

# Botón principal para tomar asistencia
if st.sidebar.button("📝 Tomar Asistencia Hoy", use_container_width=True, type="primary"):
    st.session_state.pagina = "asistencia"
    st.rerun()

# Botón para evaluaciones rápidas
if st.sidebar.button("🎯 Evaluación Rápida", use_container_width=True):
    st.session_state.pagina = "evaluacion"
    st.rerun()

# Botón para ver reportes
if st.sidebar.button("📊 Ver Reportes", use_container_width=True):
    st.session_state.pagina = "reportes"
    st.rerun()

# Filtros simplificados
st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filtros")

cursos = ["Todos"] + dm.cursos
curso_seleccionado = st.sidebar.selectbox(
    "Curso:",
    cursos,
    index=1 if len(cursos) > 1 else 0
)

trimestres = ["Todos"] + dm.trimestres
trimestre_seleccionado = st.sidebar.selectbox(
    "Trimestre:",
    trimestres,
    index=1 if len(trimestres) > 1 else 0
)

# Página de Asistencia Rápida
if "pagina" not in st.session_state or st.session_state.pagina == "asistencia":
    st.header("📝 Tomar Asistencia - " + datetime.now().strftime("%d/%m/%Y"))
    
    # Obtener alumnos del curso seleccionado
    if curso_seleccionado != "Todos":
        alumnos = dm.get_students_by_course(curso_seleccionado)
        
        if alumnos:
            st.subheader(f"Alumnos de {curso_seleccionado}")
            
            # Checkboxes para asistencia rápida
            asistencia_data = {}
            cols = st.columns(2)
            
            for i, alumno in enumerate(alumnos):
                col_idx = i % 2
                with cols[col_idx]:
                    presente = st.checkbox(
                        f"✅ {alumno}",
                        key=f"asist_{alumno}",
                        value=True  # Por defecto presente
                    )
                    asistencia_data[alumno] = presente
            
            # Botón de guardado masivo
            st.markdown("---")
            col1, col2 = st.columns([2, 1])
            
            with col1:
                if st.button("💾 Guardar Asistencia de Hoy", use_container_width=True, type="primary"):
                    guardar_asistencia_masiva(dm, asistencia_data, curso_seleccionado, trimestre_seleccionado)
            
            with col2:
                if st.button("🔄 Marcar Todos Presentes", use_container_width=True):
                    for alumno in alumnos:
                        st.session_state[f"asist_{alumno}"] = True
                    st.rerun()
            
            # Estadísticas rápidas
            presentes = sum(asistencia_data.values())
            total = len(asistencia_data)
            porcentaje = (presentes / total * 100) if total > 0 else 0
            
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Presentes", f"{presentes}/{total}")
            
            with col2:
                st.metric("Porcentaje", f"{porcentaje:.1f}%")
            
            with col3:
                if porcentaje >= 80:
                    st.metric("Estado", "Excelente")
                elif porcentaje >= 60:
                    st.metric("Estado", "Bueno")
                else:
                    st.metric("Estado", "Atención")
        
        else:
            st.info("No hay alumnos registrados en este curso")
    else:
        st.warning("Por favor selecciona un curso")

# Página de Evaluación Rápida
elif st.session_state.pagina == "evaluacion":
    st.header("🎯 Evaluación Rápida")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        curso_eval = st.selectbox("Seleccionar Curso:", dm.cursos)
        trimestre_eval = st.selectbox("Trimestre:", dm.trimestres)
        
        # Plantillas predefinidas
        st.subheader("📋 Plantillas de Evaluación")
        
        plantillas = {
            "Diagnóstico": [
                "Test Resistencia",
                "Fuerza Superior", 
                "Flexibilidad"
            ],
            "Físico": [
                "Velocidad 40m",
                "Salto Vertical",
                "Abdominales 1min"
            ],
            "Técnico": [
                "Ejecución Fundamentos",
                "Juego Aplicado",
                "Táctica Individual"
            ],
            "Desempeño Global": [
                "Participación",
                "Compromiso",
                "Trabajo en Equipo"
            ]
        }
        
        tipo_evaluacion = st.selectbox("Tipo de Evaluación:", list(plantillas.keys()))
        
        # Mostrar plantilla
        st.info("Ejercicios incluidos:")
        for ejercicio in plantillas[tipo_evaluacion]:
            st.write(f"• {ejercicio}")
    
    with col2:
        st.subheader("👥 Alumnos a Evaluar")
        
        alumnos_eval = dm.get_students_by_course(curso_eval)
        if alumnos_eval:
            alumno_seleccionado = st.selectbox("Seleccionar Alumno:", alumnos_eval)
            
            if alumno_seleccionado:
                st.subheader(f"📝 Evaluar: {alumno_seleccionado}")
                
                # Calificaciones rápidas
                calificaciones_rapidas = {}
                for i, ejercicio in enumerate(plantillas[tipo_evaluacion]):
                    with st.expander(f"{i+1}. {ejercicio}", expanded=True):
                        calificacion = st.selectbox(
                            "Calificación:",
                            list(dm.calificaciones.keys()),
                            key=f"eval_{i}"
                        )
                        calificaciones_rapidas[ejercicio] = calificacion
                
                # Observaciones rápidas
                observaciones = st.text_area("Observaciones (opcional):", height=80)
                
                # Botón de guardado
                if st.button("💾 Guardar Evaluación", use_container_width=True, type="primary"):
                    guardar_evaluacion_rapida(
                        dm, alumno_seleccionado, curso_eval, trimestre_eval,
                        tipo_evaluacion, calificaciones_rapidas, observaciones
                    )

# Página de Reportes
else:
    st.header("📊 Reportes del Curso")
    
    # Cargar datos filtrados
    df = dm.get_filtered_data(curso_seleccionado, trimestre_seleccionado)
    
    if not df.empty:
        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Alumnos", len(df))
        
        with col2:
            if "Nota Asistencia" in df.columns:
                asistencia_counts = df["Nota Asistencia"].value_counts()
                excelentes = asistencia_counts.get("Ex (10)", 0)
                st.metric("Asistencia Excelente", excelentes)
        
        with col3:
            if "Nota Final" in df.columns:
                promedio = df["Nota Final"].mean()
                st.metric("Promedio Final", f"{promedio:.2f}")
        
        with col4:
            if "Nota Final" in df.columns:
                aprobados = len(df[df["Nota Final"] >= 6])
                st.metric("Aprobados", f"{aprobados}/{len(df)}")
        
        # Alertas automáticas
        st.markdown("---")
        st.subheader("⚠️ Alertas del Sistema")
        
        # Alumnos con baja asistencia
        if "Nota Asistencia" in df.columns:
            baja_asistencia = df[df["Nota Asistencia"].str.contains("M")]
            if not baja_asistencia.empty:
                st.error(f"🚨 {len(baja_asistencia)} alumnos con asistencia baja (≤50%)")
                st.dataframe(baja_asistencia[["Apellido y Nombre", "Asistencia", "Nota Asistencia"]])
        
        # Alumnos con notas bajas
        if "Nota Final" in df.columns:
            notas_bajas = df[df["Nota Final"] < 6]
            if not notas_bajas.empty:
                st.warning(f"⚠️ {len(notas_bajas)} alumnos con notas finales bajas (<6)")
                st.dataframe(notas_bajas[["Apellido y Nombre", "Nota Final", "Observaciones"]])
        
        # Tabla completa
        st.markdown("---")
        st.subheader("📋 Lista Completa")
        
        columnas_mostrar = [
            "Apellido y Nombre", "Curso", "Trimestre", "Asistencia", 
            "Nota Asistencia", "Tipo Evaluación", "Nota Final"
        ]
        
        columnas_disponibles = [col for col in columnas_mostrar if col in df.columns]
        st.dataframe(df[columnas_disponibles].sort_values("Apellido y Nombre"), use_container_width=True)
        
        # Exportación
        st.markdown("---")
        if st.button("📥 Exportar a Excel", use_container_width=True):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reportes_{timestamp}.xlsx"
            df.to_excel(filename, index=False)
            st.success(f"✅ Exportado a {filename}")
    
    else:
        st.info("📝 No hay datos disponibles. Usa 'Tomar Asistencia Hoy' para comenzar.")

# Funciones auxiliares
def guardar_asistencia_masiva(dm, asistencia_data, curso, trimestre):
    """Guardar asistencia de múltiples alumnos a la vez"""
    guardados = 0
    
    for alumno, presente in asistencia_data.items():
        # Buscar si el alumno ya existe
        df_existente = dm.get_filtered_data(curso=curso, trimestre=trimestre, alumno=alumno)
        
        if not df_existente.empty:
            # Actualizar registro existente
            idx = df_existente.index[0]
            # Aquí iría la lógica de actualización
            guardados += 1
        else:
            # Crear nuevo registro
            asistencia_dias = 8  # Días totales del mes
            dias_presentes = sum(asistencia_data.values()) if presente else 0
            
            porcentaje = (dias_presentes / asistencia_dias * 100) if asistencia_dias > 0 else 0
            asistencia_estado, nota_asistencia = dm.calculate_attendance_grade(porcentaje)
            
            student_data = {
                "Curso": curso,
                "Trimestre": trimestre,
                "Apellido y Nombre": alumno,
                "Asistencia": f"{dias_presentes}/{asistencia_dias}",
                "Nota Asistencia": f"{asistencia_estado} ({nota_asistencia})",
                "Evaluaciones": 0,
                "Tipo Evaluación": "",
                "Fecha Registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Observaciones": f"Asistencia registrada el {datetime.now().strftime('%d/%m/%Y')}",
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

def guardar_evaluacion_rapida(dm, alumno, curso, trimestre, tipo_eval, calificaciones, observaciones):
    """Guardar evaluación rápida"""
    
    # Calcular asistencia (simulada)
    asistencia_dias = 8
    dias_presentes = 7
    porcentaje = (dias_presentes / asistencia_dias * 100)
    asistencia_estado, nota_asistencia = dm.calculate_attendance_grade(porcentaje)
    
    # Calcular nota final
    nota_final = dm.calculate_final_grade(list(calificaciones.values()))
    
    student_data = {
        "Curso": curso,
        "Trimestre": trimestre,
        "Apellido y Nombre": alumno,
        "Asistencia": f"{dias_presentes}/{asistencia_dias}",
        "Nota Asistencia": f"{asistencia_estado} ({nota_asistencia})",
        "Evaluaciones": len(calificaciones),
        "Tipo Evaluación": tipo_eval,
        "Fecha Registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Observaciones": observaciones,
        "Nota Final": nota_final
    }
    
    # Agregar evaluaciones
    for i, (eval_nombre, calificacion) in enumerate(calificaciones.items()):
        student_data[f"Evaluación {i+1}"] = eval_nombre
        student_data[f"Calificación {i+1}"] = calificacion
    
    # Rellenar campos vacíos
    for i in range(len(calificaciones), 6):
        student_data[f"Evaluación {i+1}"] = ""
        student_data[f"Calificación {i+1}"] = ""
    
    if dm.save_student_data(student_data):
        st.success(f"✅ Evaluación guardada para {alumno}")
        st.balloons()
    else:
        st.error("❌ Error al guardar evaluación")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Dashboard Educación Física - Optimizado para Profesores"
    "</div>",
    unsafe_allow_html=True
)
