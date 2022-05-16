#importing the necessary libraries
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error,r2_score
from math import sqrt
from sklearn.preprocessing import StandardScaler
import pickle


#loading the dataset
full_train=pd.read_csv("train.csv")
print("loaded")
#remove unnecessary columns
train=full_train.copy()
train.drop("Name",axis=1,inplace=True)
print("col rem")

#data sampling into x and y
X=train.drop('Global_Sales',axis=1)
Y=train['Global_Sales']
print("samp done")

#data pre processing
cat_var=[]
cont_var=[]
for i in X.columns:
    if X[i].dtypes=="object":
        cat_var.append(i)
    else:
        cont_var.append(i)
print("cat var")

#imputing the continuous variable
imputer=KNNImputer()
X[cont_var]=pd.DataFrame(imputer.fit_transform(X[cont_var]),columns=cont_var)
# imputing the categorical variables
cat_var_to_impute_X = []

for i in X.columns:
    if X[i].isna().sum() > 0:
        cat_var_to_impute_X.append(i)

for i in cat_var_to_impute_X:
    if X[i].isna().sum() < (X.shape[0] * 5 / 100):
        X[i].fillna(X[i].mode()[0], inplace=True)

    else:
        X[i + '_null'] = np.where(X[i].isna(), 1, 0)
        X[i].fillna('0', inplace=True)

print("impute done")
#Feature engineering
X['User_Score_'+'tbd']=np.where(X['User_Score']=='tbd',1,0)
X['User_Score']=np.where(X['User_Score']=='tbd',0,X['User_Score'])
X.User_Score = X.User_Score.astype(float)
print("eng done")
#agregation of the cotegorical variable based on frequency
for i in X.columns:
    if X[i].dtype=='object':
        value_dataframe=pd.DataFrame()
        value_dataframe[i]=X[i].value_counts()
        names_to_approx=value_dataframe[value_dataframe[i]<X.shape[0]*1/100].index
        for j in names_to_approx:
            X.loc[(X[i]==j), i] ='aggregate_'+i

print("aggreg done")
#model building- Random Forest Regressor
new_train=X.copy()
new_train=pd.get_dummies(new_train)
col=new_train.columns
print("dummies done")
#train test split
x_train,x_validation,y_train,y_validation=train_test_split(new_train,Y,random_state=123,test_size=0.20)
#scaling the data set
scale=StandardScaler()
x_train=scale.fit_transform(x_train)
x_validation=scale.transform(x_validation)
print("split and scaling done")

x_train=pd.DataFrame(x_train,columns=col)
x_validation=pd.DataFrame(x_validation,columns=col)

#RF=RandomForestRegressor(random_state=321)
#model1_RF=RF.fit(x_train,y_train)
print("model built")
#saving the model
#pickle.dump(model1_RF,open('model1_RF.pkl',"wb"))
print("model saved")

print(x_train.columns)
print(len(x_train.columns))

