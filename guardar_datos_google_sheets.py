from flask import Flask, request, jsonify
import gspread
from google.oauth2.service_account import Credentials
import base64
import os

# Configuración de Google Sheets
SERVICE_ACCOUNT_FILE = '/Users/marcosrodrigo/Desktop/CodeStrack/chatbot-441820-2e2f6ba91e6b.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)
SPREADSHEET_ID = '1L5WAPYBuF0s2vl0p2VEnZMpHUajHZwxMgPFbtGN17GU'
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

app = Flask(__name__)

def save_image(file, filename):
    """
    Guarda una imagen en el servidor local (puedes adaptarlo para subirla a Google Drive o S3).
    """
    file_path = os.path.join('uploads', filename)
    file.save(file_path)
    return file_path  # Retorna la ruta donde se guardó el archivo

@app.route('/guardar', methods=['POST'])
def guardar():
    try:
        # Datos enviados en formato multipart/form-data
        data = request.form
        files = request.files

        # Guardar fotos de cédula
        id_photo_path = save_image(files['id_photo'], 'cedula_adelante.jpg')
        id_photo2_path = save_image(files['id_photo2'], 'cedula_atras.jpg')

        # Guardar firma en base64
        signature_base64 = data['signature']
        signature_file_path = os.path.join('uploads', 'firma.png')
        with open(signature_file_path, "wb") as f:
            f.write(base64.b64decode(signature_base64.split(",")[1]))

        # Preparar la fila para Google Sheets
        nueva_fila = [
            data['person_type'], data['date'], data['holder_name'], 
            data['holder_email'], data['city'], id_photo_path, 
            id_photo2_path, data['phone'], data['plates'], 
            data['satellite_provider'], data['username'], 
            data['password'], signature_file_path
        ]

        # Guardar en Google Sheets
        sheet.append_row(nueva_fila)
        return jsonify({"status": "success", "message": "Datos guardados exitosamente."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    # Crear carpeta 'uploads' si no existe
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
