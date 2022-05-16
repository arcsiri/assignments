import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE


class Data_Getter_Pred:

    def __init__(self):
        self.prediction_file='Prediction_Output_File/OutputFile.csv'

    def get_data(self):

        try:
            self.data= pd.read_csv(self.prediction_file) # reading the data file
            return self.data
        except Exception as e:
            raise e

    def handleImbalanceDataset(self, X, y):
                print("entrd handleImbalanceDataset ")
                sample = SMOTE()
                X,Y= sample.fit_resample(X, y)

                return X, Y

    def scaling(self, data):
        scalar = StandardScaler()
        num_data = data[
            ["elevation", "aspect", "slope", "horizontal_distance_to_hydrology", "Vertical_Distance_To_Hydrology",
             "Horizontal_Distance_To_Roadways", "Horizontal_Distance_To_Fire_Points"]]
        cat_data = data.drop(
            ["elevation", "aspect", "slope", "horizontal_distance_to_hydrology", "Vertical_Distance_To_Hydrology",
             "Horizontal_Distance_To_Roadways", "Horizontal_Distance_To_Fire_Points"], axis=1)
        scaled_data = scalar.fit_transform(num_data)
        num_data = pd.DataFrame(scaled_data, columns=num_data.columns, index=num_data.index)
        final_data = pd.concat([num_data, cat_data], axis=1)
        return final_data
