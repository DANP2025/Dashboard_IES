import subprocess
import webbrowser
import os

def subir_a_github():
    print("Preparando para subir a GitHub...")
    print("Sigue estos pasos:")
    print()
    
    print("1. Abre GitHub en tu navegador:")
    print("   https://github.com/new")
    print()
    
    print("2. Configura el repositorio:")
    print("   - Repository name: dashboard-ies")
    print("   - Description: Dashboard de Gestion de Alumnos - IES")
    print("   - Public/Private (como prefieras)")
    print("   - NO marques 'Add README'")
    print("   - Click en 'Create repository'")
    print()
    
    # Abrir GitHub en el navegador
    webbrowser.open("https://github.com/new")
    
    # Esperar a que el usuario cree el repositorio
    input("\nPresiona ENTER cuando hayas creado el repositorio en GitHub...")
    
    print("\nAhora conecta tu repositorio local:")
    print("   Copia y pega esto en la terminal:")
    print()
    
    print("   git remote add origin https://github.com/TU_USUARIO/dashboard-ies.git")
    print("   git branch -M main")
    print("   git push -u origin main")
    print()
    
    print("Reemplaza 'TU_USUARIO' con tu nombre de usuario de GitHub")
    print()
    
    print("Despues de subir, ve a:")
    print("   https://share.streamlit.io")
    print("   - Conecta tu cuenta de GitHub")
    print("   - Selecciona el repositorio dashboard-ies")
    print("   - Archivo: app.py")
    print("   - Click en 'Deploy!'")
    print()
    
    print("Tu dashboard estara en linea!")

if __name__ == "__main__":
    subir_a_github()
