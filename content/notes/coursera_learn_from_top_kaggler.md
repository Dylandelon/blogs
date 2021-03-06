Title: How to Win a Data Science Competition: Learn from Top Kagglers | Coursera
Date: 2018-04-22 22:36
Modified: 2018-04-22 22:36
Slug: coursera-learn-from-top_kaggler
Authors: Joey Huang
Summary: How to Win a Data Science Competition: Learn from Top Kagglers 笔者
Status: draft

## 机器学习算法总结

[TOC]

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

## 特征预处理

特征有不同的数据类型，典型地有数值型（numeric feature），类别（categories feature），文本（text feature），图像（image feature）等等。不同的特征有不同的预处理方法。不同的特征的处理方法还和使用的模型相关。

比如 Tatinac dateset 里，pclass 是一个 categories feature，分别用 1，2，3 表示不同等级的座位。如果我们使用 linear model 来拟合模型，座位级别和幸存之间的关系可能不是线性的，此时模型的拟合效果就不好。如下图所示：

![pclass](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_titanic_pclass.png)

此时，就需要对特征进行预处理，比如使用 One Hot Encoder 方法，把特征转换为对线性模型友好的新特征，如下图所示：

![one hot encoder](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_tatinic_pclass_ohe.png)

scikit-learn 里的 `sklearn.preprocessing.OneHotEncoder` 是处理 One Hot Encoder 的常用方法。然而，随机森林等 tree based 模型则不需要做这种预处理，它可以很好地对 categories feature 进行处理。这是因为 tree based 模型是把空间分成一个个盒子，而 linear based 模型是把空间分成两个子空间。

TODO: 针对 Titanic dataset 验证处理前后模型准确性的差异。

总结：

* 特征预处理常常是必要的
* 通过特征分析生成新特征是一个强大的工具
* 特征预处理和特征生成的策略和方法，通常和选择的模型相关

### 数值特征预处理

* tree-based 模型的数值特征预处理
* non-tree-based 模型的数值特征预处理
* 特征生成

#### 特征预处理

non-tree-based 模型往往对数值特征的数量级别比较敏感。比如 kNN 分类时，计算预测点到周围的点的距离，如果某个特征的数值范围很大（100 - 1000），则计算出来的距离就很大；而另外一个数值的距离单位较小（1 - 10），则计算出来的距离小得多，此时就会待预测点预测为距离较短的点。Linear model 也有类似的特性，特征数值的大小，会决定分隔平面的斜率。如下图所示：

![feature scale](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_numeric_feature_scale.png)

解决此类问题的关键，是要把数值型特征进行相应的缩放，使其在同一个数量级。常用的算法有：
* `sklearn.preprocessing.MinMaxScaler`：把特征转换为 [0, 1] 之间
* `sklearn.preprocessing.StandardScaler`：把特征转换为中间点为 0，方差为 1 的，满足正态分布的数值

此外，针对 linear model，还需要特别注意异常值（outliers）的处理。因为这些异常值往往会对 linear model 有较大的影响，从而导致模型准确性受损，如下图：

![outliers](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_outliers.png)

处理异常值的一个方法是，直接去掉这个异常值，比如我们取特征的值分布的 99% 作为有效值，去掉两端的异常值。另外一个方法是使用 rank 的方法来缩减异常值和正常值的距离。常用的是 Pandas 里的 `DataFrame.rank` 或 `Series.rank`，它们按照数值的大小排序，然后取序号来代替真实值。

```python
In [1]: import pandas as pd

In [2]: s = pd.Series([-100, 0, 1e5])

In [3]: s
Out[3]:
0      -100.0
1         0.0
2    100000.0
dtype: float64

In [5]: s.rank()
Out[5]:
0    1.0
1    2.0
2    3.0
dtype: float64

In [6]: s2 = pd.Series([10, 100, 1, 30, 1e8])

In [7]: s2
Out[7]:
0           10.0
1          100.0
2            1.0
3           30.0
4    100000000.0
dtype: float64

In [8]: s2.rank()
Out[8]:
0    2.0
1    4.0
2    1.0
3    3.0
4    5.0
dtype: float64
```

如果我们没有时间去手动处理异常值，使用 rank 的方法也是一个不错的选择，linear model, kNN, neural networks 都会从这种处理方法中受益。

还有一个处理方式是使用 `np.log(1 + x)` 或使用 `np.sqrt(x + 2/3)` 来缩放数据。这种转换实际上是把异常值往中间靠拢，neural networks 算法可能会从这种转换中显著地提高性能和准确性。

最后一个常用的预处理方法是，把不同预处理方法处理后的值串联起来作为新特征，或用不同的模型分别训练不同预处理方法处理的数据。这实际上类似于 ensemble 的思想。Linear models, kNN, nueral networks 等 non-tree-based 模型可以通过这种方法显著地提高性能。

TODO: 构造一个实例来验证上述说法。

#### 特征生成

特征生成是指在分析数据特征及训练目标后，根据业务特点创造出来的新特征，它会提高模型训练的准确性和有效性。特征生成往往需要对业务背景要有足够深刻的理解，特征生成的能力往往可能区分出一般的机器学习工程师和好的机器学习工程师。

比如，房子有面积特征和价格特征，我们可以生成一个新的特征叫单位面积的价格。再如，针对价格类的特征，如 2.49, 3.99 这种，可以把小数点后面提取出来作为一个新的特征，这个特征实际上是建立在消费者对价格的后缀的敏感度角度建立的。如 3.99 用户可能感觉比较便宜，还不到 4 ，这是利用认识错觉而建立起来的特征。

再如，为了区分网络蜘蛛和人，我们可以快速闪过一个文本，网络蜘蛛和人对这个文本会有不同的表现，网络蜘蛛会获取这个文本信息，而人是不可能在瞬间读取这个文本内容的。

#### 总结

* 针对不同的模型，数值特征的预处理方法不同
    * tree-based 模型不依赖于特征数值缩放
    * non-tree-based 模型严重依赖特征数值缩放
* 常用的数值缩放方法
    * `MinMaxScaler`
    * `StandardScaler`
    * `rank`
    * `np.log(1 + x)` 和 `np.sqrt(1 + x)`
* 特征生成
    * 先验知识，业务背景知识
    * 数据分析 EDA

### Categorical and ordinal feature 的预处理

* Categorical 特征和 ordinal 特征针对不同模型的处理方法
* Categorical 特征和 ordinal 特征有哪些不同
* 怎么样生成新特征

#### 不同特征的特点

* ordinal feature 与 categorical feature 的差异
  ordinal feature = order categorical feature
* ordinal feature 与 numerical feature 的差异
  在 Titanic dataset 里，pclass 有 1, 2, 3 三个级别，这个是 ordinal feature 还是 numerical feature 呢？答案是 ordinal feature。因为 numerical feature 的一个显著特点是数值等差，即 pclass = 1 和 pclass = 2 之间的“距离”与 pclass = 2 和 pclass = 3 之间的“距离”相同。但在我们的案例里，显然没有这个特点。所以，这是一个 ordinal feature。另外一些 ordinal feature 的例子是，驾照类型 A, B, C。再如教育程度，幼儿园，小学，中学，本科，硕士，博士等。

#### 预处理方法

** LabelEncoder**

把 categorical feature 映射成数字。这种方法最简单，但只适用于 tree-based model 。Non-tree-based model ，包括 linear mode, kNN, neural networks 不适用这种处理方法，因为模型无法把它当成一个数值来进行计算。想像一下 kNN 是根据距离来分类的，而 LabelEncoder 处理后的数值不能反应真实的“距离”。如下图所示，左图，linear model 无法很好地利用 LabelEncoder 处理后的 categorical feature，而 tree-based model 可以很好地利用处理后的数据。

![LabelEncoder](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_categorical_feature.png)

**概率分布处理**

除了 `LabelEncoder` 外，`Pandas.factorize` 方法也可以实现按照出现顺序进行数值编号。另外，还有一种方法是根据出现的概率，把 categorical feature 转换为数值，如 A 出现的概率为 50%，B 出现的概率为 30%，C 出现的概率为 20%，则使用 0.5, 0.3, 0.2 分别代表 A, B, C。 这种方法可以保留一些类别分布信息，对 tree-based model 和 linear model 都有帮助。Linear model 可以从概率和目标值的相关性里找出规则；tree-based model 可以从数值和目标的相关性，获得树的较少分裂次数。但是要注意，如果类别概率差不多，会造成模型无法区分出不同的概率，从而导致模型无法从这个新特征里获得有帮助的信息。此时可以使用 `rank` 方法来处理。

**one-hot encoding**

One-hot encoding 方法是给每个类别的值创建一个新特征，等于这个类别值的样本，此特征为 1 ，其他为 0。这种方法对 non-tree-based model 非常有用。需要注意，这种方法处理后的特征其实已经经过缩放了，最大值是 1 ，最小值是 0。

如果 dataset 里有少量的 numerical feature，但有大量的 one-hot encoding 处理后的特征，此时 tree-based 模型可能会得到较差的性能。在这种情况下，其一，tree-based 模型无法有效地利用 numerical feature；其二，tree-based 模型会因此导致分裂过多，训练速度变慢，但性能没有提升。

另外一个需要注意的事项，如果 categorical feature 的类别非常多，会导致创建很多新特征，样本在这些新特征的的值大部分为 0，这个会浪费存储空间，同时减慢模型训练速度。一个好的方法是使用 Sparse Matrix 来存储数据，如 `scipy.sparse.csr_matrix`。

**categorical feature interaction**

如果多个 categorical feature 的联合体对目标有影响，那么我们可以直接把这些 categorical feature 连接起来，组成一个新的 categorical feature，然后对这个新的 categorical feature 做 one-hot encoding 操作，这样就会生成很多新的特征。Linear model 会拟合出不同的参数，来适配这个新的组合特征，从而达到较好的模型准确率。如下图，把 pclass 和 sex 两个特征合并，生成一个新的 pclass_sex 的特征，然后再针对 pclass_sex 的特征执行 one-hot encoding 操作。

![categorical feature interaction](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggle_categorical_interaction.png)

需要注意，需要从业务角度判断，只把相关的 categorical feature 合并起来处理，而不是所有的 categorical feature 合并都会产生好的效果。

#### 总结

* Ordinal feature 是一种按照某种关系排序后的 categorical feature
* Label encoding 可以把 categorical feature 映射到数值
* Frequency encoding 可以把 categorical feature 映射到某出现的概率
* Label 和 frequency encodings 对 tree-based models 比较有效，但对 non-tree-based models 效果不好
* Non-tree-based models 常常使用 One-hot encoding 的方法来进行预处理
* Interfactions of categorical features 常常对 linear model 准确性有帮助

### 时间及地理坐标特征的预处理

#### 时间特征的处理

**周期性**

比如，我们可以根据样本的时间，添加小时，分钟，秒等新特征。或者添加星期，月，日等特征。这些特征会帮助模型抓住数据里的一些周期性特征。比如，模型会发现每周五晚上几点到几点会出现服务器访问高峰期这种模式。周期性划分时，不一定按照自然单位进行划分，还可以根据业务背景进行特定地划分，比如某种药是 3 天一个疗程，我们可以以 3 天为单位进行划分，这样可以根据时间特征，创建一个新的特征叫疗程数，来帮助模型抓住疗程数和疗效之间的关联关系。

**事件锚点**

另外一个处理方式是，可以把时间参数处理成和某个事件锚点的关联关系。如离周末的天数，或离十一长假的天数等等。下面是一个典型的使用 time since 方法创建的新特征，其中 date 是原始的日期特征，sales 是目标值，中间的都是创建出来的新特征。

![time since](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_time_since.png)

**事件间距**

还有一个处理方式是，可以根据不同的事件的发生时间，计算它们之间的时间间距。这个可以帮助模型发现事件发生间隔和目标值的关系。如电商交易里，可以计算出一年中用户的平均交易时间间隔，一个月的平均交易时间间隔。此外，还可以计算交易时间和打投诉电话的时间间隔，一般情况下如果这个间隔很短，说明用户在交易过程中遇到问题，会影响这个用户的下次交易行为，从而影响用户的交易总量。

**进一步预处理**

从时间特征里创建出的新特征，有些是 numerical feature，有些是 categorical feature，这些新特征需要用上述介绍的相应方法，结合我们使用的模型，进行二次预处理，以便这些新创建的特征能对我们的模型有帮助。

#### 地理特征处理

地理特征处理需要结合地图数据进行处理。比如需要预测房子的价格，除了房子本身的特征（面积，朝向，楼层，结构）外，房子所处的地理位置也很重要。怎么样利用位置信息呢？如果我们有额外的地理信息数据，可以计算房子离最近的医院，学校，公园的距离。如果没有额外的数据，可以从训练样本样本挖掘出新的特征，比如，可以把训练样本的房子分成一些相同的区域，然后然后找出最贵的房子，并计算这个房子到最贵的房子的距离。再如，可以找出一些特征的房子，比如年限最老的房子的区域，然后计算样本到这个区域中心点的距离。

另外一个技巧是，当一条街道把两个区域的房子价格区分开时，我们可以试着增加一个特征，这个特征是这个街道做适当的旋转，使得基于 tree-based 的模型可以在一次分裂即可区分出这两种价格，从而大大提高模型的训练速度和精度。如下图所示：

![coordinate](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_coordinate.png)

#### 总结

* 时间特征
    * 周期性
    * 事件锚点
    * 事件间距
* 地理位置
    * 距离最近的标志性地点，如公园，医院，学校等
    * 计算训练样本到局域性中心点的距离
    * 对训练样本周边进行聚合统计，如公园数量，医院数量，学校数量等等

### 缺失值的处理

缺失值包括 NaN, 空字符串，奇异点。有时缺失的值也会包含有用的信息，比如为什么会有缺失值？缺失代表什么意思？有时我们可以从这些含义的背后，创建出新的特征来。

#### 缺失值的识别

有时缺失的值并不是 NaN，可能是一些不容易发现的隐藏的值，如 -1。怎么样发现 -1 是缺失值呢？可以通过 EDA 来看数据的分布，从而发现缺失的值。如下图：

![hidden missing values](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_missing_value.png)

再如，有些异常值也可以当成缺失值来处理，如年份在 2050 年上映的电影，或者重量为 100 吨的桃子等。有时，某些 categorical feature 的类别只在测试数据里出现，但没在训练数据里出现。此时模型就会把这些只在测试数据里出现的值作为缺失值处理，进而影响模型的性能。一个处理方法是，使用类别数据出现的频率来进行编码，这样那些只在测试样本里出现的数据也会被正确地编码并处理。

#### 处理缺失值

有三种常用的方法来处理缺失值：

* 替换成常数，如 999， -1，0 等：这种方法对 non-tree-based 模型不友好，可能导致模型准确性下降
* 替换成平均值，中位数值：对 linear model 比较友好
* 重新构建出缺失值

缺失值的处理方法和问题背景密切相关。比如，我们统计了一年的温度，但是中间有段时间值是缺失的，如果我们把缺失的值替换成平均值，或替换成 0，可能都不是好的方法。比如我们创建了一个新的特征，这个特征是前后两天的温度差，这样的缺失值处理会误导我们的模型。

