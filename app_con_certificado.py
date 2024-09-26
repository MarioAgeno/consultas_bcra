import requests
import certifi
from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/consulta-deudores/<cuit>', methods=['GET'])
def consulta_deudores(cuit):
    url = f"https://api.bcra.gob.ar/CentralDeDeudores/v1.0/Deudas/{cuit}"
    try:
        response = requests.get(url, verify=certifi.where())  # Usa el paquete de certificados de certifi
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "No se encontraron datos"}), 404
    except requests.exceptions.SSLError as e:
        return jsonify({"error": "Error de conexión SSL", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
