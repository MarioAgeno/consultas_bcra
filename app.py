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
        return consulta_historicas(cuit)
    elif consulta == 'cheques':
        return consulta_cheques(cuit)
    else:
        return render_template('error.html', message="Tipo de consulta no válida")

# Consulta de Deudas
@app.route('/consulta-deudores/<cuit>')
def consulta_deudores(cuit):
    url = f'https://api.bcra.gob.ar/CentralDeDeudores/v1.0/Deudas/{cuit}'
    
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        data = response.json()
        return render_template('resultado.html', data=data)
    elif response.status_code == 400:
        error_data = response.json()
        return render_template('error.html', message=error_data.get('errorMessages', ["Error en la solicitud"])[0])
    elif response.status_code == 500:
        error_data = response.json()
        return render_template('error.html', message=error_data.get('errorMessages', ["Error en el servidor"])[0])
    else:
        error_data = response.json()
        return render_template('error.html', message=error_data.get('errorMessages', ["No se encontraron datos"])[0])

# Consulta Histórica
@app.route('/consulta-historicas/<cuit>')
def consulta_historicas(cuit):
    url = f'https://api.bcra.gob.ar/CentralDeDeudores/v1.0/Deudas/Historicas/{cuit}'
    
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        data = response.json()
        return render_template('historico.html', data=data)
    elif response.status_code == 400:
        error_data = response.json()
        return render_template('error.html', message=error_data.get('errorMessages', ["Parámetro erróneo"])[0])
    elif response.status_code == 404:
        error_data = response.json()
        return render_template('error.html', message=error_data.get('errorMessages', ["No se encontraron datos"])[0])
    elif response.status_code == 500:
        error_data = response.json()
        return render_template('error.html', message=error_data.get('errorMessages', ["Error en el servidor"])[0])
    else:
        return render_template('error.html', message="Error desconocido")

# Consulta de Cheques Rechazados
@app.route('/consulta-cheques/<cuit>')
def consulta_cheques(cuit):
    url = f'https://api.bcra.gob.ar/CentralDeDeudores/v1.0/Deudas/ChequesRechazados/{cuit}'
    
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        data = response.json()
        return render_template('cheques.html', data=data)
    elif response.status_code == 400:
        error_data = response.json()
        return render_template('error.html', message=error_data.get('errorMessages', ["Parámetro erróneo"])[0])
    elif response.status_code == 500:
        error_data = response.json()
        return render_template('error.html', message=error_data.get('errorMessages', ["Error en el servidor"])[0])
    else:
        error_data = response.json()
        return render_template('error.html', message=error_data.get('errorMessages', ["No se encontraron datos"])[0])

if __name__ == '__main__':
    app.run(debug=True)
