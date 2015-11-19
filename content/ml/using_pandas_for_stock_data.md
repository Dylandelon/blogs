Title: 使用 pandas 玩转股票数据
Date: 2015-11-17 23:16
Modified: 2015-11-17 23:16
Slug: using-pandas-for-stock-data
Tags: machine-learning
Authors: Joey Huang
Summary: pandas 是数据分析的瑞士军刀。我们今天使用 pandas 来玩一下股票数据，看看能从数据里得到哪些有意思的信息。


pandas 是数据分析的瑞士军刀。我们今天使用 pandas 来玩一下股票数据，看看能从数据里得到哪些有意思的信息。

## pandas 教程

如果你熟悉 Python 的话，官网上的 [10 Minutes to pandas][1] 可以让你在短时间内了解 pandas 能干什么事以及是怎么干的。针对每个主题，都可以横向查到大量的资料和例子。

如果你 Python 不熟，但又想用 pandas 玩转数据分析的话，[Python for Data Analysis][2] 是本不错的书。书里作者使用美国新生儿的名字得出了一些很有意思的结论。还分析了 movielen 的电影评分数据。熟悉 SQL 的同学应该对这些分析会深有感触，相信这些人用 SQL 写出过这些分析过程类似的代码。这本书的缺点是有点啰嗦，如果你熟悉 Python 又想快速学习的话，看第二章就够了。但这本书很适合不熟悉 Python 的人，书的最后一章还附了 Python 的教程，即如果只玩 pandas 的话，掌握这些 Python 知识就够了，真够贴心。而且本书的作者就是 pandas 的作者。

另外补充一点，最好使用 [ipython][3] 环境来玩转数据分析。特别是 ipython notebook ，熟悉快捷键后，用起来会很顺手。本文玩转的股票数据就是使用 ipython notebook。

## 股票数据下载

搜索 ghancn 可以免费下载 2009 年之前的 5 分钟数据和 1 分钟数据。坦白讲，数据质量不高，里面有不少错误。但不影响我们玩这些数据。数据是以年为单位分不同的文件夹保存的。

我们先看一下某个股票的数据长什么样：

```python
import pandas as pd
import numpy as np


names = ['date',
         'time',
         'opening_price',
         'ceiling_price',
         'floor_price',
         'closing_price',
         'volume',
         'amount']
# 读取数据时，我们以日期为索引，并解析成日期格式
raw = pd.read_csv('raw/2008/SH600690.csv', names=names, header=None, index_col='date', parse_dates=True)
raw.head()
```

```
             time  opening_price  ceiling_price  floor_price  closing_price   volume    amount
date
2008-01-02  09:35          22.50          22.63        22.50          22.51   2042.50   4604723
2008-01-02  09:40          22.51          22.51        22.29          22.37   1545.17   3460503
2008-01-02  09:45          22.39          22.62        22.38          22.62   1744.76   3921443
2008-01-02  09:50          22.60          23.00        22.60          22.95   5339.00   12225939
2008-01-02  09:55          22.98          23.20        22.89          23.20   12577.73  28947824

```

**转化为日交易数据**

我们使用 2007 年和 2008 年的数据来作为示例。因为我们更关心是一些长期的趋势，分钟级别的交易数据太细了，我们转换为日数据。

```python
# 股票涨跌幅检查，不能超过 10% ，过滤掉一些不合法的数据
def _valid_price(g):
    return (((g.max() - g.min()) / g.min()) < 0.223).all()

# 按照日期分组
days = raw.groupby(level=0).agg(
    {'opening_price': lambda g: _valid_price(g) and g[0] or 0,
     'ceiling_price': lambda g: _valid_price(g) and np.max(g) or 0,
     'floor_price': lambda g: _valid_price(g) and np.min(g) or 0,
     'closing_price': lambda g: _valid_price(g) and g[-1] or 0,
     'volume': 'sum',
     'amount': 'sum'})
days.head()
```