![wrong missing values handler](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_mean_temp.png)

#### 总结

* 如何填充缺失值，需要根据具体的问题具体分析
* 常用的缺失值处理，是替换成常数，平均值，中位数
* 数据提供者可能已经把缺失值填充成某个特殊的值，如 -999，此时可以通过画出数据的柱状图来检查
* 添加一个新特征叫 isnull，来表示这一样本是否包含缺失值，往往对模型有帮助
* 通常情况下，避免在生成新特征前去填充缺失值。因为填充的缺失值可能会影响生成的新特征的准确性。
* XGBoost 可以自己处理 NaN 值

### 文本特征处理

文本处理的原则是把文本转换为向量，有两种转换方式，一种是 Bag of words，另外一种是 word2vec。

![text to vector](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_text_2_vec.png)

#### Bag of words

Bag of words 的原理就是把每个词语作为一个特征，然后统计这个词在一篇文章里的出现次数。

![CountVectorizer](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_counter_vec.png)

scikit-learn 里的 `CountVectorizer` 可以很好地实现这种转换。

我们前面讨论过，Linear model, kNN, neural networs 等算法对数值的大小比较敏感，需要做等量缩放。Bag of words 里另外一个能实现同等数量级缩放的方法是 TFIDF 方法，它的全称是 Term Frequency - Inverse Document Frequency 。TF 指的是一个词语在一篇文章中的出现次数，IDF 是指这个词语在整个数据集里的出现的频率的 log 值，如果一个词语在所有的文章里都出现，则它的概率是 1，其 log 值则为 0，即它的权重为 0。这个也容易理解，一个单词在每篇文章中都出现，它不带来任何的有效信息。scikit-learn 里的 `TfidfVectorizer` 可以完成这样的任务。

另外一个常用的算法是 N-grams，它不单单统计一个单词，还处理这个单词的上下文信息。当只统计一个单词时，称为 unigrams，统计两个单词时，称为 bigrams，统计三个单词时称为 trigrams。一般情况下，不会超过三阶，因为统计的单词越多，特征数量会成指数增长。

![N-grams](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_ngrams.png)

有时，可以使用字符来代替单词来应用 N-grams 模型，这样做的好处是，可以让模型发现那些我们不认识，但广泛使用的缩写词。可以通过指定 `analyzer='char'` 来启用以字符为单位的分析，可以通过 `ngram_range` 参数来指定 N-grams 阶数。

在进行 Bag of words 处理前，还需要对文本进行预处理，典型地预处理步骤包括：

* 全部转换为小写
* 词形还原（lemmatization），如把 was -> is，having -> have 等
* 词干提取（stemming），去掉词尾，提取出词根，如 democracy, democratic, democratization -> democr，
* 去掉停止词，如把常用的 in, of, at, is 等词语去掉

NLTK 是进行英文文本预处理的理想工具。

#### Word2vec

Bag of words 的方法把文本置换为一个很大的稀疏向量。而 word2vec 使用的是另外一种方法，它把文本转换为一个通常只有几百维的向量。其更大的特点是，word2vec 能精确地表达词语之间的关系，即意思相近的词，其向量也相近。如下图：

![word2vec](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_word2vec.png)

使用 word2vec 处理的单词向量，存在如下关系：king + women - man = queen。

word2vec 算法的其他典型实现包括 Glove, FastText 等。训练 word2vec 不需要我们待处理的文本，而是用一个大而全的语料库，而且需要很长的时间。网络上有一些根据通用语料库训练好的模型。比如 Glove 预训练向量可以从 https://nlp.stanford.edu/projects/glove/ 下载。FastText 预训练向量可以从 https://github.com/facebookresearch/fastText/blob/master/pretrained-vectors.md 下载，它甚至还提供了多种语言的预训练向量，包括中文。

#### 总结

* 预处理（写换为小写，词形还原，词干提取，停止词）
* 使用 N-grams 可以处理文本的上下文信息
* 后处理，使用 TFIDF
* Bag of words 和 word2vec 往往会有不同的结果，可以使用 ensemble 方法结合起来使用

### 图像特征的处理

卷积神经网络是处理图像特征的最有利武器。关于卷积运算，可以搜索“如何通俗易懂地解释卷积”。知乎上有一个非常直观的解释 https://www.zhihu.com/question/22298352 。

使用卷积神经网络处理图像时，一个方法是使用针对问题领域预训练的神经网络模型，如针对病理图像分类的问题，可以使用 VGG, ResNet 等。这种方法往往对数据量比较小的问题，比自己从头训练神经网络模型效果更好。

TODO: 关于神经网络，需要学习完 PyTorch 后再回头重看这个视频。

训练一个神经网络需要大量的数据，数据量越大，模型准确度越好。有时，我们的数据量不够，图片太少，此时可以通过对图像进行旋转，旋转后的图像作为新的训练样本，这样就可以增加训练样本的数量，从而提高模型性能。比如针对房屋朝向的预测，有四种类别，分别是坐北朝南，坐南朝北，平面房顶，其他。我们可以通过旋转图片，从而得到更多的训练样本，可以旋转 180 度，得到一组新数据，旋转 90 度得到另外一组新数据。这样我们的训练样本就增加了 4 倍。

![increase dataset](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_inc_data.png)

## EDA

EDA 的全称是 Exploratory data analysis，即数据探索和分析。这个是每个机器学习任务的基础，我们需要熟悉数据，熟悉问题的背景。为后续建模打下基础。

### 对数据建立初步印象

* 获取领域信息，即问题的背景
* 对数据获取直觉信息
* 理解数据是怎么产生的

比如，发现人类的年龄是 360 ，这肯定是个错误的数据。后续对数据进行预处理时需要解决。再如，针对广告的数据，点击数一定小于等于展示数的，没有展示哪来的点击。有了这样的领域信息，我们也可以判断是否有错误的数据。因为错误的数据会误导我们的模型。针对这种情况，我们可以创建一个新的特征，称为 "is_correct"，我们的模型可以会从这个特征里学到东西，从而提高准确性。

此外，理解数据是怎么产生的，对构建 validation 模型有重要的帮助。比如，训练数据集和测试数据集不是用相同的算法产生的，此时我们就无法从训练数据集里取出一部分来作为模型验证的数据。

TODO: 随书的 w2_002_Building intuition about the data_EDA_video2.ipynb 是个很有趣的 EDA 示例。值得一看。

### 匿名数据分析

有时候，组织者为了隐藏一些敏感信息，会把数据的字段改为匿名字段，如 x1, x2 等。针对这种类型的数据，我们需要尽量去搞清楚这些数据的含义是什么，最少也需要搞清楚这些数据的类型，如 numeric feature, categorical feature 等，这样我们才能做合适的预处理。

w2_003_Exploring anonymized data.ipynb 这个 EDA 里从匿名数据里发现一个特征是出生年份。这个特征被 `StandardScaler` 缩放和平移了。通过一步步发现缩放的系数以及平移的系数，最终发现这是一个年龄。除此之外，这个 EDA 另外一个值得学习的是，使用 `RandomForestClassifier` 构建了一个基准模型，然后训练数据后，通过模型的 `feature_importances_` 去发现这些特征的重要程度。这个方法也有助于我们去分析最重要的特征，而舍弃那些不重要的特征。

匿名数据中，有用的函数：

* df.dtypes: Pandas 猜测的数据类型
* df.info(): 数据的概要信息
* df.value_counts(): 数据的分布情况
* df.isnull(): 数据是否包含空值

### 数据可视化

* 逐个分析特征
    * 柱状图（Histograms）查看数据的分布
    * 走势图（Plots）查看数据的规律
    * 统计图（Statistics）查看数据的统计信息
* 探索特征关联关系
    * 点状图（Scatter plot）
    * 相关性（Scatter plot）

#### 单特征分析

EDA 是一门艺术，可视化工具是我们的工具。有时候，一些图形会造成误解，比如下面的柱状图：

![histoograms](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_hist.png)

突出的部分是什么？可能是数据的均值，而数据的组织者使用均值来填充这些缺失值造成的。这就需要我们进一步计算并求证。如果真的是这个情况，我们需要反向处理，比如这样处理缺失值是否合理？还是我们要用另外的缺失值处理方式，比如填充成 -999 之类的。此外，我们还可以创建一个新的特征 is_missing ，把包含缺失值的样本标记一下，这种方法对 linear model 有很大的帮助。

以下这些是常用的数据分析函数：

* 柱状图：plt.hist()
* 数据走势图：plt.plot(x, '.')
* 数据统计信息：df.describe(), df.mean(), df.var()
* 其他工具函数：x.value_counts(), x.isnull()

#### 特征关联关系分析

我们可以使用 `plt.scatter(x1, x2, c=y)` 来画出 x1 和 x2 两个特征的关系，从中找出一些规律。此外，我们还可以把训练样本和测试样本都画在同一个点阵图里，查看他们的关系。比如下图，红色表示一个类别，蓝色表示另外一个类别，灰色表示的是测试数据。因为我们没有测试数据的类别情况，所以是灰色的。

![scatter](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggle_scatter.png)

我们可以看到，测试数据的一部分和红色数据重叠在一起，另外一部分和蓝色数据重叠在一起，这是好的现象，说明我们的训练数据很好地覆盖了这部分数据。但右上角有一部分灰色数据单独分布，没有和我们的训练数据重叠，这是不好的现象，说明我们的训练样本没有覆盖这部分数据，这样我们用这个训练数据做出来的模型对没有覆盖的这部分数据性能会很差。

再如下面的特征关系图，我们可以怎么样使用呢？

![scatter 2](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggle_scatter_2.png)

首先，这样的关系图说明 x1 和 x2 之间是什么关系？实际上，说明 $x1 <= 1 - x2$（在红色以下，而红色就是 $x1 + x2 = 1$）。那么如何使用这层关系呢？这个要根据业务模型来决定，但我们可以利用这个关系，创建一个新的特征，比如 x1 和 x2 的比值，这样的新特征会对 tree-based 模型有帮助。

以下这些是常用的数据分析函数：

* 数据分布图：plt.scatter(x1, x2, c=y)
* 多特征数据分布图：pd.scatter_matrix(df)
* 特征相关性：df.corr()
* 矩阵可视化：plt.matshow(df.values)
* 查看不同特征的均值变化趋势：df.mean().sort_values().plot(style=’.’)

TODO: 探索 `df.corr`，查找特征关联性。

#### 总结

这是一个 EDA checklist:

* 获得总是的领域知识
* 获取数据的直观感受
* 理解数据是怎么产生和采集的，从而帮助我们创建新的特征
* 逐个地探索特征
* 探索多个特征的关系
* 发现缺失值，重复值

#### 示例 Springleaf EDA

w2_007_Springleaf competition EDA II_EDA_Springleaf_screencast.ipynb 是一个值得一看的 EDA 示例，几个有意思的技巧总结如下：

**删除 ID 类特征**
我们可以把那些 ID 类的特征删除。因为 ID 类的特征会误导模型。ID 类特征的特点是，每个数据样本，它的值都是唯一的。可以使用下面的代码来找出这些 ID 类的特征：

```python
feats_counts = train.nunique(dropna = False)
feats_counts.sort_values()[:10]
```

**删除重复特征**
先对使用 `factorize()` 对数据进行 categorical 编码处理，然后针对所有的特征，两两比较是否相同，并且记录这些具有相同值的特征。最后把这些值相同的特征删除掉。

**决定数据类型**
决定数据类型有时不止一个方案，比如对 1, 2, 3 这样的数值，可以是 numerical feature ，也可以是 categorical feature。一个常用的方法是使用 `nunique = train.nunique(dropna=False)` 算出每个特征的值的个数，如果个数很大，很有可能是 numerical feature。如果个数很小，则可能是 categorical feature。除此之外，还可以使用 `plt.hist(nunique.astype(float)/train.shape[0], bins=100)` 画出条形图 (bar chart)，以便更形象地观察。

**其他**
有时我们通过 EDA 可以发现一些数据的模式，比如发现某些累加值，如第一个月销售量，前两个月累计销售量，前三个月累计销售量，linear mode 可以很好地处理这种值，但 tree-based 模型就会有问题。对 tree-based 模型更友好的是转换为每个月的销量。

## 模型检验和过拟合

经常参与 kaggle 竞赛的同学会发现一个有趣的现象，很多人在 public leaderboard 上评分很高，但是在真正竞赛结果出来时，在 private leaderboard 上却掉了下来。这里的原因，就是模型没有经过很好的检验，针对 public test data 过拟合，最终导致分数下降。

本章的主要内容：

* 什么是模型检验和过拟合
* 通过怎么样的数据切分，来建立稳定的模型检验系统
* 常用的数据切分方法
* 常见的模型检验问题

在 kaggle 竞赛中，模型的过拟合通常意见的模型过拟合不同。通常意义上，模型过拟合是指模型针对训练数据集很准确，但对测试数据集性能表现较差。而在 kaggle 竞赛中，过拟合是指模型对 public test dataset 分数较高，但对 private test dataset 没有达到预期的效果。从而导致排名从 public leaderboard 上较高的位置跌落到 private leaderboard 上较低的位置。

### 模型检验策略

为确保模型准确性，我们需要建议**稳定**的模型检验系统。我们一般把训练数据分成两部分，一部分是训练数据集（train dataset），另外一部分称为检验数据集（validation dataset）。常用的划分方法有：

* Holdout: 固定地划分一定比例的数据作为检验数据集。scikit-learn 的 `train_test_split` 以及 `ShuffleSplit` 是实现这种划分的理想函数。当数据量较大时，可以使用这种方法。
* K-fold: 把模型划分成 K 份，然后拿其中的 K - 1 份来当训练数据集，另外 1 份当检验数据集。重复上述过程，只至 K 份数据的每一份，都充分过检验数据集。最后求得 K 次模型准确性评分的平均值。scikit-learn 的 `KFold` 类可以实现这种划分。需要注意，这种划分，每次检验模型准确性，都需要进行 K 次训练和 K 次检验，需要花费额外的训练数据。K-fold 和进行 K 次 Holdout 有什么区别呢？区别在于，K-fold 可以确保样本中的每个数据都只有一次作为模型检验数据集，而 K 次 Holdout 的结果是，有些样本做了多次检验数据集，有些样本根本没有机会作为模型检验数据集。
* Leave-one-out: 每次从数据集中拿**一个**样本出来当模型检验数据集，其余的数据作为训练样本。重复上述过程，直到所有的样本都当过一次模型检验数据集。这个方法类似 K-fold，当 `KFold` 的参数 `n_splits` 为样本数据个数时，K-fold 就退化为 Leave-one-out 方法。scikit-learn 的 `LeaveOneOut` 可以实现这种数据划分。这种划分方法，适用于数据量较小，且模型训练速度足够快的场合。

此外，stratification 方法帮助我们建立更稳定的模型检验方法，特别是针对数据量较小，数据**不平衡**的时候。stratification 方法的核心思想是，确保 K-fold 划分后的数据集里，每份数据都有差不多的分布。比如针对二元分类，它保证 0 和 1 目标的样本分布概率接近。scikit-learn 里的 `StratifiedKFold` 可以实现这种数据划分。

