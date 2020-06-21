import pandas as pd
import sklearn
from sklearn.externals import joblib
from flask import Flask, request, jsonify, render_template
import numpy as np


# prediction function
meal_info = pd.read_csv('meal_info.csv')
totalMeals=meal_info['meal_id'].unique()
#len(totalMeals) 
STL=[1885, 1993, 2139, 2631, 1248, 1778, 1062, 2707, 2640, 2306, 2826, 1754, 1902, 1311, 1803, 1525, 2304, 1878, 1216, 1247, 1770, 1198, 1438, 2494, 1847, 2760, 2492, 1543, 2664, 2569, 1571, 2956]
ETS=[2539, 1207, 1230, 2322, 2290, 1727, 1109, 2126, 1971, 1558, 2581, 1962, 1445, 2444, 2867, 2704, 2577, 2490, 2104]






def ValuePredictor(to_predict_list): 
    to_predict = np.array(to_predict_list).reshape(1, 2) 
    Mid=to_predict[0][0]
    #print(Mid)
    week=to_predict[0][1]
    #print(week)


    present=0
    Raw=[]

    try:
      for i in totalMeals:
        for s in STL:
          if(i==Mid):
            from stldecompose import decompose, forecast
            FName="STL"+str(i)+".xml"
            #print(FName)
            model = joblib.load(FName)
            #print(model)
            fore=forecast(model, steps=week, fc_func=naive, seasonal=True) 
            Pred=[]
            for j in fore.values:
              Pred.append(j[0])
            RawMat=Quantity.loc[Mid]
                #print(RawMat)
            for p in range(0,len(Pred)):
              qt='Week%s' % p
              qt=[]
              for q in range(0,len(RawMat)):
                rw=int(round(Pred[p]*RawMat[q]))
                qt.append(rw)
              Raw.append(qt)
            break
        for e in ETS:
          if(e==Mid):
              FName="ETS"+str(i)+".xml"
              model = joblib.load(FName)
              Pred=[]
              Pred=model.forecast(week) 
              RawMat=Quantity.loc[Mid]
              for p in range(0,len(Pred)):
                qt='Week%s' % p
                qt=[]
                for q in range(0,len(RawMat)):
                  rw=int(round(Pred[p]*RawMat[q]))
                  qt.append(rw)
                Raw.append(qt)
                break
    except (RuntimeError,TypeError, NameError, ValueError):
        Prediction="Eneter a"
        RawMaterials="raw"
    else:
      Prediction=Pred
      RawMaterials=Raw
        
 
    return Prediction,RawMaterials
  
@app.route('/result', methods = ['POST']) 
def result(): 
    if request.method == 'POST': 
        to_predict_list = request.form.to_dict() 
        to_predict_list = list(to_predict_list.values()) 
        to_predict_list = list(map(int, to_predict_list)) 
        Predicted,PredRaw = ValuePredictor(to_predict_list)         
    return render_template("result.html", prediction = Predicted, suggestions=PredRaw)