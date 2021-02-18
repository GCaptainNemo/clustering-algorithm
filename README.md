# 常用聚类算法
聚类属于无监督学习范畴，在没有标注的情况下，对数据种类进行划分(partition)。聚类算法可以看成生成式模型，存在一个不可观测的隐变量Z(类别)，控制着观测数据X的生成。

## 一、高斯混合模型(GMM)
## 1. 简介
高斯混合模型认为观测变量X|θ服从混合高斯分布，隐变量Z服从Categorical分布，x|z,θ 服从高斯分布。其中θ代表高斯分布均值、协方差矩阵、和混合系数的集合，它们都是待优化参数。
使用最大似然估计进行参数估计，即 θ* = argmax (logP(X|θ))。 
## 2. EM算法
GMM采用EM(Expectation Maximization)优化算法求解最优参数θ，EM算法分为E步和M步，其中E步需要求关于隐变量z的后验概率P(z|x, θt)，M步需要极大化Q(θ|θt)函数。具体参考 Andrew Gelman 的
Bayesian Data Analysis 书籍。
## 3. 效果
[data](./result/data.png)



