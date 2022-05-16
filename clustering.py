import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator

import model_operations


class KMeansClustering:
    #def __init__(self):
        #s
    def elbow_plot(self,data):
        wcss=[]
        try:
            #for i in range (1,11):
            #    kmeans=KMeans(n_clusters=i,init='k-means++',random_state=42)
            #    kmeans.fit(data)
            #   wcss.append(kmeans.inertia_)
            #plt.plot(range(1,11),wcss)
            #plt.title('The Elbow Method')
            #plt.xlabel('Number of clusters')
            #plt.ylabel('WCSS')
            #plt.savefig('preprocessing_data/K-Means_Elbow.PNG')
            # finding the value of the optimum cluster programmatically
            #self.kn = KneeLocator(range(1, 11), wcss, curve='convex', direction='decreasing')
            return 3 #self.kn.knee

        except Exception as e:
            raise Exception()

    def create_clusters(self,data,number_of_clusters):
        self.data=data
        try:
            print('create cluster')
            self.kmeans = KMeans(n_clusters=number_of_clusters, init='k-means++', random_state=42)
            self.y_kmeans=self.kmeans.fit_predict(data) #  divide data into clusters

            self.file_op = model_operations.Model_Operation()
            self.save_model = self.file_op.save_model(self.kmeans, 'KMeans') # saving the KMeans model to directory
                                                                                    # passing 'Model' as the functions need three parameters

            self.data['Cluster']=self.y_kmeans  # create a new column in dataset for storing the cluster information
            return self.data
        except Exception as e:
            raise Exception()