### 数据划分策略

假设，我们有过去几个月销量数据，需要预测下个月的销量。针对这样的 time serial 数据集，我们有两种划分方法，一种是随机取出一部分作为模型检验数据集，另外一个方法是按时间序列，把某个时间之前的作为训练数据集，某个时间之后的作为检验数据集。这两种划分方法训练出来的模型有差别么？

![split strategy](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_split_strategy.png)

答案是**差别巨大**。为什么呢？

想像一下，模型训练过程中，我们是通过不断进行特征选择，优化参数，使得针对交叉验证数据集的评分越来越高。故，针对第一种方法，我们的模型将很擅长预测随机的缺失值。模型所选择出来的特征，也是对这种预测友好的。方法训练出来的模型，如果要去预测未来几个连续点的值，将会表现得很差。相反，第二种方法，我们的模型将被训练成擅长预测未来一段时间的多个缺失值。故，第二种方法对我们要解决的问题更有利。

长期来看，模型预测值将和训练数据集里的目标值的平均值接近。针对第一种情况，交叉验证数据集的平均值更接近训练数据集目标值的平均值，而测试数据集的平均值则离训练数据集的平均值较远。故，第一种情况下，模型对交叉验证数据集的预测结果要好于对测试数据集的预测结果。针对第二种情况，交叉验证数据集离训练数据集的目标值的平均值比较远，测试数据集离训练数据集的目标值平均值也比较远，故模型针对交叉验证数据集的预测和对测试数据集的预测的准确性将差不多，这有助于帮助我们建立一个更稳定的交叉验证模型。从而使算法具有更大的泛化性，避免过拟合。

所以，不恰当的交叉验证数据集的划分，将导致特征以及模型偏离我们的问题目标，从而造成我们意料之外的后果。**针对 time serial 数据集，我们应该使用 time-based split 方法来划分训练数据集和交叉验证数据集**。更一般化的结论，我们需要根据具体的问题，或者说针对 kaggle 竞赛的测试数据的产生机制，在我们模型交叉验证阶段，就模拟这种机制，以便我们的模型能更好地预测测试数据集。

常用的交叉验证数据集的划分策略有以下几种：

**按行随机选择**
这是最常用的一种划分方法。这种方法需要确保每行数据是独立的，不存在依赖关系。

**时间序列划分**
这种方法开头的例子里讨论过了。如果数据量足够多，我们可以使用“滑动窗口”交叉验证机制。如，使用第 1, 2, 3 周的数据作为训练数据集，第 4 周的数据作为交叉验证数据集。然后使用第 2, 3, 4 周的数据作为训练数据集，使用第 5 周的数据作为交叉验证数据集。

**基于 ID 的划分**
假设，我们有一个根据造影图片，预测病人疾病的任务。每个病人都有多个不同的图片，每个图片当作一个样本。我们在划分交叉验证数据集时，如果随机划分，那么可能把一个病人的部分图片划分到训练数据集里，另外一部分图片划分到交叉验证数据集里。这样的结果是造成了训练数据集和交叉验证数据集的数据“重合”，从而非常容易造成模型过拟合。正确地划分方法，应该是根据人来划分，同一个人的所有图片，要么都在训练数据集里，要么都在交叉验证数据集里。这就是基于 ID 的划分方法。其总体思想，是根据某个类别来划分，从而避免造成训练数据集和交叉验证数据集数据重叠。有时，这种基于 ID 的划分方法，ID 并不是现成的，需要我们自己去发现。比如，有些图片分类数据里，图片是连续拍摄的，这些图片的差异性很小，那么这些相似的图片应该被归到同一组里去。

**总之，我们划分出来的交叉验证数据集，需要尽量的模仿测试数据集的产生机制**。

### 交叉验证常见问题

正常情况下，针对交叉验证数据集的预测结果改善，会带来 public leaderboard 的改善。但有时，却没有这种预期的结果。引起这个问题主要有两个原因：

* 交叉验证原因：这往往是由于数据不一致造成的。比如，我们使用 Handout 划分法来划分交叉验证数据集，这样训练出来的模型对交叉验证数据集过拟合。
* 提交阶段的原因：交叉验证结果改善了，但 public leaderboard 没改善，这往往是因为我们的交叉验证数据集没有很好的模仿测试数据集。

#### 交叉验证阶段的问题

* 数据数量太少
* 数据易变，一致性比较差

解决方案：

* 从多个 KFold 里再平均来获取交叉验证评分，或者增加 KFold 里的 K 参数
* 从一组 KFold 里来训练模型，得到最优参数，使用另外一组 KFold 来检验模型质量

示例：

需要使用这个解决方案的竞赛有 Liberty Mutual Group Property Inspection Prediction competition 和 Santander Customer Satifaction competition。

#### 提交阶段的原因

* public learderboard 数据量太少
* train dataset 和 test dataset 的分布不一致

针对每一个原因，我们只需要相信我们的交叉验证结果即可，可以忽略 public leaderboard 的评分。针对第二个情况解决方案要复杂一些，我们先来看一个例子，搞清楚什么叫**分布不一致**。

![different distribution](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_diff_distribution.png)

上图中，我们要预测人的身高。训练数据集都是女性，其平均身高是 63 inch，而测试数据集都是男性，其平均身高是 70 inch。这样导致模型针对测试数据集的预测性能很差。我们可以计算训练数据集和测试数据集的平均值，然后直接在提交给 public leaderboard 的模型中加入一个参数，比如直接把预测结果加上 7 inch 。问题是，训练数据集的平均值好计算，测试数据集的平均值怎么计算呢？我们称为 leaderboard probing，即通过 LOG 来探测测试数据集。

但有时，不会这么极端，更常见的情景是，训练数据集里大部分是女性，少部分男性；测试数据集里大部分是男性，少部分是女性。我们可以通过 EDA 来发现数据分布的不均匀。 针对这种情况，我们选择出来的交叉验证数据集需要符合测试数据集的分布情况，这样我们的模型就会包含这种不平衡的分布规则，从而在 public leaderboard 上取得较好的预测结果。

![validation distribution](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_validation_2.png)

在之前 EDA 章节里介绍过 Google 广告成本预测的竞赛题目。通过 EDA 我们发现，训练数据集里只包含那些展示过的广告（未展示过的广告是因为 Google 的广告展示策略导致的），而测试数据集里却包含了所有的广告。针对这种分布的不均衡，我们需要根据测试数据集的生成规则，生成相似分布的交叉验证数据集，即要交叉验证数据集里，包含未展示的广告。

![Google Ads](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_validation_3.png)

详细的 EDA 及分析发现这一分布不均衡的过程，可参阅 w2_002_Building intuition about the data_EDA_video2.ipynb 。

TODO: 如何从训练数据集里生成包含未展示广告的交叉验证数据集？

针对音乐推荐的应用，测试数据包含的是所有的推荐音乐，判断用户是否喜欢这个推荐的音乐。而训练数据集包含的是系统推荐的音乐以及用户民自己选择的音乐。我们在构造交叉验证数据集时，需要只从系统推荐的音乐中选择，而不应该把用户自己选择的音乐也包含进去。如果我们没有这样构造交叉验证数据集，而是从训练数据集里随机抽一份作为交叉验证数据集，造成的结果就是我们的模型对交叉验证数据集不断地优化，质量越来越好，但对 public leaderboard 的结果却没有提高。

#### 结论

* public leaderboard 的数据样本太少：如果是这种情况，我们只需要信任交叉验证结果即可
* train/test 数据分布不一致：针对这种情况，我们需要按照 test dataset 的数据分布，从 train 里构造出相同分布的交叉验证数据集

### 排行版洗牌

即使我们的交叉验证数据集全部做对了，我们使用了正确的交叉验证策略，我们也使用了正确的交叉验证数据集生成策略，我们规避数据分布不均衡问题，让交叉验证数据集和测试数据集具有相同的分布，但是依然会出现排行版洗牌，即在 public leaderboard 上排位很高，但在 private leaderboard 上排位不高。这是为什么呢？主要有以下三个原因：

* 随机因素
  随机因素有二，一是模型对 public leaderboard 过拟合。二是欠拟合，针对那些非常难预测的金融交易数据，随机因素在这里占用了非常大的比例，这样就导致了排行版被洗牌。
* 数据量太少
  特别是针对 private test dataset 的数据量太少
* public/private test dataset 的分布不一致
  针对这种问题，我们需要忽略 public leaderboard 的结果。相信交叉验证数据集的结果。比如，针对时间序列数据，一般情况下 public test dataset 包含的是某个时间段的数据，而 private test dataset 包含的是更后面某个时间段的数据。如果我们一味地追求 public leaderboard 上的高分，就会造成过拟合，从而导致 private test dataset 上的分数变低。

TODO: w2_105_Addtional material and links.pdf 的阅读材料。

## 数据泄漏

Data leakage 指的是在测试数据里包含了一些 ground true 信息，导致我们可以达到很高的预测精度。数据泄漏针对现实世界是没有用的，而如果在 kaggle 竞赛中以追求名次为目的，则可能是有用的。但我们始终应该清楚，数据泄漏是意外的错误，我们不应该有过多地依赖。

针对数据泄漏，我们举一个例子。假设有一个竞赛是对图片进行分类，我们需要识别中图片中的动物是猫还是狗。在这些数据的收集过程中，先拍摄猫的图片，隔几天后拍摄狗的图片。然后把拍摄的图片分成训练数据集和测试数据集。一个竞赛参与者，可以直接根据图片拍摄的日期来判断是猫还是狗，从而达到 100% 的准确率。这样，我们利用数据泄漏达到很高的分数。虽然可以排名很高，但在实际中其实是没有用途的。

理论上讲，数据集的 ID 和行的顺序跟模型质量是无关的。但在 kaggle 竞赛中，有时候会发现，把 ID 和行序号作为特征加入训练，会提高模型的质量？为什么呢？因为这些 ID 和行序号，和目标值存在某种关联，这是竞赛组织者无心之过，比如忘记随机排序了，导致了有这样的关联关系。

**计算测试数据的分布**：
针对 Quora 问题配对竞赛中。train dataset 和 test dataset 的分布是不同的。但据说，public test dataset 和 private test dataset 的分布是相同的。我们要怎么样从 public test dataset 里算出分布，然后来构造交叉验证数据集呢？

我们可以从逻辑回归算法的成本函数入手：

$$
- L * N = \sum_{i=1}^N(y_i ln C + (1-y_i) ln (1 - C))
$$

其中，L 是 public test dataset 给出的测试评分，我们可以通过向 kaggle 网站提交预测结果得到。N 是数据样本的数量，C 是我们给定的常量预测值，如 0.5。

此外，成本函数还可以通过以下公式计算：

$$
- L * N = N_1 ln C + (N - N_1) ln (1 - C)
$$

其中，$N_1$ 是数据集里目标为 1 的记录个数。我们要求的是 public test dataset 里的数据分布，即求的是 $\frac{N_1}{N}$ 的值，综合以下两式，可以得到：

$$
\frac{N_1}{N} = \frac{-L - ln (1 - C)}{ln C - ln (1 - C)}
$$

这样，我们给定一个常数预测值 C，然后构建一个 submission 文件，提交到 kaggle 上，得到评分 L，就可以算出数据分布。这就是利用 leaderboard probing 来获取数据分布的方法。有了这个分布，我们在构造交叉验证数据集时，就可以构造出相同的分布用来检测模型。这种方法会大大地提高提高模型针对测试数据预测的准确性。

**其他案例**：
有另外一个竞赛，参赛者需要预测一个 HTML 文本里的内容是否包含赞助信息，即是不是软文。这个竞赛的数据压缩包的日期有个数据泄漏，能用来区分是否是软文。另外一个例子是 Expedia Hotel Recommendations，竞赛的目标是通过用户搜索的操作记录，预测用户会预测哪个酒店。但实际，这里面也有一个数据泄漏，可以搜索这个相关的视频查学习怎么样通过 EDA 来发现这个数据泄漏的过程。这个数据泄漏可以让我们很轻松地对测试数据集，达到很高的准确性。

TODO: 合理地利用数据泄漏有时是获得高分的关键。

## 模型评估

不同的竞赛往往会使用不同的模型评估方法。那是因为模型的性能评估方法很多，很多公司会根据自己的业务场景选择适合自己业务场景的模型性能评估方法。

针对模型评估方法的优化，有时候能达到意想不到的效果。比如，针对时间序列的预测，这是最有挑战性的预测。我们往往需要采用好多种不同的策略，如根据**时间线**来划分训练数据集和交叉验证数据集，使用**滑动窗口**技术，确保交叉验证数据集和测试数据集的数据分布相同。即使使用了这些策略，可能依然效果不如人意。为什么呢？

这是因为，交叉验证数据集往往对模型的预测趋势起到限制作用。如下图，假设红色的时间线是我们的训练数据集，蓝色时间线是我们的交叉验证数据集，假设模型预测值在平均线之上，而真正的趋势是下跌的，那么模型的错误值就会很高，会受到模型评估函数的惩罚，从而倾向于预测下跌。

![time serial](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_metrics_1.png)

一种改进的模型评估方法是，只预测下一个时间点相对于最后一个己知时间点是上涨还是下跌，然后根据预测结果，把预测值设置为最后一个己知值加上或减去一个很小的常数。如上图所示。这样的优化结果，变成了预测趋势，而不去预测数值。

### 数值回归模型评估

#### MSE

MSE 的全称是 Mean Square Error，即均方根法。这是最常用的回归模型评估方法。它的计算公式如下：

$$
MSE = \frac{1}{N}\sum_{i=1}^{N}(y_i - \hat{y_i})^2
$$

针对 MSE ，我们可以找到使得其值最小的一个常量预测值。如下图所示的例子中，左侧是示例数据，右上角是每个特征的变化引起 MSE 变化的曲线，右下角是找到使得 MSE 最小的常量预测值的过程。

![MSE](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_mse.png)

我们找到的常量预测值接近 11，实际上就是 y 的平均值。我们可以通过求解微分来直接计算这个最小值。可以使用 `sklearn.metrics.mean_squared_error` 来计算 MSE 。

#### RMSE

RMSE 的全称是 Root Mean Square Error，它是 MSE 的一个扩展：

$$
RMSE = \sqrt{\frac{1}{N}\sum_{i=1}^{N}(y_i - \hat{y_i})^2} = \sqrt{RMSE}
$$

RMSE 和 MSE 相比，其基本性能都差不多。但针对**梯度下降 (Gradient-Based)**类算法有一点区别。针对梯度下降算法，针对 RMSE 偏微分是针对 MSE 的偏微分乘以一个常数：

$$
\frac{\partial{RMSE}}{\partial{\hat{y_i}}} = \frac{1}{2\sqrt{MSE}}frac{\partial{MSE}}{\partial{\hat{y_i}}}
$$

这意味着，沿着 RMSE 和沿着 MSE 的梯度下降趋势是相同的，但学习率不同。如果沿着 RMSE 来进行梯度下降，它的学习率受 MSE 的大小动态影响。当 MSE 越大，学习率越小，算法收敛地越慢。所以，大部分时候，使用 MSE 来作为算法评估标准。那为什么还要 RMSE 呢？RMSE 的作为是使得算法评估曲线更平滑，因为 RMSE 的平方根刚才抵消了 MSE 里的平方运算。

