Title: NLP and Deep Learning
Date: 2016-02-29 23:20
Modified: 2016-02-29 23:20
Slug: cs224d
Authors: Joey Huang
Summary: Notes of Stanford cc224d, Deep Learning with NLP
Status: draft

[TOC]

## Lecture 1

**深度学习 (Deep Learning) 和传统的机器学习 (Machine Learning) 的区别是什么？**

传统的机器学习主要分两部分，一部分是特征提取，需要人工从数据中提取出特征，并且想办法用计算机能理解的格式来表达这些特征。另外一部分是是模型，使用计算机能理解的特征数据来训练模型。人工提取的特征慢，而且很容易遗漏。

深度学习能够从原始数据中学习出特征，然后用来训练模型。

**深度学习和神经网络是什么关系？**

神经网络是深度学习的一种算法。实际上，还有其他的概率模型可以应用到深度学习中来。但目前在 NLP 领域效果比较好的，还是神经网络算法。

**应用**

iPhone 上的 Siri 和 Android 上的 Google Now 都是使用深度学习算法来进行语音识别。就连这个课程视频的字幕，也是使用深度学习的算法，把语音直接转换为字幕的。

按照从易到难，自然语言处理的几个典型的应用如下：

**简单**

* 拼写检查
* 关键字搜索
* 查找同义词

**中等难度**

* 从网络或文档中提取信息

**难**

* 机器翻译（号称自然语言领域的圣杯）
* 语义分析（一句话是什么意思）
* 交叉引用（一句话中，他，这个等代词所对应的主体是哪个）
* 问答系统（Siri, Google Now, 小娜等）

## Lecture 2 如何表达一个词语

这一节课探讨如何表达一个词。

### 词典

