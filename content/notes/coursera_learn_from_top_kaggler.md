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

#### 总结

* 预处理（写换为小写，词形还原，词干提取，停止词）
* 使用 N-grams 可以处理文本的上下文信息
* 后处理，使用 TFIDF
