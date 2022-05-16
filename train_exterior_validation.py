import json
import pandas as pd
import os
import shutil


class regex():
    def __init__(self,path):
        self.schema_path = path
        self.goodDataPath = "Training_Batch_Files_validated/Good_Raw"


    def valuesFromSchema(self):
        try:
            print("i entered here valuesFromSchema")
            with open(self.schema_path, 'r') as f:
                dic = json.load(f)
                f.close()
            pattern = dic['SampleFileName']
            LengthOfDateStampInFile = dic['LengthOfDateStampInFile']
            LengthOfTimeStampInFile = dic['LengthOfTimeStampInFile']
            column_names = dic['ColName']
            NumberofColumns = dic['NumberofColumns']

        except Exception as e:
            raise e

        return LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, NumberofColumns

    def goodbad_del(self):
        print("i entered here goodbad_del")
        try:
            path = 'Training_Batch_Files_validated/'
            if os.path.isdir(path + 'Good_Raw/'):
                    shutil.rmtree(path + 'Good_Raw/')


        except Exception as e:
            raise e

        try:
            path = 'Training_Batch_Files_validated/'
            if os.path.isdir(path + 'Bad_Raw/'):
                shutil.rmtree(path + 'Bad_Raw/')


        except Exception as e:
            raise e


    def validate_name(self,LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, noofcolumns,path):
        print("i entered here validate_name")
        self.create_good_bad()
        #path="C:\\Users\\91738\Desktop\\pythonProject\\Training_Batch_Files"
        for f in os.listdir(path):
            re=f.split('.')
            re=re[0].split('_')

            if (re[0]+"_"+re[1])=='forest_cover':
                if len(re[2]) == LengthOfDateStampInFile:
                    if len(re[3]) == LengthOfTimeStampInFile:
                        shutil.copy("Training_Batch_Files/" + f, "Training_Batch_Files_validated/Good_Raw")
                    else:
                        shutil.copy("Training_Batch_Files/" + f, "Training_Batch_Files_validated/Bad_Raw")
                else:
                    shutil.copy("Training_Batch_Files/" + f, "Training_Batch_Files_validated/Bad_Raw")
            else:
                shutil.copy("Training_Batch_Files/" + f, "Training_Batch_Files_validated/Bad_Raw")

    def validate_columns(self,noofcolumns):
        print("i entered here validate_columns")
        try:
            for file in os.listdir('Training_Batch_Files_validated/Good_Raw/'):

                csv = pd.read_csv("Training_Batch_Files_validated/Good_Raw/" + file)
                if csv.shape[1] == noofcolumns:
                    pass
                else:
                    shutil.move("Training_Batch_Files_validated/Good_Raw/" + file, "Training_Batch_Files_validated/Bad_Raw")
        except Exception as e:
            raise e

    def create_good_bad(self):
        print("i entered here create_good_bad")
        try:
            path = os.path.join("Training_Batch_Files_validated/", "Good_Raw/")
            if not os.path.isdir(path):
                os.makedirs(path)
            path = os.path.join("Training_Batch_Files_validated/", "Bad_Raw/")
            if not os.path.isdir(path):
                os.makedirs(path)

        except Exception as e:
            raise e

    def validateMissingValuesInWholeColumn(self):
        print("i entered here validateMissingValuesInWholeColumn")
        try:
            for file in os.listdir('Training_Batch_Files_validated/Good_Raw/'):
                csv = pd.read_csv("Training_Batch_Files_validated/Good_Raw/" + file)
                count = 0
                for columns in csv:
                    if (len(csv[columns]) - csv[columns].count()) == len(csv[columns]):
                        count += 1
                        shutil.move("Training_Batch_Files_validated/Good_Raw/" + file,
                                    "Training_Batch_Files_validated/Bad_Raw")
                        break
                if count == 0:
                    csv.to_csv("Training_Batch_Files_validated/Good_Raw/" + file, index=None, header=True)
        except Exception as e:
            raise e


    def addQuotesToStringValuesInColumn(self):
        print("i entered here addQuotesToStringValuesInColumn")
        try:
            for f in os.listdir(self.goodDataPath):
                data = pd.read_csv(self.goodDataPath + "/" + f)
                data['class'] = data['class'].apply(lambda x: "'" + str(x) + "'")
                data.to_csv(self.goodDataPath + "/" + f, index=None, header=True)
        except Exception as e:
               raise e