```
            floor_price opening_price   ceiling_price   volume      amount      closing_price
date
2008-01-02  22.29       22.50           24.50           200809.34   476179680   24.03
2008-01-03  23.81       24.03           25.20           166037.98   406906304   24.54
2008-01-04  23.68       24.53           24.76           149078.64   358418560   24.17
2008-01-07  23.75       24.03           24.75           93950.43    227289136   24.38
2008-01-08  23.49       24.38           24.38           149056.24   355752416   23.53
```

这里只是为了玩这些数据，如果你真的需要股票日数据，雅虎财经网站上有质量非常高的日交易数据可供下载。

按照上述方法，可以把一个股票几年的数据合并起来，生成一个包含所有年份的历史日交易数据。具体可以参阅 [stock.py][4] 里的 `minutes_to_days_batch` 函数。

## 股票波动率

什么股票是好股票？要回答这个问题，先要把最简单的问题说清楚。炒股就是**低买高卖，实现获利**。那么好股票的标准就是在你的持股周期内，波动最大的股票。这很好理解吧，波动最大，我们才有可能在相对低点买入，在相对高点卖出，获利最大。

在一定的时间周期内，衡量股票波动的指标定义为 最高价/最低价。以我们表格中的数据，就是 ceiling_price/floor_price。这个比率最大的股票就是好股票。关于时间周期，这个和炒股策略有关。有些人喜欢做短线，可能就持股几天，或一两周。有些人习惯做长线，可能持股几个月甚至几年。也有些人本来打算做短线，做着做着变成长线，再做着做着，变成了股东。

为了简单起见，我们拿波动周期为 30 个自然日来计算，即如果某个股票停牌，那么他的价格就一直没有变化，则波动为 0。
这里，我们直接使用 600690 这个股票来作为示例。我们直接读取已经合并过日交易的数据。

```python
qdhr = pd.read_csv('test-data/SH600690.csv', index_col='date', parse_dates=True)
qdhr.head()
```

```

                floor_price     opening_price   ceiling_price   volume      amount      closing_price
date
2007-01-04      9.28            9.30            10.14           259264.75   254734000   9.80
2007-01-05      9.53            9.70            10.15           171169.97   170154432   9.90
2007-01-08      9.93            9.93            10.78           159340.58   164954896   10.60
2007-01-09      10.08           10.68           11.15           227163.31   246309216   10.55
2007-01-10      10.26           10.49           11.13           232858.18   246221520   11.10
```

我们发现数据中间有空洞，即周末和停牌时间里是没有数据的。我们把这些数据填充完整，我们看看 pandas 如何处理 missing data 。

### 填充数据

我们先生成一段连续的日期数据作为索引：

```python
# 填充数据：生成日期索引
l = len(qdhr)
start = qdhr.iloc[0:1].index.tolist()[0]
end = qdhr.iloc[l - 1: l].index.tolist()[0]
idx = pd.date_range(start=start, end=end)
idx
```

```
DatetimeIndex(['2007-01-04', '2007-01-05', '2007-01-06', '2007-01-07',
               '2007-01-08', '2007-01-09', '2007-01-10', '2007-01-11',
               '2007-01-12', '2007-01-13',
               ...
               '2008-12-22', '2008-12-23', '2008-12-24', '2008-12-25',
               '2008-12-26', '2008-12-27', '2008-12-28', '2008-12-29',
               '2008-12-30', '2008-12-31'],
               dtype='datetime64[ns]', length=728, freq='D')
```

接着使用 `reindex` 函数缺失的数据被全。填充股票数据时有个要求，我们把缺失的价格数据用前一个交易日的数据来填充，但交易量需要填充为 0。

```python
data = qdhr.reindex(idx)
zvalues = data.loc[~(data.volume > 0)].loc[:, ['volume', 'amount']]
data.update(zvalues.fillna(0))
data.fillna(method='ffill', inplace=True)
data.head()
```

```
            floor_price opening_price   ceiling_price   volume      amount      closing_price
2007-01-04  9.28        9.30            10.14           259264.75   254734000   9.8
2007-01-05  9.53        9.70            10.15           171169.97   170154432   9.9
2007-01-06  9.53        9.70            10.15           0.00        0           9.9
2007-01-07  9.53        9.70            10.15           0.00        0           9.9
2007-01-08  9.93        9.93            10.78           159340.58   164954896   10.6
```
我们可以看到，06， 07 两天的数据被正确地填充了。

