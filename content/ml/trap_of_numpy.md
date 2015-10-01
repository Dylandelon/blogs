Title: numpy 矩阵运算的陷阱
Date: 2015-09-30 20:20
Modified: 2015-09-30 20:20
Slug: trap-of-numpy
Tags: machine-learning
Authors: Joey Huang
Summary: numpy 的矩阵运算有不少陷阱，一不小心踩进去就出不来了

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

从 Out[101] 可以看到一个陷阱，`a[:, 0]` 过滤完应该是一个 3 x 1 的列向量，可是它变成了行向量。其实也不是真正意义上的行向量，因为行向量 shape 应该是 3 x 1，可是他的 shape 是 (3,) ，这其实已经退化为一个数组了。所以，导致最后 In [110] 出错。只有像 In [111] 那样 reshape 一下才可以。我不知道大家晕了没有，我是已经快晕了。

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

看起来还不错。不过槽点就来了。Out [114] 我们预期的输入结果应该是一个 2 x 1 的列向量，可是这里变成了 1 x 2 的行向量！

为什么我会在意行向量和列向量？在矩阵运算里，行向量和列向量是不同的。比如一个 m x 3 的矩阵可以和 3 x 1 的列向量叉乘，结果是 m x 1 的列向量。而如果一个 m x 3 的矩阵和 1 x 3 的行向量叉乘是会报错的。

## 陷阱二：数据处理能力不足，语言效率低

我们再看个例子。假设 X 是 5 x 2 的矩阵，Y 是 5 X 1 的 bool 矩阵，我们想用 Y 来过滤 X ，即取出 Y 值为 True 的项的索引，拿这些索引去 X 里找出对应的行，再组合成一个新矩阵。

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

In [81]: X[Y == True]
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

In [88]: np.column_stack((x[:, 0][y == True].reshape(3,1), x[:, 1][y == True].reshape(3,1)))
Out[88]:
matrix([[ 34.62365962,  78.02469282],
        [ 35.84740877,  72.90219803],
        [ 60.18259939,  86.3085521 ]])
```

我们预期 X 过滤完是 3 x 2 列的矩阵，但不幸的是从 Out[81] 来看 numpy 这样过滤完只会保留第一列的数据，且把它转化成了行向量，即变成了 1 x 3 的行向量。不知道你有没有抓狂的感觉。如果按照 In [85] 的写法，还会报错。如果要正确地过滤不同的列，需要写成 In [86] 和 In [87] 的形式。但是即使写成 In [86] 和 In [87] 的样式，还是一样把列向量转化成了行向量。所以，要实现这个目的，得复杂到按照 In [88] 那样才能达到目的。实际上，这个还达不到目的，因为那里面写了好多硬编码的数字，要处理通用的过滤情况，还需要写个函数来实现。而这个任务在 matlab/octave 里只需要写成 `X(Y==1, :)` 即可完美达成目的。

## 陷阱三：数值运算句法混乱

在机器学习算法里，经常要做一些矩阵运算。有时候要做叉乘，有时候要做点乘。我们看一下 numpy 是如何满足这个需求的。

假设 x, y, theta 的值如下，我们要先让 x 和 y 点乘，再让结果与 theta 叉乘，最后的结果我们期望的是一个 5 x 1 的列向量。

```python
In [22]: x
Out[22]:
matrix([[  1.        ,  34.62365962,  78.02469282],
        [  1.        ,  30.28671077,  43.89499752],
        [  1.        ,  35.84740877,  72.90219803],
        [  1.        ,  60.18259939,  86.3085521 ],
        [  1.        ,  79.03273605,  75.34437644]])

In [23]: y
Out[23]:
matrix([[1],
        [2],
        [3],
        [2],
        [2]])

In [24]: theta
Out[24]:
matrix([[2],
        [2],
        [2]])
```

直观地讲，我们应该会想这样做：(x 点乘 y) 叉乘 theta。但很不幸，当你输入 `x * y` 时妥妥地报错。那好吧，我们这样做总行了吧，`x[:, 0] * y` 这样两个列向量就可以点乘了吧，不幸的还是不行，因为 numpy 认为这是 matrix，所以执行的是矩阵相乘（叉乘），要做点乘，必须转为 array 。

```python
In [37]: x * y
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-37-ae1a0a4af750> in <module>()
----> 1 x * y

/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/numpy/matrixlib/defmatrix.pyc in __mul__(self, other)
    339         if isinstance(other, (N.ndarray, list, tuple)) :
    340             # This promotes 1-D vectors to row vectors
