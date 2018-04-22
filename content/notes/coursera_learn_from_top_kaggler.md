Title: How to Win a Data Science Competition: Learn from Top Kagglers | Coursera
Date: 2018-04-22 22:36
Modified: 2018-04-22 22:36
Slug: coursera-learn-from-top_kaggler
Authors: Joey Huang
Summary: How to Win a Data Science Competition: Learn from Top Kagglers 笔者
Status: draft

## 机器学习算法总结

### 机器学习算法的分类

* Linear: scikit-learn(@); vowpal wabbit
  Split space into 2 subspaces
* Tree-based: scikit-learn; XGBoost(@); LightGBM(@)
  Split space into boxes
* kNN: scikit-learn
  heavy rely on how to measure points "closeness"
* Neural Networks: Pytorch(@); TensorFlow; mxnet; Lasagne
  Produce smooth non-linear decision boundary

VOWPAL WABBIT: 处理超大型数据的 Linear 算法库
Pytorch: 更符合 Python/Unix 的设计哲学；更简单易懂；适合学术型研究。
TensorFlow: 完整的工具链，适合产品经应用；但构造模型不直观，对程序员来说难以理解。

参考链接：https://www.zhihu.com/question/65578911/answer/249995561

经验总结：
一般情况下，GBDT (Gradient Boost Decision Tree like XGBoost, LightGBM) 和 Neural Networks 是更强大的算法。但有时，可以考虑 Linear 和 kNN，它们在有些场景下可以实现更快的训练和更高的准确率。

### 不同的算法特点

不同算法适用范围不同，特别是每种算法的决策边界形状不同导致了不同的算法对不同的数据分布形状有不同的准确性和通用性。需要熟悉每种算法的决策边界的特征，然后根据数据的分布情况，选择合适的算法模型。

参阅链接：http://scikit-learn.org/stable/auto_examples/classification/plot_classifier_comparison.html


