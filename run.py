from flask import Flask, render_template, jsonify
from ClaseLaberinto import Laberinto

app = Flask(__name__)


laberinto = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crear_laberinto')
def crear_laberinto():
    global laberinto
    try:
        laberinto = Laberinto(10, 10)  # Crear un laberinto de 7x7
        matriz = laberinto.obtener_matriz_laberinto_1_0()
        matrizNodo = laberinto.obtener_matriz_laberinto()
        return jsonify({"matriz": matriz,"matrizNodo": matrizNodo})
        
    except Exception as e:
        app.logger.error(f"Error al crear laberinto: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/obtener_solucion')
def obtener_solucion():
    global laberinto
    if laberinto:
        try:
            solucion = laberinto.obtener_solucion_completa()
            if 'camino' not in solucion or not solucion['camino']:
                raise ValueError("No se encontró un camino válido.")
            return jsonify(solucion)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "No se ha creado un laberinto"}), 400

if __name__ == '__main__':
    app.run(debug=True)