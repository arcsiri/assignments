import load_preprocess_input
import clustering
from sklearn.model_selection import train_test_split
import model_finder
import model_operations

class model_building():
    def model(self):
        try:
                #preprocessing the data


                load_preprocess=load_preprocess_input.load_preprocess_input()
                data=load_preprocess.get_data()
                data = load_preprocess.enocdeCategoricalvalues(data)
                print('data shape is',data.shape)
                X = data.drop(['class'], axis=1)
                Y = data['class']
                X, Y = load_preprocess.handleImbalanceDataset(X, Y)
                print('x shape is',X.shape)

                #clustering the data
                kmeans=clustering.KMeansClustering()
                number_of_clusters=kmeans.elbow_plot(X)
                print(number_of_clusters)
                X=kmeans.create_clusters(X,number_of_clusters)
                print('x shape is',X.shape)
                X['Labels']=Y
                list_of_clusters=X['Cluster'].unique()

                #going through every cluster for the best model
                for i in list_of_clusters:
                        print('entereed here')
                        cluster_data = X[X['Cluster'] == i]
                        # Prepare the feature and Label columns
                        cluster_features = cluster_data.drop(['Labels', 'Cluster'], axis=1)
                        cluster_label = cluster_data['Labels']
                        # splitting the data into training and test set for each cluster one by one
                        x_train, x_test, y_train, y_test = train_test_split(cluster_features, cluster_label, test_size=1 / 3,
                                                                            random_state=355)
                        x_train = load_preprocess.scaling(x_train)
                        x_test = load_preprocess.scaling(x_test)

                        model_find = model_finder.Model_Finder() # object initialization

                        # getting the best model for each of the clusters
                        best_model_name, best_model = model_find.get_best_model(x_train, y_train, x_test, y_test)

                        # saving the best model to the directory.
                        file_op = model_operations.Model_Operation()
                        save_model = file_op.save_model(best_model, best_model_name + str(i))

        except Exception as e:
                raise e


