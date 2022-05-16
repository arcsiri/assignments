import pandas
import model_operations
import load_preprocess_prediction
import prediction_validation


class prediction:

    def __init__(self,path):
        self.pred_data_val = prediction_validation.prediction_validation(path)

    def predictionFromModel(self):

        try:
            # deletes the existing prediction file from last run!
            self.pred_data_val.deletePredictionFile()
            # getting the outputfile
            data_getter=load_preprocess_prediction.Data_Getter_Pred()
            data=data_getter.get_data()
            #preprocess the file
            data=data_getter.scaling(data)
            #load the kmeans model
            model_loader=model_operations.Model_Operation()
            kmeans=model_loader.load_model('KMeans')
            #predict on data
            clusters=kmeans.predict(data)
            data['clusters']=clusters
            clusters=data['clusters'].unique()
            result =[]
            for i in clusters:
                cluster_data= data[data['clusters']==i]
                cluster_data = cluster_data.drop(['clusters'],axis=1)
                model_name = model_loader.find_correct_model_file(i)
                model = model_loader.load_model(model_name)
                for val in (model.predict(cluster_data)):
                    if val ==0:
                        result.append("Lodgepole_Pine")
                    elif val==1:
                        result.append("Spruce_Fir")
                    elif val==2:
                        result.append("Douglas_fir")
                    elif val==3:
                        result.append("Krummholz")
                    elif val==4:
                        result.append("Ponderosa_Pine")
                    elif val==5:
                        result.append("Aspen")
                    elif val==6:
                        result.append("Cottonwood_Willow")
            result = pandas.DataFrame(result, columns=['Predictions'])
            path="Prediction_Output_File/Predictions.csv"
            result.to_csv("Prediction_Output_File/Predictions.csv",header=True,mode='a+')


        except Exception as e:
            raise e

        return path





