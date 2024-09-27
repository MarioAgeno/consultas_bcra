from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests

app = Flask(__name__)

# Ruta principal con formulario
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/consulta-deudores', methods=['GET'])
def redireccion_consulta():
    cuit = request.args.get('cuit')
    consulta = request.args.get('consulta')
    
    if consulta == 'deudores':
        return consulta_deudores(cuit)
    elif consulta == 'historica':
        return consulta_historica(cuit)
    elif consulta == 'cheques':
        return consulta_cheques(cuit)
    else:
        return render_template('error.html', message="Tipo de consulta no válida")


'''
@app.route('/consulta-deudores', methods=['GET'])
def consulta_deudores_form():
    cuit = request.args.get('cuit')
    consulta_tipo = request.args.get('consulta')
    
    if consulta_tipo == 'historica':
        return redirect(url_for('consulta_historica', cuit=cuit))
    else:
        return redirect(url_for('consulta_deudores', cuit=cuit))
'''

# Ruta para consulta de deudores
@app.route('/consulta-deudores/<cuit>', methods=['GET'])
def consulta_deudores(cuit):
    url = f"https://api.bcra.gob.ar/CentralDeDeudores/v1.0/Deudas/{cuit}"
    
    try:
        response = requests.get(url, verify=False)
        
        if response.status_code == 200:
            data = response.json()
            #print(data)  # Imprimir para depuración
            return render_template('resultado.html', data=data)
        else:
            return jsonify({"error": "No se encontraron datos"}), 404
    
    except requests.exceptions.SSLError as e:
        return jsonify({"error": "Error de conexión SSL", "details": str(e)}), 500

# Nueva ruta para la consulta histórica
@app.route('/consulta-historica/<cuit>', methods=['GET'])
def consulta_historica(cuit):
    url = f"https://api.bcra.gob.ar/CentralDeDeudores/v1.0/Deudas/Historicas/{cuit}"
    
    try:
        response = requests.get(url, verify=False)
        
        if response.status_code == 200:
            data = response.json()
            #print(data)  # Imprimir para depuración
            return render_template('historico.html', data=data)
        else:
            return jsonify({"error": "No se encontraron datos"}), 404
    
    except requests.exceptions.SSLError as e:
        return jsonify({"error": "Error de conexión SSL", "details": str(e)}), 500


# Consulta de cheques rechazados
@app.route('/consulta-cheques/<cuit>')
def consulta_cheques(cuit):
    url = f'https://api.bcra.gob.ar/CentralDeDeudores/v1.0/Deudas/ChequesRechazados/{cuit}'
    
    # Realizamos la consulta a la API, con verificación de SSL desactivada (solo en desarrollo)
    response = requests.get(url, verify=False)

    # Verificamos que la respuesta sea exitosa
    if response.status_code == 200:
        data = response.json()
        return render_template('cheques_rechazados.html', data=data)
    else:
        return jsonify({"error": "No se encontraron datos"}), 404


if __name__ == '__main__':
    app.run(debug=True)