--> 341             return N.dot(self, asmatrix(other))
    342         if isscalar(other) or not hasattr(other, '__rmul__') :
    343             return N.dot(self, other)

ValueError: matrices are not aligned

In [38]: x[:, 0] * y
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-38-d55ad841fa29> in <module>()
----> 1 x[:, 0] * y

/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/numpy/matrixlib/defmatrix.pyc in __mul__(self, other)
    339         if isinstance(other, (N.ndarray, list, tuple)) :
    340             # This promotes 1-D vectors to row vectors
--> 341             return N.dot(self, asmatrix(other))
    342         if isscalar(other) or not hasattr(other, '__rmul__') :
    343             return N.dot(self, other)

ValueError: matrices are not aligned

In [39]: sp.array(x[:,0]) * sp.array(y)
Out[39]:
array([[ 1.],
       [ 2.],
       [ 3.],
       [ 2.],
       [ 2.]])

In [42]: xy = sp.column_stack(((sp.array(x[:,0]) * sp.array(y)), (sp.array(x[:,1]) * sp.array(y)), (sp.array(x[:,2]) * sp.array(y))))

In [43]: xy
Out[43]:
array([[   1.        ,   34.62365962,   78.02469282],
       [   2.        ,   60.57342154,   87.78999504],
       [   3.        ,  107.54222631,  218.70659409],
       [   2.        ,  120.36519878,  172.6171042 ],
       [   2.        ,  158.0654721 ,  150.68875288]])
```

所以，我们需要象 In [39] 那样一列列转为 array 和 y 执行点乘，然后再组合回 5 x 3 的矩阵。好不容易算出了 x 和 y 的点乘了，终于可以和 theta 叉乘了。

```python
In [44]: xy * theta
Out[44]:
matrix([[ 227.29670488],
        [ 300.72683316],
        [ 658.4976408 ],
        [ 589.96460596],
        [ 621.50844996]])
```

看起来结果还不错，但实际上这里面也是陷阱重重。

```python
In [45]: xy * sp.array(theta)
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-45-5ea2f7324fbe> in <module>()
----> 1 xy * sp.array(theta)

ValueError: operands could not be broadcast together with shapes (5,3) (3,1)

In [46]: sp.dot(xy, sp.array(theta))
Out[46]:
array([[ 227.29670488],
       [ 300.72683316],
       [ 658.4976408 ],
       [ 589.96460596],
       [ 621.50844996]])
```

In [45] 会报错，因为在 array 里 `*` 运算符是点乘，而在 matrix 里 `*` 运算符是叉乘。如果要在 array 里算叉乘，需要用 `dot` 方法。看起来提供了灵活性，实际上增加了使用者的大脑负担。而我们的需求在 matlab/octave 里只需要写成 `x .* y * theta` ，直观优雅。


## 陷阱四：语法复杂，不自然

比如，我们要在一个 5 x 2 的矩阵的前面加一列全部是 1 的数据，变成一个 5 x 3 的矩阵，我们必须这样写

```python
In [11]: x
Out[11]:
matrix([[ 34.62365962,  78.02469282],
        [ 30.28671077,  43.89499752],
        [ 35.84740877,  72.90219803],
        [ 60.18259939,  86.3085521 ],
        [ 79.03273605,  75.34437644]])

In [18]: sp.column_stack(((sp.ones((5,1)), x)))
Out[18]:
matrix([[  1.        ,  34.62365962,  78.02469282],
        [  1.        ,  30.28671077,  43.89499752],
        [  1.        ,  35.84740877,  72.90219803],
        [  1.        ,  60.18259939,  86.3085521 ],
        [  1.        ,  79.03273605,  75.34437644]])
```

有兴趣的人可以数数 In [18] 里有多少个括号，还别不服，括号写少了妥妥地报错。而这个需求在 matlab/octave 里面只需要写成 `[ones(5,1) x]` ，瞬间脑袋不短路了，直观优雅又回来了。

## 结论

有人说 python 是机器学习和数据分析的新贵，但和专门的领域语言 matlab/octave 相比，用起来确实还是比较别扭的。当然有些槽点是因为语言本身的限制，比如 python 不支持自定义操作符，导致 numpy 的一些设计不够优雅和直观，但默认把列向量转化为行向量的做法只能说是 numpy 本身的设计问题了。这或许就是 Andrew Ng 在他的 Machine Learning 课程里用 matlab/octave ，而不用 python 或其他的语言的原因吧。