可以使用 `sklearn.metrics.mean_squared_error` 结合 `numpy.sqrt` 来计算 RMSE 。

#### R-squared

有时很难从 MSE 和 RMSE 的绝对值里来评估模型性能到底是好还是坏，我们经常是使用相对法，即和某个基准 MSE 值比较。R-squared 评估方法可以实现基于某个基准的比较值。

$$
R^2 = 1 - \frac{MSE}{\frac{1}{N}\sum_{i=1}^{N}(y_i - \bar{y_i})^2}
$$

其中，$\bar{y_i}$ 是指目标的平均值。当 MSE 接近于 0 时，R-squared 的值接近于 1；当 MSE 接近于最小常量预测模型的 MSE 时，R-squared 的值接近于 0。这样模型的评分性能都在 [0, 1] 之间。可以使用 `sklearn.metrics.r2_score` 来计算 R-squared 。

#### MAE

MAE 的全称是 Mean Absolute Error，它使用绝对值代替平方。

$$
MAE = \frac{1}{N}\sum_{i=1}^{N}|y_i - \hat{y_i}|
$$

MAE 和 MSE 相比，对异常值的容忍度比较高，同样的误差，使用 MSE 时算的是平方，而使用 MAE 时算的是绝对值。MAE 经常用在金融领域。10 元的误差是 5 元的误差的 2 倍，这个逻辑关系能正确地被 MAE 表达。最小常量预测值是目标值的中位数。

是不是 MAE 比 MSE 好呢？不一定。需要根据业务场景来判断，MAE 比 MSE 对异常值的容忍度较高，但要取决于这个异常值是真正的异常值还是只是值比较高，但也需要被关注和预测的目标值？如果是前者，可以用 MAE，但如果是后者，显然 MAE 会减少对异常值的关注，从而导致这类的值的预测准确性受影响。可以使用 `sklearn.metrics.mean_absolute_error` 来计算 MAE 。

#### MSPE 和 MSAE

假设，我们预测商店的电脑销量，商店 1 的实际销量是 10，我们预测成了 9，商店 2 的实际销量是 1000，我们预测成了 999。这两个样本的 MSE 都是 1。但实际上，从误差的角度来讲，针对商店 1 的误差要大得多。MSPE (Mean Square Percentage Error) 可以比较好地衡量这种误差，它增加了权重信息：

$$
MSPE = \frac{1}{N}\sum_{i=1}^{N}(\frac{y_i - \hat{y_i}}{y_i})^2
$$

MSPE 会偏向于小的目标值，大的目标值对其权限影响较小，如下图：

![MSPE](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_mspe.png)

它的最小常量预测值比 MSE 要小。而且，从右上图可以看到，目标值越小，其变化值对 MSPE 的影响越大；目标值越大，其变化值对 MSPE 的影响越小。

MSAE 与此类似，它的最小常量预测值比 MSPE 更小，即更偏向于对小的目标值更敏感。

![MAPE](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_mape.png)

#### RMSLE

RMSLE 的全称是 Root Mean Square Logarithmic Error。它是 RMSE 的对数版：

$$
RMSLE = \sqrt{\frac{1}{N}\sum_{i=1}^{N}(log(y_i + 1) - log(\hat{y_i} + 1))^2} = RMSE(log(y_i + 1), log(\hat{y_i} + 1))
$$

RMSLE 也是某种带权重的相对误差计算法。它对小的目标值更敏感，对大的目标值的变化更不敏感。其次，它的一个最大的特点是，对于特定的目标值，大于目标值的预测会比小于目标值的预测受到的“惩罚”要小，即两边是不对称的。左侧曲线更陡，右侧曲线更平滑。如下图右上角所示：

![RMSLE](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_rmsle.png)

针对示例数据，RMSLE 的最小常量预测值是 9.1 左右，比 MSE 要小，但比其他的几种模型评估方法要大。MSE 对大的目标值最敏感，更倾向于让目标值比较大的样本预测得更准确一些，为此可以牺牲目标值比较小的样本的准确性。而 MAPE 则与 MSE 相反，倾向于让目标值较小的样本预测更准确，为此可以牺牲目标值较大的样本的准确性。其他的模型评估方法介于这两者之间。

可以使用 `sklearn.metrics.mean_squared_log_error` 结合 `numpy.sqrt` 来计算 RMSLE 。

### 分类模型评估

分类模型评估用来评估分类问题。常用的几个评估方法有：

* 准确率 Accuracy Score
* 对数失真 Logarithmic Loss
* ROC 曲线面积 Area under ROC Curve
* Cohen's kappa

分类算法的输出值分为两类，一类是 soft predictions，即针对一个类别，预测出概率。如预测是否酒驾时，输出 [0.9, 0.1]，即有 90% 的概率酒驾。我们往往可以取一个门限值，大于门限值，预测为 1 ，小于门限值预测为 0。另外一个类别称为 hard predictions，即直接输出 1 或 0，而不输出概率。

#### Accuracy

$$
Accuracy = \frac{1}{N}\sum_{i=1}^N[\hat{y_i} = y_i]
$$

准确率是最简单最直观的评估方法，但往往有带来问题。如癌症病灶检测，如果我们的模型不管什么输入，都预测为 0，则我们的准确率可能达到 99% 以上。但这样的模型是没有价值的。可以使用 `sklearn.metrics.accuracy_score` 来计算 Accuracy 。

**Log Loss**

Log Loss 可以处理 soft predictions 输出，它利用概率来计算准确率：

$$
LogLoss = -\frac{1}{N}\sum_{i=1}^N[ y_i \log{\hat{y_i}} + (1 - y_i) \log{(1 - \hat{y_i})}]
$$

针对多类别的问题，它的计算公式如下：

$$
LogLoss = -\frac{1}{N}\sum_{i=1}^N\sum_{j=1}^L y_{il} \log{\hat{y_{il}}}
$$

在实践中，为了避免计算时溢出，一般选择一个较小的数，来处理预测值：

$$
LogLoss = -\frac{1}{N}\sum_{i=1}^N\sum_{j=1}^L y_{il} \log{min(max(\hat{y_{il}}, 10^{-15}), (1 - 10^{-15}))}
$$

对比 Accuracy 和 LogLoss ，当 $y_i = 0$ 时，其 LogLoss 和预测值 $\hat{y_i}$ 的关系：

![Log Loss](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_logloss.png)

从图中可以看出来，当 $\hat{y_i}$ 接近于 1 时，LogLoss 非常大。这说明，LogLoss 会对完全错误的预测给于非常大的惩罚。此外，针对 LogLoss ，最小常量预测值是一个向量，向量里的元素每个类别的出现概率。如针对 10 只猫，90 只狗的类别预测里，最小常量预测值是 [0.1, 0.9]。可以使用 `sklearn.metrics.log_loss` 来计算 LogLoss 。

