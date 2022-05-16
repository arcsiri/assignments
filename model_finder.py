from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier
from sklearn.metrics  import roc_auc_score,accuracy_score

class Model_Finder:
    def __init__(self):

        self.clf = RandomForestClassifier()
        self.xgb = XGBClassifier(objective='binary:logistic')

    def get_best_params_for_random_forest(self,train_x,train_y):
        try:
            #self.param_grid = {"n_estimators": [10, 50, 100, 130], "criterion": ['gini', 'entropy'],
                             # "max_depth": range(2, 4, 1), "max_features": ['auto', 'log2']}

            #Creating an object of the Grid Search class
            #self.grid = GridSearchCV(estimator=self.clf, param_grid=self.param_grid, cv=5,  verbose=3,n_jobs=-1)
            #finding the best parameters
            #self.grid.fit(train_x, train_y)

            #extracting the best parameters
            self.criterion ='gini'#self.grid.best_params_['criterion']
            self.max_depth =3 #self.grid.best_params_['max_depth']
            self.max_features ='log2' #self.grid.best_params_['max_features']
            self.n_estimators =100 #self.grid.best_params_['n_estimators']

            #creating a new model with the best parameters
            self.clf = RandomForestClassifier(n_estimators=self.n_estimators, criterion=self.criterion,
                                              max_depth=self.max_depth, max_features=self.max_features)
            # training the mew model
            self.clf.fit(train_x, train_y)
            return self.clf
        except Exception as e:
            raise Exception()

    def get_best_params_for_xgboost(self,train_x,train_y):

        try:
            # initializing with different combination of parameters
            #self.param_grid_xgboost = {

              #  'learning_rate': [0.5, 0.1, 0.01, 0.001],
             #   'max_depth': [3, 5, 10, 20],
               # 'n_estimators': [10, 50, 100, 200]

            #}
            # Creating an object of the Grid Search class
            #self.grid= GridSearchCV(XGBClassifier(objective='multi:softprob'),self.param_grid_xgboost, verbose=3,cv=5,n_jobs=-1)
            # finding the best parameters
            #self.grid.fit(train_x, train_y)

            # extracting the best parameters
            self.learning_rate =0.5#elf.grid.best_params_['learning_rate']
            self.max_depth =5     #self.grid.best_params_['max_depth']
            self.n_estimators = 50 # self.grid.best_params_['n_estimators']

            # creating a new model with the best parameters
            self.xgb = XGBClassifier(learning_rate=self.learning_rate, max_depth=self.max_depth, n_estimators=self.n_estimators)
            # training the mew model
            self.xgb.fit(train_x, train_y)
            return self.xgb
        except Exception as e:
            raise Exception()


    def get_best_model(self,train_x,train_y,test_x,test_y):
        # create best model for XGBoost
        try:
            self.xgboost= self.get_best_params_for_xgboost(train_x,train_y)
            # we will using predict_proba in case of a multiclass classification as roc_auc_score needs predict_proba to calculate the score
            self.prediction_xgboost = self.xgboost.predict_proba(test_x) # Predictions using the XGBoost Model

            if len(test_y.unique()) == 1: #if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                self.xgboost_score = accuracy_score(test_y, self.prediction_xgboost)
            else:
                self.xgboost_score = roc_auc_score(test_y, self.prediction_xgboost, multi_class='ovr') # AUC for XGBoost


            # create best model for Random Forest
            self.random_forest=self.get_best_params_for_random_forest(train_x,train_y)
            # we will using predict_proba in case of a multiclass classification as roc_auc_score needs predict_proba to calculate the score
            self.prediction_random_forest=self.random_forest.predict_proba(test_x) # prediction using the Random Forest Algorithm

            if len(test_y.unique()) == 1:#if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                self.random_forest_score = accuracy_score(test_y,self.prediction_random_forest)
            else:
                self.random_forest_score = roc_auc_score(test_y, self.prediction_random_forest,multi_class='ovr') # AUC for Random Forest


            #comparing the two models
            if(self.random_forest_score <  self.xgboost_score):
                return 'XGBoost',self.xgboost
            else:
                return 'RandomForest',self.random_forest

        except Exception as e:
            raise Exception()

