import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from flask import Flask, request, render_template
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import train_test_split


app = Flask(__name__)

@app.route("/")
def hello_hackathon():
    return render_template('home.html')

def data():
  # Cargamos datos
  datos = pd.read_csv('data/datos_novus.csv')
  X = datos.drop(["Heart_Disease"],axis=1)
  y = datos['Heart_Disease']
  scaler = MinMaxScaler()
  scaler.fit(X)
  X_train_scaled= scaler.transform(X)

  # Entrenar el modelo Random Forest
  modelo_rf = RandomForestClassifier()
  modelo_rf.fit(X_train_scaled, y)


if __name__  == "__main__":
  app.run(host="0.0.0.0", debug=True)