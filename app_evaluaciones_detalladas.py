import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
from utils import DataManagement

# Configuración de la página
st.set_page_config(
    page_title="Dashboard IES - Evaluaciones Detalladas",
    page_icon="📊",
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
st.title("📊 Dashboard de Evaluaciones Detalladas")
st.markdown("### Sistema de Calificaciones y Promedios")
st.markdown("---")

# Sidebar con filtros y acciones
st.sidebar.title("📋 Acciones y Filtros")

# Botones principales
if st.sidebar.button("📝 Tomar Asistencia", use_container_width=True):
    st.session_state.pagina = "asistencia"
    st.rerun()

if st.sidebar.button("🎯 Nueva Evaluación", use_container_width=True, type="primary"):
    st.session_state.pagina = "evaluacion"
    st.rerun()

if st.sidebar.button("📊 Ver Evaluaciones", use_container_width=True):
    st.session_state.pagina = "ver_evaluaciones"
    st.rerun()

if st.sidebar.button("✏️ Editar Alumno", use_container_width=True):
    st.session_state.pagina = "editar"
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

# Sistema de calificaciones
CALIFICACIONES = {
    "M": {"nombre": "Malo", "valor": 4, "color": "🔴", "descripcion": "Menos de 5"},
    "R-": {"nombre": "Regular-", "valor": 5.5, "color": "🟠", "descripcion": "5.5 - 6"},
    "R+": {"nombre": "Regular+", "valor": 6, "color": "🟡", "descripcion": "6"},
    "B": {"nombre": "Bueno", "valor": 7, "color": "🟢", "descripcion": "7"},
    "MB": {"nombre": "Muy Bueno", "valor": 8, "color": "🔵", "descripcion": "8"},
    "Ex": {"nombre": "Excelente", "valor": 9.5, "color": "🟣", "descripcion": "9 - 10"}
}

def calcular_promedio_calificaciones(calificaciones_lista):
    """Calcular promedio de calificaciones usando el sistema M, R-, R+, B, MB, Ex"""
    if not calificaciones_lista:
        return 0, "Sin evaluaciones"
    
    valores = []
    for cal in calificaciones_lista:
        if cal in CALIFICACIONES:
            valores.append(CALIFICACIONES[cal]["valor"])
    
    if not valores:
        return 0, "Sin calificaciones válidas"
    
    promedio = sum(valores) / len(valores)
    
    # Determinar la calificación correspondiente al promedio
    if promedio < 5:
        calificacion_final = "M"
    elif promedio < 6.5:
        calificacion_final = "R-"
    elif promedio < 6.5:
        calificacion_final = "R+"
    elif promedio < 7.5:
        calificacion_final = "B"
    elif promedio < 8.5:
        calificacion_final = "MB"
    else:
        calificacion_final = "Ex"
    
    return promedio, calificacion_final

# Página de Nueva Evaluación
if "pagina" not in st.session_state or st.session_state.pagina == "evaluacion":
    st.header("🎯 Registrar Nueva Evaluación")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Datos básicos
        nombre_alumno = st.text_input("👤 Nombre del Alumno:", placeholder="Ej: García López, María")
        curso_eval = st.selectbox("🎯 Curso:", dm.cursos)
        trimestre_eval = st.selectbox("📊 Trimestre:", dm.trimestres)
        tipo_evaluacion = st.selectbox("📝 Tipo de Evaluación:", dm.tipos_evaluacion)
        
        # Asistencia
        st.subheader("📋 Datos de Asistencia")
        asistencia_dias = st.number_input("Total días de clase:", min_value=1, max_value=100, value=20)
        dias_presentes = st.number_input("Días presentes:", min_value=0, max_value=asistencia_dias, value=18)
        
        porcentaje = (dias_presentes / asistencia_dias * 100) if asistencia_dias > 0 else 0
        st.info(f"📊 Porcentaje de asistencia: {porcentaje:.1f}%")
        
        asistencia_estado, nota_asistencia = dm.calculate_attendance_grade(porcentaje)
        st.success(f"✅ Nota de asistencia: {asistencia_estado} ({nota_asistencia})")
    
    with col2:
        # Evaluaciones
        st.subheader("📝 Evaluaciones Detalladas")
        
        evaluaciones = []
        calificaciones = []
        
        for i in range(1, 7):  # 6 evaluaciones como máximo
            with st.expander(f"Evaluación {i}", expanded=(i <= 3)):
                nombre_eval = st.text_input(
                    f"Nombre de la evaluación {i}:",
                    key=f"eval_{i}",
                    placeholder=f"Ej: Test de Resistencia"
                )
                
                calificacion = st.selectbox(
                    f"Calificación {i}:",
                    list(CALIFICACIONES.keys()),
                    key=f"cal_{i}",
                    format_func=lambda x: f"{CALIFICACIONES[x]['color']} {x} - {CALIFICACIONES[x]['nombre']} ({CALIFICACIONES[x]['valor']})"
                )
                
                if nombre_eval:
                    evaluaciones.append(nombre_eval)
                    calificaciones.append(calificacion)
        
        # Promedio en tiempo real
        if calificaciones:
            promedio, calif_final = calcular_promedio_calificaciones(calificaciones)
            st.markdown("---")
            st.subheader("📊 Promedio de Evaluaciones")
            st.metric("📈 Promedio Numérico", f"{promedio:.2f}")
            st.metric(f"{CALIFICACIONES[calif_final]['color']} Calificación Final", f"{calif_final} - {CALIFICACIONES[calif_final]['nombre']}")
    
    # Observaciones
    observaciones = st.text_area("📝 Observaciones:", height=100, placeholder="Observaciones sobre el desempeño del alumno...")
    
    # Botones de acción
    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("💾 Guardar Evaluación Completa", use_container_width=True, type="primary"):
            if nombre_alumno and curso_eval and trimestre_eval and evaluaciones:
                # Preparar datos
                student_data = {
                    "Curso": curso_eval,
                    "Trimestre": trimestre_eval,
                    "Apellido y Nombre": nombre_alumno,
                    "Asistencia": f"{dias_presentes}/{asistencia_dias}",
                    "Nota Asistencia": f"{asistencia_estado} ({nota_asistencia})",
                    "Evaluaciones": len(evaluaciones),
                    "Tipo Evaluación": tipo_evaluacion,
                    "Fecha Registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Observaciones": observaciones,
                    "Nota Final": promedio if calificaciones else nota_asistencia
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
                    st.success("✅ Evaluación guardada exitosamente!")
                    st.balloons()
                else:
                    st.error("❌ Error al guardar la evaluación")
            else:
                st.error("❌ Por favor complete todos los campos obligatorios")
    
    with col2:
        if st.button("🔄 Limpiar Formulario", use_container_width=True):
            st.rerun()

# Página de Ver Evaluaciones
elif st.session_state.pagina == "ver_evaluaciones":
    st.header("📊 Evaluaciones Registradas")
    
    # Cargar datos filtrados
    df = dm.get_filtered_data(curso_seleccionado if curso_seleccionado != "Todos" else None, 
                              trimestre_seleccionado if trimestre_seleccionado != "Todos" else None)
    
    if not df.empty:
        # Estadísticas generales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 Total Alumnos", len(df))
        
        with col2:
            if "Nota Final" in df.columns:
                promedio_general = df["Nota Final"].mean()
                st.metric("📈 Promedio General", f"{promedio_general:.2f}")
        
        with col3:
            if "Nota Asistencia" in df.columns:
                asistencia_counts = df["Nota Asistencia"].value_counts()
                excelentes = asistencia_counts.get("Ex (10)", 0)
                st.metric("🌟 Excelente Asistencia", excelentes)
        
        with col4:
            if "Evaluaciones" in df.columns:
                total_eval = df["Evaluaciones"].sum()
                st.metric("📝 Total Evaluaciones", int(total_eval))
        
        # Tabla detallada de evaluaciones
        st.markdown("---")
        st.subheader("📋 Detalle de Evaluaciones por Alumno")
        
        for idx, row in df.iterrows():
            with st.expander(f"👤 {row['Apellido y Nombre']} - {row['Curso']} - {row.get('Trimestre', 'N/A')}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**📅 Fecha Registro:** {row.get('Fecha Registro', 'N/A')}")
                    st.write(f"**🎯 Tipo Evaluación:** {row.get('Tipo Evaluación', 'N/A')}")
                    st.write(f"**📋 Asistencia:** {row.get('Asistencia', 'N/A')} - {row.get('Nota Asistencia', 'N/A')}")
                    
                    # Mostrar evaluaciones individuales
                    st.subheader("📝 Evaluaciones Individuales:")
                    evaluaciones_lista = []
                    calificaciones_lista = []
                    
                    for i in range(1, 7):
                        eval_nombre = row.get(f"Evaluación {i}", "")
                        calificacion = row.get(f"Calificación {i}", "")
                        
                        if eval_nombre and calificacion:
                            evaluaciones_lista.append(eval_nombre)
                            calificaciones_lista.append(calificacion)
                            
                            # Mostrar cada evaluación con su calificación
                            col_a, col_b = st.columns([3, 1])
                            with col_a:
                                st.write(f"• {eval_nombre}")
                            with col_b:
                                cal_info = CALIFICACIONES.get(calificacion, {})
                                st.write(f"{cal_info.get('color', '❓')} {calificacion}")
                                st.write(f"({cal_info.get('valor', 0)})")
                    
                    # Calcular y mostrar promedio
                    if calificaciones_lista:
                        promedio, calif_final = calcular_promedio_calificaciones(calificaciones_lista)
                        st.markdown("---")
                        st.subheader("📊 Promedio de Evaluaciones")
                        col_a, col_b = st.columns([1, 1])
                        with col_a:
                            st.metric("📈 Promedio Numérico", f"{promedio:.2f}")
                        with col_b:
                            cal_info = CALIFICACIONES.get(calif_final, {})
                            st.metric(f"{cal_info.get('color', '❓')} Calificación Final", 
                                    f"{calif_final} - {cal_info.get('nombre', 'N/A')}")
                
                with col2:
                    # Nota final del sistema
                    st.subheader("📈 Nota Final del Sistema")
                    nota_final = row.get("Nota Final", 0)
                    st.metric("🎯 Nota Final", f"{nota_final:.2f}")
                    
                    # Observaciones
                    if row.get("Observaciones"):
                        st.subheader("📝 Observaciones")
                        st.write(row["Observaciones"])
                    
                    # Botón de edición
                    if st.button(f"✏️ Editar {row['Apellido y Nombre']}", key=f"edit_{idx}"):
                        st.session_state.alumno_editar = row['Apellido y Nombre']
                        st.session_state.pagina = "editar"
                        st.rerun()
        
        # Resumen de calificaciones
        st.markdown("---")
        st.subheader("📊 Resumen de Calificaciones")
        
        # Contar todas las calificaciones
        todas_calificaciones = []
        for idx, row in df.iterrows():
            for i in range(1, 7):
                cal = row.get(f"Calificación {i}", "")
                if cal and cal in CALIFICACIONES:
                    todas_calificaciones.append(cal)
        
        if todas_calificaciones:
            # Contar por tipo
            conteo_califs = {}
            for cal in todas_calificaciones:
                conteo_califs[cal] = conteo_califs.get(cal, 0) + 1
            
            # Mostrar distribución
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.write("**Distribución de Calificaciones:**")
                for cal, count in sorted(conteo_califs.items()):
                    cal_info = CALIFICACIONES[cal]
                    st.write(f"{cal_info['color']} {cal} - {cal_info['nombre']}: {count} veces")
            
            with col2:
                # Gráfico de barras
                cal_counts_df = pd.DataFrame([
                    {"Calificación": cal, "Cantidad": count} 
                    for cal, count in conteo_califs.items()
                ])
                st.bar_chart(cal_counts_df.set_index("Calificación"))
        
        # Exportación
        st.markdown("---")
        if st.button("📥 Exportar Evaluaciones", use_container_width=True):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"evaluaciones_{timestamp}.xlsx"
            df.to_excel(filename, index=False)
            st.success(f"✅ Exportado a {filename}")
    
    else:
        st.info("📝 No hay evaluaciones registradas. Usa 'Nueva Evaluación' para comenzar.")

# Página de Editar Alumno
elif st.session_state.pagina == "editar":
    st.header("✏️ Editar Datos de Alumno")
    
    df_total = dm.load_data()
    
    if not df_total.empty:
        # Seleccionar alumno
        alumnos_unicos = df_total["Apellido y Nombre"].unique()
        alumno_seleccionado = st.selectbox(
            "👤 Seleccione alumno para editar:",
            alumnos_unicos,
            index=0 if "alumno_editar" not in st.session_state else 
                   list(alumnos_unicos).index(st.session_state.alumno_editar) if st.session_state.alumno_editar in alumnos_unicos else 0
        )
        
        # Mostrar registros del alumno
        registros_alumno = df_total[df_total["Apellido y Nombre"] == alumno_seleccionado]
        
        if not registros_alumno.empty:
            for idx, registro in registros_alumno.iterrows():
                with st.expander(f"📅 {registro.get('Trimestre', 'N/A')} - {registro.get('Fecha Registro', 'N/A')}", expanded=True):
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        # Datos editables
                        nuevo_nombre = st.text_input("👤 Nombre:", registro.get("Apellido y Nombre", ""), key=f"nombre_{idx}")
                        nuevo_curso = st.selectbox("🎯 Curso:", dm.cursos, 
                                                index=dm.cursos.index(registro.get("Curso", dm.cursos[0])), key=f"curso_{idx}")
                        nuevo_trimestre = st.selectbox("📊 Trimestre:", dm.trimestres,
                                                    index=dm.trimestres.index(registro.get("Trimestre", dm.trimestres[0])), key=f"trimestre_{idx}")
                        nuevo_tipo = st.selectbox("📝 Tipo Evaluación:", dm.tipos_evaluacion,
                                               index=dm.tipos_evaluacion.index(registro.get("Tipo Evaluación", dm.tipos_evaluacion[0])) if registro.get("Tipo Evaluación") in dm.tipos_evaluacion else 0, key=f"tipo_{idx}")
                    
                    with col2:
                        # Asistencia editable
                        asistencia_actual = registro.get("Asistencia", "0/0")
                        try:
                            partes = asistencia_actual.split("/")
                            dias_totales = int(partes[1]) if len(partes) > 1 else 20
                            dias_presentes = int(partes[0]) if len(partes) > 0 else 0
                        except:
                            dias_totales = 20
                            dias_presentes = 0
                        
                        nuevos_dias_totales = st.number_input("📅 Total días:", min_value=1, value=dias_totales, key=f"total_{idx}")
                        nuevos_dias_presentes = st.number_input("✅ Días presentes:", min_value=0, max_value=nuevos_dias_totales, value=dias_presentes, key=f"presentes_{idx}")
                        
                        porcentaje = (nuevos_dias_presentes / nuevos_dias_totales * 100) if nuevos_dias_totales > 0 else 0
                        st.info(f"📊 Porcentaje: {porcentaje:.1f}%")
                        
                        asistencia_estado, nota_asistencia = dm.calculate_attendance_grade(porcentaje)
                        st.success(f"✅ Nota: {asistencia_estado} ({nota_asistencia})")
                    
                    # Evaluaciones editables
                    st.subheader("📝 Evaluaciones:")
                    calificaciones_editadas = []
                    
                    for i in range(1, 7):
                        col_a, col_b = st.columns([2, 1])
                        
                        with col_a:
                            eval_nombre = st.text_input(
                                f"Evaluación {i}:",
                                registro.get(f"Evaluación {i}", ""),
                                key=f"eval_edit_{i}_{idx}"
                            )
                        
                        with col_b:
                            calificacion_actual = registro.get(f"Calificación {i}", "")
                            calificacion = st.selectbox(
                                f"Calif:",
                                list(CALIFICACIONES.keys()),
                                index=list(CALIFICACIONES.keys()).index(calificacion_actual) if calificacion_actual in CALIFICACIONES else 0,
                                key=f"cal_edit_{i}_{idx}",
                                format_func=lambda x: f"{CALIFICACIONES[x]['color']} {x}"
                            )
                            
                            if eval_nombre and calificacion:
                                calificaciones_editadas.append(calificacion)
                    
                    # Promedio actualizado
                    if calificaciones_editadas:
                        promedio, calif_final = calcular_promedio_calificaciones(calificaciones_editadas)
                        st.markdown("---")
                        col_a, col_b = st.columns([1, 1])
                        with col_a:
                            st.metric("📈 Promedio Evaluaciones", f"{promedio:.2f}")
                        with col_b:
                            st.metric(f"{CALIFICACIONES[calif_final]['color']} Calificación Final", f"{calif_final}")
                    
                    # Observaciones
                    nuevas_observaciones = st.text_area(
                        "📝 Observaciones:",
                        registro.get("Observaciones", ""),
                        key=f"obs_{idx}"
                    )
                    
                    # Botón de guardado
                    if st.button(f"💾 Guardar Cambios - {alumno_seleccionado}", key=f"guardar_{idx}"):
                        st.success(f"✅ Cambios guardados para {alumno_seleccionado}")
                        # Aquí iría la lógica de actualización real
    
    else:
        st.warning("📝 No hay alumnos registrados")

# Página de Asistencia (simplificada)
else:
    st.header("📝 Tomar Asistencia Rápida")
    
    curso_asistencia = st.selectbox("🎯 Seleccione curso:", dm.cursos)
    fecha_asistencia = st.date_input("📅 Fecha de clase:", value=datetime.now().date())
    
    alumnos_curso = dm.get_students_by_course(curso_asistencia)
    
    if alumnos_curso:
        st.subheader(f"👥 Asistencia - {curso_asistencia} - {fecha_asistencia.strftime('%d/%m/%Y')}")
        
        asistencia_data = {}
        for alumno in alumnos_curso:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"👤 {alumno}")
            with col2:
                presente = st.checkbox("✅", key=f"asist_{alumno}_{fecha_asistencia}")
                asistencia_data[alumno] = presente
        
        if st.button("💾 Guardar Asistencia", use_container_width=True):
            presentes = sum(asistencia_data.values())
            total = len(asistencia_data)
            st.success(f"✅ Asistencia guardada: {presentes}/{total} presentes")
    
    else:
        st.warning("📝 No hay alumnos en este curso")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Dashboard de Evaluaciones Detalladas - Educación Física"
    "</div>",
    unsafe_allow_html=True
)
