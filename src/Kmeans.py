import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_moons
from matplotlib.patches import Ellipse

class kmeans:
    def __init__(self, cluster_number, dimension):
        """
        :param cluster_number: number of center
        :param dimension: data X ∈ R^dimention
        """
        self.cluster_num = cluster_number
        self.dimension = dimension

    def make_data(self):
        self.X_data, self.Y_data = make_moons(100, noise=.04, random_state=0)
        one_index = np.where(self.Y_data == 1)
        zero_index = np.where(self.Y_data == 0)
        plt.scatter(self.X_data[one_index, 0], self.X_data[one_index, 1], c='r')
        plt.scatter(self.X_data[zero_index, 0], self.X_data[zero_index, 1], c='b')
        plt.show()
        self.index_set = np.zeros(self.X_data.shape[0])

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
        center = self.farthest_point_sampling()
        # print("init_miu = ", center)
        # center = np.random.random([self.number, self.dimention])
        old_dist = np.inf
        while True:
            dist = self.e_step(center)
            center = self.m_step()
            if abs(dist - old_dist) < 1e-5:
                break
            old_dist = dist
        self.center = center

    def e_step(self, center_array):
        """ 求离各中心最近样本的指标集，相当于对样本指标集进行了一个划分 """
        dist = 0
        for i in range(self.X_data.shape[0]):
            sample_coordinate = self.X_data[i, :self.dimension]
            min_dis = np.inf
            for j in range(self.cluster_num):
                centerj = center_array[j, :]
                dis = np.linalg.norm(sample_coordinate - centerj)
                if dis < min_dis:
                    min_dis = dis
                    self.index_set[i] = j
            dist += min_dis
        return dist

    def m_step(self):
        """ 对样本关于划分的指标集取平均作为新的中心 """
        center = np.zeros([self.cluster_num, self.dimension])
        for i in range(self.cluster_num):
            index_lst = np.where(self.index_set == i)
            center[i, :] = np.mean(self.X_data[index_lst, :])
        return center

    def prediction(self):
        dic = {0: "r", 1: "g", 2: "b", 3: "k"}
        plt.figure()
        ax = plt.gca()
        ax.axis("equal")
        for i in range(self.cluster_num):
            index_lst = np.where(self.index_set == i)
            plt.scatter(self.X_data[index_lst, 0],
                        self.X_data[index_lst, 1],
                        c=dic[i])
            plt.scatter(self.center[i, 0], self.center[i, 1],
                        marker="h", s=10, c="y")

            for nsig in range(1, 3):
                ellipse = Ellipse(self.center[i, :], nsig, nsig,
                        0)
                ax.add_patch(ellipse)
                ellipse.set(alpha=0.1,
                            color='lightskyblue'
                            )
        plt.show()


if __name__ == "__main__":
    a = kmeans(4, 2)
    a.make_data()
    a.cluster()
    a.prediction()
    print(a.center)