### 分组计算

我们需要计算 30 个自然日里的股票平均波动周期。这样，我们必须以 30 天为单位，对所有的历史数据进行分组。然后逐个分组计算其波动率。

**生成分组索引**

```python
# 定义产生分组索引的函数，比如我们要计算的周期是 20 天，则按照日期，20 个交易日一组
def gen_item_group_index(total, group_len):
    """ generate an item group index array

    suppose total = 10, unitlen = 2, then we will return array [0 0 1 1 2 2 3 3 4 4]
    """

    group_count = total / group_len
    group_index = np.arange(total)
    for i in range(group_count):
        group_index[i * group_len: (i + 1) * group_len] = i
    group_index[(i + 1) * group_len : total] = i + 1
    return group_index.tolist()
```

```python
In [7]: gen_item_group_index(10, 3)
Out [7]: [0, 0, 0, 1, 1, 1, 2, 2, 2, 3]
```

**根据分组索引来分组**

```python
period = 30

group_index = gen_item_group_index(len(data), period)
# 把分组索引数据添加到股票数据里
data['group_index'] = group_index
print len(data)
data.head().append(data.tail())
```

我们看一下添加了分组索引后的数据最前面 5 个和最后 5 个数据，注意 `group_index` 的值。我们接下来就是根据这个值进行分组。

```
            floor_price opening_price   ceiling_price   volume      amount      closing_price   group_index
2007-01-04  9.28        9.30            10.14           259264.75   254734000   9.80            0
2007-01-05  9.53        9.70            10.15           171169.97   170154432   9.90            0
2007-01-06  9.53        9.70            10.15           0.00        0           9.90            0
2007-01-07  9.53        9.70            10.15           0.00        0           9.90            0
2007-01-08  9.93        9.93            10.78           159340.58   164954896   10.60           0
2008-12-27  8.97        9.15            9.23            0.00        0           9.08            24
2008-12-28  8.97        9.15            9.23            0.00        0           9.08            24
2008-12-29  8.73        9.04            9.15            38576.07    34625144    9.11            24
2008-12-30  8.95        9.14            9.14            62983.38    56876600    8.96            24
2008-12-31  8.95        9.00            9.11            32829.30    29620508    8.99            24
```

**分组计算最高价和最低价**

```python
# 针对下跌的波动，我们把最高价设置为负数。什么是下跌的波动？就是先出现最高价，再出现最低价
def _ceiling_price(g):
    return g.idxmin() < g.idxmax() and np.max(g) or (-np.max(g))


# 根据索引分组计算
group = data.groupby('group_index').agg({
                                        'volume': 'sum',
                                        'floor_price': 'min',
                                        'ceiling_price': _ceiling_price})
group.head()
```

```
                volume      ceiling_price   floor_price
group_index
0               1271711.00  22.33           16.21
1               1831018.01  24.75           18.98
2               2038944.01  -27.20          20.08
3               477219.16   23.49           21.40
4               203932.07   -22.48          20.10
```

**给每个分组添加起始日期**

有时我们看到某个周期内下跌了很多，或上涨了很多，我们想知道是什么时候发生的，所以需要给每个分组添加起始日期。

```python
# 添加每个分组的起始日期
date_col = pd.DataFrame({"group_index": group_index, "date": idx})
group['date'] = date_col.groupby('group_index').agg('first')
group.head()
```

idx 是我们在上面代码里生成的连续的日期索引数据。添加日期数据后的样子：

```
                volume      ceiling_price   floor_price     date
group_index
0               4634226.68  -12.38          9.02            2007-01-04
1               3499001.47  11.64           8.80            2007-02-03
2               6061972.34  12.79           9.41            2007-03-05
3               6086797.19  15.50           12.00           2007-04-04
4               5687407.73  17.15           13.49           2007-05-04
```

**添加波动率**

```python
# 添加我们的波动指标 股票波动系数 = 最高价/最低价
group['ripples_radio'] = group.ceiling_price / group.floor_price
group.head()
```

