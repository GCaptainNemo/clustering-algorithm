# DBSCAN 聚类算法
## 一、简介
DBSCAN(Density-Based Spatial Clustering of Applications with Noise)是一种基于密度，对噪声具有鲁棒性的空间聚类算法。
DBSCAN算法认为，数据之所以可以聚类成团簇，是因为团簇类数据点的密度比团簇外的点的密度高得多。此外，区域中噪声的密度比任何
团簇中数据点的密度低得多。具体来说，DBSCAN算法需要赋予两个参数，半径R和最小点数minPts。点p属于某个团簇，则必定存在q属于该团簇，且
以点q为中心半径为R的邻域内需要超过最小点数minPts，且包括p。即密度需超过一个阈值。