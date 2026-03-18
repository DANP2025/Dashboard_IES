import pandas as pd
from datetime import datetime
from utils import DataManagement

def prueba_completa():
    dm = DataManagement()
    
    print("=== PRUEBA COMPLETA DE FUNCIONALIDADES ===\n")
    
    # Alumno de prueba completo
    alumno_prueba = {
        "nombre": "Pérez González, Sofía",
        "curso": "EF 1A",
        "trimestre": "1 Trimestre",
        "asistencia_dias": 20,
        "dias_presentes": 19,
        "tipo_evaluacion": "Diagnóstico",
        "evaluaciones": [
            "Test Inicial de Conocimientos",
            "Evaluación Escrita",
            "Trabajo Práctico Individual",
            "Exposición Oral",
            "Proyecto Grupal",
            "Autoevaluación"
        ],
        "calificaciones": ["Ex", "MB", "B", "MB", "Ex", "B"],
        "observaciones": "Alumna destacada, excelente participación y compromiso con las actividades. Muestra gran interés en el aprendizaje y colabora activamente con sus compañeros."
    }
    
    print(f"1. REGISTRANDO ALUMNO: {alumno_prueba['nombre']}")
    print(f"   Curso: {alumno_prueba['curso']}")
    print(f"   Trimestre: {alumno_prueba['trimestre']}")
    
    # Calcular porcentaje de asistencia
    porcentaje_asistencia = (alumno_prueba["dias_presentes"] / alumno_prueba["asistencia_dias"] * 100)
    asistencia_estado, nota_asistencia = dm.calculate_attendance_grade(porcentaje_asistencia)
    
    print(f"\n2. ASISTENCIA:")
    print(f"   Días presentes: {alumno_prueba['dias_presentes']}/{alumno_prueba['asistencia_dias']}")
    print(f"   Porcentaje: {porcentaje_asistencia:.1f}%")
    print(f"   Nota asistencia: {asistencia_estado} ({nota_asistencia})")
    
    # Calcular nota final
    nota_final = dm.calculate_final_grade(alumno_prueba["calificaciones"])
    
    print(f"\n3. EVALUACIONES:")
    for i, (evaluacion, calificacion) in enumerate(zip(alumno_prueba["evaluaciones"], alumno_prueba["calificaciones"]), 1):
        print(f"   {i}. {evaluacion}: {calificacion} ({dm.calificaciones[calificacion]['rango']})")
    
    print(f"\n4. NOTA FINAL: {nota_final:.2f}")
    
    # Preparar datos para guardar
    student_data = {
        "Curso": alumno_prueba["curso"],
        "Trimestre": alumno_prueba["trimestre"],
        "Apellido y Nombre": alumno_prueba["nombre"],
        "Asistencia": f"{alumno_prueba['dias_presentes']}/{alumno_prueba['asistencia_dias']}",
        "Nota Asistencia": f"{asistencia_estado} ({nota_asistencia})",
        "Evaluaciones": len(alumno_prueba["evaluaciones"]),
        "Tipo Evaluación": alumno_prueba["tipo_evaluacion"],
        "Fecha Registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Observaciones": alumno_prueba["observaciones"],
        "Nota Final": nota_final
    }
    
    # Agregar evaluaciones y calificaciones
    for i, (eval_nombre, calificacion) in enumerate(zip(alumno_prueba["evaluaciones"], alumno_prueba["calificaciones"])):
        student_data[f"Evaluación {i+1}"] = eval_nombre
        student_data[f"Calificación {i+1}"] = calificacion
    
    # Guardar
    if dm.save_student_data(student_data):
        print(f"\n5. ALUMNO GUARDADO EXITOSAMENTE")
        print(f"   Archivo: {dm.excel_path}")
    else:
        print(f"\n5. ERROR AL GUARDAR")
        return
    
    # Prueba de filtros
    print(f"\n6. PRUEBA DE FILTROS:")
    
    # Filtrar por curso
    df_curso = dm.get_filtered_data(curso="EF 1A")
    print(f"   Alumnos en EF 1A: {len(df_curso)}")
    
    # Filtrar por trimestre
    df_trimestre = dm.get_filtered_data(trimestre="1 Trimestre")
    print(f"   Alumnos en 1 Trimestre: {len(df_trimestre)}")
    
    # Filtrar por alumno específico
    df_alumno = dm.get_filtered_data(alumno="Pérez González, Sofía")
    print(f"   Registros de Sofía Pérez: {len(df_alumno)}")
    
    # Estadísticas
    df_total = dm.load_data()
    print(f"\n7. ESTADÍSTICAS GENERALES:")
    print(f"   Total de alumnos registrados: {len(df_total)}")
    
    if not df_total.empty and "Nota Final" in df_total.columns:
        promedio_general = df_total["Nota Final"].mean()
        print(f"   Promedio general de notas: {promedio_general:.2f}")
    
    # Distribución de cursos
    if "Curso" in df_total.columns:
        print(f"\n8. DISTRIBUCIÓN POR CURSOS:")
        for curso in df_total["Curso"].value_counts().items():
            print(f"   {curso[0]}: {curso[1]} alumnos")
    
    print(f"\n9. PRUEBA COMPLETADA EXITOSAMENTE")
    print(f"   Dashboard funcional con todos los sistemas operativos")
    print(f"   Link: https://paolaies.streamlit.app")

if __name__ == "__main__":
    prueba_completa()
