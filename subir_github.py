import subprocess
import webbrowser
import os

def subir_a_github():
    print("🚀 Preparando para subir a GitHub...")
    print("📋 Sigue estos pasos:")
    print()
    
    print("1️⃣  Abre GitHub en tu navegador:")
    print("   https://github.com/new")
    print()
    
    print("2️⃣  Configura el repositorio:")
    print("   • Repository name: dashboard-ies")
    print("   • Description: Dashboard de Gestión de Alumnos - IES")
    print("   • Public/Private (como prefieras)")
    print("   • NO marques 'Add README'")
    print("   • Click en 'Create repository'")
    print()
    
    print("3️⃣  Copia los comandos que GitHub te muestra")
    print()
    
    # Abrir GitHub en el navegador
    webbrowser.open("https://github.com/new")
    
    # Esperar a que el usuario cree el repositorio
    input("\n📝 Presiona ENTER cuando hayas creado el repositorio en GitHub...")
    
    print("\n🔗 Ahora conecta tu repositorio local:")
    print("   Copia y pega esto en la terminal:")
    print()
    
    # Obtener el usuario de GitHub (necesitarás ingresarlo)
    print("   git remote add origin https://github.com/TU_USUARIO/dashboard-ies.git")
    print("   git branch -M main")
    print("   git push -u origin main")
    print()
    
    print("📝 Reemplaza 'TU_USUARIO' con tu nombre de usuario de GitHub")
    print()
    
    print("🌐 Después de subir, ve a:")
    print("   https://share.streamlit.io")
    print("   • Conecta tu cuenta de GitHub")
    print("   • Selecciona el repositorio dashboard-ies")
    print("   • Archivo: app.py")
    print("   • Click en 'Deploy!'")
    print()
    
    print("✅ ¡Tu dashboard estará en línea!")

if __name__ == "__main__":
    subir_a_github()
