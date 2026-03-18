import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime
import json
import os

# Configuración de Google Drive
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'google_drive_credentials.json'

class GoogleDriveBackup:
    def __init__(self):
        self.creds = None
        self.client = None
        self.spreadsheet = None
        self.setup_credentials()
    
    def setup_credentials(self):
        """Configurar las credenciales de Google Drive"""
        try:
            # Intentar cargar credenciales desde archivo
            if os.path.exists(SERVICE_ACCOUNT_FILE):
                self.creds = ServiceAccountCredentials.from_json_keyfile_name(
                    SERVICE_ACCOUNT_FILE, SCOPES)
                self.client = gspread.authorize(self.creds)
                print("✅ Credenciales de Google Drive cargadas correctamente")
            else:
                print("❌ Archivo de credenciales no encontrado")
                return False
        except Exception as e:
            print(f"❌ Error al configurar credenciales: {e}")
            return False
        
        return True
    
    def create_or_get_spreadsheet(self, title="Dashboard IES - Backup Automático"):
        """Crear o obtener el spreadsheet de backup"""
        try:
            # Intentar abrir spreadsheet existente
            try:
                self.spreadsheet = self.client.open(title)
                print(f"✅ Spreadsheet encontrado: {title}")
            except gspread.SpreadsheetNotFound:
                # Crear nuevo spreadsheet
                self.spreadsheet = self.client.create(title)
                print(f"✅ Spreadsheet creado: {title}")
                
                # Compartir con el email especificado
                self.spreadsheet.share('solpeschuk@gmail.com', 
                                   perm_type='user', 
                                   role='writer')
                print("✅ Spreadsheet compartido con solpeschuk@gmail.com")
            
            return True
        except Exception as e:
            print(f"❌ Error al crear/obtener spreadsheet: {e}")
            return False
    
    def backup_data(self, df, sheet_name=None):
        """Hacer backup de datos a Google Drive"""
        if not self.client or not self.spreadsheet:
            if not self.setup_credentials():
                return False
            
            if not self.create_or_get_spreadsheet():
                return False
        
        try:
            # Nombre de la hoja
            if not sheet_name:
                sheet_name = f"Backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Limpiar nombre de hoja
            sheet_name = sheet_name.replace('/', '_').replace('\\', '_')
            
            # Crear o limpiar hoja
            try:
                worksheet = self.spreadsheet.worksheet(sheet_name)
                worksheet.clear()
            except gspread.WorksheetNotFound:
                worksheet = self.spreadsheet.add_worksheet(title=sheet_name, rows="1000", cols="50")
            
            # Convertir DataFrame a lista de listas
            data = [df.columns.tolist()] + df.values.tolist()
            
            # Escribir datos
            worksheet.update('A1', data)
            
            print(f"✅ Backup completado en Google Drive - Hoja: {sheet_name}")
            print(f"📊 Total de registros: {len(df)}")
            print(f"📁 Spreadsheet: {self.spreadsheet.title}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error al hacer backup: {e}")
            return False
    
    def backup_attendance(self, df, trimester):
        """Backup específico de asistencias"""
        sheet_name = f"Asistencias_{trimester.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}"
        return self.backup_data(df, sheet_name)
    
    def backup_evaluations(self, df, trimester):
        """Backup específico de evaluaciones"""
        sheet_name = f"Evaluaciones_{trimester.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}"
        return self.backup_data(df, sheet_name)
    
    def get_spreadsheet_url(self):
        """Obtener URL del spreadsheet"""
        if self.spreadsheet:
            return self.spreadsheet.url
        return None

# Función para crear credenciales (instrucciones)
def create_credentials_instructions():
    """Crear archivo de instrucciones para credenciales"""
    instructions = """
# INSTRUCCIONES PARA CONFIGURAR GOOGLE DRIVE BACKUP

## 1. Crear Proyecto en Google Cloud
1. Ve a https://console.cloud.google.com/
2. Crea un nuevo proyecto (ej: "Dashboard IES Backup")
3. Habilita las APIs:
   - Google Drive API
   - Google Sheets API

## 2. Crear Cuenta de Servicio
1. Ve a "IAM y administración" > "Cuentas de servicio"
2. Crea una nueva cuenta de servicio
3. Descarga la clave JSON
4. Renombra el archivo a: google_drive_credentials.json
5. Coloca el archivo en la misma carpeta que la app

## 3. Compartir Spreadsheet
1. El sistema creará automáticamente un spreadsheet
2. Se compartirá automáticamente con: solpeschuk@gmail.com
3. Recibirás un email para aceptar el acceso

## 4. Verificar Backup
1. Los datos se guardarán automáticamente en Google Drive
2. Podrás verlos en: https://docs.google.com/spreadsheets
3. Se crearán hojas por fecha y tipo de datos

## 5. Archivo de Credenciales
El archivo google_drive_credentials.json debe contener algo como:
{
  "type": "service_account",
  "project_id": "tu-proyecto-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "...@...gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token"
}
"""
    
    with open('INSTRUCCIONES_GOOGLE_DRIVE.txt', 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print("📋 Archivo de instrucciones creado: INSTRUCCIONES_GOOGLE_DRIVE.txt")

# Instalación de dependencias
def install_dependencies():
    """Instalar las dependencias necesarias"""
    try:
        import subprocess
        import sys
        
        packages = [
            'gspread==5.7.2',
            'oauth2client==4.1.3',
            'google-auth==2.16.0',
            'google-auth-oauthlib==1.0.0',
            'google-auth-httplib2==0.1.1'
        ]
        
        for package in packages:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"✅ Paquete instalado: {package}")
            except:
                print(f"❌ Error al instalar: {package}")
        
        return True
    except Exception as e:
        print(f"❌ Error al instalar dependencias: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Configuración de Google Drive Backup")
    print("=" * 50)
    
    # Crear instrucciones
    create_credentials_instructions()
    
    # Instalar dependencias
    print("\n📦 Instalando dependencias...")
    install_dependencies()
    
    print("\n✅ Configuración completada!")
    print("📋 Sigue las instrucciones en INSTRUCCIONES_GOOGLE_DRIVE.txt")
