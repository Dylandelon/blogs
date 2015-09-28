Title: 几个常用的微分运算法则
Date: 2015-09-28 23:20
Modified: 2015-09-28 23:20
Slug: computation-rules-for-derivative
Tags: machine-learning
Authors: Joey Huang
Summary: 本文总结了几个常用的微分运算法则，并运用这个法则计算分类器预测模型 Sigmoid Function 的微分公式。

机器学习涉及到较多的数学知识，在工程应用领域，这些数学知识不是必要的，其实很多算法都是数值运算专家写好了的。然而知其然知其所以然，了解这些数学公式的来龙去脉是帮助理解算法的关键。本文直接给出常用的微分运算法则，并运用这些法则来计算分类回归算法 (Logistic Regression) 预测模型 Sigmoid Function 的微分公式。

## 基础函数的微分运算法则

* 幂函数法则
  $$\begin{align} \frac{d}{dx} x^n = nx^{n-1} \end{align}$$
* 指数函数法则
  $$\begin{align} \frac{d}{dx} e^x = e^x \end{align}$$
  $$\begin{align} \frac{d}{dx} a^x = ln(a)a^x \end{align}$$
* 对数函数法则
  $$\begin{align} \frac{d}{dx} ln(x) = \frac{1}{x} \end{align}$$
  $$\begin{align} \frac{d}{dx} log_a(x) = \frac{1}{xln(a)} \end{align}$$
* 三角函数法则
  $$\begin{align} \frac{d}{dx} sin(x) = cos(x) \end{align}$$
  $$\begin{align} \frac{d}{dx} cos(x) = -sin(x) \end{align}$$
  $$\begin{align} \frac{d}{dx} tan(x) = sin^2(x) = \frac{1}{cos^2(x)} = 1 + tan^2(x) \end{align}$$
* 反三角函数法则
  $$\begin{align} \frac{d}{dx} arcsin(x) = \frac{1}{\sqrt{1-x^2}}, -1 < x < 1 \end{align}$$
  $$\begin{align} \frac{d}{dx} arccos(x) = -\frac{1}{\sqrt{1-x^2}}, -1 < x < 1 \end{align}$$
  $$\begin{align} \frac{d}{dx} arctan(x) = \frac{1}{1+x^2} \end{align}$$

## 组合函数的微分运算法则

* 常数法则：如果 $f(x) = n$，n 是常数，则
  $$\begin{align} f' = 0 \end{align}$$
* 加法法则
  $$\begin{align} (\alpha f + \beta g)' = \alpha f' + \beta g' \end{align}$$
* 乘法法则
  $$\begin{align} (fg)' = f'g + fg' \end{align}$$
* 除法法则
  $$\begin{align} \left( \frac{f}{g} \right)' = \frac{f'g - fg'}{g^2} \end{align}$$
  根据除法法则和指数法则，可以得出推论
  $$\frac{d}{dx} e^{-x} = \frac{d}{dx} \frac{1}{e^x} = \frac{0-e^x}{e^{2x}} = -\frac{1}{e^x} = -e^{-x}$$
* 链接法则：如果 $f(x) = h(g(x))$，则
  $$\begin{align} f'(x) = h'(g(x)) g'(x) \end{align}$$

## 计算 Sigmoid Function 的微分

$g(x) = \frac{1}{1+e^{-x}}$ 是分类算法的预测函数，也称为 Sigmoid Function 或 Logistic Function。我们利用上文介绍的微分运算法则来证明 Sigmoid Function 的一个特性：

$$
\frac{d}{dx} g(x) = g(x) (1 - g(x))
$$

### 方法一

假设 $f(x) = \frac{1}{x}$，则 $f(g(x)) = \frac{1}{g(x)}$，根据除法法则得到

$$
\begin{align}
f'(g(x)) & = \left( \frac{1}{g(x)} \right)' = \frac{1' g(x) - 1 g'(x)}{g(x)^2} \\\\
& = - \frac{g'(x)}{g(x)^2}
\end{align}
$$

其中 (17) 是根据除法法则得出的结论，除数是常数函数 1，被除数是 $g(x)$。(18) 是根据常数法则得出的结论。

另一方面，$f(g(x)) = \frac{1}{g(x)} = 1 + e^{-x}$，根据指数法则直接计算微分得到

$$
\begin{align}
f'(g(x)) & = \frac{d}{dx} (1 + e^{-x}) \\\\
& = -e^{-x} \\\\
& = 1 - \frac{1}{g(x)} \\\\
& = \frac{g(x) - 1}{g(x)}
\end{align}
$$

(18) 和 (22) 两式是相等的，即

$$
\begin{align}
- \frac{g'(x)}{g(x)^2} & = \frac{g(x) - 1}{g(x)} \\\\
g'(x) & = g(x)(1 - g(x))
\end{align}
$$

这样就得到了我们的结果。

### 方法二

由 $g(x) = \frac{1}{1+e^{-x}}$ 的定义可知

$$
\begin{align}
& (1+e^{-x})g(x) = 1 \\\\
\Rightarrow & \frac{d}{dx} \left( (1+e^{-x})g(x) \right) = 0  \\\\
\Rightarrow & -e^{-x}g(x) + (1+e^{-x})\frac{d}{dx}g(x) = 0    \\\\
\Rightarrow & \frac{d}{dx}g(x) = g(x) \frac{e^{-x}}{1+e^{-x}} \\\\
\Rightarrow & \frac{d}{dx}g(x) = g(x) \frac{(1 + e^{-x}) - 1}{1+e^{-x}} \\\\
\Rightarrow & \frac{d}{dx}g(x) = g(x) \left[ 1 - \frac{1}{1+e^{-x}}\right] \\\\
\Rightarrow & \frac{d}{dx}g(x) = g(x) (1 - g(x)) \\\\
\end{align}
$$

(26) 两边取微分；(27) 根据微分的乘法法则。

### 方法三

根据除法法则直接计算微分：

$$
\begin{align}
\frac{d}{dx} g(x) & = \frac{d}{dx} \left( \frac{1}{1 + e^{-x}} \right) \\\\
& = \frac{0 - (- e^{-x})}{(1 + e^{-x})^2} \\\\
& = \frac{e^{-x}}{(1 + e^{-x})^2} \\\\
& = \frac{1}{(1 + e^{-x})} \frac{e^{-x}}{(1 + e^{-x})} \\\\
& = \frac{1}{(1 + e^{-x})} \frac{(1 + e^{-x}) - 1}{(1 + e^{-x})} \\\\
& = \frac{1}{(1 + e^{-x})} \left[1 - \frac{1}{(1 + e^{-x})} \right] \\\\
& = g(x) (1 - g(x)) \\\\
\end{align}
$$

(33) 是根据除法法则得出的，其中除数是常数 1，被除数是 $1 + e^{-x}$。

## 参考资料

* StackExchange 上有个 [Sigmoid Function 微分计算的问题及答案][1]
* WikiPedia 上有关[微分运算法则][2]的资料

[1]: http://math.stackexchange.com/questions/78575/derivative-of-sigmoid-function-sigma-x-frac11e-x
[2]: https://en.wikipedia.org/wiki/Derivative#Rules_of_computation
