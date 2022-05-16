import training_validation
import prediction_validation
import model_buildibg
import prediction
from wsgiref import simple_server
from flask import Flask, request, render_template
from flask import Response
from flask_cors import CORS, cross_origin
import os
import flask_monitoringdashboard as dashboard

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)

@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/train", methods=['POST'])
@cross_origin()
def trainRouteClient():
    try:
        if request.json['folderPath'] is not None:
            path = request.json['folderPath']

            #train validation
            train_valObj = training_validation.training_validation(path)
            train_valObj.train_validation()

            #model building
            trainModelObj = model_buildibg.model_building() #object initialization
            trainModelObj.model()  #training the model for the files in the table

    except Exception as e:
            raise e


@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        if request.json is not None:
            path = request.json['filepath']
            #validate predict data
            prediction_valObj = prediction_validation.prediction_validation(path)
            prediction_valObj.prediction_validation()

            #get the model for the data
            pred = prediction.prediction()
            path = pred.predictionFromModel()
            return Response("Prediction File created at %s!!!" % path)
        elif request.form is not None:
            path = request.form['filepath']
            prediction_valObj = prediction_validation.prediction_validation(path)
            prediction_valObj.prediction_validation()
            pred = prediction.prediction()
            path = pred.predictionFromModel()
            return Response("Prediction File created at %s!!!" % path)

    except Exception as e:
        return Response("Error Occurred! %s" %e)



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8001, debug=True)
