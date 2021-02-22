import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_moons


class FCM:
    def __init__(self, cluster_number, dimension, fuzzy_coefficient):
        """
        :param cluster_number: number of center
        :param dimension: data X ∈ R^dimention
        """
        self.cluster_num = cluster_number
        self.dimension = dimension
        self.fuzzy_coefficient = fuzzy_coefficient

    def make_data(self):
        self.X_data, self.Y_data = make_moons(100, noise=.04, random_state=0)
        one_index = np.where(self.Y_data == 1)
        zero_index = np.where(self.Y_data == 0)
        plt.scatter(self.X_data[one_index, 0], self.X_data[one_index, 1], c='r')
        plt.scatter(self.X_data[zero_index, 0], self.X_data[zero_index, 1], c='b')
        plt.show()
        self.membership = np.zeros([self.X_data.shape[0], self.cluster_num])

    def farthest_point_sampling(self):
        """ 取Kmeans算法的初始值 """
        num = self.X_data.shape[0]
        center = np.zeros([self.cluster_num, self.dimension])
        initial_index = np.random.randint(0, num)
        center[0, :] = self.X_data[initial_index, :]
        dist_lst = [np.inf for _ in range(num)]
        for i in range(1, self.cluster_num):
            new_ele = center[i - 1, :]
            for j in range(num):
                dist = np.linalg.norm(new_ele - self.X_data[j, :])
                dist_lst[j] = min(dist_lst[j], dist)
            center[i, :] = self.X_data[np.argmax(dist_lst), :]
        return center

    def cluster(self):
        """ 使用 self.membership进行类别判断 """
        center = self.farthest_point_sampling()
        # print("init_miu = ", center)
        # center = np.random.random([self.number, self.dimention])
        old_dist = np.inf
        while True:
            dist = self.optimize_membership(center)
            print("dist = ", dist)
            center = self.optimize_miu()
            if abs(dist - old_dist) < 1e-5:
                break
            old_dist = dist
        self.center = center


    def optimize_membership(self, center_array):
        """ 对隶属度进行优化 """

        for i in range(self.X_data.shape[0]):
            sample_coordinate = self.X_data[i, :self.dimension]
            dist = 0
            for j in range(self.cluster_num):
                centerj = center_array[j, :]
                dis_square = np.power(np.linalg.norm(sample_coordinate - centerj), 2)
                # print("x = ", 2 / (1 - self.fuzzy_coefficient))
                if dis_square != 0:
                    self.membership[i, j] = np.power(dis_square, 1 / (1 - self.fuzzy_coefficient))
                dist += self.membership[i, j]
            self.membership[i, :] = self.membership[i, :] / dist

        total_dist = 0
        for i in range(self.X_data.shape[0]):
            sample_coordinate = self.X_data[i, :self.dimension]
            for j in range(self.cluster_num):
                centerj = center_array[j, :]
                dis_square = np.linalg.norm(sample_coordinate - centerj)
                total_dist += dis_square * dis_square * np.power(self.membership[i, j], self.fuzzy_coefficient)
        return total_dist

    def optimize_miu(self):
        """ 对样本关于隶属度取平均作为新的μ """
        center = np.zeros([self.cluster_num, self.dimension])
        for j in range(self.cluster_num):
            wj = np.power(self.membership[:, j], self.fuzzy_coefficient)
            center[j, :] = sum(np.array([wj]).T * self.X_data[:, :self.dimension]) / \
                           sum(wj)
           
        return center

    def prediction(self):
        dic = {0: "r", 1: "g", 2: "b", 3: "k"}
        plt.figure()
        ax = plt.gca()
        ax.axis("equal")
        index_set = np.array([np.argmax(self.membership[i, :])
                              for i in range(self.X_data.shape[0])])
        for i in range(self.cluster_num):
            index_lst = np.where(index_set == i)
            plt.scatter(self.X_data[index_lst, 0],
                        self.X_data[index_lst, 1],
                        c=dic[i])
            plt.scatter(self.center[i, 0], self.center[i, 1],
                        marker="h", s=10, c="y")


        plt.show()


if __name__ == "__main__":
    a = FCM(2, 2, 3)
    a.make_data()
    a.cluster()
    a.prediction()
    print(a.center)