现实生活中，我们通过查词典来知道一个词的意思，这实际上是用另外的词或短语来表达一个词。这一方法在计算机领域也有，比如 [WordNet](http://wordnet.princeton.edu) 实际上就是个电子化的英语词典。

然而，这一方式有以下几个问题：

* 有大量的同义词，不利于计算
* 更新缓慢，没有办法自动地添加新词
* 一个词释义含有比较明显的主观色彩
* 需要人工来创建和维护
* 很难计算词的相似性
* 很难进行计算，因为计算机本质上只认识 0 和 1

### 基于统计的词语向量表达

在统计语言模型里，我们使用向量来表达一个词。比如，在一个精灵国里，他们的语言非常简单，总共只有三句话：

1. I like NLP.
2. I like deep learning.
3. I enjoy flying.

这样，我们可以看到这个精灵国的词典是 [I, like, NLP, deep, learning, enjoy, flying, .]。没错，我们把标点也认为是一个词。用向量来表达词时，我们创建一个向量，向量的维度与词典的个数相同，然后让向量的某个位置为 1 ，其他位置全为 0。这样就创建了一个向量词 (one-hot)。

比如，在我们的精灵国里，I 这个词的向量是：[1 0 0 0 0 0 0 0], deep 这个词的向量表达是 [0 0 0 1 0 0 0 0]。

看起来挺好，我们终于把词转换为 0 和 1 这种计算机能理解的格式了。然而，这种表达也有个问题，很多同义词没办法表达出来，因为他们是不同的向量。怎么解决这个问题呢？我们可以通过词的上下文来表达一个词。通过上下文表达一个词的另外一个好处是，一个词往往有多个意思，具体在某个句子里是什么意思往往由它的上下文决定。

### 基于上下文的表达

> You shall know a word by the company it keeps. --- (J. R. Firth 1957: 11)

这是现代基于统计语言模型的词的表达方法。有两种方法可以实现基于上下文的词的表达。一种是基于词和文档关系矩阵 word-document matrix，另外一个是基于窗口的 word-word cooccurence matrix。分别介绍如下：

#### word-document matrix

这一表达的理解基础上，词义相近或关联较大的词比较大的概率会出现在同一篇文章里，而词义想差较远的词出现在同一个文章里的概率比较低。这样我们就可以建立一个基于统计语言模型的词的表达。比如，“银行”，“股票”，“投资”等词出现在同一篇文章中的概率会比较高，而“银行”，“猴子”，“椅子”出现在同一篇文章中的概率会比较低。基于这个思想，我们建立一个矩形 X ，当第 i 个词出现在第 j 篇文章中时，就把 $X_ij$ 的值加上 1 。这个矩阵是 $R^{|V| \times M}$，其中 |V| 是词库的大小，M 是文章的个数。这一方法就是经典的 [Latent semantic analysis](https://en.wikipedia.org/wiki/Latent_semantic_analysis)，简称 LSA。

据统计，目前互联网上有 100 亿篇文章，可以看出来这将是个巨大无比的矩阵。另外一个角度，一篇文章里不可能包含所有的词，所以这也是一个稀疏矩阵，矩阵里很多元素的值都是 0。

#### word-word cooccurence matrix

基于窗口机制的词关联性矩阵可以很好地表达语义 (semantic) 和语法 (syntactic)。它也需要建立一个矩阵，所不同的是行和列都是词典里的词，所以这是一个方阵。来看一下我们精灵国的词典 [I, like, NLP, deep, learning, enjoy, flying, .]，精灵国的语料库也非常简单：

1. I like NLP.
2. I like deep learning.
3. I enjoy flying.

假设我们的窗口大小为 1 ，即一个词只关心前面和后面 1 个词的关联性，通过扫描这个语料库，可以得到下面的矩阵：

counts    | I | like | enjoy | deep | learning | NLP | flying | .
----------|---|------|-------|------|----------|-----|--------|---
I         | 0 | 2    | 1     | 0    | 0        | 0   | 0      | 0
like      | 2 | 0    | 0     | 1    | 0        | 1   | 0      | 0
enjoy     | 1 | 0    | 0     | 0    | 0        | 0   | 1      | 0
deep      | 0 | 1    | 0     | 0    | 1        | 0   | 0      | 0
learning  | 0 | 0    | 0     | 1    | 0        | 0   | 0      | 1
NLP       | 0 | 1    | 0     | 0    | 0        | 0   | 0      | 1
flying    | 0 | 0    | 1     | 0    | 0        | 0   | 0      | 1
.         | 0 | 0    | 0     | 0    | 1        | 1   | 1      | 0

这样的矩阵可以很好地捕获到词之间的关联性信息。但这个矩阵也是比较大的，典型地，它随着词典的增加而增加。而且这也是个稀疏矩阵。因为词典中，能组成上下文的词还是少数的。我们的首要任务是给矩阵降维。

#### 奇异值分解

通过奇异值分解可以有效地把矩阵的维度降下来。在学习线代时，根本就不知道奇异值分解这种奇怪的东西到底有什么用，没有想到会在这里派上用场。关于奇异值分解的几何含义，可以参阅[We Recommend a Singular Value Decomposition](http://www.flickering.cn/数学之美/2015/01/奇异值分解（we-recommend-a-singular-value-decomposition）/)，这是一篇深入浅出的译文。

针对 word-word cooccurence matrix，奇异值分解的思路如下：

![neural networks](https://raw.githubusercontent.com/kamidox/blogs/master/images/nlp_svd.png)

分解后矩阵 U 里的行向量就表示一个词。我们可以用 Python 简单实现如下：

```python
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

# 词典
words = ['I', 'like', 'enjoy', 'deep', 'learning', 'NLP', 'flying', '.']
X = np.zeros((8,8))
# 语料库
corpus = ['I like NLP.', 'I like deep learning.', 'I enjoy flying.']
# 这里我们简单起见，直接写出从语料库里扫描后得到的字典
X[0, 1] = X[1, 0] = 2
X[0, 2] = X[2, 0] = 1
X[1, 3] = X[3, 1] = 1
X[1, 5] = X[5, 1] = 1
X[2, 6] = X[6, 2] = 1
X[3, 4] = X[4, 3] = 1
X[4, 7] = X[7, 4] = 1
X[5, 7] = X[7, 5] = 1
X[6, 7] = X[7, 6] = 1

U, s, V = np.linalg.svd(X, full_matrices=True)
plt.xlim(-0.8, 0.2)
plt.ylim(-0.8, 0.8)
for i in range(len(words)):
    plt.text(U[i, 0], U[i, 1], words[i])
```

*在 ipython notebook 环境下运行*

运行后会输出如下图片：

![neural networks](https://raw.githubusercontent.com/kamidox/blogs/master/images/nlp_word_relation.png)

从图中，我们可以看到一些有意思的现象，在二维空间里，NLP 和 deep 靠得很近，从我们有限的只有三句话的语料库里就能把这个特征捕获出来了。如果语料库足够大，就可以表达出更多的语义和语法信息了。

我们使用奇异值分解后的矩阵 U 的行向量$u_i$ 来表示一个词。比如，$u_0$ 就表示 I 这个单词，其值为：

```python
In [20]: U[0]

Out[20]:
array([-0.52412493, -0.57285914,  0.0954463 ,  0.38322849, -0.17696338,
       -0.17609218, -0.4191856 , -0.05577027])

In [21]: U[3]

Out[21]:
array([-0.28563741, -0.24791213,  0.35461032, -0.07319013,  0.44578449,
        0.08361414,  0.54872107, -0.46801241])

In [22]: U[5]

Out[22]:
array([-0.30513468, -0.29398899, -0.22343359, -0.19161425,  0.12746094,
        0.49121941,  0.2095928 ,  0.65753537])
```

$u_3$ 和 $u_5$ 分别表示 deep 和 NLP 这两个词。从数据中也可以看到，向量的前两个值比较接近。

这就是数学的美妙之处。一个词竟然可以通过向量来表达。

然而，这样的向量表达还是有一些问题：

* 功能性词汇 (the, is, he, 的, 是) 出现地太频繁了，会影响语法分析。一个方法是生成 word-word cooccurence matrix 时使用计数上限，另外一个方法直接去掉这些功能性
* 上述例子里，我们只计算前后一个词的关联性。我们可以计算得远一点，不同距离使用不同的权重值
* 使用 [Pearson correlations](https://en.wikipedia.org/wiki/Pearson_product-moment_correlation_coefficient) 替代 counts 计数

这些优化的方案可以参阅 [An Improved Model of Semantic Similarity Based on Lexical Cooccurrence - Rohde et al. 2005](http://tedlab.mit.edu/~dr/Papers/RohdeGonnermanPlaut-COALS.pdf)。

然而奇异值分解的方法有一个最大的缺点是计算量还是很大，达到了 $O(mn^2)$ (m > n时)，而且每次添加了一个新词或新的文章，需要重新做奇异值分解，所有的词向量都会更新。作为替代方法，能不能直接学习出这个词的向量，而不通过奇异值分解后获得呢？

### 基于迭代的词语向量表达

实际上，科学家们已经发明了很多这样的算法。

* Learning representations by back-propagating errors.  (Rumelhart et al., 1986)
* [A neural probabilistic language model (Bengio et al., 2003)](http://machinelearning.wustl.edu/mlpapers/paper_files/BengioDVJ03.pdf)
* [NLP from Scratch (Collobert & Weston, 2008)](http://ronan.collobert.com/pub/matos/2011_nlp_jmlr.pdf)
* [word2vec (Mikolov et al. 2013)](https://en.wikipedia.org/wiki/Word2vec)
* [Glove: Global Vectors for  Word Representation - by Pennington et al. (2014)](http://nlp.stanford.edu/projects/glove/)

特别提一下 GloVe 模型，这个是课程老师 Richard Socher 和几位同事在2014年发表的论文。本课程重点介绍 word2vec ，它的主要思想是：直接通过预测一个词的前后几个词的出现概率，来直接得到词的向量。

#### word2vec

这是这节课最难理解的部分，涉及到大量的背景知识，有信息论里的[交叉熵](https://en.wikipedia.org/wiki/Cross_entropy)，有概率论里的 [softmax function](https://en.wikipedia.org/wiki/Softmax_activation_function)，还有一些[微分运算法则](http://blog.kamidox.com/computation-rules-for-derivative.html)。

基于迭代模型的原理，就是利用语料库里的句子作为训练数据集，以每一个词作为中心词，预测其左右两边的一定个数 (称为窗口大小) 的词的概率，最终使整体概率最大。

我们先通过一个简单的例子来看一下基于迭代模型的原理。假设我们的语料库里有一个句子："The cat jumped over the puddle."。模型刚开始训练时，我们以一个很小的随机数作为一个词可能出现在另外一个词前后的概率，作为先验概率。假设我们的窗口大小 c = 2，当 t = 2 时，当中心词 "jumped" 时，它的上下文词是 ["The", "cat", "over", "the"] ，通过这个语料库里的信息，我们就知道这些词分别出现在 "jumped" 单词两边的概率就增加一点点，因为我们从语料库里学习到了这个特征。当 t = 3 时，中心词是 "over"，这个时候上下文词是 ["cat", "jumped", "the", "puddle"]，我们的模型又从这个输入里学习到了一点点特征。这样一直通过语料库来训练这个模型，只要语料库足够大，就可以把这些特征全部学习出来。

这个模型可以很好地解决基于奇异值分解模型的缺点，语料库可以随意增加，只需要作为新的输入来训练模型即可，而不需要从头开始计算。二是新词也可以随意增加，模型遇到没遇到过的词时，可以自己从语料库里学习出这个词的用法。

当然，上面的定性描述是为了帮助理解模型原理，怎么样通过数学来严格地描述这个模型呢？我们直接给出模型的目标函数：

$$
J = \frac{1}{T} \sum_{t=1}^T \sum_{-c \leq j \leq c, j \neq 0} log (p(w_{t+j}|w_t))
$$

我们的目标就是让 J 取最大值，目标函数里有个 log 函数的主要目的是为了数学上的方便。T 是训练时的迭代次数。直观地描述，就是让所有的迭代后，中心词 $w_t$ 的上下文词出现的概率最大。当使用[梯度下降算法](http://blog.kamidox.com/gradient-descent.html)来求 J 的最大值时，我们需要计算目标函数基于 $w_t$ 的偏微分。

在计算偏微分之前，先来看一下 $p(w_{t+j}|w_t)$ 概率怎么算。这是个条件概率，我们重写成 $p(w_o|w_i)$，其中 $w_o$ 表示出现在上下文的词，$w_i$ 表示中心词。这是一个多选择的逻辑回归概率函数。就是我们上文提到的 Softmax function。

$$
p(w_o|w_i) = \frac{\exp \left( {u_o^T v_i} \right) } {\sum_{w=1}^W \exp \left( {u_w^T v_i} \right)}
$$

其中 W 是词库的个数。这个公式看起来挺吓人的。简单而直观地理解，可以看成特定的词 $w_o$ 出现的次数，与所有词可能出现的次数之和相除。实际上，之前我们介绍[逻辑回归模型](http://blog.kamidox.com/logistic-regression.html)时，介绍的 [Sigmoid Fuction](https://en.wikipedia.org/wiki/Sigmoid_function) 是这个公式的一个特例。Sigmoid function 适用在只有两个选择的概率问题上，而 Softmax function 适用在两个以上可选项的概率问题上。

这样，对目标函数求偏微分，关键就是对 $log (p(o|i))$ 求偏微分，其中 o 和 i 分别是指上下文词和中心词的序号。老师在课堂上花了大量的时间在计算偏微分，过程中用到了对矩阵求偏微分，链接法则 (chain rules)，exp 及 log 求微分等，这些法则可参阅[微分运算法则](http://blog.kamidox.com/computation-rules-for-derivative.html)。具体推导过程可查阅视频，最终求出的偏微分如下：

$$
\frac{\partial}{\partial{v_i}} log (p(o|i)) = u_o - \sum_{x=1}^W p(x|i) u_x
$$

这是一个类似递归的结果。利用这个偏分结果，就可以使用梯度下降算法来训练模型。

#### 语言模型

#### Continuous Bag of Words Model (CBOW)

#### Skip-Gram Model

