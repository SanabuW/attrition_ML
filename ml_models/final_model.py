import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer

## Functions 
def preprocess_cat_columns(data):
    data["Education"] = data["Education"].map({1:"Below College", 2:"College", 3:"Bachelor", 4:"Master",5:"Doctor"}) 
    data["EnvironmentSatisfaction"] = data["EnvironmentSatisfaction"].map({1:"Low", 2:"Medium", 3:"High", 4:"Very High"})
    data["JobInvolvement"] = data["JobInvolvement"].map({1:"Low", 2:"Medium", 3:"High", 4:"Very High"})
    data["JobSatisfaction"] = data["JobSatisfaction"].map({1:"Low", 2:"Medium", 3:"High", 4:"Very High"})
    data["PerformanceRating"] = data["PerformanceRating"].map({1:"Low", 2:"Medium", 3:"High", 4:"Very High"})
    data["RelationshipSatisfaction"] = data["RelationshipSatisfaction"].map({1:"Low", 2:"Medium", 3:"High", 4:"Very High"})
    data["WorkLifeBalance"] = data["WorkLifeBalance"].map({1:"Bad", 2:"Good", 3:"Better", 4:"Best"})
    return data


def num_pipeline_transformer(data):
    numerics = ['int64']
    num_attrs = data.select_dtypes(include=numerics)
    num_pipeline = Pipeline([
        ('std_scaler', StandardScaler()),
        ])
    return num_attrs, num_pipeline


def pipeline_transformer(data):
    cat_attrs = ["BusinessTravel", "Department", "Education", 
                    "EducationField", "EnvironmentSatisfaction", "Gender",
                    "JobInvolvement", "JobRole", "JobSatisfaction", 
                    "MaritalStatus", "OverTime", "PerformanceRating", 
                    "RelationshipSatisfaction", "WorkLifeBalance"]
    num_attrs, num_pipeline = num_pipeline_transformer(data)
    prepared_data = ColumnTransformer([
        ("num", num_pipeline, list(num_attrs)),
        ("cat", OneHotEncoder(), cat_attrs),
        ])
    prepared_data.fit_transform(data)
    return prepared_data


def predict_attrition(config, model):

    if type(config) == dict:
        df = pd.DataFrame(config)
    else:
        df = config

    preproc_df = preprocess_cat_columns(df)
    print(preproc_df)
    pipeline = pipeline_transformer(preproc_df)
    prepared_df = pipeline.transform(preproc_df)
    print(len(prepared_df))
    y_pred = model.predict(prepared_df)
    probability = model.predict_proba(prepared_df)
    
    return y_pred, probability


# def make_predictions(processed_df, model):
#     prediction = model.predict(processed_df)
#     probability = model.predict_proba(processed_df)
#     probabilities = []
#     for prob_array in probability:
#         probabilities.append(prob_array[1])
    
#     predictions_df = pd.DataFrame({"prediction": prediction,
#                                    "probability": probabilities})
    
#     predictions_json = predictions_df.to_json(orient='records')
#     return predictions_json 

# def generate_predictions():
#     test_df = pd.read_json("holdout_test.json")

#     model_path = "attrition_prediction_model.bin"
