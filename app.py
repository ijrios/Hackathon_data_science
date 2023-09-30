import pickle
import pandas as pd
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)

mapeo_respuestas = {
    'Pobre': 0,
    'Regular': 1,
    'Bueno': 2,
    'Muy bueno': 3,
    'Excelente': 4,
    'Nunca': 0,
    'En el último año': 1,
    'En los últimos 2 años': 2,
    'En los últimos 5 años': 3,
    'Hace 5 o más años': 4,
    'Sí': 1,
    'No': 0,
    'Poco': 1,
    'Mucho': 2,
}

#Abrimos el index
@app.route("/")
def hello_hackathon():
    return render_template('home.html')

#Se crea evento para procesar encuesta
@app.route('/procesar_encuesta', methods=['POST'])
def procesar_encuesta():
   #Obtenemos los datos del formulario
    if 'name' in request.form:
      nombre = request.form['name']
      apellido = request.form['apellido']
      tipo_documento = request.form['type']
      numero_documento = request.form['doc']
      fecha_nacimiento = request.form['fechaNacimiento']
      correo = request.form['email']
      telefono = int(request.form['telefono'])
      
     #Creamos un diccionario con las preguntas y convertir las respuestas a valores numéricos
      encuesta_data = {
          'Nombre': [nombre],
          'Apellido': [apellido],
          'Tipo de documento': [tipo_documento],
          'Número de documento': [numero_documento],
          'Fecha de nacimiento': [fecha_nacimiento],
          'Correo electrónico': [correo],
          'Telefono': [telefono],
          'Estado de salud': [mapeo_respuestas.get(request.form['estadoSalud'], 0)],
          'Última visita médica': [mapeo_respuestas.get(request.form['ultimaVisita'], 0)],
          'Realiza ejercicio físico': [mapeo_respuestas.get(request.form['realizaEjercicio'], 0)],
          'Fuma': [mapeo_respuestas.get(request.form['fuma'], 0)],
          'Enfermedad cardiovascular': [mapeo_respuestas.get(request.form['enfermedadCardiovascular'], 0)],
          'Diabetes': [mapeo_respuestas.get(request.form['diabetes'], 0)],
          'Hipertensión': [mapeo_respuestas.get(request.form['hipertension'], 0)],
          'Obesidad': [mapeo_respuestas.get(request.form['obesidad'], 0)],
          'Síntomas recientes': [mapeo_respuestas.get(request.form['sintomas'], 0)],
          'Artritis': [mapeo_respuestas.get(request.form['artritis'], 0)],
          'Enfermedades familiares': [mapeo_respuestas.get(request.form['enfermedadesFamilia'], 0)],
          'Consumo de frutas': [mapeo_respuestas.get(request.form['consumoFrutas'], 0)],
          'Consumo de vegetales': [mapeo_respuestas.get(request.form['consumoVegetales'], 0)],
          'Consumo de fritos o comida rápida': [mapeo_respuestas.get(request.form['consumoFritos'], 0)],
      }
      datos_encuesta = pd.DataFrame(encuesta_data)
      datos_encuesta.to_csv('data/encuesta.csv', mode='a', header=False, index=False)
    else:
      response = {'mensaje': 'La respuesta no ha sido enviada.'}
      
    df = pd.read_csv('data/encuesta.csv',header=None)
    columns_to_drop = [7,8,9,10,11,12]
    filtered_df = df.drop(columns=columns_to_drop)
    with open("code (models)/modelo_entrenado.pkl", "rb") as f:
      model = pickle.load(f)
    prediction = model.predict(filtered_df).tolist()
    prediction.to_csv('data/predict.csv', mode='a', header=False, index=False)
    response = {'mensaje': 'La respuesta ha sido enviada al correo electrónico.'}
    return jsonify(response)

if __name__  == "__main__":
  app.run(host="0.0.0.0", debug=True)