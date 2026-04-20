import pandas as pd
import sys
import os

# Agregar el directorio actual al path para importar desde app.py
sys.path.append('.')

from app import guardar_datos_excel

def cargar_alumnos_faltantes():
    """Carga masivamente todos los alumnos faltantes al 1 Trimestre"""
    archivo_excel = "sistema_educativo.xlsx"
    
    # Lista completa de alumnos faltantes
    alumnos_faltantes = {
        "EF 2A": [
            "BALAICHES, IARA CAROLINA",
            "BIALI, DELFINA ANNELICE", 
            "BURG, IARA ABRIL",
            "CHESANI, ANGELES AGOSTINA",
            "CLOS, MARÍA MARTA",
            "COMBY, LEONELA GUADALUPE",
            "DA LUZ, PIERINA GERALDINE",
            "GOMEZ DE OLIVERA, ZOE LUISANA",
            "GONZALEZ, VALENTINA MAITÉ",
            "KOCUR, MARTINA",
            "LEITES, SOFIA",
            "LOPEZ, EMILSE GUADALUPE",
            "MACIEL DE AVILA, ANGELES CAROLINA",
            "MEZA, AINHARA",
            "MOTTO GROSS, ANNA CATALINA",
            "ORTIZ, ANA BELEN",
            "PITTANA, KYARA MAGALÍ",
            "RADKE, PAULA",
            "RIVERO ABITBOL, DANNA",
            "ROJAS QUEDNAU, PAZ CAMILA",
            "ROSLER, GRETA SABRINA",
            "TAVARES, GUILLERMINA",
            "WDOVIN SUAREZ, FIORELA ABIGAIL"
        ],
        "EF 1B": [
            "ANDERSEN, MARIA DELFINA",
            "ASUNCION, PRISCILA",
            "BECKER MARQUEZ, AYLIN ANABEL",
            "CERVO, AMBAR MYLENA",
            "CHAMPE, NAIARA SALOMÉ",
            "CORREA DUTRA, FRANCESCA MAYLÉN",
            "DE SOSA, LUCIA NAHIARA",
            "ESPINOLA, MARTINA ANTONELLA",
            "GOMEZ, LUCIANA VALENTINA",
            "GONZALEZ RUSAK, MARIA GUADALUPE",
            "HEIN ZURAKOSKI, MAGALÍ",
            "KRUJOSKI, LUANA CANDELA",
            "MARCONETTI, IRINA",
            "MARKWART, KEREN",
            "MARKWART, KIARA",
            "MARAÑUK, ADABEL CHARLOTTE",
            "MEZA, CANDELA MAGALÍ",
            "PRAT KRICUN, MARIA JULIETA",
            "RADKE ESPINDOLA, SOL VICTORIA",
            "RITTER, SOPHIA VALENTIA",
            "RIVERO, ALMA VALENTINA",
            "ROTA, KYARA MAGALI",
            "SCHMIDT, NATALY BELEN",
            "TERECZUR, ZOE MARTINA",
            "UJEIKA, JAZMIN ALDANA",
            "ZOMBON, JIMENA",
            "MONTERO",
            "MIKITIUK",
            "ZUBIANI",
            "SILVO",
            "BLANCO",
            "AGUILAR, ALANIS MAGALÍ"
        ],
        "EF 2B": [
            "AGUILAR, ALANIS MAGALÍ",
            "ANTONELLI AMIL, SOFIA EUGENIA",
            "BLANCO, CONSTANZA",
            "BRITEZ, AMPARO VICTORIA",
            "EPSTEIN, GUILLERMINA",
            "GARCIA, VALENTINA SOLEDAD",
            "GREGORCHUK, SIOMARA DOMINIC",
            "HAYDAZ BOIDI, CAROLINA FERNANDA",
            "LANGE, YASMINA NAARA",
            "KOCZUK, AGUSTINA MADELEINE",
            "MARKOVIC, MARIA AGUSTINA",
            "MAZZONI, RAFAELA",
            "MIRA, EMILIA",
            "SENA, RENATA AGUSTINA",
            "SILVA, NICOL ELIZABET",
            "STECKLER, DAIRA BELEN",
            "SUAREZ, ALICIA SELENE",
            "TREJO, MARIA EMILIA",
            "VALLEJOS KRIEGER, ALLEGRA",
            "WOLLENBERG, NAHIARA"
        ]
    }
    
    try:
        # Leer el DataFrame actual del 1 Trimestre
        df_1t = pd.read_excel(archivo_excel, sheet_name="1 Trimestre")
        
        # Obtener la estructura de columnas del DataFrame existente
        columnas_existentes = df_1t.columns.tolist()
        
        # Crear filas nuevas para cada alumno
        nuevas_filas = []
        alumnos_agregados = 0
        
        for curso, alumnos in alumnos_faltantes.items():
            for nombre_alumno in alumnos:
                # Verificar si el alumno ya existe
                alumno_existente = df_1t[
                    (df_1t["Apellido y Nombre"] == nombre_alumno) & 
                    (df_1t["Curso"] == curso)
                ]
                
                if alumno_existente.empty:
                    # Crear nueva fila con valores por defecto
                    nueva_fila = {}
                    for col in columnas_existentes:
                        if col == "Apellido y Nombre":
                            nueva_fila[col] = nombre_alumno
                        elif col == "Curso":
                            nueva_fila[col] = curso
                        elif col.startswith(("Mar-", "Abr-", "May-")):  # Días de asistencia del 1er trimestre
                            nueva_fila[col] = "Ausente"
                        elif col in ["Nota Asistencia", "Tipo Evaluación", "Eval 1", "Calif 1", "Eval 2", "Calif 2", 
                                  "Eval 3", "Calif 3", "Eval 4", "Calif 4", "Eval 5", "Calif 5", "Eval 6", "Calif 6", 
                                  "Nota Final Evaluaciones", "Observaciones"]:
                            nueva_fila[col] = ""  # Columnas de evaluación vacías
                        else:
                            nueva_fila[col] = None
                    
                    nuevas_filas.append(nueva_fila)
                    alumnos_agregados += 1
                    print(f"Agregando: {nombre_alumno} - {curso}")
        
        # Si hay nuevas filas, agregarlas al DataFrame
        if nuevas_filas:
            df_nuevas_filas = pd.DataFrame(nuevas_filas)
            df_1t_actualizado = pd.concat([df_1t, df_nuevas_filas], ignore_index=True)
            
            # Guardar el resultado
            if guardar_datos_excel(df_1t_actualizado, "1 Trimestre", archivo_excel):
                print(f"\n¡ÉXITO! Se agregaron {alumnos_agregados} alumnos al 1 Trimestre")
                print(f"Total de alumnos en 1 Trimestre: {len(df_1t_actualizado)}")
                
                # Mostrar resumen por curso
                print("\nResumen por curso:")
                for curso in ["EF 1A", "EF 2A", "EF 1B", "EF 2B", "TD 2A", "TD 2B"]:
                    count = len(df_1t_actualizado[df_1t_actualizado["Curso"] == curso])
                    print(f"  {curso}: {count} alumnos")
                
                return alumnos_agregados
            else:
                print("Error guardando el archivo")
                return 0
        else:
            print("No se agregaron alumnos nuevos (todos ya existían)")
            return 0
            
    except Exception as e:
        print(f"Error en la carga: {e}")
        return 0

if __name__ == "__main__":
    print("=== CARGA MASIVA DE ALUMNOS FALTANTES ===")
    resultado = cargar_alumnos_faltantes()
    print(f"\nProceso finalizado. Resultado: {resultado}")
