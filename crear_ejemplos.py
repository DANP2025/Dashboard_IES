import pandas as pd
from datetime import datetime
from utils import DataManagement

# Crear datos de ejemplo
def crear_datos_ejemplo():
    dm = DataManagement()
    
    # Alumnos de ejemplo
    alumnos_ejemplo = [
        {
            "nombre": "García López, María",
            "curso": "EF 1A",
            "trimestre": "1 Trimestre",
            "asistencia_dias": 20,
            "dias_presentes": 18,
            "tipo_evaluacion": "Diagnóstico",
            "evaluaciones": ["Test inicial", "Evaluación escrita", "Trabajo práctico", "Exposición oral", "Proyecto final", "Autoevaluación"],
            "calificaciones": ["B", "MB", "B", "R+", "MB", "Ex"],
            "observaciones": "Alumna aplicada, participa activamente en clase"
        },
        {
            "nombre": "Rodríguez Pérez, Juan",
            "curso": "EF 1A", 
            "trimestre": "1 Trimestre",
            "asistencia_dias": 20,
            "dias_presentes": 15,
            "tipo_evaluacion": "Físico",
            "evaluaciones": ["Test condición física", "Flexibilidad", "Resistencia", "Fuerza", "Velocidad", "Coordinación"],
            "calificaciones": ["R+", "R-", "B", "B", "R+", "MB"],
            "observaciones": "Buena condición física, necesita mejorar en flexibilidad"
        },
        {
            "nombre": "Martínez Sánchez, Ana",
            "curso": "EF 2A",
            "trimestre": "1 Trimestre", 
            "asistencia_dias": 20,
            "dias_presentes": 20,
            "tipo_evaluacion": "Técnico",
            "evaluaciones": ["Ejecución básica", "Técnica avanzada", "Precisión", "Táctica individual", "Trabajo en equipo", "Creatividad"],
            "calificaciones": ["Ex", "MB", "MB", "B", "Ex", "MB"],
            "observaciones": "Excelente técnica, liderazgo natural en el grupo"
        },
        {
            "nombre": "López Gómez, Carlos",
            "curso": "EF 2A",
            "trimestre": "2 Trimestre",
            "asistencia_dias": 22,
            "dias_presentes": 16,
            "tipo_evaluacion": "Desempeño global",
            "evaluaciones": ["Participación", "Compromiso", "Progresión", "Actitud", "Colaboración", "Responsabilidad"],
            "calificaciones": ["B", "B", "R+", "MB", "B", "B"],
            "observaciones": "Buena actitud, pero con irregularidad en asistencia"
        },
        {
            "nombre": "Fernández Torres, Laura",
            "curso": "EF 1B",
            "trimestre": "2 Trimestre",
            "asistencia_dias": 22,
            "dias_presentes": 22,
            "tipo_evaluacion": "Diagnóstico",
            "evaluaciones": ["Evaluación inicial", "Test práctico", "Trabajo grupal", "Presentación", "Informe escrito", "Defensa oral"],
            "calificaciones": ["MB", "Ex", "MB", "Ex", "MB", "Ex"],
            "observaciones": "Alumna destacada, excelente rendimiento en todas las áreas"
        },
        {
            "nombre": "Giménez Ruiz, Pedro",
            "curso": "EF 1B",
            "trimestre": "3 Trimestre",
            "asistencia_dias": 21,
            "dias_presentes": 8,
            "tipo_evaluacion": "Físico",
            "evaluaciones": ["Test resistencia", "Fuerza superior", "Velocidad", "Agilidad", "Equilibrio", "Potencia"],
            "calificaciones": ["M", "R-", "M", "R-", "M", "R-"],
            "observaciones": "Asistencia muy deficiente, dificulta el seguimiento académico"
        },
        {
            "nombre": "Sánchez Morales, Sofía",
            "curso": "EF 2B",
            "trimestre": "3 Trimestre",
            "asistencia_dias": 21,
            "dias_presentes": 19,
            "tipo_evaluacion": "Técnico",
            "evaluaciones": ["Fundamentos", "Técnica individual", "Juego colectivo", "Estrategia", "Adaptación", "Mejora continua"],
            "calificaciones": ["MB", "B", "MB", "B", "MB", "B"],
            "observaciones": "Buena evolución técnica, colaboradora en equipo"
        },
        {
            "nombre": "Díaz Herrera, Miguel",
            "curso": "TD 2A",
            "trimestre": "1 Trimestre",
            "asistencia_dias": 20,
            "dias_presentes": 17,
            "tipo_evaluacion": "Desempeño global",
            "evaluaciones": ["Iniciativa", "Creatividad", "Trabajo en equipo", "Liderazgo", "Resolución problemas", "Comunicación"],
            "calificaciones": ["B", "MB", "B", "B", "MB", "B"],
            "observaciones": "Buen desempeño general, destaca en creatividad"
        },
        {
            "nombre": "Romero Castro, Elena",
            "curso": "TD 2A",
            "trimestre": "2 Trimestre",
            "asistencia_dias": 22,
            "dias_presentes": 20,
            "tipo_evaluacion": "Diagnóstico",
            "evaluaciones": ["Análisis inicial", "Identificación problemas", "Propuestas solución", "Planificación", "Ejecución", "Evaluación final"],
            "calificaciones": ["Ex", "MB", "Ex", "MB", "Ex", "MB"],
            "observaciones": "Excelente capacidad analítica y de planificación"
        },
        {
            "nombre": "Vargas Mendoza, Diego",
            "curso": "TD 2B",
            "trimestre": "3 Trimestre",
            "asistencia_dias": 21,
            "dias_presentes": 12,
            "tipo_evaluacion": "Físico",
            "evaluaciones": ["Condición general", "Resistencia aeróbica", "Fuerza muscular", "Flexibilidad", "Velocidad", "Coordinación"],
            "calificaciones": ["R+", "B", "R+", "R-", "B", "R+"],
            "observaciones": "Necesita mejorar asistencia, buen potencial físico"
        }
    ]
    
    # Guardar cada alumno
    for alumno in alumnos_ejemplo:
        # Calcular porcentaje de asistencia
        porcentaje_asistencia = (alumno["dias_presentes"] / alumno["asistencia_dias"] * 100)
        asistencia_estado, nota_asistencia = dm.calculate_attendance_grade(porcentaje_asistencia)
        
        # Calcular nota final
        nota_final = dm.calculate_final_grade(alumno["calificaciones"])
        
        # Preparar datos
        student_data = {
            "Curso": alumno["curso"],
            "Trimestre": alumno["trimestre"],
            "Apellido y Nombre": alumno["nombre"],
            "Asistencia": f"{alumno['dias_presentes']}/{alumno['asistencia_dias']}",
            "Nota Asistencia": f"{asistencia_estado} ({nota_asistencia})",
            "Evaluaciones": len(alumno["evaluaciones"]),
            "Tipo Evaluación": alumno["tipo_evaluacion"],
            "Fecha Registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Observaciones": alumno["observaciones"],
            "Nota Final": nota_final
        }
        
        # Agregar evaluaciones y calificaciones
        for i, (eval_nombre, calificacion) in enumerate(zip(alumno["evaluaciones"], alumno["calificaciones"])):
            student_data[f"Evaluación {i+1}"] = eval_nombre
            student_data[f"Calificación {i+1}"] = calificacion
        
        # Rellenar campos vacíos si hay menos de 6 evaluaciones
        for i in range(len(alumno["evaluaciones"]), 6):
            student_data[f"Evaluación {i+1}"] = ""
            student_data[f"Calificación {i+1}"] = ""
        
        # Guardar
        dm.save_student_data(student_data)
        print(f"Guardado: {alumno['nombre']} - {alumno['curso']} - {alumno['trimestre']}")
    
    print(f"\nSe han creado {len(alumnos_ejemplo)} alumnos de ejemplo")
    print(f"Los datos estan guardados en: {dm.excel_path}")

if __name__ == "__main__":
    crear_datos_ejemplo()
