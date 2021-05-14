####################################
# Import libraries
####################################
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect
)
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from ml_models.final_model import predict_attrition
import pickle
import numpy as np
## Comment out when using live ver.
import os

# Query functions to be applied to the separate api routes

# For secure/live ops version deployment
# from flask_sqlalchemy import SQLAlchemy
from test_alg_1 import predictor_func


####################################
# Begin Flask app setup
####################################
# Set up Flask app
app = Flask(__name__)

####################################
# Create/Define Flask app routes
####################################
# Front-end page routes
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/form.html")
def form():
    return render_template("form.html")

data_dict = {
    "dict_val1" : None,
    "dict_val2" : None
}

# APIs for data retrieval from server
# Remove "db." when switching to dev version

# with open('./ml_models/attrition_prediction_model.bin', 'rb') as file:
#     model = pickle.load(file)

@app.route('/send', methods=["GET", "POST"])
def predict():

    with open('./ml_models/attrition_prediction_model.bin', 'rb') as file:
        model = pickle.load(file)
        file.close()
    if request.method == "POST":
        val1_data = request.form['Age']
        val2_data = request.form['Education']
        val3_data = request.form['HourlyRate']
        val4_data = request.form['JobRole']
        val5_data = request.form['JobInvolvement']
        val6_data = request.form['DistanceFromHome']
        data_dict = {"Age": val1_data, 
                      "Education": val2_data, 
                      "HourlyRate": val3_data,
                      "JobRole": val4_data,
                      "JobInvolvement": val5_data,
                      "DistanceFromHome": val6_data}
        response = predict_attrition(model, data_dict)
        prob_output = response["probability"]
        predict_output = response["y_pred"]
    return render_template("form.html", prob_text = prob_output, predict_text = predict_output)



# Combined predictor route to post back out into HTML
# @app.route("/send", methods=["GET", "POST"])
# def send():
#     if request.method == "POST":
#         # check on if all types are correct
#         # add all values into object
#         val1_data = request.form["val_1_form_name"]
#         val2_data = request.form["val_2_form_name"]
#         data_dict["dict_val1"] = val1_data
#         data_dict["dict_val2"] = val2_data
#         response = predictor_func(request.form["val_1_form_name"], request.form["val_2_form_name"])
#         prob_output = response["probability"]
#         predict_output = response["prediction"]
#         return render_template("form.html", prob_text = prob_output, predict_text = predict_output)


# Run app
if __name__ == "__main__":
    app.run()
