Title: Machine Learning
Date: 2015-08-29 20:20
Modified: 2015-08-29 20:20
Slug: machine-learning
Authors: Joey Huang
Summary: Notes of Stanford Machine Learning, by Andrew Ng, on www.coursera.org
Status: draft

[TOC]

## 机器学习

课程在 [Coursera][1] 上, 讲师是 Andrew Ng。PDF 格式的课件在 [Stanford 网站][2]上。课程讨论组在[这里][3]可以找到。

## Week 1 机器学习介绍

### What is Machine Learning?

Two definitions of Machine Learning are offered. Arthur Samuel described it as: "the field of study that gives computers the ability to learn without being explicitly programmed." This is an older, informal definition.

Tom Mitchell provides a more modern definition: "A computer program is said to learn from experience E with respect to some class of tasks T and performance measure P, if its performance at tasks in T, as measured by P, improves with experience E."

Example: playing checkers.

* E = the experience of playing many games of checkers
* T = the task of playing checkers.
* P = the probability that the program will win the next game.

### Supervised learning

> In supervised learning, we are given a data set and already know what our correct output should look like, having the idea that there is a relationship between the input and the output.

> Supervised learning problems are categorized into "regression" and "classification" problems. In a regression problem, we are trying to predict results within a continuous output, meaning that we are trying to map input variables to some continuous function. In a classification problem, we are instead trying to predict results in a discrete output. In other words, we are trying to map input variables into discrete categories.

1. Supervised learning: 结果形式己知的机器学习。比如，从过往销售数据，预测未来三个月的销售数据。
1. Classfication learning: 输出结果是离散的。
2. Regression learning: 输出结果是连续的。

### Unsupervised learning

> Unsupervised learning, on the other hand, allows us to approach problems with little or no idea what our results should look like. We can derive structure from data where we don't necessarily know the effect of the variables.

> With unsupervised learning there is no feedback based on the prediction results, i.e., there is no teacher to correct you. It’s not just about clustering.

数据挖掘，从给定的数据集合里去发现规律，进行模式匹配。结果形式不可知。计算结果无法对数据进行反馈。

**例子：声音处理**
从一个有背景音乐的吵杂的会议中演讲的录音文件中，通过数据挖掘和特征匹配来处理这段录音，最终分离出演讲录音和音乐。

* Supervised learning: Given email labed as spam/not spam; learn a email filter.
* Unsupervised learning: Given as set of news articles found on web, group them as a set of articles about the same story.
* Unsupervised learning: Given a set of customer data, automatically discover the market segment and group customers into different market segment.
* Supervised learning: Given a dataset of patients diagnosed as either having diabets or not, learn to classify new patients as having diabets or not.

### 线性回归算法

* Cost Function: 成本函数，用来测量模型的准确度。成本函数把把建模问题转换为求成本函数的极小值。
* Contour plots: 等高线。多参数的成本函数里，有一组参数的值会有相同的成本。这些参数联接起来就是成本函数的等高线。
* Gradient Descent: 阶梯下降，假设的模型逐步逼近真实数据的过程

REF:
1. [Linear Regression with One Variable][4]
2. [Partial derivative in gradient descent for two variables][5]

根据上面两个链接推导出阶梯下降函数。

### 数学

* [微积分][5] 四个最简单的规则
	* 针对 $F(x) = cx^n$，其导函数是 $F'(x) = cn\times{x^{(n-1)}}$
	* 常数的导数是 0
	* 导函数可以穿透累加器，即 $\displaystyle\frac{\partial}{\partial x_0}\sum_{i=0}^nF(x_i) = \sum_{i=0}^n\frac{\partial}{\partial x_0}F(x_i)$
	* 微分传导机制，即$\displaystyle\frac{\partial}{\partial x}g(f(x)) = g'(f(x))\times f'(x)$
* [线性代数][6]
* [最小二阶乘数拟合数据][7]
* 概率论复习

### 术语

* Calculus: 微积分
* Partial derivatives: 偏导数
* Derivatives: 导数
* Gradient Descent: 梯度下降
* Cost Function: 成本函数
* Contour plots: 等高线
* Least Mean Squares: LSM, 最小均方

### TODO

* 使用 markdown + MathJax 来书写数学公式
    * [MathJax 简明中文教程][13] 这是一个质量很高的博客文章
    * [LaTex 教程][8]
    * [LaTex 支持的所有符号列表][9]
* 推导出模型参数的梯度下降公式 (Gradient Descent)
* 推导出 LSM (Widrow-Hoff学习算法)

## Week 2 多变量梯度下降算法

### 多变量梯度下降算法

预测函数：
$$
h(\theta) = \theta_0 + \theta_1 x_1 + \theta_2 x_2 + ... + \theta_n + x_n = \theta^T x^{(i)}
$$
其中，$x_0 = 1$，$x^{(i)}$ 是训练数据集里的第 i 个数据。$\theta_T$ 是 n + 1 维列向量；$x^{(i)}$ 是 n + 1 维行向量。

成本函数：
$$
J(\theta) = \frac{1}{2m} \sum_{(i=0)}^n \left( h(\theta) - y^{(i)} \right)^2
$$

