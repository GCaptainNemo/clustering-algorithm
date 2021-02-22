import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_moons
from matplotlib.patches import Ellipse


class GMM:
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
        miu = np.zeros([self.cluster_num, self.dimension])
        initial_index = np.random.randint(0, num)
        miu[0, :] = self.X_data[initial_index, :]
        dist_lst = [np.inf for _ in range(num)]
        for i in range(1, self.cluster_num):
            new_ele = miu[i - 1, :]
            for j in range(num):
                dist = np.linalg.norm(new_ele - self.X_data[j, :])
                dist_lst[j] = min(dist_lst[j], dist)
            miu[i, :] = self.X_data[np.argmax(dist_lst), :]
        return miu

    def cluster(self):
        miu_lst = self.farthest_point_sampling()
        covariance_lst = [np.eye(self.dimension) for _ in range(self.cluster_num)]
        alpha_lst = [1 / self.cluster_num for _ in range(self.cluster_num)]

        # miu = np.random.random([self.number, self.dimention])
        old_Qfunction = np.inf
        while True:
            wik, Qfunction = self.e_step(miu_lst, covariance_lst, alpha_lst)
            alpha_lst, miu_lst, covariance_lst = self.m_step(wik, miu_lst)
            if abs(Qfunction - old_Qfunction) < 0.1:
                break
            old_Qfunction = Qfunction
        self.alpha_lst = alpha_lst
        self.miu_lst = miu_lst
        self.covariance_lst = covariance_lst
        self.wik = wik

    def e_step(self, miu, covariance, alpha_lst):
        """ 求关于隐变量的后验概率 wik =  p(z|xi,Θt) """
        wik = np.zeros([self.X_data.shape[0], self.cluster_num])
        for i in range(self.X_data.shape[0]):
            sum_ = 0
            for j in range(self.cluster_num):
                vector = np.array([self.X_data[i, :] - miu[j]])
                wik[i, j] = alpha_lst[j] * \
                            np.power(np.linalg.det(covariance[j]), -0.5) \
                            * np.exp(-1/2 * (vector @ np.linalg.inv(covariance[j]) @ vector.T))
                sum_ += wik[i, j]
            wik[i, :] = wik[i, :] / sum_

        Qfunction = 0
        for i in range(self.X_data.shape[0]):
            for j in range(self.cluster_num):
                vector = np.array([self.X_data[i, :] - miu[j]])
                Qfunction += wik[i, j] * np.log(0.0000001 + alpha_lst[j] *
                np.power(np.linalg.det(covariance[j]), -0.5) \
              * np.exp(-1/2 * (vector @ np.linalg.inv(covariance[j]) @ vector.T)))
        print(Qfunction)
        return wik, Qfunction

    def m_step(self, wik, old_miu):
        """ 对Q(Θ|Θt)函数关于Θ求 max """
        wik_ = np.array(wik)
        new_alpha_lst = wik_.sum(axis=0) / self.X_data.shape[0]
        new_miu_lst = np.zeros([self.cluster_num, self.dimension])
        for k in range(self.cluster_num):
            sum_data = np.zeros([self.dimension])
            sum = 0
            for i in range(self.X_data.shape[0]):
                # print("sum_data = ", sum_data)
                # print("X_data = ", self.X_data[i, :self.dimention] )
                sum_data += self.X_data[i, :self.dimension] * wik_[i, k]
                sum += wik_[i, k]
            new_miu_lst[k, :] = sum_data / sum

        new_covariance_lst = [np.zeros(self.dimension) for _ in range(self.cluster_num)]
        for k in range(self.cluster_num):
            sum_variance = np.zeros([self.dimension, self.dimension])
            sum = 0
            for i in range(self.X_data.shape[0]):
                vector = np.array([self.X_data[i, :] - old_miu[k]])
                sum_variance += vector.T * vector * wik_[i, k]
                sum += wik_[i, k]
            new_covariance_lst[k] = sum_variance / sum

        return new_alpha_lst, new_miu_lst, new_covariance_lst

    def prediction(self):
        dic = {0: "r", 1: "g", 2: "b", 3: "k"}
        plt.figure()
        ax = plt.gca()
        ax.axis("equal")
        index_set = np.array([np.argmax(self.wik[i, :]) for i in
                              range(self.X_data.shape[0])])
        for i in range(self.cluster_num):
            index_lst = np.where(index_set == i)
            plt.scatter(self.X_data[index_lst, 0],
                        self.X_data[index_lst, 1],
                        c=dic[i])
            plt.scatter(self.miu_lst[i, 0], self.miu_lst[i, 1],
                        marker="h", s=10, c="y")

            for nsig in range(1, 3):
                covariance_matrix = self.covariance_lst[i]
                u, s, vT = np.linalg.svd(covariance_matrix)
                width, height = 2 * np.sqrt(s)
                angle = np.degrees(np.arctan2(u[1, 0], u[0, 0]))
                ellipse = Ellipse(self.miu_lst[i, :], nsig * width, nsig * height, angle)
                ax.add_patch(ellipse)
                ellipse.set(alpha=0.1,
                            color='lightskyblue'
                            )
        plt.show()


if __name__ == "__main__":
    a = GMM(2, 2)
    a.make_data()
    a.cluster()
    a.prediction()
