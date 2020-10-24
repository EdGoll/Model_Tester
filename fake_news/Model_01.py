import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.metrics import confusion_matrix
from sklearn.metrics import confusion_matrix, f1_score, classification_report
import pandas as pd
import numpy as np
from  utils.DataSetUtils import get_excel_dataset
from  utils.DataSetUtils import build_train_and_scaler

def exec_xgboost(dataset,y_column) :
    X,Y = get_excel_dataset(dataset,y_column)
    X_train, X_test, y_train, y_test = build_train_and_scaler(X, Y, 0.25, 1)
    data_dmatrix = xgb.DMatrix(data=X_train,label=y_train)
    xg_reg = xgb.XGBClassifier(objective ='binary:logistic', 
                                colsample_bytree = 0.3, 
                                learning_rate = 0.1,
                                max_depth = 6, 
                                alpha = 10, 
                                n_estimators = 10)
    xg_reg.fit(X_train,y_train)
    y_pred_l  = xg_reg.predict(X_test)
    return confusion_matrix(y_test, y_pred_l),  classification_report(y_test, y_pred_l)