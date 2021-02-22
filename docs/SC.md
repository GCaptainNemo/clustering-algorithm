# 谱聚类(Spectral clustering)算法
## 1. 介绍
谱聚类基于图论中无向带权图的切图，一个无向带权图可以表示成G = (V, E, W)有序三元组的形式，其中V代表图中所有节点的集合，E代表所有边的集合，
W代表边上所有权重的集合(衡量的是相似度，即两个点的距离越远则权重越小)。

### 1.1 计算邻接矩阵(Adjacent matrix)
观测数据只是图上的顶点，首先需要给观测数据赋予图的拓扑结构，
或者说用某种规则计算图的邻接矩阵(Adjacent matrix)，这两者是等价的。
这里用三种方式计算邻接矩阵(又称为相似度矩阵)：近邻法(ε-neighborhood graph)，k近邻法(k-nearest nerghbor graph)，全连接法(fully connected graph)。

#### 1.1.1 ε-neighborhood graph

![ε-neighborhood graph](../resources/Spectral_clustering/SC_episilon.jpg)
可以看到ε-neighborhood graph把带权图退化成无权图。

### 1.1.2 k-nearest nerghbor graph

![k-nearest nerghbor graph](../resources/Spectral_clustering/SC_K_neighbour.jpg)

### 1.1.3 fully connected graph

该方法认为数据构成的图是一张全连接图
![fully connected graph](../resources/Spectral_clustering/SC_fully_connect.jpg)










