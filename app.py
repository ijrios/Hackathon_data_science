import pickle
from typing import List

import numpy as np
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_hackathon():
    return render_template('home.html')

@app.post("/predict")
def predict(data):
    with open("gbm_model.pkl", "rb") as f:
        model = pickle.load(f)
    prediction = model.predict(data).tolist()
    return {"prediction": prediction}

if __name__  == "__main__":
  app.run(host="0.0.0.0", debug=True)