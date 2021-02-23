# 谱聚类(Spectral clustering)算法
## 1. 介绍
谱聚类基于图论中无向带权图(undirected weighted graph)的切图，是解决松弛版本加了平衡条件(balancing condition)最小割问题的方法。
一个无向带权图可以表示成G = (V, E)有序二元组的形式，其中V代表图中所有节点的集合，E代表所有边的集合，
相似矩阵W又称为邻接矩阵，其中的元素W<sub>ij</sub>衡量的是点i和点j的相似度。

### 1.1 计算邻接矩阵(Adjacence matrix)
观测数据只是图上的顶点，首先需要给观测数据赋予图的拓扑结构和权重，
或者说计算图的邻接矩阵(Adjacence matrix)，这两者是等价的。
有三种方式计算邻接矩阵(又称为相似度矩阵)：近邻法(ε-neighborhood graph)，k近邻法(k-nearest nerghbor graph)，全连接法(fully connected graph)。

#### 1.1.1 ε-neighborhood graph

![ε-neighborhood graph](../resources/Spectral_clustering/SC_episilon.jpg)

可以看到ε-neighborhood graph把带权图退化成无权图。

### 1.1.2 k-nearest nerghbor graph

![k-nearest nerghbor graph](../resources/Spectral_clustering/SC_K_neighbour.jpg)

### 1.1.3 fully connected graph

该方法认为数据构成的图是一张全连接图

![fully connected graph](../resources/Spectral_clustering/SC_fully_connect.jpg)


## 1.2 Laplacian matrix

### 1.2.1 Unnormalized Laplacian Matrix
图论中有四大矩阵：
1. Degree matrix D
2. Adjacency matrix W
3. Laplacian matrix L
4. Incidence matrix A

其中 L = D - W = A<sup>T</sup>A，其中D是一个对角阵，对角元素等于W每行元素的和。考虑矩阵L的二次型：

![laplace quadratic form](../resources/Spectral_clustering/laplace_quadratic.jpg)

且L**1** = **0** 由此得拉普拉斯矩阵是一个对称半正定矩阵。

### 1.2.2 Normalized Laplacian Matrix

归一化拉普拉斯矩阵有两种表示方法，1. 基于随机游走(Random Walk)的标准化拉普拉斯矩阵L<sub>rw</sub> 2. 对称标准化拉普拉斯矩阵L<sub>sym</sub>，
定义如下：

![normalize laplace](../resources/Spectral_clustering/laplace_normalize.jpg)

不难发现矩阵L<sub>rw</sub> 和矩阵L<sub>sym</sub>相似，具有相同的特征值。除此之外，归一化后的拉普拉斯矩阵有如下性质:

![attribute](../resources/Spectral_clustering/laplace_normalize_attribute.jpg)

不同版本谱聚类算法的区别在于相似度矩阵W的计算方式和拉普拉斯矩阵的计算方法，其它步骤基本相同。

## 1.3 谱聚类算法模板
n个样本点聚成k类：
1. 计算相似度矩阵W
2. 计算度矩阵D
3. 计算Laplace矩阵L(标准化或者非标准化)
4. 计算L的特征值，特征值从小到大排列，取前k个特征值对应的特征向量，构成矩阵U∈R<sup>n×k</sup>
5. 使用K-means或其它聚类算法将U的每一行作为数据新的表示聚成k类

**注意**：
1. 在sklearn中默认是使用K-Means算法，也可以用其它聚类算法，比如在R<sup>k</sup>中用一个超平面分类。
2. 该算法模板对于L和L<sub>rw</sub>矩阵是完全一致的，但对于L<sub>sym</sub>，还需要在聚类前加一步行归一化。

为什么可以用Laplace矩阵最小特征值对应的特征向量作为数据新的表示进行聚类？这里给出一个直观的解释，回看1.2.1节Laplace矩阵的二次型，
考虑最小化该二次型，对于那些w<sub>ij</sub>较大的点(即数据i和j的相似程度较高)，(xi-xj)<sup>2</sup>会较小，
所以如果最小化该二次型会趋向于给w<sub>ij</sub>较大的两个数据点相近的xi和xj，xi和xj就可以用来作为原数据聚类的一个表示。
此外谱聚类还可以理解为将高维空间的数据映射到低维嵌入空间(embedding space),又称为谱嵌入(spectral embedding)，然后在低维嵌入空间进行聚类。

## 1.4 理解谱聚类的不同视角
谱聚类最常见的理解是一种解决松弛版本加了平衡条件的图最小割问题的方法。对NormalCut问题松弛即归一化谱聚类，对RatioCut问题松弛即非归一化谱聚类。
但需要注意的是，松弛问题的解和原问题的解之间的差距可以任意大，也就是说谱聚类不一定能找到加了平衡条件最小割问题一个足够好的解。谱聚类之所以吸引人，
是因为它把聚类问题变成一个简单的线性代数问题。除此之外，谱聚类还可以用随机游走(random walk)和扰动理论(perturbation theory)理解，参考
**A Tutorial on Spectral Clustering**。

## 2. 效果

经过试验，使用不同的Laplacian矩阵对聚类结果的影响并不大。这里采用全连接图，未归一化的Laplace矩阵。

#### 1. variance = 1， K = 2

![SC_2](../result/Spectral_clustering/SC_2.png)

#### 2. variance = 0.1， K = 3

![SC_3](../result/Spectral_clustering/SC_3.png)

##  3. 总结
1. 谱聚类是一种用Laplace矩阵较小特征值对应的特征向量作为特征进行聚类的算法。相当于将原数据映射到了一个低维的嵌入空间中，
因此谱聚类适合用于高维数据的聚类。
2. 当聚类类别多的时候不建议使用谱聚类。
3. 谱聚类对相似度矩阵的改变和方差的改变十分敏感，往往需要调参。
4. 谱聚类适合用于均衡分类问题，即各簇之间的点数差别不大。


##  4. 参考资料
1. [A Tutorial on Spectral Clustering](http://yaroslavvb.com/papers/luxburg-tutorial.pdf)










