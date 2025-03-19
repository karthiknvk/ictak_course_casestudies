from flask import Flask,request,render_template,redirect
import pickle
import numpy as np
from create_model import threshold,min_max_dict

model=pickle.load(open('model_rfr.pkl','rb'))

app=Flask(__name__)

@app.route('/')
def home():
  return render_template("home.html",min_max_dict=min_max_dict)


@app.route('/predict',methods=['POST'])
def predict():
  temp_list=[]

  #taking values from form
  for key in min_max_dict.keys():
    value=request.values[key]
    temp_list.append(value)
    if len(min_max_dict[key])>2:
      min_max_dict[key].pop()
    min_max_dict[key].append(float(value))
  
  wine_features_list=[]
  for item in temp_list:
      wine_features_list.append(float(item))

  #reshaping   
  wine_features_list=np.reshape(wine_features_list,(1,11))

  #predicting result
  result=model.predict(wine_features_list)

  #rendering template
  if result>threshold:
    prediction=f"IS BOUGHT"
  else:
    prediction=f"IS NOT BOUGHT"
  return render_template('result.html',prediction=prediction,result=result,min_max_dict=min_max_dict)

if __name__=='__main__':
  app.run(debug=True)
