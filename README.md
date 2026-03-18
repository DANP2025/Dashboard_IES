# Dashboard de Gestión de Alumnos - IES

Este es un dashboard desarrollado en Streamlit para la gestión de alumnos, asistencias y evaluaciones.

## Instalación

1. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar la aplicación:
```bash
streamlit run app.py
```

## Funcionalidades

- Gestión de alumnos por curso (EF 1A, EF 2A, EF 2A, EF 1B, EF 2B, TD 2A, TD 2B)
- Control de asistencia por trimestre
- Sistema de evaluaciones con múltiples categorías
- Cálculo automático de promedios y notas finales
- Exportación de datos a Excel
- Interfaz optimizada para uso móvil

## Estructura de Trimestres

- **1 Trimestre**: Marzo - Mayo
- **2 Trimestre**: Junio - Septiembre  
- **3 Trimestre**: Octubre - Diciembre

## Sistema de Calificaciones

- **M**: Menos de 5
- **R-**: 5.5 - 6
- **R+**: 6
- **B**: 7
- **MB**: 8
- **Ex**: 9 - 10
