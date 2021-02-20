import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_moons


class hierachical:
    def __init__(self, cluster_number):
        """
        :param cluster_number: number of center
        :param dimension: data X ∈ R^dimention
        """
        self.cluster_num = cluster_number

    def make_data(self):
        self.X_data, self.Y_data = make_moons(100, noise=.04, random_state=0)
        one_index = np.where(self.Y_data == 1)
        zero_index = np.where(self.Y_data == 0)
        plt.scatter(self.X_data[one_index, 0], self.X_data[one_index, 1], c='r')
        plt.scatter(self.X_data[zero_index, 0], self.X_data[zero_index, 1], c='b')
        plt.show()



    def cluster(self):
        """ bottom-to-top clustering """
        data_num = self.X_data.shape[0]
        dis_matrix = np.diag([np.inf for _ in range(data_num)])
        for i in range(data_num):
            for j in range(i + 1, data_num):
                dis_matrix[i, j] = np.linalg.norm([self.X_data[i] - self.X_data[j]])
                dis_matrix[j, i] = dis_matrix[i, j]
        self.index_lst= [[i] for i in range(data_num)]
        while dis_matrix.shape[0] > self.cluster_num:
            index = np.argmin(dis_matrix)
            row = index // dis_matrix.shape[0]
            column = index % dis_matrix.shape[0]
            print("row = ", row, "column = ", column)
            self.index_lst.append(self.index_lst[row] + self.index_lst[column])
            if row < column:
                self.index_lst.pop(column)
                self.index_lst.pop(row)
            else:
                self.index_lst.pop(row)
                self.index_lst.pop(column)
            new_dis_array = np.zeros(dis_matrix.shape[0])
            for i in range(dis_matrix.shape[0]):
                new_dis_array[i] = min(dis_matrix[i, row], dis_matrix[i, column])
            print("before shape = ", dis_matrix.shape)

            dis_matrix = np.concatenate((dis_matrix, np.array([new_dis_array]).T), axis=1)
            new_dis_array = np.array([np.append(new_dis_array, np.inf)])
            dis_matrix = np.concatenate((dis_matrix, new_dis_array), axis=0)
            print("after shape = ", dis_matrix.shape)

            dis_matrix = np.delete(dis_matrix, [row, column], 0)
            dis_matrix = np.delete(dis_matrix, [row, column], 1)
            print("after delete shape = ", dis_matrix.shape)


    def prediction(self):
        dic = {0: "r", 1: "g", 2: "b", 3: "k"}
        plt.figure()
        ax = plt.gca()
        ax.axis("equal")
        for i in range(self.cluster_num):
            index_lst = np.array(self.index_lst[i])
            plt.scatter(self.X_data[index_lst, 0],
                        self.X_data[index_lst, 1],
                        c=dic[i])

        plt.show()


if __name__ == "__main__":
    a = hierachical(3)
    a.make_data()
    a.cluster()
    a.prediction()
