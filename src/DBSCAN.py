import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_moons, make_blobs

class DBSCAN:
    def __init__(self, radius, min_pts):
        """
        具有噪声的基于密度的聚类算法。
        :param radius: 邻域半径
        :param min_pts: 邻域内点数
        """
        self.radius = radius
        self.min_pts = min_pts

    def make_data(self):
        X_data_noise, y_data = make_blobs(n_samples=10, n_features=2, center_box=(0.25, 0.5), centers=1, cluster_std=1.5)
        X_data, self.Y_data = make_moons(100, noise=.04, random_state=0)
        print("shape = ")
        print(X_data.shape)
        print(X_data_noise.shape)

        self.X_data = np.concatenate([X_data, X_data_noise], axis=0)
        print(self.X_data.shape)
        one_index = np.where(self.Y_data == 1)
        zero_index = np.where(self.Y_data == 0)
        plt.scatter(self.X_data[one_index, 0], self.X_data[one_index, 1], c='r')
        plt.scatter(self.X_data[zero_index, 0], self.X_data[zero_index, 1], c='g')
        plt.scatter(self.X_data[X_data.shape[0]:, 0],
                    self.X_data[X_data.shape[0]:, 1], c='b')
        plt.show()

    def cluster(self):
        """
        两种方法：
        1. 求出所有的kernel point，把kernel point之间距离小于radius的聚成一类
        2. 以unvisitied kernel point为种子点用类似区域生长法的方法进行聚类
        这里采用第二种
        """
        data_num = self.X_data.shape[0]
        self.dis_matrix = np.diag([np.inf for _ in range(data_num)])
        for i in range(data_num):
            for j in range(i + 1, data_num):
                self.dis_matrix[i, j] = np.linalg.norm([self.X_data[i] - self.X_data[j]])
                self.dis_matrix[j, i] = self.dis_matrix[i, j]
        self.musk = np.zeros([data_num, 1])
        self.cluster_num = 0
        for i in range(data_num):
            if self.musk[i, 0] == 0:   # unvisited
                linyu_point_index_lst = np.where(
                    self.dis_matrix[i, :] <= self.radius)[0].tolist()
                if len(linyu_point_index_lst) < self.min_pts:
                    # noise
                    self.musk[i, 0] = -1
                else:
                    # kernel point
                    self.cluster_num += 1
                    self.musk[i, 0] = self.cluster_num

                    stack = []
                    for neighbour_index in linyu_point_index_lst:
                        if self.musk[neighbour_index, 0] in [0, -1]:
                            stack.append(neighbour_index)
                    # stack = linyu_point_index_lst.copy()
                    while stack:
                        last_index = stack.pop()
                        self.musk[last_index, 0] = self.cluster_num
                        new_neighbour_list = np.where(self.dis_matrix[last_index, :] <= self.radius)[0].tolist()
                        if len(new_neighbour_list) >= self.min_pts:
                            for neighbor_index in new_neighbour_list:
                                if self.musk[neighbor_index, 0] in [0, -1]:
                                    stack.append(neighbor_index)

    def prediction(self):
        dic = {0: "r", 1: "g", 2: "b", 3: "k", 4:"y"}
        plt.figure()
        ax = plt.gca()
        ax.axis("equal")
        noise_index_array = np.where(self.musk == -1)[0]
        plt.scatter(self.X_data[noise_index_array, 0],
                    self.X_data[noise_index_array, 1], c=dic[0])
        for i in range(self.cluster_num):
            index_array = np.where(self.musk == i + 1)[0]
            plt.scatter(self.X_data[index_array, 0],
                        self.X_data[index_array, 1],
                        c=dic[i + 1])
        plt.show()


if __name__ == "__main__":
    a = DBSCAN(0.3, 4)
    a.make_data()
    a.cluster()
    a.prediction()
