import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline



## Functions
def preprocess_cat_columns(data):
    data["Education"] = data["Education"].map({1:"Below College", 2:"College", 3:"Bachelor", 4:"Master",5:"Doctor"})
    data["JobInvolvement"] = data["JobInvolvement"].map({1:"Low", 2:"Medium", 3:"High", 4:"Very High"})
    # data["BusinessTravel"] = data["BusinessTravel"].map({1:"Travel_Frequently", 2:"Travel_Rarely", 3:"Non_Travel"})
    # data["Gender"] = data["Gender"].map({1:"Female", 2:"Male"})
    # data["JobRole"] = data["JobRole"].map({1:"Sales Executive",
    #     2:"Research Scientist",
    #     3:"Laboratory Technician",
    #     4:"Manufacturing Director",
    #     5:"Healthcare Representative",
    #     6:"Manager",
    #     7:"Sales Representative",
    #     8:"Research Director",
    #     9:"Human Resources"})



    # attrition_df["EnvironmentSatisfaction"] = attrition_df["EnvironmentSatisfaction"].map({1:"Low", 2:"Medium", 3:"High", 4:"Very High"})
    # data["Education"] = data["Education"].map({"Below College":1, "College":2, "Bachelor":3, "Master":4,"Doctor":5})
    # data["JobInvolvement"] = data["JobInvolvement"].map({"Low":1, "Medium":2, "High":3, "Very High":4})
    # data["BusinessTravel"] = data["BusinessTravel"].map({"Travel_Frequently":1, "Travel_Rarely":2, "Non_Travel":3})
    # attrition_df["JobSatisfaction"] = attrition_df["JobSatisfaction"].map({1:"Low", 2:"Medium", 3:"High", 4:"Very High"})
    # attrition_df["PerformanceRating"] = attrition_df["PerformanceRating"].map({1:"Low", 2:"Medium", 3:"High", 4:"Very High"})
    # attrition_df["RelationshipSatisfaction"] = attrition_df["RelationshipSatisfaction"].map({1:"Low", 2:"Medium", 3:"High", 4:"Very High"})
    # attrition_df["WorkLifeBalance"] = attrition_df["WorkLifeBalance"].map({1:"Bad", 2:"Good", 3:"Better", 4:"Best"})
    return data


def num_pipeline_transformer(data):
    numerics = ['int64']
    num_attrs = data.select_dtypes(include=numerics)
    num_pipeline = Pipeline([
        ('std_scaler', StandardScaler()),
        ])
    return num_attrs, num_pipeline


def pipeline_transformer(data):
    cat_attrs = ["Education", "JobInvolvement", "BusinessTravel", "Gender", "JobRole"]
    # cat_attrs = ["BusinessTravel", "Department", "Education", 
    #                 "EducationField", "EnvironmentSatisfaction", "Gender",
    #                 "JobInvolvement", "JobRole", "JobSatisfaction", 
    #                 "MaritalStatus", "OverTime", "PerformanceRating", 
    #                 "RelationshipSatisfaction", "WorkLifeBalance"]
    num_attrs, num_pipeline = num_pipeline_transformer(data)
    global full_pipeline
    full_pipeline = ColumnTransformer([
        ("num", num_pipeline, list(num_attrs)),
        ("cat", OneHotEncoder(), cat_attrs),
        ])
    prepared_data = full_pipeline.fit_transform(data)
    return prepared_data


def predict_attrition(config, model):

    if type(config) == dict:
        # REVIEW HERE
        df_prep = config.copy()
        df = pd.DataFrame(df_prep, index=[0])
        print(df)
    else:
        df = config.copy()

    preproc_df = preprocess_cat_columns(df)
    print(preproc_df)
    #which "data" is this?
    #"data_labels" should be the OG X
    attrition_df_temp = pd.read_csv("misc_resources/data/IBM_attrition_data.csv")
    data_temp = attrition_df_temp.copy()
    data_temp_dropped_X = data_temp[["Age", "Education", "DistanceFromHome", "JobInvolvement", "HourlyRate", "JobRole", "Gender", "BusinessTravel"]].copy()
    # data_temp_dropped_X = data_temp[["Age", "Education", "DistanceFromHome", "JobInvolvement", "HourlyRate", "JobRole", "Gender", "BusinessTravel"]].copy()
    data_temp_dropped_X_procc = preprocess_cat_columns(data_temp_dropped_X).copy()
    data_temp_dropped_Y = data_temp["Attrition"].copy()

    print(data_temp_dropped_X_procc)
    # data_temp_dropped_Y = data_temp[["Attrition"]].copy()
    print(data_temp_dropped_Y)
    prepared_df = pipeline_transformer(data_temp_dropped_X_procc)
    pipe = make_pipeline(full_pipeline, model)

    pipe.fit(data_temp_dropped_X_procc, data_temp_dropped_Y)
    # y_pred = pipe.predict(prepared_df)
    print(df)
    # y_pred = pipe.predict(prepared_df)
    # y_pred = pipe.predict(preproc_df)
    y_pred = pipe.predict(df)


    print(y_pred)

    # prepared_df = pipeline.transform(preproc_df)
    # print(len(prepared_df))
    # y_pred = model.predict(prepared_df)
    # probability = model.predict_proba(prepared_df)

    return y_pred