迭代函数：
$$
\theta_j = \theta_j - \alpha \sum_{i=0}^m \left(\left(h(x^{(i)}) - y^{(i)}\right) x_j^{(i)}\right)
$$

### 变量缩放 Feature Scaling

当变量在 [-1, 1] 这个范围内时，梯度下降算法能较快地收敛。可以使用下面的公式来缩放变量，以让变量在快速收敛的范围内：

$$
x_i := \frac{x_i - \mu_i}{s_i}
$$

其中，$\mu_i$ 是 $x_i$ 的平均值，即 $\mu_i = \frac{1}{n} \sum_{i=1}^n x_i$， $s_i$ 是 $x_i$ 的范围，即 $s_i = max(x_i) - min(x_i)$。

经过这样的转换，变量的范围全部落在 [-0.5, 0.5] 之间。

### 学习率

使用 $\alpha$ 来表示学习率，值太高会导致无法收敛，太低收敛又太慢。一个好的办法是画出成本函数 $J(\theta)$ 随着迭代次数不断变化的曲线。这样可以直观地观察到随着迭代地不断进行，成本函数的值的变化情况。在实际情况中，可以从几个经验值里去偿试，比如 0.0001, 0.0003, 0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1。


### 标准方程 Normal Equalation

通过微分公式可以知道，我们要求成本函数 $J(\theta)$ 的最小值，只需要令其偏导数为零，即：
$$
\frac\partial{\partial{\theta_j}}J(\theta) := 0
$$

把 $J(\theta)$ 用矩阵来表示，并根据矩阵运算定律最终可以推导出下面的方程式：

$$
\theta = \left( X^T X \right)^{-1} X^T y
$$

推导过程可参阅 [cs229-notes1.pdf][10]。推导过程会用到大量的矩阵运算知识。其中 X 是训练数据集，y 是结果数据向量。这样我们就可以通过直接计算的方式，而不是线性回归的方式来求得参数 $\theta$ 的值。


### Octave 教程

#### Octave 基本教程

可以和 numpy, scipy 等结合起来学习。实际上接口较为类似。

#### 向量化

向量化可以让代码运算更简洁，效率更高。比如，我们的预测函数的普通形式可以写成：

$$
h_\theta(x) = \sum_{i=0}^{n} \theta_ix^{(i)}
$$

那么其 Octave 代码如下：

```matlab
prediction = 0.0
for i=1:n+1,
    prediction = predicition + theta(i) * x(i)
end;
```

我们也可以把预测函数向量化：

$$
h_\theta(x) = \theta^T x
$$

这样，我们的预测函数可以实现如下：

```matlab
prediction = theta' * x
```

另外一个例子是梯度下降算法里的参数迭代函数：

$$
\theta_j = \theta_j - \alpha \frac{1}{m} \sum_{i=1}^{m} \left( h_\
theta(x^{(i)}) -y^{(i)} \right) x_j^{(i)}
$$

我们可以向量化为：

$$
\theta = \theta - \alpha \delta
$$

其中，$\theta$ 是个 n + 1 维向量；$\alpha$ 是一个标量；$\delta$ 是一个 n + 1 维向量。$\delta$ 可以向量化为：

$$
\delta = \frac{1}{m} \sum_{i=1}^{m} \left( h_\theta(x^{(i)}) - y^{(i)} \right) x^{(i)}
$$

其中，$\left( h_\theta(x^{(i)}) - y^{(i)} \right)$ 是个标量；$x^{(i)}$ 是个 n + 1 维向量，其行元素为 $x^{(i)}_0, x^{(i)}_1, x^{(i)}_2 ... x^{(i)}_n$，其上标为第 i 项训练样例数据，下标为第 j 项变量；而 m 项求和，实际上可以看成是一个线性方程组的表达形式。

#### 通用方程和奇异矩阵

$$
\theta = (X^T X)^{-1} X^T y
$$

这是我们的通用方程，当训练数据集较少时，利用矩阵运算可以较快的算出参数 $\theta$ 的值。但如果 $X^T X$ 是奇异矩阵的话，它就没有逆矩阵存在，这个时候通用方程的解是什么呢？答案是，在 octave 里用 `pinv` 来代替 `inv` 来计算逆矩阵。这样即使 $X^T X$ 是奇异矩阵，`pinv` 也能算出其"伪"逆矩阵，从而顺利算出通用方向的解。

那么，物理上讲，$X^T X$ 如果为奇异矩阵的话，到底代表什么意思呢？

* 模型变量之间线性相关
  比如，在房价预测模型里，$x_1$ 代表房子的长度，$x_2$ 代表房子的宽度，而 $x_3$ 代表房子的面积，这里假设房子是方形的，那么实际上 $x_3$ 和 $x_1, x_2$ 是线性相关的。
* 训练样例少于变量个数，即 m < n
  这种情况下，需要减少变量个数来解决问题

### TODO

1. 如何从数学上证明变量绽放后能较快收敛？
2. 可以使用 `pylab` 的等高线在二维平面上画出成本函数和两个参数的关系图
3. 找一个数据集，选择不同的学习率来实现，画出不同学习率时的成本函数随着迭代次数的变化情况
4. 总结 matlab/octave 和 scipy/numpy 在数值计算上的差异和优缺点

