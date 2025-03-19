import pandas as pd 
import numpy as np 
import math
#reading data
data=pd.read_csv('winequality-red.csv')

#preprocessing steps
#duplicates
data.drop_duplicates(inplace=True)

X=data.drop('quality',axis=1)
y=data['quality']

X_describe=X.describe()
#outliers
X_columns=X.columns
for col in X_columns:
  outlier_list=[]
  col_mean=X[col].mean()
  q1=np.percentile(X[col],25)
  q3=np.percentile(X[col],75)
  iqr=q3-q1
  upper=q3+iqr*1.5
  lower=q1-iqr*1.5
  outlier_list=X[(X[col]>upper)|(X[col]<lower)].index
  for i in outlier_list:
    X.loc[i,col]=col_mean


#splitting data
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test=train_test_split(X,y,random_state=42,test_size=0.25)


#training model
#random forest
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error,r2_score,mean_squared_error

rfr=RandomForestRegressor(random_state=42)
rfr.fit(X_train,y_train)
rfr_y_pred=rfr.predict(X_test)

#saving model
import pickle 

with open("model_rfr.pkl","wb") as f:
  pickle.dump(rfr,f)

threshold = data['quality'].mean()


min_max_dict={}
for col in X_columns:
  min=math.floor(X_describe[col].loc['min'])
  max=math.ceil(X_describe[col].loc['max'])
  min_max_dict[col.replace(' ','_')]=[min,max]


