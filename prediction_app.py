from flask import Flask,render_template,request
import pandas as pd 
import pickle
import numpy as np
from ml_models.final_model import predict_attrition

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/form', methods=['POST'])
def predict():
    feature_input = [str(x) for x in request.form.values()]
    final_features = [np.array(feature_input)]
    with open('./ml_models/attrition_prediction_model.bin', 'rb') as f_in:
        model = pickle.load(f_in)
        f_in.close()
    predictions = predict_attrition(final_features, model)
    output = predictions[0]
    
    return render_template('form.html', predict_text = output)



if __name__ == '__main__':
    app.run(debug=True)
    
