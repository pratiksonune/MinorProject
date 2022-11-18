
# coding: utf-8

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier 
from sklearn import metrics
from flask import Flask, request, render_template
import pickle

app = Flask("__name__")

df_1=pd.read_csv("StudentData.csv")

q = ""

@app.route("/")
def loadPage():
	return render_template('home.html', query="")


@app.route("/", methods=['POST'])
def predict():
    
    '''
    Gender
    Education
    Infrastructure
    PlacementSupport
    FacultySupport
    Events
    Fees
    Sport Facility
    DegreeYears

    '''
    

    
    inputQuery1 = request.form['query1']
    inputQuery2 = request.form['query2']
    inputQuery3 = request.form['query3']
    inputQuery4 = request.form['query4']
    inputQuery5 = request.form['query5']
    inputQuery6 = request.form['query6']
    inputQuery7 = request.form['query7']
    inputQuery8 = request.form['query8']
    inputQuery9 = request.form['query9']


    model = pickle.load(open("model.sav", "rb"))
    
    data = [[inputQuery1, inputQuery2, inputQuery3, inputQuery4, inputQuery5, inputQuery6, inputQuery7, 
             inputQuery8, inputQuery9]]
    
    new_df = pd.DataFrame(data, columns = [ 'Gender', 'Education', 'Infrastructure', 'PlacementSupport', 'FacultySupport', 'Events', 'Fees', 'Sport Facility', 'DegreeYears'])
    
    df_2 = pd.concat([df_1, new_df], ignore_index = True) 
    
    labels = ["{0} - {1}".format(i, i + 11) for i in range(1, 72, 12)]
   
    df_2['DegreeYears_group'] = pd.cut(df_2.DegreeYears.astype(int), range(1, 80, 12), right=False, labels=labels)
  
    df_2.drop(columns= ['DegreeYears'], axis=1, inplace=True) 
    
    
    
    
    new_df__dummies = pd.get_dummies(df_2[[ 'Gender', 'Education', 'Infrastructure', 'PlacementSupport', 'FacultySupport', 'Events', 'Fees', 'Sport Facility', 'DegreeYears']])
    
    
        
    
    single = model.predict(new_df__dummies.tail(1))
    probablity = model.predict_proba(new_df__dummies.tail(1))[ :,1]
    
    if single==1:
        o1 = "This student is likely to be churned!!"
        o2 = "Confidence: {}".format(probablity*100)
    else:
        o1 = "This student is likely to continue!!"
        o2 = "Confidence: {}".format(probablity*100)
        
    return render_template('home.html', output1=o1, output2=o2, 
                           query1 = request.form['query1'], 
                           query2 = request.form['query2'],
                           query3 = request.form['query3'],
                           query4 = request.form['query4'],
                           query5 = request.form['query5'], 
                           query6 = request.form['query6'], 
                           query7 = request.form['query7'], 
                           query8 = request.form['query8'], 
                           query9 = request.form['query9'])
    
app.run()

