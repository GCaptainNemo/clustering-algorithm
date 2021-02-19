# FCM聚类算法
## 一、介绍
前面介绍的GMM和K-means聚类算法都可以看做用EM算法求解一个隐变量模型。FCM的出发点是改进K-means优化函数的形式，认为数据点不再是硬分配(hard assignment)取0或者1的形式，而是具有某种隶属度u<sub>ij</sub>，
优化目标函数如下所示：

![FCM loss function](resources/FCM_loss_function.jpg)

优化变量为均值v<sub>j</sub>和隶属度u<sub>ij</sub>，其中u<sub>ij</sub>的幂次m称为模糊稀疏(fuzzy coefficient)，和聚类个数同为超参数。
FCM优化方式同样是交替优化，即固定一个变量优化另一个变量，交替进行，直至收敛，FCM每步优化和GMM一样都具有闭式解。

## 二、效果
### 1. 聚类个数为3， 模糊系数取3

![FCM_3.png](result/FCM_3.png)

### 2. 聚类个数为4， 模糊系数取3

![FCM_4.png](result/FCM_4.png)

# 三、总结
如果从概率的角度看FCM的话，可以将其目标函数看作EM算法中的Q函数，E步和M步分别对应着对隶属度进行优化和对每类均值进行优化。隶属度相当于对隐变量的后验概率，但是有一点不同的是，FCM没法进行prediction，即无法预测新样本的类别。而GMM和K-means这样的模型可以预测新样本的类别。

# 四、参考资料
1. [website](https://zhuanlan.zhihu.com/p/85244505)
