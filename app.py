from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Página principal con el formulario

@app.route('/consulta-deudores', methods=['GET'])
def consulta_deudores_form():
    cuit = request.args.get('cuit')  # Obtener el CUIT del formulario
    return redirect(url_for('consulta_deudores', cuit=cuit))

@app.route('/consulta-deudores/<cuit>', methods=['GET'])
def consulta_deudores(cuit):
    url = f"https://api.bcra.gob.ar/CentralDeDeudores/v1.0/Deudas/{cuit}"
    
    try:
        # Hacer la solicitud a la API
        response = requests.get(url, verify=False)  # Usar verify=False para evitar errores de SSL
        
        if response.status_code == 200:
            data = response.json()
            print(data)  # Imprimir para depuración
            return render_template('resultado.html', data=data)  # Renderizar la plantilla con los datos
        else:
            return jsonify({"error": "No se encontraron datos"}), 404
    
    except requests.exceptions.SSLError as e:
        return jsonify({"error": "Error de conexión SSL", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
