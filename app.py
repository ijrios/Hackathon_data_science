from flask import Flask, request, render_template
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

# Cargamos datos
datos_entrenamiento = pd.read_csv('data/CVD_cleaned.csv')

X = datos_entrenamiento[['edad', 'otras_caracteristicas']]  
y = datos_entrenamiento['variable_objetivo']  

# Entrenar el modelo Random Forest
modelo_rf = RandomForestClassifier()
modelo_rf.fit(X, y)

@app.route("/")
def hello_hackathon():
    return render_template('home.html')

@app.route('/procesar_encuesta', methods=['POST'])
def procesar_encuesta():
    datos_encuesta = {
        'General_Health': float(request.form['general_fealth']),
        'Checkup': request.form['checkup'],
        'Heart_Disease': request.form['heart_Disease'],
        'Depression': request.form['depression'],
        'Arthritis': request.form['arthritis'],
        'Sex': request.form['sex'],
    }

    resultado_prediccion = modelo_rf.predict([[
        datos_encuesta['General_Health'],
        datos_encuesta['Checkup'],
        datos_encuesta['Heart_Disease']
        datos_encuesta['Depression']
        datos_encuesta['Arthritis']
        datos_encuesta['Sex']
      
    ]])

    return render_template('resultado.html', resultado=resultado_prediccion[0])

if __name__  == "__main__":
  app.run(host="0.0.0.0", debug=True)