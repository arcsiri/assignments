import prediction_validation
import prediction

prediction_valObj = prediction_validation.prediction_validation('C:\\Users\\91738\\Desktop\\pythonProject\\Prediction_Batch_files')
prediction_valObj.prediction_validation()

pred=prediction.prediction('C:\\Users\\91738\\Desktop\\pythonProject\\Prediction_Batch_files')
path = pred.predictionFromModel()