#### AUC ROC

 AUC ROC 的全称是 Area Under Receiver Operating Characteristic Curve。AUC 通过计算**ROC 曲线**下的面积来评价分类模型。它主要适用于二元分类问题，并且只于 Positive 和 Negative 的顺序。如何构造 ROC 曲线呢？[维基百科](https://en.wikipedia.org/wiki/Receiver_operating_characteristic)的定义是：

 > The ROC curve is created by plotting the true positive rate (TPR) against the false positive rate (FPR) at various threshold settings.

ROC 的横坐标是 FPR (False Positive Rate)，即假阳性的概率；纵坐标是 TPR (True Postive Rate)，即真阳性的概率。ROC 曲线就是在不同的 threshold 取值的情况下 FPR 和 TPR 的值。threshold 聚会范围从 0 到 1 。

![AUC ROC](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_auc_roc.png)

如上图，横坐标是 FP (False Positive) 的数量，纵坐标是 TP (True Positive) 的数量。当 threshold 从 0 到 1 移动的过程中，FP 的数量和 TP 的数量变化连成一条曲线，即是 ROC 曲线。比如，threshold 在第一个红点处时，TP 的数量增加 1，当 threshold 继续向右移动到第一个绿点的位置时，FP 的数量增加 1 ，依此类推，即可画出 ROC 曲线。

![ROC in practice](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_auc_roc_real.png)

当点数很多时，会得到上图所求的典型的 ROC 曲线。AUC ROC 的最大值是 1，最小值是 0，最小常量基准值是 0.5。可以使用 `sklearn.metrics.roc_auc_score` 来计算 AUC ROC 。

#### Cohen's Kappa

之前讨论过的例子，如果我们有 10 只猫，90 只狗。我们使用常量来预测，可能达到 90% 的准确率，这个称作 baseline（基准）。Cohen's Kappa 的基本原理是，如果预测的准确率达到 baseline，则为 0，如果准确率达到 100% 则为 1。这样的话，kappa 的计算公式如下：

$$
kappa = 1 - \frac{1 - p_o}{1 - p_e}
$$

其中，$p_o$ 表示 Accuracy，即准确率。$p_e$ 是 baseline。其计算公式如下：

$$
p_e = \frac{1}{N^2} \sum_k n_{k1} n_{k2}
$$

具体的例子可参阅 https://en.wikipedia.org/wiki/Cohen%27s_kappa 上的一个例子。怎么理解 $p_e$ 呢？实际上，它表达的是一种**随机一致性**。拿 Wikipedia 上的例子，A 和 B 两个教授分别对 50 份奖学金申请提出自己的意见，如下图：

![kappa](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_kappa_1.png)

这个表格说明，A 对 50 份申请中的 25 份说了 YES，另外 25 份说了 NO。B 对 50 份申请中的 30 份说了 YES，对另外的 20 份说了 NO。我们先计算 $p_o$ ，它表示观察到的意见一致的概率，其中对角线上的元素就是意见一致的概率：

$$
p_o = \frac{20 + 15}{50} = 0.7
$$

那么，$p_e$ 的意思是，针对一个随机申请者，A 和 B 意见一致的概率是多少？针对这个随机的申请者，A 和 B 可能都说了 YES，也可能都说了 NO。意见一致的概率为：

$$
p_e = p_{yes} + p_{no} = 0.5 * 0.6 + 0.5 * 0.4 = 0.5
$$

**针对随机样本意见一致的概率就是我们的基线**。

再计算 kappa:

$$
kappa = 1 - \frac{1 - 0.7}{1 - 0.5} = 0.4
$$

kappa 的一个延伸的概念是 weighted kappa，即加入权重信息。如下表所示：

假设有三个类别，猫，狗，老虎。把猫预测成猫，或把狗预测成猫的权重为 1，而如果猫和狗错误地预测为老虎，其权重为 10。依照上图中的公式即可计算中 weighed kappa。

weighted kappa 的另外一个延伸是 quadratic weighed kappa，即权重按照平方递增。如 1 预测成 2 的权重是 1，而 1 预测成 3 的权重则是 4，这样按照类别顺序，平方递增，生成的权重表算出来的 kappa 称为 quadratic weighed kappa。

kappa 的物理含义，是表达模型预测的结果与实际结果的一致性。如，针对疾病检测系统，用来表达模型预测的结果与专业医生的诊断结果的一致性程度。实际应用时，可以使用 `sklearn.metrics.cohen_kappa_score` 来计算 kappa 评分。

## 模型优化

有时候，人们经常混淆模型的 metric 和 loss 。实际上，这是完全不同的两个概念。loss 相当于模型的成本函数，模型在训练的过程中会想办法让 loss 函数的值达到最小，比如通过梯度下降算法，不断地逼得 loss 函数的最小值。而 metric 是用来评价模型的准确性的指标，比如前文介绍的 Accuracy, MSE 等等。

下面是一些常用的模型 loss 函数：

* MSE, LogLoss: 大部分模型支持这个 loss 函数。只要选择合适的模型即可。
* MSPE, MAPE, RMSLE: 大部分模型不直接支持这些 loss 函数。如 XGBoost 无法对 MSPE 进行直接优化，故需要对训练样本进行重新采样，然后转为优化 MSE 。
* Accuracy, Kappa: 优化其他可优化的 metric，然后再进行 post-process 来处理预测值。
* 自定义 loss 函数: 我们可以通过模型提供的接口，自定义 loss 函数来优化我们的目标模型。
* 使用 early stopping 来让模型收敛到一个可接受的阈值

上面的描述很抽象，这里只是做下总览。后续章节详细描述各种模型优化方法。

### 数值回归模型优化

这里的**优化**，指的是模型依照选定的 loss 函数，通过训练样本不断地让 loss 函数最小的过程。

#### MSE/RMSE/R-Squared

MSE 是支持最广泛的模型 loss 函数。比如，针对 `sklearn.linear_model.SGDRegressor` 模型里的 `loss` 参数，默认情况下即使用 MSE 作为模型 loss 函数。`sklearn.ensemble.RandomForestRegressor` 模型的 `criterion` 参数可以指定模型的 loss 函数，默认也是使用 MSE 作为模型优化目标。

![MSE Loss](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_mse_loss.png)

#### MAE

支持以 MAE 作为模型 loss 函数的模型会少一点。比如 `sklearn.linear_model.SGDRegressor` 不支持使用 MAE 作为优化目标，但它定义了另外一个称为 `huber` 的 loss 函数，和 MAE 类似，特别是在错误值较大时。而 `sklearn.ensemble.RandomForestRegressor` 模型直接支持 MAE 作为优化目标，可以通过参数 `criterion='mae'` 达成这一目的。

![MAE Loss](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_mae_loss.png)

#### MSPE/MAPE

很难找到直接支持以 MSPE/MAPE 作为优化目标的模型。我们可以通过自定义 loss 函数来达到这一目的；或者换成其他的 loss 函数，然后通过 earyly stopping 来达成这一目的。这里介绍的是另外一种方法，通过设置样本的权重，重新采样的方法。

![MAE Loss](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_mspe_loss.png)

我们可以使用上图中的右侧的公式计算每个训练样本的权重值 $w_i$。然后通过权重重新对训练样本进行采样：

```python
df.sample(weights=sample_weights)
```

最后使用 MSE 作为模型优化目标，这样即可实现 PSPE 作为模型的优化目标。此外，有些模型如 XGBoost, LightGBM 等，直接支持通过 sample weights 作为模型参数。此时，就不需要通过 `df.sample` 进行重新采样了。

采用重采样方法时，有几点需要注意：

* 测试数据集不需要经过权重重新采样。这是模型已经按照 MSPE 目标优化，测试数据可以直接使用其来预测。
* 一个技巧可以提高模型的稳定性：通过多次重采样，每次采样都训练一个模型出来。然后最终的预测值取几次模型的平均值。

#### RMSLE

回顾 RMSLE 的计算公式：

$$
RMSLE = \sqrt{\frac{1}{N}\sum_{i=1}^{N}(log(y_i + 1) - log(\hat{y_i} + 1))^2} = RMSE(log(y_i + 1), log(\hat{y_i} + 1))
$$

故，我们可以通过训练样本进行如下预处理：

$$
z_i = log(y_i + 1)
$$

这样把训练样本的目标值从 $y_i$ 转换为 $z_i$，然后使用 MSE 作为模型优化目标。这样训练出来的模型的预测值为 $\hat{z_i}$ ，可以通过下面的公式转换为原来预测值 $\hat{y_i}$：

$$
\hat{y_i} = \exp(\hat{z_i}) - 1
$$

总结起来，就是把训练样本数值转换为 log 空间，然后进行 MSE 为目标的模型训练。最后预测值需要从 log 空间转换回原始空间。

### 分类模型优化

#### LogLoss

LogLoss 在大部分分类模型里都有内置的实现。我们要做的，是选择一个合适的模型，直接训练即可。

![LogLoss](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_logloss_loss.png)

需要注意，`sklearn.ensemble.RandomForestClassifier` 使用 `gini` 或 `entropy` 来作为 loss 函数，它对 LogLoss 的性能很差。但有方法可以解决这个问题。我们可以对预测值进行**校准**，以便它的 LogLoss 性能更好。为什么需要校准呢？因为 `sklearn.ensemble.RandomForestClassifier` 不是以 LogLoss 为模型优化目标，而是使用 gini 或 entropy 作为模型优化目标。所以，当我们以 LogLoss 作为模型评价的 metric 时，就需要对模型进行校准。

![RandomForest](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_logloss_rf.png)

如上图，蓝色线表示随机森林的预测值分布，红色线表示训练数据集的滑动窗口平均值，绿色线表示校准后的预测值。从图中可以看出来，蓝色线需要经过校准，才能获得更好的预测值，从而让 LogLoss 的值更小。

预测概率校准的方法大体有以下几种：

* Platt scaling: 以原模型的预测值作为输入，使用 Logistic Regression 模型进行拟合。类似模型叠加（model stacking）的方法。具体参阅 https://en.wikipedia.org/wiki/Platt_scaling
* Isotonic regression: 以原模型的预测值作为输入，使用 Isotonic Regression 模型进行拟合，这也是一种模型叠加的方法。具体参阅 https://en.wikipedia.org/wiki/Isotonic_regression
* Stacking：模型叠加。使用 XGBoost 或其他的神经网络叠加在原模型的预测值上。

#### Accuracy

没有模型能够直接针对 Accuracy 进行收敛，但有一些通用的方法。如果是二元分类，使用任何一个分类 loss 函数（如，Logloss）进行训练，然后通过一个 grid search 的循环，调整 threshold 值，以取得最优的 Accuracy 值。如果是多类别分类问题，使用任何一个分类 loss 函数进行训练，然后根据对参数进行微调，以便选择一个 Accuracy 评分最高的模型。

为什么 Accuracy 不能作为模型的 Loss 函数来直接优化呢？请看下图：

![Accuracy Loss](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_accuracy_loss.png)

横坐标是训练样本离决策边界线的距离，纵坐标是模型所受到的惩罚。从上图可以看出来，针对 Accuracy 的是 zero-one-loss，即要么 0，要么 1。跟样本离决策边界的距离无关。这样模型就无法知道，当参数变化时，到底 Accuracy 是变好了还是变坏了，从而导致模型无法以 Accuracy 为目标来直接优化。而针对 Logistic Loss 等，模型通过调整参数，能很容易地计算出 Loss 函数的变化幅度，是变好了还是变坏了。这样模型就可以直接使用这个 Loss 函数来作为目标直接优化。

#### AUC

少部分模型支持直接以 AUC 作为模型优化目标，但大部分不支持。

![AUC Loss](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_auc_loss.png)

针对 AUC，大部分人直接使用 LogLoss 作为模型优化目标。针对 XGBoost，使用 LogLoss 作为优化目标和使用 pairwise loss 作为优化目标实际效果差不多。

**Quadratic weighted Kappa**

Kappa 无法通过模型优化得到。但是，从 Kappa 计算公式得知，它的公式里分子部分是 MSE ，分母部分和预测值相关。针对多类别的问题，如果我们允许模型输出类似 4.5 这样的中间值，那么可以近似地认为 Kappa 和 MSE 相关。所以，在实践中，通常大家的做法是直接使用 MSE 作为模型优化目标。这个在理论上其实是不严谨的，但在实践中往往起作用。

![kappa Loss](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_kappa_mse_loss.png)

MSE 能给我们一个连续值，我们可以通过调节 threshold 值来获得更好的 kappa 值。调节 threshold 的方法很简单，也是通过 grid search 方法通过循环来找到最好的 threshold 即可。

此外，有个论文讨论如何直接让 kappa 作为模型优化目标。

TODO: 参阅  https://arxiv.org/abs/1509.07107 或 w3_008_Classification metrics optimization II_soft_kappa_xgboost.ipynb 。

## Mean Encoding

Mean Encoding 有时也称为 likelihood encoding，有时也叫 target encoding。它是一种添加新特征的方法。

### 基本原理

它的主要原理是：针对 categorical feature，不使用如 label encoding 的技术，而是使用这个特征里每个类别所对应的目标值的平均值来编码，如下图所示：

![Mean Encoding](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_mean_encoding_1.png)

### 原理分析

问题是，为什么 mean encoding 会有效呢？我们把 categorical feature 经过 label encoding 和 mean encoding 编码后的值和目标值画成柱状图如下：

![Mean Encoding Hist](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_mean_encoding_2.png)

从上图可以看出来，label encoding 后，特征和目标值的关系没有规律，显得比较随机。而 mean encoding 的特征和目标值形成了明显的规律，这样模型就可以很容易地发现这个规律，从而提高模型的准确性。

我们常用的 tree-based 模型，如 XGBoost, LightGBM 等，比较难处理那些连续值的特征。使用 mean encoding 可以使得 tree-based 模型使用较少的树的深度，来达到较低的 loss 值。如下图所示：

![Mean Encoding Loss](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_mean_encoding_loss.png)

在实践中，怎么样判断 mean encoding 是否能帮助我们提高模型的准确性呢？下图是一个使用不同的深度的树训练出来的模型，上图是针对训练数据集的 AUC 评分，下图是针对交叉验证数据集的 AUC 评分。

![Mean Encoding Loss](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_mean_encoding_diag.png)

从图中可以看出来，随着树的深度越来越大，针对训练数据集的评分越来越高。而这一过程中，我们并没有过拟合，因为针对交叉验证数据集的评分也越来越高，虽然提高得比较少。这一证据，说明针对一些特征，决策树会通过很多次的分裂来处理这个特征，我们可以把决策树 dump 出来，查看这个树的分裂点来证实这个问题。针对这样的问题，我们可以利用 mean encoding 来解决。它可以减少树的深度，减少树的分裂次数，提高模型的性能。

### 计算方法

除了我们上文介绍的均值方法外，还有其他的几种生成方法，如下图所示：

![Mean Encoding](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_mean_encoding.png)

我们来看一个例子。我们使用下面的代码来处理训练数据集和交叉验证数据集，以便生成新的 mean encoding 特征：

```python
means = x_tr.groupby(col).target.mean()
x_tr_new = [col + '_mean_target'] = x_tr_new[col].map(means)
x_cv_new = [col + '_mean_target'] = x_cv_new[col].map(means)
```

接下来，我们使用 XGBoost 来训练模型，得到如下的学习曲线。我们发现，针对训练数据集的评分很高，而针对交叉验证数据集的评分在 0.5 左右徘徊。从这个特点可以看出来，使用 mean encoding 后模型明显地过拟合了。

![Mean Encoding Overfit](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_mean_encoding_overfit.png)

所以，使用 mean encoding 时，必须要引入一些正则项来解决过拟合问题。为什么会造成过拟合呢？根本原因在于，针对每个类别，其在训练数据集和交叉验证数据集里的分布概率不同，导致算出来的 mean encoding 值不一样。

### 正则化

使用 mean encoding 时必须使用正则化来解决模型过拟合问题。总共有四种正则化的方法，下面逐一介绍。

#### CV Loop

CV Loop 的特点如下：

* 直观且稳定
* 通常把数据集分成 4 到 5 个 Fold 即可，不需要对这个参数进行调整
* 需要特别小心 Leave-One-Out 的情景，这种情景可能导致交叉验证数据集的数据泄漏，从而导致无效

其计算方法是，使用 `StratifiedKFold` 把数据集分成 5 个 fold，然后每个 fold 的平均值从其他 4 个 fold 里计算得来。这样算出所有的平均值。最后，由于某些类别的数据量比较少，可能导致没有在全部的 fold 里出现，故会出现 NaN，我们把这些 NaN 使用全局平均值替代。其伪代码如下：

```python
y = df_tr['target'].values
x = df_tr.drop(labels='target', axis=1, inplace=True)
x_new = x.copy()
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=23)

for tr_index, cv_index in skf.split(x, y):
    x_tr, x_cv = x.iloc[tr_index], x.iloc[cv_index]
    for col in cols:  # interate through the columns we want to encode
        means = x_cv[col].map(x_tr.groupby(col).target.mean())
        x_cv[col + '_mean_target'] = means
    x_new.iloc[cv_index] = x_cv

prior = y.mean()
x_new.fillna(prior, inplace=True)
```

#### Smoothing

Smoothing 方法一般需要和其他的正则化方法结合起来使用，比如和上面介绍的 CV Loop 方法结合。它的思想是引入一个 alpha 变量，让这个变量控制正则化的程度。当 alpha 为 0 时，则没有正则化，当 alpha 趁近于无穷大时，则 mean encoding 使用全局平均值。

$$
mean_target = \frac{mean(target) * nrows + globalmean * alpha}{nrows + alpha}
$$

#### Noise

Noise 方法的原则是给 mean encoding 后的特征加入一些随机的噪声。因为 mean encoding 对训练数据集提供了近乎完美的特征，但对交叉验证数据集则没那么好。但这个方法不好操作，加入太多噪声会导致特征变成垃圾，太少特征又无法达到合适的正则项。主定方法通常和 CV Loop 结合起来使用。而且需要严格调试噪声的大小。

#### Expending mean

Expending mean 方法最少限度地导致目标泄漏（即把目标值引入到特征里），而且没有类似 alpha 的调试参数。它的思想就是，根据 n - 1 行的数据计算第 n 行的 mean encoding 的值。如下代码片段所示：

```python
cumsum = df_tr.groupby(col)['target'].cumsum() - df_tr['target']
cumcnt = df_tr.groupby(col).cumcount()
tr_new[col + '_mean_target'] = cumsum / cumcnt
```

在实践中，常用的是 CV Loop 和 Expending Mean 的方法。

### Mean encoding 的泛化和扩展

本节主要内容有：

* 针对数值回归和多类别分类问题的 mean encoding
* 多对多关系
* 针对时间序列的应用
* 怎么样对 numerical feature 进行编码

#### 数值回归和多类别分类

二元分类问题对 target 只有一个解读。而数值回归则有多种解读，比如可以取 categorical feature 对应的每种类别的均值，方差，中位值，甚至分布信息。比如目标值是 1 到 100 之间的分布值，我们可以分成 10 个 bin，然后计算每个 bin 的样本数量，如计算 1 - 10 之间的样本目标值的数量，再算 11 - 20 之间的样本目标值的数量，依此类推。总之，数值回归问题在 feature engineering 方面比二元分类问题更灵活，也有更多的处理方法。具体哪个方法效果更好，需要根据数据的特征和分布情况进行信偿试和调优。

多类别分类问题的 encoding 方法也比较直观，直接针对多个类别对应的值计算平均值进行编码。大部分情况下，多元分类问题采用的是 one-vs-all 的分类方法，即每个类别有自己的模型和参数，彼此之间不知道对方的存在。而 mean encoding 实际上是引入了其他类别的信息。

#### 多对多关系

有时候，categorical feature 是多对多的关系，比如用户和他们手机上安装的 App 这样的一个例子。一个用户会安装多个 App，而一个 App 也会被多个用户安装。这就是多对多关系。如下图所示：

![Many To Many](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_mean_encoding_m2m.png)

针对这样的数据，我们如果要对 userid 和 app 进行编码，首先需要根据 app 作展开，针对每个 user 和 app 创建唯一的配对，即进行向量叉乘。如图右侧所示，这个称为 long representation。然后，针对每个 app 计算其 mean encoding。计算出来的 mean encoding 如何再映射到 user 上去呢？可以采用的方法可以是加和，最大值，最小值，平均值，方差等等。总之，根据每个 user 的 app 的 mean encoding 组成的向量，应用一些统计方法算出一个值，当成 user 的 mean encoding 值即可。

#### 时间序列

时间序列是有内在关联关系的数据。针对其他的数据，我们都是针对所有的行来求平均值，而对时间序列，则可以更灵活，比如我们可以求之前 2 天的平均值，也可以求之前 1 周的平均值等等。

比如，针对不同的用户在不同的品类上的消费这样的例子，如下图：

![Time Serial](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_mean_encoding_ts.png)

我们有 2 天的数据，总共有 2 个用户，3 个品类。针对这样的数据，可以创建出一些很有用的特征。比如，用户前天花了多少钱；用户在某个品类中平均每天花多少钱等。如上图所示。数据越多，可以创建出越多越复杂的特征。

#### 处理 numerical feature

tree-based 模型对连续的 numerical feature 并不友好。所以，我们可以借助 mean encoding 的思想对 numerical feature 进行处理。在实践中，通常可以对 numerical feature 以及几个 numerical feature 结合起来做 mean encoding 处理。其方法是把 numerical feature 划分成几个等级，然后把它当成 categorical feature 进行处理。

现在，需要回答两个问题。一是，怎么样对 numerica feature 进行等级划分？二是，选择哪些 feature 进行结合？答案是通过分析决策树的结构进行判断，如果一个特征在决策树里有多次分裂，那么可能是这个特征太复杂了，我们可以采用 mean encoding 的方法进行处理。再如，两个特征经常出现在一起，对决策树进行分裂，那么这两个特征可能有关联关系，可以把这两个特征结合起来作为 categorical feature 进行 mean encoding 处理。

![feature interactions](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_mean_encoding_interaction.png)

如上图，如果 feature1 和 feature2 在决策树里频繁地出现在相临的位置进行分裂，说明这两个特征联合起来对目标值有复杂的关联关系，模型在试图找出这种规律。这个时候，我们可以把这两个特征合并起来，使用类似 many-to-many 的方法进行 mean encoding，然后拿这个新的特征让模型去训练。实际上，这样做的终极目的是，创建一个新的特征，让模型通过这个特征更容易地找到规律。

那么如何导出决策树特征呢？针对 scikit-learn，我们可以使用 `sklearn.tree.export_graphviz()` 函数把决策树模型参数导出到文件，然后使用 `graphviz` 工具包生成决策树示意图。如下代码所示：

```python
from sklearn.tree import export_graphviz

with open("titanic.dot", 'w') as f:
    f = export_graphviz(clf, out_file=f)

# 1. 在电脑上安装 graphviz
# 2. 运行 `dot -Tpng titanic.dot -o titanic.png`
# 3. 在当前目录查看生成的决策树 titanic.png
```

Kaggle 上的 Amazone Employee Access Challenge Competition 只有 9 个类别特征，如果我们不做特征工程，直接把这 9 个特征丢给 XGBoost 处理，那么不管我们怎么调试参数，AUC 评分只能达到大概 0.87 。这样大概在 public learderboard 的 700 位左右。甚至，我们针对每个 categorical feature 进行 mean encoding，也没能提高 AUC 评分。

但是，如果我们使用 [CatBoost](https://github.com/catboost/catboost) 库进行训练，会马上把 AUC 评分提高到 0.91 ，从而让我们的排名大幅提高。这是因为 CatBoost 的实现里，默认会对不同的 categorical feature 进行关联 mean encoding 处理。

但是 CatBoost 也不是万能钥匙，为了进一步提高排名，我们仍然需要分析决策树结构，然后手动添加不同 categorical feature 的关联 mean encoding 创建出来的新特征。

TODO: 使用 Amazone Employee Access Challenge Competition 的数据验证 feature interaction 的效果。

#### 交叉验证注意事项

由于 mean encoding 容易造成过拟合，在交叉验证数据集上，需要特点注意。在本地验证以及在 kaggle 提交时有不同的处理策略。

在本地进行交叉验证时：

* 把数据集分成训练数据集 x_tr 和交叉验证数据集 x_cv
* 在 x_tr 上计算 mean encoding ，然后 map 到 x_tr 和 x_cv 上
* 针对 x_tr 采取正则化措施
* 使用 x_tr 和 x_cv 两个数据集对模型进行交叉验证

千万不要在划分数据之前对数据进行 mean encoding 计算。因为这样会造成目标数据泄漏 (target leackage)，即把目标值引入到交叉验证数据集里，最后造成的结果是训练数据集评分很高，交叉验证数据集评分也很高，而提交到 public learderboard 时评分很低。

TODO: 找一个例子验证，通过正则项解决 mean encoding 过拟合问题。从而把整个流程串起来。

在提交到 kaggle 上运行时：

* 针对整个训练数据集计算 mean encoding
* 将计算结果 map 到训练数据集和测试数据集
* 针对训练数据集进行正则化
* 针对训练数据集进行模型训练
* 使用模型对测试数据集进行预测

需要注意，使用哪种正则化方法应该在本地交叉验证阶段已经固定下来了，在提交阶段使用相同的方法。

### 总结

优点：

* Mean encoding 是处理 categorical feature 的有效方法
* Mean encoding 是特征工程的强有力的基础

缺点：

* 因为存在目标值泄漏，需要特点小心地处理交叉验证集。否则非常容易造成过拟合问题。
* 只对部分数据集有效，不是针对所有的竞赛都管用。但要注意，如果有效，会显著地提高模型质量。

TODO: w3_104_Programming_Assignment.ipynb

## 模型参数调校

本章主要内容是介绍模型参数调校的一般性原则，然后介绍针对不同的模型进行参数调优的方法，主要包括：

* 通用流水线
* 手动和自动调校
* 我们应该理解模型的哪些参数及其含义
* tree-based 模型参数调优
* 神经网络模型参数调优
* 线性模型参数调优

### 通用流程

模型调校时，首先需要选择要调优的参数。针对每个模型，可能都有一堆参数可以调，但往往只有少数几个参数对模型的准确性影响是最大的，我们只需要集中力量调试这些参数即可。怎么样找到这些参数呢？一个方法是网上搜索，参考 kaggle kernel 上别人的做法，另外一个方法是参阅官方文档，一般情况下，文档里也会明确写出哪些参数应该要优先调校。

手动调校比较直观，修改参数，运行模型，查看交叉验证数据集的评分。重复上述过程，直到找到合适的参数。另外一种方法是自动调校，一些可以用来自动调校的库有：

* hyperopt
* scikit-optimize
* spearmint
* gpyopt
* robo
* smac3

自动调校一般分为两个步骤，一是定义一个模型训练和评价的函数，二是定义模型参数空间，即所有我们要调校和设置的模型参数范围。模型调校一般需要运行很长时间，比较常用的做法是 让它运行一个晚上。当然，在实践中，不少人仍然使用手动调校的方法。

模型参数调校，实质上是让模型工作在欠拟合和过拟合之间，达到最好的泛化效果。每种模型都有两种类型的参数，一种参数，当增大它的值时，模型针对训练数据集的训练效果更好。另外一种参数，当增大它的值时，模型针对训练数据集的拟合效果变差。

### tree-based 模型参数调校

tree-based 模型主要有以下几种：

* Gradient Boost Decision Tree
  * XGBoost - 广泛应用，准确性高，训练效率稍低
  * LightGBM - 广泛应用，准确性高，训练效率高
  * CatBoost - 比较新的 GBDT 实现，目前应用还不多，但看起来前景不错。特别是对 categorical feature 处理方面。
* scikit-learn
  * RandomForest
  * ExtraTrees
* 其他
  * fast_rgf - 百度开源的模型。接口不友好，训练比较慢。但对有些数据集有非常好的准确性。

#### GBDT

**max_depth**

这个参数控制决策树的深度。一般来讲，数值越大，生成的数越复杂，能越好的拟合训练数据集。不同的数据集对这个参数的数值要求不同，有些可能是 2，有些可能是 27 等等。**当我们不停地增大 `max_depth` 参数，甚至达到一个较大的值时，仍然能够有效地提高模型的准确性，且不过拟合。即在交叉验证数据集里的评分越来越好。这时，给我们的一个信号是，我们的数据集里有很多相互作用的特征 (interfaction features)，这个时候一般我们需要停止参数调校，而是去发现这些相互作用的特征，然后根据它们创建出新的特征。**使用新的创建出来的特征代替相互作用的特征，减少树的深度。这样做会让模型训练更快，也具备更好的泛化性。

针对 `max_depth` 一个推荐的数值是 7，即从 7 开始调校。如果不能百分百确定，不建议使用过大的 `max_depth` 的值。过大的值一来会让模型训练时间变长，而且会减弱模型的泛化性。

针对 LightGBM，还有一个 `num_leaves` 的参数，可以控制树叶节点的个数。这样树深度可能很深，但树叶节点是受控的，不至于过拟合。

**subsample**

XGBoost 里的 `subsample` 可以控制生成决策树时，使用多少的训练数据集，它的值在 0 到 1 之间。使用所有的训练集来生成决策树不是更好？其实这是一个误解。在实践中，每轮迭代过程中，使用不同的一部分数据来生成决策树，会避免过拟合，让决策树的泛化效果更佳。这个实际上类似于一个正则化参数。LightGBM 里对应的是 `bagging_fraction` 参数。

**colsample_bytree/colsample_bylevel**

XGBoost 的这个参数可以让模型迭代时，使用一部分特征来生成决策树。这个参数也是解决过拟合问题，增加模型泛化性。避免某些权重高的特征对模型造成过大的影响。在 LightGBM 里，对应的参数是 `feature_fraction` 。

**min_child_weight**

这是一个正则项参数，当增大这个数值时，模型的正则项权重变大。针对 XGBoost 和 LightGBM 模型，这是个非常重要的调优参数。针对不同的数据集，这个参数的最优值，可以从 0 到 300，所以不要设置一些不必要的限制。在 LightGBM 里对应的参数叫 `min_data_in_leaf`。除此之外，正则项参数还有 lambda, alpha 等正则项参数可以调校。

**eta/num_round**

`eta` 是学习率，`num_round` 是迭代次数，针对 GBDT 就是要构造多少棵决策树。通常情况下，较小的学习率可以获得更好的泛化性，但需要更多地迭代次数相配合。这样导致训练时间会变长。一个策略是，固定一个较小的学习率，如 0.1 或 0.01，然后通过调整迭代次数来控制模型的训练。还可以使用 early stopping 技术，即检查交叉验证数据集的评分，当交叉验证数据集的评分不再增加时，停止训练。

当获得一个较好的迭代次数时，有一个技巧可以增加模型的准确性。即，把学习率减半，但把迭代次数翻倍。这样处理后，模型的训练时间会变长，但准确性会提高。

**seed**

另外一个参数是随机因子。针对有些竞赛，改变一个随机因子，可能就会导致更好的模型准确性。实际上，这个是不太合理的，说明数据有问题。或者，另外一个解决方案是把随机因素通过 KFold 交叉验证数据集考虑进去。一般情况下，只需要检查一下，随机因子不太影响训练结果即可。如果影响较大，需要找其他的办法来解决这个问题。

#### RandomForest/ExtraTrees

RandomForest 和 GBDT 算法不同的地方在于，RandomForest 会构造多个独立的决策树，所以构造的树越多越不容易过拟合。而 GBDT 算法中，后面的树是在前面的树的基础构建的，所以树越多，越容易造成过拟合。

**n_estimators**

决策树的个数越多，训练起来越慢。决策树数量越过一定程度后，训练变慢但算法准确性却不再提高。一般情况下，可以选择 10 作为初始值，观察训练的时间以及模型的准确性，以此为基础进行微调。如果模型训练起来很快，可以设置一个更大的值，比如 200 再观察训练的时间。最终可以画出一个决策树数量和模型针对交叉验证数据集准确性的学习曲线，从而选择一个合适的参数。

**max_depth**

控制树的深度，树的深度越大，对一些互相作用的特征越有效。可以设置为 None，这样树的深度是没有限制的。但过深的树会容易造成模型过拟合。一般经验值是设置为 7，然后再调整。当然，这个参数的最优值可能是 10，20 甚至更大。当树的深度很大，模型没有过拟合时，需要考虑手动合并一些特征，或者找出互相作用的特征。

**max_features**

构造决策树时，哪些特征可以用来作为树的分支判断条件。值越大，树模型的训练越快。

**min_samples_split**

决策树可分支的最小节点数。这一参数用来作为正则项避免模型过拟合。

**criterion**

决策树分裂的依据，可以基于 gini 或基于 entropy 。一般情况下 gini 会好一点，但有时 entropy 会更好。

### 神经网络

市面上有神经网络库，Keras, TensorFlow, MxNet, PyTorch 等。相对而言，Keras 和 PyTorch 更容易使用一些。

TODO: 学习完 PyTorch 后再来重看这个视频

### 线性模型

Scikit-learn 的 SVC/SVM 模型的最大优势是基本不需要对参数进行优化，默认参数已经足够好了。scikit-learn 里的 SVC/SVM 是对 liblinear 和 libSVM 的封装，一个缺点是不支持多线程并行训练。要做到这一点，需要自己手动编译相应的库。

此外，常见的线性模型还有 LogisticRegression/LinearRegress 以及 SGDClassifier/SGDRegressor 等算法。Vowpal Wabbit 的 FTRL 有个大的特点是，它不会一次性地把所有数据都读入内存，而是一次从硬盘读一条训练样本。这样我们可以使用它训练超大数据集。

针对 SVM ，一般先选择一个比较小的 `C` 参数，比如 $10^{-6}$，然后看看训练速度及准确性如何，然后不断地加大，每次增大 10 倍。因为较小的 `C` 参数可以获得较快的训练速度。

针对 L1 和 l2 正则项，他们各有优势。L1 正则项会产生一个稀疏参数矩阵，它会直接把不重要的特征丢弃。L2 正则项会尽量让每个特征都有少量的贡献。

### 总结

* 不要花费太多时间来调节模型参数。
  只有当没有办法从特征工程里获得更好的改善时；或者在有限制的计算资源，需要回忆训练速度时，才花时间来调度模型参数。我们不可能通过调整模型参数来从竞赛中获胜。分析特征，创建新特征，利用一些数据泄漏以及适当的洞察力，才是从竞赛中获胜的法宝。
* 保持耐心。
  有时候一个模型需要训练较长时间，超过几十分钟。
* 尽量取平均值。
  比如提交前，训练选择 5 个 random seed，然后训练五个模型，取他们预测值的平均值作为预测结果提交。再如，使用 XGBoost 时，最佳的树深度是 5 ，那么我们可以选择深度分别是 4, 5, 6 ，然后训练三个模型，并取其预测值的平均值作为最终预测值提交。这样也可以尽可能地增大模型的泛化效果。

## 竞赛实践

本节描述实际参加竞赛时的一些思路。

### 简介

不同的参赛目标会有不同的做法。具体参阅 w4_101_Practical guide.pdf

#### 数据导入

* 对数据做一些基本的预处理，然后把数据保存成 hdf5/npy 格式。这样可以节省大量的加载数据的时间。
* 默认情况下，数据是在 64-bit 数组保存的。大部分时候这是不必要的，可以转换为 32-bit 来节省一半的内存和训练时间。
* Pandas 支持把数据分块处理。这样可以利用有限的内存处理大量的数据。

#### 模型性能验证

大部分情况下，即使针对只有 5 万或 10 万行的中等大小的数据集，也可以使用简单的 `train_test_split` 就够了，而不需要复杂的 `KFold` 交叉验证。因为 `KFold` 交叉验证不但复杂，而且速度慢。只有在后期遇到瓶颈，模型性能很难再优化，你试图做模型进行细节的优化时，才需要使用 `KFold` 循环验证来判断是否模型性能有提升。

#### 模型选择

针对模型选择，开始时可以从较快的模型，如 LightGBM 开始。模型训练速度快，可以快速验证特征工程是否有效。此外，要注意模型一般情况下包含 linear model 和 tree-based model，不同的模型对特征预处理不同。只有在对特征工程效果较满意的情况下，才去偿试一些训练较慢的模型，如 SVM, RandomForest, Neural Networks 等。

#### 快即是好

* 不需要花费太多时间关注代码质量，或编写好的类层次结果。这往往很花时间，但对结果没有大的帮助。
* 不要试图去验证每次微小的变化。对特征做了一些小的变化，就去验证结果，可能会花费很多时间。
* 如果计算资源不足，需要等待很长时间。一个更好的选择是花钱租用一个更强大的服务器。

#### 建立流水线

从最简单的模型开始建立流水线，不要一开始就选择复杂而慢的模型。从读取数据到预处理再到训练，最终写入提交结果。由简入繁，遵循规律。此外，对问题的领域知识要有足够的了解，只有这样，我们才能根据领域知识生成一些高效的特征。

### 流水线

* 理解问题，学习问题领域知识（1 天）
* 通过 EDA 理解数据，据此确定交叉验证策略（1-2 天）
* 特征工程（3-4 天）
* 偿试不同的模型（3-4 天）
* 对模型进行组合（3-4 天）

#### 理解问题

* 问题的种类（图像识别，文档归类，时间序列等等）及问题领域知识
* 数据量大小
* 使用什么样的模型评价标准

#### EDA

* 分别针对训练样本和测试样本，画出原始特征的柱状图。确保这些特征在训练样本和测试样本里分布情况是差不多的。如果分布不一致，则在交叉验证数据集的制作时就需要特别小心。
* 画出单个特征和目标值的关系图，如果有时间特征的话，还会画出时间与目标值的关系图
* 对数值特征进行分段，并画出相关矩阵

#### 交叉验证策略

确认交叉验证策略很重要，它可以帮助我们以适当地方式评估模型的性能。有了交叉验证方法，我们创建新特征，或使用不同的模型进行训练时，才能正确地评估是否有用。

* 如果是时间序列数据，那么需要使用 time-based validation，即使用过去的数据预测未来的数据。这就要求对交叉验证数据集进行以时间为基础的划分。
* 如果测试数据集有分组的情况，那么在制作交叉验证数据集时，也要创建适当的分组，确保交叉验证数据集和结构和测试数据集类似。
* 如果是测试数据集是随机样本，那么可以使用 KFold 来进行交叉验证。

#### 特征工程

不同的问题需要有不同的特征工程策略，对图片识别，声音识别，文本归类，他们都有不同的特征工程策略。

![feature engineering](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_feature_engineering.png)

#### 建模

不同的问题需要用不同的模型。

![modeling](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_modeling.png)

#### 模型组合

![ensembling](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_ensembling.png)

## 特征工程

特征工程的主要目的是根据现有的特征生成新的特征，让模型更容易训练，提高模型的准确性。

### 基于统计信息和邻近信息的特征工程

假设有如下的数据集，一个典型的解法是，使用 categorical feature 来处理这些特征，然后使用模型进行训练。但这种解法有个问题是，总是把一个样本当作独立的个体来看待，没法明确地和整体信息关联。

![categorical feature](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_feature_engineer.png)

为了解决这个问题，可以使用特征工程算出一些统计信息，比如算出一个用户和页面的平均，最高，最低价格。这样就可以创建出一些新特征，丰富了训练样本数据的信息量。

![categorical feature](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_feature_engineer_2.png)

![categorical feature](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_feature_engineer_3.png)

实际上，不止于此，还可以创建一些其他的特征，比如用户访问的页面数量，一个 session 的页面访问数量，用户访问最多的页面的数量等等。其核心思想是使用统计学的方法，增加训练样本的信息量。

如果可以分组的特征怎么办呢？一个方法是使用临近的数据来产生新特征。一方面，这种方法，比较难实现，也比较难提取出有价值的信息。从另外一个方面来看，正因为这种方法灵活，需要根据业务场景和背景知识来进行特征工程，有更多的可能性和潜力。比如，需要预测房价，可以计算邻近 500m, 1km, 5km 的的房价均值。或者计算邻近区域的医院数量，学校数量等。

### 基于矩阵因子的特征工程

#### 什么是矩阵因子

矩阵因子 (Matrix Factorization) 是一种数据降维的技术。矩阵因子的数学定义是，一个矩阵 A ，找到另外两个矩阵，P 和 Q ，使得 $A \approxeq P Q$。问题是，我们为什么要这样做呢？其目的有：

* 数据压缩
  假设一个矩阵是 1000 x 1000 的矩阵，保存这个矩阵需要保存 100 万个数据。如果 A 是一个低[秩](https://baike.baidu.com/item/秩/13388670)矩阵，它的秩是 50，这样我们可以找出矩阵 P 和 Q，使得 $A = PQ$，且 P 这 1000 x 50 的矩阵，Q 为 50 x 1000 的矩阵。这样保存了矩阵 P 和 Q，就可以算出矩阵 A 。而保存 P 和 Q 只需要保存 1000 x 50 + 50 x 1000 ，即 10 万个数据，比原来的 100 万减少了 90%。这种一般应用在图片压缩等领域。
* 区分模式和噪音
  假设矩阵 A 的行表示一个用户，列表示一部电影，矩阵元素 $A^{i,j}$ 表示第 i 个用户是否喜欢第 j 个电影。这个数据的收集过程是这样的，用户看过的电影会点喜欢，对没看过或不喜欢的，则没有任何操作。故 0 表示用户没看过或不喜欢这个电影，1 表示用户喜欢这个电影。如果我们要基于这个数据开发一个推荐系统，当用户点击了喜欢某个电影后，我们希望给用户推荐一些他也可能喜欢的电影。怎么样实现这个推荐系统呢？一个方法是，找到这个矩阵 A 的矩阵因子 P 和 Q，使得 $A \approxeq P Q$。通过降低 P 和 Q 的秩，我们可以使得模型尽量描述数据的特征，丢弃数据的噪声。假设我们找到了最优的 P 和 Q，则计算出来的 $\hat{A} = P Q$ 矩阵里，某个元素是 1，而对应的 A 矩阵的元素是 0，则我们可以认为这个用户可能是喜欢这个电影的。就可以推荐给用户。

参考链接：https://www.quora.com/What-is-matrix-factorization

矩阵因子在特征工程上的应用方向之一，是进行特征合并。比如针对文本信息，我们可以使用 Vanilla BOW 技术，使用 TF-IDF 技术，还可以使用 BOW bigrams 来处理文本，从而得到不同的特征矩阵，我们可以合并这些特征矩阵，只取里面最有用的信息，这就是数据降维技术来进行特征合并。

![Dimension reduction](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_mf.png)

#### 矩阵因子的实现

scikit-learn 在 `sklearn.decomposition` 包里有 Matrix Factorization 的各种实现。

* SVD 和 PCA 是矩阵因子的标准工具
* TruncatedSVD 适用于稀疏矩阵，比如 TF-IDF 处理后的矩阵
* Non-negative Matrix Factorization (NMF) 处理的矩阵元素必须是非负数，处理后矩阵因子的元素也都是非负数

NMF 处理后的特征数据对 tree-based 模型更做好。针对 Microsoft Mobile Classification Challenge，分别使用 PCA 和 NMF 对特征进行处理后的效果图。从图中可以看出来，NMF 把特征转换为坐标轴对齐，从而使得 tree-based 模型更容易对特征进行处理。

![NMF](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_nmf.png)

我们还可以使用一些变形的 NMF 转换来提高模型的泛化效果。如下图，使用标准的 NMF 和变形的 NMF 转换出来不同的特征，使用模型组合的方法，可以达到更高的模型泛化效果。

![非标准 NMF](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_n_nmf.png)

另外一个需要注意的事是，我们需要对训练数据和测试数据使用统一的转换规则。比如下面是错误的处理方法：

```python
pca = PCA(n_component=5)
x_train_pca = pca.fit_transform(x_train)
x_test_pca = pca.fit_transform(x_test)
```

下面者正确地处理方法：

```python
x_all = np.concatenate(x_train, x_test)
pca.fit(x_all)
x_train_pca = pca.transform(x_train)
x_test_pca = pca.transform(x_test)
```

矩阵因子分解是一种带信息失真的处理技术，不是对所有的模型都有用。但对特定的问题，可以产生良好的效果。它起作用的主要机制是提高模型的泛化效果，通过矩阵因子分解，去除噪声数据。

### 特征相互作用法创建新特征

特征相互作用法，是指通过分析特征，把在逻辑意义上有相互作用的特征合并起来，从而创建出新的特征。举个例子，针对广告预测的例子，有个特别是广告类型，是个 categorical feature，还有一个是网站类型，也是个 categorical feature。实际上，用户对广告的点击率，和广告类型和网站类型的组合相关，而不是单单和广告类型或网站类型相关。基于这样的事实，我们可以把这两个特征合并成一个新的组合特征，如下图所示：

![特征组合](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_feature_interaction.png)

数值类的特征也可以进行组合，比如针对数据中心主机性能的监控，我们知道主机的 CPU 占用率和网络吞吐量。一般情况下，CPU 使用率和网络吞吐量是成正比的，即用户访问越多，CPU 使用率就越高。当 CPU 使用率很高，但网络吞吐量比较小时，这个时候这个机器可能就出现异常了，比如进入了死循环了。如果我们想检测出这种异常，可以选择 *CPU 使用率* / *网络吞吐量* 来作为一个新的特征。常用的特征交互计算公式可以是任何数值计算方法，包括求和，乘法，除法等等。

特征相互作用法对 tree-based 模型特别有用，因为 tree-based 模型往往比较难从数据里获取出特征相互作用的模式。在实践中也需要注意，如果我们有 N 个特征，则我们可以有 N * N 种特征交互方法，到底哪些特征有相互交互作用呢？可以从两个维度来看这个问题。

* 其一：通过业务背景知识，来手动选择特征进行合并
* 其二：通过查看决策树的特征分裂点，那些经常一些出现的特征分裂点，可能存在相互作用关系。这种方法往往对我们有启发意义。

对特征相互作用法来说，一般是先构建两个特征的相互作用。更多个特征的相互作用有时是一种艺术，而不是技术。此外，特征相互作用很难进行自动化选择和处理 (CatBoost 可以部分地支持 categorical feature 的自动相互作用处理，在某些问题下，这个库的性能很好)。

针对决策树，有一个通用的交互特征创建方法是：

* 把决策树中每个叶子节点，都创建一个 binary feature
* 把训练样本在决策树中的树叶的索引位置作为一个新的 categorical feature

实际这一机制很简单，scikit-learn 的 tree-based 模型都有 `apply()` 方法可以直接返回训练数据集的树叶索引。XGBoost 库里的 `predict(pred_leaf=True)` 也可以返回类似的值。

![从决策树构建交互特征](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_fi_dt.png)

### tSNE

#### Manifold learning

在 scikit-learn 里有个专门的包 `sklearn.manifold` 实现 Manifold learning 。scikit-learn 里有篇文章 [Comparison of Manifold Learning methods](http://scikit-learn.org/stable/auto_examples/manifold/plot_compare_methods.html) 对比了不同的 manifold learning 方法的转换效果。

![Manifold learning](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_manifold_learning.png)

tSNE 是一种 manifold learning 技术，即特征转换的技术。

#### 什么是 tSNE

什么是 tSNE？可参阅链接：[how to use t-sne effectively](https://distill.pub/2016/misread-tsne/)

* Those hyperparameters really matter
* Cluster sizes in a t-SNE plot mean nothing
* Distances between clusters might not mean anything
* Random noise doesn’t always look random.
* You can see some shapes, sometimes
* For topology, you may need more than one plot

简单地讲，tSNE 是一种数据可视化技术，它可以在一个二维空间里展示高维度的数据，经常用在 EDA 里。通过 tSNE 技术，也可以创建新特征。

#### 使用 tSNE 创建新特征

使用 tSNE 合建新特征的方法是，调整好 tSNE 的参数，然后使用 tSNE 转换后的特征与原特征联合起来即可。但要注意几个事情：

1. tSNE 的参数非常重要，tSNE 的参数决定了创建出来的特征是否会对模型有帮助。
   解决方法是使用多个 `perplexity` 参数，生成多个数据转换，同时使用这些转换后的数据。
2. 训练数据集和测试数据集必须合并起来，使用同一个 tSNE 进行转换。
3. tSNE 所呈现出来的数据类别有时会有误导性，比如随机数据在某些参数下也会呈现结构化特征。
4. 如果原始特征太多，如超过 500 ，tSNE 需要很长时间来转换。最好用 PCA, TruncatedSVD 等方案进行数据降维后再使用 tSNE 处理。
5. scikit-learn 库里有 tSNE 的实现，但一个单独的 python 包 `tSNE` 具备更快地性能

## 模型组合 ensemble

模型组合通过把多个模型通过一定的方式组合起来，达到更高的准确性。几个常用的模型组合：

* Averaging: 对模型求平均值，典型地两个模型权重各占一半
* Weighted averaging: 可能对模型取特定的权重，比如第一个模型占 70%，第二个模型占 30%
* Conditional averaging: 条件均值。比如对两个模型，当特征 x < 50 时采用模型 1，当 x>= 50 时，采用模型二

![ensemble - averaging](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_ensemble_average.png)

针对上图的两个模型，纵坐标是实际的年龄，横坐标是预测的年龄。左边的模型，针对 50 岁以下的预测效果好，针对 50 岁以上的误差较大。右边的模型相反。可以使用模型组合来优化这个问题。可以分别使用 averaging, weighted averaging, conditional averaging 来优化这一问题。需要注意，两个模型平均起来，合并后的模型指标 $R^2$ 可能比两个单独的模型都差，比如使用 averaging 方法时。但总体上讲，模型组合会有更好的模型泛化性。

### Bagging

Bagging 是指通过对相同模型的不同版本进行组合以提高模型指标的方法，bagging 组合的各个版本之间是独立的。典型的 bagging 技术是随机森林。bagging 组合可调的参数有：

* seed: 随机数种子
* row sampling: 每个模型只用部分训练数据集进行训练
* shuffling: 对训练数据集打乱重排
* column sampling: 每个模型只用部分特征进行训练
* 调整模型本身的参数
* number of models: 进行 bagging 的模型个数。一般情况下，个数越多模型指标越好，但模型越多，训练时间也会越长
* 并行训练

下面是使用随机森林进行 bagging 的示例代码：

```python
model = RandomForestClassifier()
bags = 10
seed = 1

bagged_predictions = np.zero(test.shape[0])
for n in range(0, bags):
    model.set_params(random_state=seed + n)
    model.fit(train, y)
    preds = model.predict(test)
    bagged_predictions += preds

bagged_predictions /= bags
```

### Boosting

Boosting 和 bagging 不同的地方在于，使用 bagging 进行组合的模型之间是相互独立的。而 boosting 则是串行建立模型组合，**每个模型都建立在之前的模型的训练结果之上**。主要的的 boosting 方法有：

* 基于权重的 boosting 方法（weight based）
* 基于残差的 boosting 方法（residual based）

#### Weight based boosting

Weight based boosting 的原理是：

1. 用模型基于训练数据集对结果进行预测
2. 计算预测值和真实值的误差绝对值 abs.error
3. 创建一个新的特征 weight，称为权重特征，其值为 1 + abs.error
4. 使用包含权重特征的数据集继续训练模型，得出预测值
5. 重复上述步骤，直到模型达到理想的指标

![weight based boosting](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_weight_boosting.png)

Weight based boosting 有一些可调的参数：

**学习率 Learing rate (shrinkage or eta)**

学习率控制控制每个模型的贡献程度，比较理想的情况是，每个模型贡献一点点。这样可以有效地控制过拟合。针对第 N 个新训练的模型，其预测值为：

PredictionN = pred_0 * eta + pred_1 * eta + ... + pred_N * eta

**模型个数 number of estimator**

这个参数和学习率成反比，即更多个数的模型，我们需要更小的学习率。有时候很难找到一个合适的最优值，往往需要借助交叉验证数据集来找到合适的值。一个典型的方法是，我们先设置一个固定的模型个数，比如 100。然后保持模型个数不变，基于交叉验证数据集的验证结果，找到学习率的最优值是 0.1。然后，我们把模型个数翻倍，把学习率减小为原来的一半，这样我们就可以用较快的速度找到较好的组合。因为模型越多，学习率越小，训练时间就越长。当然，模型个数和学习率不一定是严格的线性的关系，模型个数翻倍后，可能最优的学习率是原来的 0.6 或原来的 0.4 。

**输入模型 input model**

输入的模型即进行 weight based boosting 的模型可以是任意支持设置训练样本权重的模型。

**boosting 子类型**

AdaBoost: scikit-learn 里的 `AdaBoostClassifier` 和 `AdaBoostRegressor` 是性能良好的实现。
LogitBoost: Weka (Java) 是个不错的实现

#### Residual based boosting

Residual based boosting 的原理是：

1. 用模型基于训练数据集对结果进行预测
2. 计算预测值和真实值的误差值，这里的误差是带方向性的，即预测值比目标值大，则为负数，称为残差 (residual)
3. 把残差作为新的预测值 y，然后用原来的训练数据集对新的预测值进行预测
4. 重复上述步骤，直到模型达到理想的指标

![residual based boosting](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_residual_boosting_1.png)

这里给出的例子中，第二行目标值是 1 ，预测值是 0.75，残差是 0.25。接下来，我们使用残差作为目标值，再次进行预测。

![residual based boosting](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_residual_boosting_2.png)

此时，第二行的目标值是 0.25，预测值是 0.20。这两次预测组合起来，第二行的预测值是 0.75 + 0.20 = 0.95，离真正的目标值 1 已经很接近了。我们可以继续这个过程，第三轮迭代时，目标值是新的残差 0.05，以此作为目标值进行预测。逐步迭代下去，即可得到非常接近目标值的预测值。

著名的 XGBoost, LightGBM，H2O's GBM, Catboost, Sklean's GBM 等都是这个算法的实现。

Residual based boosting 的可调参数有：

**学习率 Learing rate (shrinkage or eta)**

学习率控制控制后续模型的贡献程度，经过 N 轮迭代后，预测值为：

Prediction = pred_0 + pred_1 * eta + ... + pred_N * eta

从上式可以看出来，第一个模型占的比重是最大的，而后面的模型的预测值会乘以学习率。如，学习率为 0.1 时，表达的含义是总的预测值往新叠加的模型的预测值方向移动 10% 。针对上述的例子，如果学习率是 0.1，则经过二轮迭代后，其预测值为 0.75 + 0.2 * 0.1 = 0.77。

**模型个数 number of estimator**

这个参数和学习率成反比，即更多个数的模型，我们需要更小的学习率。有时候很难找到一个合适的最优值，往往需要借助交叉验证数据集来找到合适的值。一个典型的方法是，我们先设置一个固定的模型个数，比如 100。然后保持模型个数不变，基于交叉验证数据集的验证结果，找到学习率的最优值是 0.1。然后，我们把模型个数翻倍，把学习率减小为原来的一半，这样我们就可以用较快的速度找到较好的组合。因为模型越多，学习率越小，训练时间就越长。当然，模型个数和学习率不一定是严格的线性的关系，模型个数翻倍后，可能最优的学习率是原来的 0.6 或原来的 0.4 。

**使用训练数据集的子集 row resampling**

可以有效地控制过拟合，实际上这个参数在 weight based boosting 里也可以使用。

**使用特征子集 column resampling**

可以有效地控制过拟合，实际上这个参数在 weight based boosting 里也可以使用。

**输入模型 input model**

输入的模型，一般适用于基于决策树的模型。

**boosting 子类型**

Fully gradient based: 如上述学习率参数，对后续的模型，使用一个百分比来靠近预测值。
Dart: 迭代的模型里，不采用前面的全部模型，而随机去掉几个模型。假设，drop out 比例是 20%，当前我们训练了 10 个模型，则第 11 个模型不使用前面 10 个模型的预测结果，相反，它会随机丢掉 2 个模型，只取 8 个模型进行叠加组合。

### Stacking

Stacking 也是一种性能优良的模型组合的技术。在 kaggle 竞赛中，最终总是或多或少会用到 stacking 技术来提升分数。

它的主要步骤如下：

1. 把数据集分成训练数据集和交叉验证数据集
2. 使用一个模型对训练数据集进行训练，然后同时对交叉验证数据集和测试数据集进行预测
3. 使用另外一个不同的模型，重复上述步骤，直到把所有你想 stacking 的模型都用上为止
4. 把所有的模型针对交叉验证数据集预测结果组装成一个数组，组成一个新的训练数据集
5. 把所有的模型针对测试数据集预测结果组装成一个数组，组成一个新的测试数据集
6. 使用另外一个新的简单的模型（元模型），对交叉验证数据集的预测结果进行训练
7. 使用这个元模型，对新的测试数据集进行预测

![stacking](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_stacking.png)

如上图所示，A 是训练数据集，B 是交叉验证数据集，C 是测试数据集。针对数据集 A 分别训练模型 0，1，2，然后使用这三个模型分别对 B 和 C 进行预测，预测结果分别放在 B1 和 C1 数组里，生成新的训练数据集和测试数据集。然后，再拿 B1 训练出模型 3，再拿模型 3 来对 C1 进行预测。最终得到预测结果。

下面是一个用 Python 写的简单的 stacking 的例子。例子中，使用 `RandomForestRegressor` 和 `LinearRegression` 模型进行叠加，最后再使用 `LinearRegression` 作为元模型进行第二轮的训练和预测。

```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.model_selection import train_test_split

tr, cv y_tr, y_cv = train_test_split(train, y, test_size=0.5)
# 模型 1 和模型 2 进行叠加
model1 = RandomForestRegressor()
model2 = LinearRegression()

model1.fit(tr, y_tr)
model2.fit(tr, y_tr)

pred1 = model1.predict(cv)
pred2 = model2.predict(cv)

pred1_test = model1.predict(test)
pred2_test = model2.predict(test)
# 预测结果进行叠加
pred_stacked_cv = np.column_stack((pred1, pred2))
pred_stacked_test = np.column_stack((pred1_test, pred2_test))
# 元模型进行训练/预测
meta_model = LinearRegression()
meta_model.fit(pred_stacked_cv, y_cv)
pred_test_final = meta_model.predict(pred_stacked_test)
```

Stacking 可以达到很好的效果。如下图所求，右图是我们在之前章节里提到，使用条件平均的方式组合起来的模型。右图是使用 stacking 训练的效果。从图中可以看出来，两者效果差不多。而使用条件平均方式组合，需要预测知道预测值（大于 50 还是小于 50），这是实际问题中往往不具备可操作性，因为预测值往往是未知的。

![stacking](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_stacking_2.png)

stacking 组合技术有几个注意事项：

* 时间序列：当训练数据集是时间序列时，数据划分需要以时间为维度进行划分
* 多样性和性能并重：叠加的模型多样机，比如结合 tree base 模型和 linear base 模型。特征多样机，比如针对 categorical feature，分别使用 one hot encoding 和使用 label encoding 来处理特征。
* 指标瓶颈：当叠加的模型个数超出一定数量后，模型的指标就没法再提升了。所以，太多的模型无法提升指标，反而需要花费很多时间去训练。
* 元模型要尽量简单。因为我们期望叠加的模型已经把数据规律都抓出来了，元模型只是做个简单的组合。一般使用线性模型。使用树模型时，树的深度要尽量控制在较小的水平。

### StackNet

StackNet 比 stacking 更进一步，它利用 stacking 的技术，构建一个类似神经网络的多层结构。与神经网络不同的是，神经网络的不同层的神经元之间一般是一个线性模型（逻辑回归），而 StackNet 则不限制模型。

![stacking](https://raw.githubusercontent.com/kamidox/blogs/master/images/kaggler_stacknet.png)

回忆 stacking 的过程，我们需要把数据集分成两半。如果使用 StackNet，则每叠加一层，就要把数据分成两半，这样对数据量较小的情况下就会有问题。一个解决方案是使用 `KFold` ，比如针对 4 fold，每次拿其中 75% 的数据来训练，25% 的数据作为交叉验证数据集做预测，分别针对这些 fold 执行相同的操作，则可以完整地把所有的训练数据集都利用起来。

此外，和神经网络相比，StackNet 除了可以使用上一层的结果作为输入，也可以直接拿第一层的结果作为输入，甚至可以把原始的输入也加上。这样可以更灵活地处理这些特征。

第一层技巧：构建 StackNet 第一层模型时的一些技巧

* 模型多样性
  * 2-3 个 gradient boost trees，如 LightGBM, XGBoost, H2O, CatBoost 等。为了确保多样机，可以选择不同深度的树，然后调整一个合适的参数。
  * 2-3 个神经网络模型，keras, pytorch 等。为了确保多样性，可以让模型从多层神经网络到三层神经网络，各一个。
  * 1-2 个 ExtraTree/RandomFroest 等（scikit-learn）
  * 1-2 个线性模型，如 logicstic/ridge regression, linear SVM 等
  * 1-2 个 KNN 模型
  * 1 个非线性 SVM，如果数据量不大的情况下
* 特征多样性
  * Categorial feature: one hot encoding, label encoding, target encoding, frequency encoding 多种编码方式，这样可以抓到特征的多样性
  * Numerical feature: 去掉/保留 outliers, binning, derivatives, percentiles, scaling
  * 使用 Feature interactions 创建新特征

中间层技巧：

* 简单的模型
  * gradient boost tree with small depth (2-3 层即可)
  * linear model with high regularzation
  * extra trees
  * shallow networks with one hidden layer
  * knn
* 特征工程
  * pairwise differences between meta features
  * row-wise statistics like average or stds
  * standard feature selection techniques

StackNet 的参考实现：

* https://github.com/kaz-Anova/StackNet StackNet 的实现，不过是用 Java 实现的
* Stacked ensembles from H2O
* https://github.com/reiinakano/xcessiv 是个完整的工具，提供基于网页的多种模型的组合工具
* w4_407_Ensembling Tips and Tricks.pdf 文档值得一读，它提供了各种各样的 StackNet 构建方法，包括时间序列数据的处理方法。
* https://mlwave.com/kaggle-ensembling-guide/ 值得一读的文章，从原理到实践，还有 Github 上的代码可用
* https://github.com/MLWave/Kaggle-Ensemble-Guide 上文对应的一些工具脚本，包含多种模型组合技术的实现。是个简单的工具，没有正规的产品化。
* https://github.com/rushter/heamy 提供了几种简单的 stacking 实现，包括 stacking, blend, weighted average，是个完备的可用的库。

## 实例

### Crowdflower Competition

### Springleaf Competition

### Microsoft Malware Classification Challenge

https://github.com/geffy/kaggle-malware
https://github.com/xiaozhouwang/kaggle_Microsoft_Malware

### 过往解决方案

Kaggle 过往竞赛的解决方案：http://www.chioka.in/kaggle-competition-solutions/ 。


### Titanic Competition

#### 模型叠加

https://www.kaggle.com/arthurtok/introduction-to-ensembling-stacking-in-python

要点总结如下。

**特征相关性**

去除相关性太高的特征可以提高模型的性能指标。特征的相关性太高意味着有一个是多余的，因为它没有带来额外的信息量。

```python
colormap = plt.cm.RdBu
plt.figure(figsize=(14,12))
plt.title('Pearson Correlation of Features', y=1.05, size=15)
sns.heatmap(train.astype(float).corr(), linewidths=0.1, vmax=1.0,
            square=True, cmap=colormap, linecolor='white', annot=True)
```

需要注意，`train` 是一个 Pandas 的 `DataFrame` 实例，且所有的数据必须都是数值型的。

**特征重要性**

`RandomForestClassifier` 等模型，训练完后，可以通过 `feature_importances_` 获得特征的重要性。当使用多个模型进行叠加时，可以分别查看每个模型的特征重要性信息。甚至把特征权重信息通过条形图 (bar chart) 画出来，直观地观察每个特征的权重。通过特征权重的信息，可以把对所有的模型都不重要的特征去除。这也是一种特征选择方法。此外，还可以看到每个模型对对特定的特征的重要性不同，这也是模型多样性的一种查看方法。针对模型组合，多样性的模型组合才能得到较好的结果。

**模型相关性**

针对模型组合，需要确保模型的多样性。可以把第一层模型的预测结果保存到一个 `DataFrame` 实例里，然后通过 `sns.heatmap` 函数画出各个模型预测结果的相关性。这样可以直观地观察到每个基础模型预测结果的相关性。

#### EDA 数据分析

https://www.kaggle.com/sinakhorami/titanic-best-working-classifier

**特征与目标相关性**

可以使用如下代码快捷地查看特征和目标值的关联关系：

```python
print (train[['Pclass', 'Survived']].groupby(['Pclass'], as_index=False).mean())

   Pclass  Survived
0       1  0.629630
1       2  0.472826
2       3  0.242363
```

上述代码可以简单地看到不同舱位的幸存概率。

**连续值离散化**

有时我们需要把连续值进行离散化。比如年龄，我们希望划分为儿童，少年，青年，中年，老年等。一个简易的方法是直接使用 Pandas 里的 `cut` 函数进行等距离划分。此外，`qcut` 还可以进行分位数划分。

*注：分位数也称为 Quantile ，把一组按照升序排列的数据分割成n个等份区间并产生 n - 1 个等分点后每个等分点所对应的数据。按照升序排列称作第一至第 n - 1 的 n 分位数（如果等分点在其左右两个数据的中间，那么该等分点所对应的数就是其左右两数的平均数）。*

如果需要更复杂的自定义划分，可以画出柱状图，根据数据的分布情况，选取自定义的划分点。然后使用 `Series.apply()` 函数把连续值离散化。

**缺失值处理**

针对 Emarked 特征，因为它的缺失值较少，且大部分类别都是 S 的，故可以直接把缺失值填充成 S 类别。

针对 Age 特征，缺失值较多。可以求出均值和方差，然后在把 Age 填充为均值左右方差的随机值，如下：

```python
age_avg = dataset['Age'].mean()
age_std = dataset['Age'].std()
age_null_count = dataset['Age'].isnull().sum()

age_null_random_list = np.random.randint(age_avg - age_std, age_avg + age_std, size=age_null_count)
dataset['Age'][np.isnan(dataset['Age'])] = age_null_random_list
dataset['Age'] = dataset['Age'].astype(int)
```

**其他技巧**

使用 `Series.map()` 函数可以把类别数据转换为整数。如：

```python
dataset['Sex'] = dataset['Sex'].map( {'female': 0, 'male': 1} ).astype(int)
dataset['Embarked'] = dataset['Embarked'].map( {'S': 0, 'C': 1, 'Q': 2} ).astype(int)
# Mapping Age
dataset.loc[ dataset['Age'] <= 16, 'Age'] = 0
dataset.loc[(dataset['Age'] > 16) & (dataset['Age'] <= 32), 'Age'] = 1
dataset.loc[(dataset['Age'] > 32) & (dataset['Age'] <= 48), 'Age'] = 2
dataset.loc[(dataset['Age'] > 48) & (dataset['Age'] <= 64), 'Age'] = 3
dataset.loc[ dataset['Age'] > 64, 'Age'] = 4
```

#### 完整流水线

TODO: https://www.kaggle.com/ldfreeman3/a-data-science-framework-to-achieve-99-accuracy

**数据划分策略**

使用 `model_selection.cross_validate` 时，只拿 90% 的数据进行训练，故意留出 10% 的数据不使用，这样可以有效地减少过拟合。

```python
cv_split = model_selection.ShuffleSplit(n_splits=10, test_size=.3, train_size=.6, random_state=0 )
cv_results = model_selection.cross_validate(alg, data1[data1_x_bin], data1[Target], cv=cv_split)
```

**scikit-learn 里的投票模型**

`sklearn.ensemble.VotingClassifier` 是 scikit-learn 里的投票模型。可以实现“硬”投票，即根据 1 和 0 来投票。也可以实现“软”投票，即根据概率来投票。

