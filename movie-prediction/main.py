# importing the necessary dependencies
import pandas as pd
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import pickle

app = Flask(__name__) # initializing a flask app

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            #getting the columns
            Name=str(request.form['Year_of_Release'])
            Platform=str(request.form['Year_of_Release'])
            Year_of_Release=float(request.form['Year_of_Release'])
            Genre=str(request.form['Year_of_Release'])
            Publisher=str(request.form['Year_of_Release'])
            NA_Sales=float(request.form['Year_of_Release'])
            EU_Sales=float(request.form['Year_of_Release'])
            JP_Sales=float(request.form['Year_of_Release'])
            Critic_Score=float(request.form['Year_of_Release'])
            Critic_Count=float(request.form['Year_of_Release'])
            User_Score=float(request.form['Year_of_Release'])
            User_Count=float(request.form['Year_of_Release'])
            Developer=str(request.form['Year_of_Release'])
            Rating=float(request.form['Year_of_Release'])


            test=pd.DataFrame([[0 for i in range(78)]],columns=col)
            test['Year_of_Release']=float(request.form['Year_of_Release'])
            test['Critic_Score'] = float(request.form['Critic_Score'])
            test['Critic_Count'] = float(request.form['Critic_Count'])
            test['User_Score'] = float(request.form['User_Score'])
            test['User_Count'] = float(request.form['User_Count'])
            Platform = float(request.form['Platform'])
            Genre = float(request.form['Genre'])
            Publisher = float(request.form['Publisher'])
            Developer = float(request.form['Developer'])
            Rating = float(request.form['Rating'])


            #B = float(request.form['B'])
            #LSTAT = float(request.form['LSTAT'])
            #filename = 'model1.pkl'
            #loaded_model = pickle.load(open(filename, 'rb')) # loading the model file from the storage
            # predictions using the loaded model file
            prediction=loaded_model.predict([[CRIM,ZN,INDUS,CHAS,NOX,RM,AGE,DIS,RAD,TAX,PTRATIO,B,LSTAT]])
            print('prediction is', prediction)
            # showing the prediction results in a UI
            return render_template('results.html',prediction=round(1000*prediction[0]))
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')
    else:
        return render_template('index.html')



if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True) # running the app