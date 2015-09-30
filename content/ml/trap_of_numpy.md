Title: numpy 矩阵运算的陷阱
Date: 2015-09-23 20:20
Modified: 2015-09-11 20:20
Slug: trap-of-numpy
Tags: machine-learning
Authors: Joey Huang
Summary: numpy 的矩阵运算有不少陷阱，一不小心踩进去就出不来了
Status: draft

## 陷阱一：数据结构混乱

array 和 matrix 都可以用来表示多维矩阵

```python
In [98]: a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

In [99]: a
Out[99]:
array([[1, 2, 3],
       [4, 5, 6],
       [7, 8, 9]])

In [100]: A = np.matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

In [101]: A
Out[101]:
matrix([[1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]])

In [102]: a.shape
Out[102]: (3, 3)

In [103]: A.shape
Out[103]: (3, 3)
```

看起来效果不错。假设我们要对数据进行筛选，取第 1 列的第 1 行和第 3 行数据构成一个 2 x 1 的列向量。先看对 array 的做法

```python
In [99]: a
Out[99]:
array([[1, 2, 3],
       [4, 5, 6],
       [7, 8, 9]])

In [100]: y
Out[100]:
matrix([[1],
        [0],
        [1]])

In [101]: a[:, 0]
Out[101]: array([1, 4, 7])

In [102]: a[:, 0].shape
Out[102]: (3,)

In [110]: a[:, 0][y == 1]
---------------------------------------------------------------------------
IndexError                                Traceback (most recent call last)
<ipython-input-110-f32ed63aa2a8> in <module>()
----> 1 a[:, 0][y == 1]

IndexError: too many indices for array

In [111]: a[:, 0].reshape(3, 1)[y == 1]
Out[111]: array([1, 7])
```
从 Out[109] 可以看到，一个陷阱，`a[:, 0]` 过滤完应该是一个 3 x 1 的列向量，可是它变成了行向量。其实也不是真正意义上的行向量，因为行向量 shape 应该是 3 x 1，可是他的 shape 是 (3,) ，这其实已经退化为一个数组了。所以，导致最后 In [110] 都会导出出错。只有像 In [111] 那样 reshape 一下才可以。我不知道大家晕了没有，我是已经快晕了。

相比之下，matrix 可以确保运算结果全部是二维的，结果相对好一点。为什么只是相对好一点呢？呆会儿我们再来吐吐 matrix 的槽点。

```python
In [101]: A
Out[101]:
matrix([[1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]])

In [112]: y
Out[112]:
matrix([[1],
        [0],
        [1]])

In [113]: A[:,0]
Out[113]:
matrix([[1],
        [4],
        [7]])

In [102]: A[:, 0].shape
Out[102]: (3,1)

In [114]: A[:,0][y == 1]
Out[114]: matrix([[1, 7]])

In [114]: A[:,0][y == 1].shape
Out[114]: (1,2)
```

看起来还不错。不过很快槽点就来了。Out [114] 我们预期的输入结果应该是一个 2 x 1 的列向量，可是这里变成了 1 x 2 的行向量！

为什么我会在意行向量和列微量？在矩阵运算里，行向量和列向量是不同的。比如一个 m x 3 的矩阵可以和 3 x 1 的列向量叉乘，结果是 m x 1 的列向量。而如果一个 m x 3 的矩阵和 1 x 3 的行向量叉乘是会报错的。

## 陷阱二：数据筛选结果是一维

假设 X 是 5 x 2 的矩阵，Y 是 5 X 1 的 bool 矩阵，用 Y 来过滤 X 时，的效果如下

```python
In [79]: X
Out[79]:
matrix([[ 34.62365962,  78.02469282],
        [ 30.28671077,  43.89499752],
        [ 35.84740877,  72.90219803],
        [ 60.18259939,  86.3085521 ],
        [ 79.03273605,  75.34437644]])

In [80]: Y
Out[80]:
matrix([[ True],
        [False],
        [ True],
        [ True],
        [False]], dtype=bool)

In [81]: X[Y==True]
Out[81]: matrix([[ 34.62365962,  35.84740877,  60.18259939]])

In [85]: X[Y == True, :]
---------------------------------------------------------------------------
IndexError                                Traceback (most recent call last)
<ipython-input-85-2aeabbc2bcc5> in <module>()
----> 1 X[Y == True, :]

C:\Python27\lib\site-packages\numpy\matrixlib\defmatrix.pyc in __getitem__(self, index)
    314
    315         try:
--> 316             out = N.ndarray.__getitem__(self, index)
    317         finally:
    318             self._getitem = False

IndexError: too many indices for array

In [86]: X[:, 0][Y == True]
Out[86]: matrix([[ 34.62365962,  35.84740877,  60.18259939]])

In [87]: X[:, 1][Y == True]
Out[87]: matrix([[ 78.02469282,  72.90219803,  86.3085521 ]])
```

我们预期 X 过滤完应该还是 2 列的矩阵，但不幸的是从 Out[81] 来看 numpy 这样过滤完只会保留第一列的数据。且，如果按照 In [85] 的写法，还会报错。如果要正确地过滤不同的列，需要写成 In [86] 和 In [87] 的形式。

## 默认会把列向量转换为行向量

numpy 运算时，如果结果是一维的，则会默认把列向量转换为行向量。

```python
In [79]: X
Out[79]:
matrix([[ 34.62365962,  78.02469282],
        [ 30.28671077,  43.89499752],
        [ 35.84740877,  72.90219803],
        [ 60.18259939,  86.3085521 ],
        [ 79.03273605,  75.34437644]])

In [80]: Y
Out[80]:
matrix([[ True],
        [False],
        [ True],
        [ True],
        [False]], dtype=bool)

In [87]: X[:, 1][Y == True]
Out[87]: matrix([[ 78.02469282,  72.90219803,  86.3085521 ]])

In [88]: X[:, 1][Y == True].shape
Out[88]: (1, 3)

In [89]: X[:, 1][Y == True].reshape(3, 1)
Out[89]:
matrix([[ 78.02469282],
        [ 72.90219803],
        [ 86.3085521 ]])
```

从 Out[87] 的输出可以看到，我们预期按列切割后应该还是列向量，但不幸的是 numpy 把它变成了行向量。这个默认的转换行为在矩阵运算时会变得很麻烦，因为我们必须时刻留心 numpy 的默认转换行为，要进行正确的矩阵运算，必须转换回我们数学上预期的形式。比如，我们预期数据筛选后是 3 x 1 的列向量 theta，我们有另外一个矩阵 data 是 m x 3 的矩阵，那么 data 和 theta 叉乘将得到 m x 1 的列向量。而在 numpy 里如果不留心 numpy 的默认转换行为，则会报错，且最终的计算结果也是 1 x m 的行向量，而不是列向量。


* 次方运算符 ** 与 numpy.power 的区别
* numpy.hstack 与 numpy.column_stack 的区别
* 向量，行向量，列向量，N x 1 维矩阵，1 x N 维矩阵的区别

