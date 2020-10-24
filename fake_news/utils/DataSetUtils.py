import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder

__all__ = ['get_excel_dataset']

def build_train_data(X, Y, _test_size, _random_state) :
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=_test_size, random_state=_random_state)
    return X_train, X_test, y_train, y_test 

def build_scaler_data(data_train,data_test) :
    escala=MinMaxScaler()
    escala.fit(data_train)
    data_train=escala.transform(data_train)
    escala.fit(data_test)
    data_test=escala.transform(data_test)
    return data_train, data_test

def build_train_and_scaler(X, Y, _test_size, _random_state) :
    X_train, X_test, y_train, y_test = build_train_data(X, Y, _test_size, _random_state)
    X_train,X_test = build_scaler_data(X_train,X_test)
    #y_train,y_test = build_scaler_data(y_train,y_test)
    return X_train,X_test,y_train,y_test

def get_excel_dataset(ds_path,Y):
    df=pd.read_excel(ds_path)
    X, y_colum = get_x_y_values(df,Y)
    return X, y_colum

#Separa en conjunto de inicio y llegada
def get_x_y_values(df,Y) :
    if (df[Y] is not None) :
        y_colum = LabelEncoder().fit_transform(df[Y].values)
        X=df.drop(columns=[Y])
    return X, y_colum

#Analisis de Sentimiento
def addSentimentFromTweet(df,colValue):
    polaridad = df[colValue].apply(lambda x: TextBlob(x).sentiment.polarity)
    return polaridad

#Analisis de Subjetividad
def addSubjectibityFromTweet(df,colValue):
    subjetividad = df[colValue].apply(lambda x: TextBlob(x).sentiment.subjectivity)
    return subjetividad
