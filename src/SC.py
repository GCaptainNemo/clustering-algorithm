import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_moons
import heapq
from src.Kmeans import kmeans

class Spectral_custering:
    def __init__(self, cluster_number, graph_option="fc", *args):
        """
        :param cluster_number: number of center
        :param graph_option:
            fc: fully connected graph
            mutual_knn: mutual knn graph
            knn: knn graph
            episilon: episilon-neighbour graph
        """
        self.cluster_num = cluster_number
        self.graph_option = graph_option
        self.parameter = args

    def make_data(self):
        self.X_data, self.Y_data = make_moons(100, noise=.04, random_state=0)
        one_index = np.where(self.Y_data == 1)
        zero_index = np.where(self.Y_data == 0)
        plt.scatter(self.X_data[one_index, 0], self.X_data[one_index, 1], c='r')
        plt.scatter(self.X_data[zero_index, 0], self.X_data[zero_index, 1], c='b')
        plt.show()

    def cluster(self):
        """ spectral clustering """
        self.adjacent_matrix = self.cal_adjacent_matrix(self.graph_option, *self.parameter)
        self.degree_matrix = np.diag(np.sum(self.adjacent_matrix, axis=0))
        self.cal_laplace_matrix()
        [egvalue, egvector] = np.linalg.eig(self.laplace_matrix)
        # 找出特征值中最小的K个数的索引
        min_num_index_list = list(map(list(egvalue).index,
                                     heapq.nsmallest(self.cluster_num, list(egvalue))))
        Rnk = egvector[:, min_num_index_list]
        self.kmeans_obj = kmeans(self.cluster_num, self.cluster_num)
        self.kmeans_obj.X_data = Rnk
        self.kmeans_obj.index_set = np.zeros(self.kmeans_obj.X_data.shape[0])
        self.kmeans_obj.cluster()

    def cal_adjacent_matrix(self, graph="fc", *args):
        if graph == "fc":
            # 全连接图
            variance = args[0]
            data_num = self.X_data.shape[0]
            adjacent_matrix = np.zeros([data_num, data_num])
            for i in range(data_num):
                for j in range(i + 1, data_num):
                    adjacent_matrix[i, j] = np.exp(-np.linalg.norm([self.X_data[i] - self.X_data[j]]) /
                                                   (2 * variance))
                    adjacent_matrix[j, i] = adjacent_matrix[i, j]
        elif graph == "mutual_knn":
            k = args[0]
            variance = args[1]
            data_num = self.X_data.shape[0]
            dist_matrix = np.zeros([data_num, data_num])
            for i in range(data_num):
                for j in range(i + 1, data_num):
                    dist_matrix[i, j] = np.linalg.norm([self.X_data[i] - self.X_data[j]])
                    dist_matrix[j, i] = dist_matrix[i, j]

            adjacent_matrix = np.zeros([data_num, data_num])
            for i in range(data_num):
                for j in range(i + 1, data_num):
                    i_knn = list(map(list(dist_matrix[i, :]).index,
                                                  heapq.nsmallest(k + 1, list(dist_matrix[i, :]))))
                    j_knn = list(map(list(dist_matrix[j, :]).index,
                                     heapq.nsmallest(k + 1, list(dist_matrix[j, :]))))
                    if (j in i_knn) and (i in j_knn):
                        adjacent_matrix[i, j] = np.exp(-np.linalg.norm([self.X_data[i] - self.X_data[j]]) /
                                                       (2 * variance))
                        adjacent_matrix[j, i] = adjacent_matrix[i, j]
        elif graph == "knn":
            k = args[0]
            variance = args[1]
            data_num = self.X_data.shape[0]
            dist_matrix = np.zeros([data_num, data_num])
            for i in range(data_num):
                for j in range(i + 1, data_num):
                    dist_matrix[i, j] = np.linalg.norm([self.X_data[i] - self.X_data[j]])
                    dist_matrix[j, i] = dist_matrix[i, j]

            adjacent_matrix = np.zeros([data_num, data_num])
            for i in range(data_num):
                for j in range(i + 1, data_num):
                    i_knn = list(map(list(dist_matrix[i, :]).index,
                                     heapq.nsmallest(k + 1, list(dist_matrix[i, :]))))
                    j_knn = list(map(list(dist_matrix[j, :]).index,
                                     heapq.nsmallest(k + 1, list(dist_matrix[j, :]))))
                    if (j in i_knn) or (i in j_knn):
                        adjacent_matrix[i, j] = np.exp(-np.linalg.norm([self.X_data[i] - self.X_data[j]]) /
                                                       (2 * variance))
                        adjacent_matrix[j, i] = adjacent_matrix[i, j]
        elif graph == "episilon":
            episilon = args[0]
            data_num = self.X_data.shape[0]
            adjacent_matrix = np.zeros([data_num, data_num])
            for i in range(data_num):
                for j in range(i + 1, data_num):
                    dis = np.linalg.norm([self.X_data[i] - - self.X_data[j]])
                    if dis < episilon:
                        adjacent_matrix[j, i] = adjacent_matrix[i, j] = 1

        return adjacent_matrix

    def cal_laplace_matrix(self, option="unnormalized"):
        if option == "unnormalized":
            self.laplace_matrix = self.degree_matrix - self.adjacent_matrix
        elif option == "sym":
            # Lsym = I - D-0.5WD-0.5
            a = np.power(np.linalg.inv(self.degree_matrix), 0.5)
            self.laplace_matrix = np.eye(self.X_data.shape[0]) - \
                                  a @ self.adjacent_matrix @ a
        elif option == "rw":
            # random walk based
            # Lrw = I - D-1W
            self.laplace_matrix = np.eye(self.X_data.shape[0]) - np.linalg.inv(self.degree_matrix) @ self.adjacent_matrix

    def prediction(self):
        dic = {0: "r", 1: "g", 2: "b", 3: "k"}
        plt.figure()
        ax = plt.gca()
        ax.axis("equal")
        for i in range(self.cluster_num):
            index_lst = np.where(self.kmeans_obj.index_set == i)
            plt.scatter(self.X_data[index_lst, 0],
                        self.X_data[index_lst, 1],
                        c=dic[i])
        plt.show()


if __name__ == "__main__":
    a = Spectral_custering(2, "mutual_knn", 5, 0.1)
    a.make_data()
    a.cluster()
    a.prediction()