```
                volume          ceiling_price   floor_price     date            ripples_radio
group_index
0               4634226.68      -12.38          9.02            2007-01-04      -1.372506
1               3499001.47      11.64           8.80            2007-02-03      1.322727
2               6061972.34      12.79           9.41            2007-03-05      1.359192
3               6086797.19      15.50           12.00           2007-04-04      1.291667
4               5687407.73      17.15           13.49           2007-05-04      1.271312
```

**排序**

按照波动率排序，可以看到某段时间内波动最大的一些时间段。

```python
# 降序排列。我们把分组的起始日期，交易量总和都列出来，也可以观察一下交易量和股票波动比的关系
ripples = group.sort_values('ripples_radio', ascending=False)
ripples.head()
```

```
            volume          ceiling_price   floor_price     date            ripples_radio
group_index
101         4352881.31      14.85           9.18            2008-04-21      1.617647
90          5703121.25      18.89           11.85           2007-05-27      1.594093
92          4545365.71      23.96           16.42           2007-07-26      1.459196
85          4126972.83      12.38           8.58            2006-12-28      1.442890
84          2952951.46      9.20            6.40            2006-11-28      1.437500
```

从数据可以看出来，波动最大的在 30 个自然日内上涨了 61.76%。发生在 2008-04-21 开始的 30 天内。

当然，我们也可以计算前 10 大上涨波动的平均值。

```python
ripples.head(10).ripples_radio.mean()
```

```
1.3657990069195818
```

也可以计算前 10 大下跌波动的平均值。

```python
ripples.tail(10).ripples_radio.mean()
```

```
-1.4124407127785106
```

看来下跌的平均值比上涨的还大呀。

我们针对每个股票都使用上述方法计算其平均波动，这样我们就可以从一系列股票里找出那些波动最大的股票了。当然，上涨波动越大，下跌波动也越大，正所谓风险和机遇并存嘛。具体可参阅 [stock.py][4] 里的 `stock_ripples_batch` 函数。

## 其他玩法

### 计算涨跌幅

我们注意到原始数据里没有涨跌幅的数据。涨跌幅定义为今日收盘价减去昨日收盘价。我们换个股票，取出原始数据。

```python
data = pd.read_csv('test-data/SZ000565.csv', index_col='date', parse_dates=True)
data.head()
```

```
            floor_price     opening_price   ceiling_price   volume      amount          closing_price
date
2007-01-04  4.16            4.22            4.27            17877.88    7477370.52      4.19
2007-01-05  4.15            4.16            4.27            10857.66    4588246.02      4.24
2007-01-08  4.27            4.27            4.45            30770.01    13467986.00     4.44
2007-01-09  4.42            4.48            4.54            26276.89    11726492.00     4.45
2007-01-10  4.36            4.45            4.90            80840.76    37866240.01     4.90
```

利用 `diff` 函数快速计算涨跌幅。


```python
rise = data.closing_price.diff()
data['rise'] = rise
data.head()
```

```
    floor_price opening_price   ceiling_price   volume  amount  closing_price   rise
date
2007-01-04  4.16    4.22    4.27    17877.88    7477370.52  4.19    NaN
2007-01-05  4.15    4.16    4.27    10857.66    4588246.02  4.24    0.05
2007-01-08  4.27    4.27    4.45    30770.01    13467986.00 4.44    0.20
2007-01-09  4.42    4.48    4.54    26276.89    11726492.00 4.45    0.01
2007-01-10  4.36    4.45    4.90    80840.76    37866240.01 4.90    0.45
```

注意到第一条记录的涨跌幅为 `NaN`，因为第一条记录的昨日是没有数据的。感兴趣的同学可以再计算一下涨跌百分比，其定义为当日的涨跌幅除以昨日的收盘价。


### 计算指定时间点之前的一段时间内波动最大的股票

有时我们关心某个时间点之前的一段时间变化最剧烈的股票。比如最近一周涨幅最大的，最近一周跌幅最大的，或者最近一个月交易量变化最大的等等。

我们看一下 000565 这个股票在 2008-12-31 之前 30 个自然日里的波动率。

