import sqlite3
import os
import csv
import shutil

class dBOperation:
    def __init__(self):
        self.path = 'Prediction_Database/'
        self.badFilePath = "Prediction_Batch_Files_validated/Bad_Raw"
        self.goodFilePath = "Prediction_Batch_Files_validated/Good_Raw"


    def dataBaseConnection(self,DatabaseName):
        print("i entered here dataBaseConnection")

        try:
            conn = sqlite3.connect(self.path+DatabaseName+'.db')
        except ConnectionError:
            raise ConnectionError
        return conn


    def createTableDb(self,DatabaseName,column_names):

        try:
            print("i entered here createTableDb")
            conn = self.dataBaseConnection(DatabaseName)
            c=conn.cursor()
            c.execute("SELECT count(name)  FROM sqlite_master WHERE type = 'table'AND name = 'Good_Raw_Data'")
            if c.fetchone()[0] ==1:
                conn.close()
            else:
                for key in column_names.keys():
                    type = column_names[key]
                    try:
                        conn.execute('ALTER TABLE Good_Raw_Data ADD COLUMN "{column_name}" {dataType}'.format(column_name=key,dataType=type))
                    except:
                        conn.execute('CREATE TABLE  Good_Raw_Data ({column_name} {dataType})'.format(column_name=key, dataType=type))
                conn.close()
        except Exception as e:
            raise e


    def insertIntoTableGoodData(self,Database):
        conn = self.dataBaseConnection(Database)
        goodFilePath= self.goodFilePath
        badFilePath = self.badFilePath
        onlyfiles = [f for f in os.listdir(goodFilePath)]
        count =1
        print("i entered here insertIntoTableGoodData")
        for file in onlyfiles:
            try:

                with open(goodFilePath+'/'+file, "r") as f:
                    next(f)
                    reader = csv.reader(f, delimiter="\n")
                    for line in enumerate(reader):
                        for list_ in (line[1]):
                            try:
                                conn.execute('INSERT INTO Good_Raw_Data values ({values})'.format(values=(list_)))
                                conn.commit()
                                count+=1
                            except Exception as e:
                                raise e
            except Exception as e:
                conn.rollback()
                shutil.move(goodFilePath+'/' + file, badFilePath)
                conn.close()
        conn.close()



    def selectingDatafromtableintocsv(self,Database):
        print("i enterd")
        self.fileFromDb = 'Prediction_Output_File/'
        self.fileName = 'OutputFile.csv'
        try:
            print('i enterd')
            conn = self.dataBaseConnection(Database)
            sqlSelect = "SELECT *  FROM Good_Raw_Data"
            cursor = conn.cursor()
            cursor.execute(sqlSelect)
            results = cursor.fetchall()
            headers = [i[0] for i in cursor.description]
            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)
            csvFile = csv.writer(open(self.fileFromDb + self.fileName, 'w', newline=''),delimiter=',', lineterminator='\r\n',quoting=csv.QUOTE_ALL, escapechar='\\')
            csvFile.writerow(headers)
            csvFile.writerows(results)
        except Exception as e:
            raise e