## Week 3 分类回归算法 Logistic Regression

### 分类及其表现形式 Classification and Representation

#### 引言 为什么需要分类回归算法

分类问题的值是离散的，如果考虑二元分类总是，则其值是 0 或 1。如果用 linear regresstion 来作为分类问题的预测函数是不合理的。因为因为预测出来的数值可能远小于 0 或远大于 1。我们需要找出一个预测函数模型，使其值的输出在 [0, 1] 之间。

#### 逻辑回归预测函数的表现形式 Hypothesis Representation

**逻辑回归预测函数**

线性回归算法的预测函数是 $h_\theta(x) = \theta^T x$，为了让预测函数的输出值在 [0, 1] 之间，我们给定逻辑回归模型 (Logistic Regression Model) $g(z) = \frac{1}{1 + e^{-z}}$，则我们的逻辑回归模型的预测函数如下：

$$
h_\theta(x) = g(\theta^T x) = \frac{1}{1 + e^{-\theta^T x}}
$$

**解读逻辑回归预测函数的输出值**

$h_\theta(x)$ 表示针对输入值 $x$ 以及参数 $\theta$ 的前提条件下，$y=1$ 的概率。用概率论的公式可以写成：

$$
h_\theta(x) = P(y=1 \vert x; \theta)
$$

上面的概率公式可以读成：**在输入 $x$ 及参数 $\theta$ 条件下 $y=1$ 的概率**。由概率论的知识可以推导出，

$$
P(y=1 \vert x; \theta) + P(y=0 \vert x; \theta) = 1
$$

#### 判定边界 Decision Boundary

**从逻辑回归公式说起**

逻辑回归预测函数由下面两个公式给出的：

$$
h_\theta(x) = g(\theta^T x)
$$

$$
g(z) = \frac{1}{1 + e^{-z}}
$$

假定 $y=1$ 的判定条件是 $h_\theta(x) \geq 0.5$，$y=0$ 的判定条件是 $h_\theta(x) < 0.5$，则我们可以推导出 $y=1$ 的判定条件就是 $\theta^T x \geq 0$，$y=0$ 的判定条件就是 $\theta^T x < 0$。所以，$\theta^T x = 0$ 即是我们的判定边界。

**判定边界**

假定我们有两个变量 $x_1, x_2$，其逻辑回归预测函数是 $h_\theta(x) = g(\theta_0 + \theta_1 x_1 + \theta_2 x_2)$。假设我们给定参数

$$
\theta = \begin{bmatrix} -3 \\\\ 1 \\\\ 1 \end{bmatrix}
$$

那么我们可以得到判定边界 $-3 + x_1 + x_2 = 0$，即 $x_1 + x_2 = 3$，如果以 $x_1$ 为横坐标，$x_2$ 为纵坐标，这个函数画出来就是一个通过 (0, 3) 和 (3, 0) 两个点的斜线。这条线就是我们的判定边界。

**非线性判定边界**

如果预测函数是多项式 $h_\theta(x) = g(\theta_0 + \theta_1 x_1 + \theta_2 x_2 + \theta_3 x_1^2 + \theta_4 x_2^2)$，且给定 $\theta^T = \left[ -1 0 0 1 1\right]$，则可以得到判定边界函数

$$
x_1^2 + x_2^2 = 1
$$

还是以 $x_1$ 为横坐标，$x_2$ 为纵坐标，则这是一个半径为 1 的圆。这是二阶多项式的情况，更一般的多阶多项式可以表达出更复杂的判定边界。

### TODO

1. 使用 pylab 画出 逻辑回归预测函数的图形
2. 是否有类似 MathJax 类似的，使用 JavaScript 来在网页上画图的库呢？[这里][12]有个相似的问题。
3. 复习[概率论][11]基础知识


[1]: https://www.coursera.org/learn/machine-learning/home/welcome
[2]: http://cs229.stanford.edu/materials.html
[3]: https://www.coursera.org/learn/machine-learning/discussions?sort=lastActivityAtDesc&page=1
[4]: https://www.coursera.org/learn/machine-learning/supplement/Mc0tF/linear-regression-with-one-variable
[5]: http://math.stackexchange.com/questions/70728/partial-derivative-in-gradient-descent-for-two-variables/189792#189792
[6]: https://www.coursera.org/learn/machine-learning/supplement/NMXXL/linear-algebra-review
[7]: https://en.wikipedia.org/wiki/Linear_least_squares_%28mathematics%29#Derivation_of_the_normal_equations
[8]: http://www.forkosh.com/mathtextutorial.html
[9]: http://mirrors.ctan.org/info/symbols/math/maths-symbols.pdf
[10]: http://cs229.stanford.edu/notes/cs229-notes1.pdf
[11]: http://cs229.stanford.edu/section/cs229-prob.pdf
[12]: http://stackoverflow.com/questions/119969/javascript-chart-library
[13]: http://mlworks.cn/posts/introduction-to-mathjax-and-latex-expression/
