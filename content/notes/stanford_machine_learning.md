Title: Machine Learning
Date: 2015-08-29 20:20
Modified: 2015-08-29 20:20
Slug: machine-learning
Authors: Joey Huang
Summary: Notes of Stanford Machine Learning, by Andrew Ng, on www.coursera.org
Status: draft

## 机器学习

课程在 [Coursera][1] 上, 讲师是 Andrew Ng。PDF 格式的课件在 [Stanford 网站][2]上。课程讨论组在[这里][3]可以找到。

## Week 1

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

* Cost Function: 成本函数，用来测量模型的准确度
* Gradient Descent: 阶梯下降，假设的模型逐步逼近真实数据的过程

REF: 
1. [Linear Regression with One Variable][4]
2. [Partial derivative in gradient descent for two variables][5]

根据上面两个链接推导出阶梯下降函数。

### 数学

* [导函数][5]
* [线性代数][6]
* [最小二阶乘数拟合数据][7]

[1]: https://www.coursera.org/learn/machine-learning/home/welcome
[2]: http://cs229.stanford.edu/materials.html
[3]: https://www.coursera.org/learn/machine-learning/discussions?sort=lastActivityAtDesc&page=1
[4]: https://www.coursera.org/learn/machine-learning/supplement/Mc0tF/linear-regression-with-one-variable
[5]: http://math.stackexchange.com/questions/70728/partial-derivative-in-gradient-descent-for-two-variables/189792#189792
[6]: https://www.coursera.org/learn/machine-learning/supplement/NMXXL/linear-algebra-review
[7]: https://en.wikipedia.org/wiki/Linear_least_squares_%28mathematics%29#Derivation_of_the_normal_equations
