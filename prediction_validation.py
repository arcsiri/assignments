import prediction_exterior_validation
import prediction_database
import os


class prediction_validation():
    def __init__(self, path):
        self.path =path
        #self.train_exterior_validation = train_exterior_validation()
        #self.train_database = train_database()

    def prediction_validation(self):
        try:

            # get the values
            reg_exp = prediction_exterior_validation.regex('prediction.json')
            LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, noofcolumns = reg_exp.valuesFromSchema()
            # delete preexisting folders
            reg_exp.goodbad_del()
            # add to the folders
            reg_exp.validate_name(LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, noofcolumns,self.path)

            # validate columnlength
            reg_exp.validate_columns(noofcolumns)

            # validate the empty columns
            reg_exp.validateMissingValuesInWholeColumn()

            # database operations
            dbop = prediction_database.dBOperation()
            dbop.createTableDb('prediction', column_names)
            dbop.insertIntoTableGoodData('prediction')

            # reading the contents of database inthe form of csv
            dbop.selectingDatafromtableintocsv('prediction')
        except Exception as e:
            raise e

    def deletePredictionFile(self):

        if os.path.exists('Prediction_Output_File/Predictions.csv'):
            os.remove('Prediction_Output_File/Predictions.csv')













