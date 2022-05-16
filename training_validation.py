import train_exterior_validation
import train_database


class training_validation():
    def __init__(self, path):
        self.path =path
        #self.train_exterior_validation = train_exterior_validation()
        #self.train_database = train_database()

    def train_validation(self):
        try:

            # get the values
            reg_exp = train_exterior_validation.regex('train.json')
            LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, noofcolumns = reg_exp.valuesFromSchema()
            # delete preexisting folders
            reg_exp.goodbad_del()
            # add to the folders
            reg_exp.validate_name(LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, noofcolumns,self.path)

            # validate columnlength
            reg_exp.validate_columns(noofcolumns)

            # validate the empty columns
            reg_exp.validateMissingValuesInWholeColumn()

            # addQuotesToStringValuesInColumn
            reg_exp.addQuotesToStringValuesInColumn()

            # databse operations
            dbop = train_database.dBOperation()
            dbop.createTableDb('Training', column_names)
            dbop.insertIntoTableGoodData('Training')

            # reading the contents of database inthe form of csv
            dbop.selectingDatafromtableintocsv('Training')
        except Exception as e:
            raise e