**选定数据**

这里涉及到用日期对数据进行分片的技术，我们需要选择指定日期及之前一段时间内的数据。

```python
end_date = '2008-12-31'
period = 30

end_date = pd.Timestamp(end_date)
start_date = end_date - pd.Timedelta(days=period)

data = pd.read_csv('test-data/SZ000565.csv', index_col='date', parse_dates=True)
data = data.loc[start_date:end_date]
data
```

```
            floor_price     opening_price   ceiling_price   volume          amount          closing_price
date
2008-12-01  7.40            7.58            7.90            41747.12        3.214610e+07    7.88
2008-12-02  7.55            7.56            8.38            74552.15        6.029661e+07    8.32
2008-12-03  8.40            8.40            8.93            85361.64        7.420082e+07    8.82
2008-12-04  8.42            8.88            9.08            110410.46       9.740610e+07    8.50
2008-12-05  8.33            8.40            9.35            126479.91       1.133572e+08    9.35
2008-12-08  9.35            9.40            9.99            149491.39       1.436038e+08    9.69
2008-12-09  9.10            9.73            9.73            89871.90        8.405230e+07    9.15
2008-12-10  9.09            9.11            9.55            70036.94        6.571389e+07    9.46
2008-12-11  9.06            9.40            9.47            57735.24        5.328468e+07    9.06
2008-12-12  8.15            8.80            9.00            59210.49        5.038026e+07    8.29
2008-12-15  8.30            8.33            8.72            41758.27        3.534860e+07    8.50
2008-12-16  8.02            8.48            8.60            38808.62        3.220561e+07    8.60
2008-12-17  8.58            8.67            8.89            46993.48        4.114008e+07    8.65
2008-12-18  8.50            8.62            8.81            34061.97        2.965074e+07    8.78
2008-12-19  8.79            8.79            9.39            70327.47        6.435001e+07    9.18
2008-12-22  8.95            9.19            9.39            50195.75        4.592311e+07    9.11
2008-12-23  8.20            9.17            9.17            75732.72        6.507140e+07    8.20
2008-12-24  7.59            8.03            8.18            61498.16        4.823624e+07    7.82
2008-12-25  7.40            7.90            7.93            34791.00        2.672370e+07    7.52
2008-12-29  6.96            7.50            7.55            31694.04        2.274100e+07    7.26
2008-12-30  7.11            7.29            7.48            25533.01        1.865500e+07    7.15
2008-12-31  6.94            7.16            7.25            22324.32        1.577828e+07    6.95
```

选出数据后，计算波动率就简单了。我们按照老办法，上涨的波动率为正数，下跌的波动率为负数。

```python
# 计算波动值
_ripple_radio = lambda data: data.ceiling_price.max() / data.floor_price.min()
ripple_radio = data.floor_price.idxmin() < data.ceiling_price.idxmax() and _ripple_radio(data) or -_ripple_radio(data)
ripple_radio
```

```
-1.4394812680115274
```

最后，遍历所有的股票，计算其指定日期之前的一段时间的波动值，选出波动最大的股票，即是我们关注的股票。比如，经历股票大跌，我们判断会反弹，我们想抢反弹，抢哪个股票呢？答案是抢大跌中下跌最多的，因为下跌最多的股票往往反弹也最多。这部分代码可参阅 [stock.py][4] 里的 `recent_ripples` 函数。

## 为什么要用 pandas 玩转股票数据

答案应该已经比较明显了，虽然很多数据股票软件里都有。但一些高级的数据筛选方式其实这些股票软件都不支持的。最后，需要补充一句，大家都是成年人，文章里的任何策略是个人的思路，不构成投资建议啊，后果自负啊。

最最后，感兴趣的可以看一下 [stock.ipynb][5]，这个是本文在 ipython notebook 环境下的所有代码。


[1]: http://pandas.pydata.org/pandas-docs/stable/10min.html
[2]: http://book.douban.com/subject/25717197/
[3]: http://ipython.org
[4]: https://github.com/kamidox/stock-data/blob/master/stock.py
[5]: https://github.com/kamidox/stock-data/blob/master/stock.ipynb
