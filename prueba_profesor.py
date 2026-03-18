import pandas as pd
from datetime import datetime
from utils import DataManagement

def prueba_profesor_ef():
    dm = DataManagement()
    
    print("=== PRUEBA REAL - PROFESOR DE EDUCACION FISICA ===\n")
    
    # Simular 2 semanas de clases (2 días por semana)
    semanas_clase = [
        {"semana": 1, "dia": "Lunes", "fecha": "2024-03-04"},
        {"semana": 1, "dia": "Miércoles", "fecha": "2024-03-06"},
        {"semana": 2, "dia": "Lunes", "fecha": "2024-03-11"},
        {"semana": 2, "dia": "Miércoles", "fecha": "2024-03-13"}
    ]
    
    # Alumnos reales de EF 1A
    alumnos_ef1a = [
        "García López, María",
        "Rodríguez Pérez, Juan", 
        "Martínez Sánchez, Ana",
        "López Gómez, Carlos",
        "Fernández Torres, Laura"
    ]
    
    print("REGISTRO DE ASISTENCIA - EF 1A - 1 TRIMESTRE")
    print("=" * 50)
    
    # Registrar asistencia para cada día de clase
    for semana_info in semanas_clase:
        print(f"\n{semana_info['semana']}° Semana - {semana_info['dia']} {semana_info['fecha']}")
        print("-" * 40)
        
        for alumno in alumnos_ef1a:
            # Simular asistencia aleatoria (80% de asistencia general)
            import random
            presente = random.random() > 0.2  # 80% de probabilidad de estar presente
            
            print(f"  {alumno}: {'Presente' if presente else 'Ausente'}")
            
            # Si es el último día del mes, registrar evaluaciones
            if semana_info['semana'] == 2 and semana_info['dia'] == "Miércoles":
                if presente:  # Solo evaluar a los presentes
                    registrar_evaluacion_rapida(dm, alumno, "EF 1A", "1 Trimestre")
    
    print(f"\nESTADÍSTICAS FINALES:")
    mostrar_estadisticas_curso(dm, "EF 1A", "1 Trimestre")

def registrar_evaluacion_rapida(dm, nombre_alumno, curso, trimestre):
    """Registro rápido de evaluaciones para optimizar tiempo del profesor"""
    
    # Evaluaciones típicas de Educación Física
    evaluaciones_tipicas = {
        "Diagnóstico": [
            ("Test Resistencia", "B"),
            ("Fuerza Superior", "MB"),
            ("Flexibilidad", "R+")
        ],
        "Físico": [
            ("Velocidad 40m", "B"),
            ("Salto Vertical", "MB"),
            ("Abdominales 1min", "B")
        ],
        "Técnico": [
            ("Ejecución Fundamentos", "MB"),
            ("Juego Aplicado", "B"),
            ("Táctica Individual", "R+")
        ]
    }
    
    # Seleccionar tipo de evaluación aleatorio
    import random
    tipo_eval = random.choice(list(evaluaciones_tipicas.keys()))
    evaluaciones = evaluaciones_tipicas[tipo_eval]
    
    print(f"    Evaluación {tipo_eval}:")
    
    # Calcular asistencia (simulada como alta para este ejemplo)
    asistencia_dias = 8
    dias_presentes = 7
    porcentaje_asistencia = (dias_presentes / asistencia_dias * 100)
    asistencia_estado, nota_asistencia = dm.calculate_attendance_grade(porcentaje_asistencia)
    
    # Preparar datos del alumno
    student_data = {
        "Curso": curso,
        "Trimestre": trimestre,
        "Apellido y Nombre": nombre_alumno,
        "Asistencia": f"{dias_presentes}/{asistencia_dias}",
        "Nota Asistencia": f"{asistencia_estado} ({nota_asistencia})",
        "Evaluaciones": len(evaluaciones),
        "Tipo Evaluación": tipo_eval,
        "Fecha Registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Observaciones": f"Evaluación {tipo_eval} - {datetime.now().strftime('%d/%m/%Y')}",
        "Nota Final": 0
    }
    
    # Agregar evaluaciones
    calificaciones = []
    for i, (eval_nombre, calificacion) in enumerate(evaluaciones):
        student_data[f"Evaluación {i+1}"] = eval_nombre
        student_data[f"Calificación {i+1}"] = calificacion
        calificaciones.append(calificacion)
        print(f"      - {eval_nombre}: {calificacion}")
    
    # Calcular nota final
    nota_final = dm.calculate_final_grade(calificaciones)
    student_data["Nota Final"] = nota_final
    
    # Guardar
    dm.save_student_data(student_data)
    print(f"      Guardado - Nota Final: {nota_final:.2f}")

def mostrar_estadisticas_curso(dm, curso, trimestre):
    """Mostrar estadísticas del curso"""
    
    df = dm.get_filtered_data(curso=curso, trimestre=trimestre)
    
    if df.empty:
        print("   No hay datos registrados")
        return
    
    print(f"   Total alumnos evaluados: {len(df)}")
    
    if "Nota Final" in df.columns:
        promedio_curso = df["Nota Final"].mean()
        print(f"   Promedio general del curso: {promedio_curso:.2f}")
        
        # Mejor alumno
        mejor_alumno = df.loc[df["Nota Final"].idxmax()]
        print(f"   Mejor rendimiento: {mejor_alumno['Apellido y Nombre']} ({mejor_alumno['Nota Final']:.2f})")
    
    # Distribución de notas de asistencia
    if "Nota Asistencia" in df.columns:
        asistencia_counts = df["Nota Asistencia"].value_counts()
        print(f"   Distribución asistencia:")
        for estado, count in asistencia_counts.items():
            print(f"     {estado}: {count} alumnos")
    
    print(f"\n   Datos guardados en: {dm.excel_path}")

def crear_interfaz_optimizada():
    """Crear sugerencias para optimizar la interfaz del profesor"""
    
    sugerencias = """
SUGERENCIAS PARA OPTIMIZAR USO DEL PROFESOR:

1. REGISTRO RAPIDO DE ASISTENCIA:
   - Boton "Tomar Asistencia Hoy" que muestre lista de alumnos
   - Checkboxes para marcar presente/ausente
   - Guardado masivo con un solo click

2. EVALUACIONES RAPIDAS:
   - Plantillas predefinidas por tipo de evaluacion
   - Seleccion multiple de calificaciones
   - Autoguardado cada 30 segundos

3. VISTA PROFESOR:
   - Dashboard simplificado solo con sus cursos
   - Estadisticas en tiempo real
   - Alertas de alumnos con baja asistencia

4. OPTIMIZACION MOVIL:
   - Botones grandes y faciles de tocar
   - Formularios que se completen con un solo click
   - Modo offline que sincronice cuando haya internet

5. RECORDATORIOS:
   - Notificaciones los dias de clase
   - Recordatorio de registrar asistencia
   - Alertas de alumnos con problemas

¿Quieres que implemente estas mejoras ahora?
"""
    
    print(sugerencias)

if __name__ == "__main__":
    prueba_profesor_ef()
    crear_interfaz_optimizada()
