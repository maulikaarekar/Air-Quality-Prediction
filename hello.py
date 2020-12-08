import flask
import os
import pandas as pd
import numpy as np
import pickle
import seaborn as sns
from flask import Flask,render_template,url_for,request,redirect
app= Flask(__name__)
aqi=0
city=''

def pollval(aqi):
    if aqi < 50:
        return ('Good','Green')
    elif aqi < 101:
        return ('Moderate','Yellow')
    elif aqi < 151:
        return ('Poor','Orange')
    elif aqi < 201:
        return ('Unhealthy','Red')
    elif aqi < 300:
        return ('Severe','Violet')
    return ('Hazardous','Blue')

@app.route('/')
def index():
    return flask.render_template('homepage.html')

@app.route('/stateselect',methods=['GET','POST'])
def stateselect():
    return flask.render_template('index.html')

@app.route('/city/',methods=['GET','POST'])
def city():
    city=request.args.get('city', default='')
    return flask.render_template('city.html',city=city)

@app.route('/datesel',methods=['POST'])
def datesel():
    data=request.form.to_dict()
    dateval1 = list(map(str,data.values()))
    datev = dateval1[0]
    city = dateval1[1]
    dff=pd.read_csv('datasets/'+city+'.csv')
    print(city)
    a = dff[dff['ds']==datev]
    aqi=a.iloc[0]['yhat']
    arima=a.iloc[0]['yhat_lower']
    naive=a.iloc[0]['yhat_upper']
    print(aqi)
    aqi=int(aqi)
    arima = int(arima)
    naive=int(naive)
    arima = aqi-arima//2
    naive = naive-aqi//2
    pollute = pollval(aqi)
    aqilvl = pollute[0]
    colorss = pollute[1]
    return flask.render_template('dashboard.html',aqi=aqi,aqilvl=aqilvl,colorss=colorss,city=city,arima=arima,naive=naive)

if __name__ == '__main__':
    app.run(debug=True)
