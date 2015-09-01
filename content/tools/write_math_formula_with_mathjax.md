Title: 使用 Markdown + MathJax 在博客里插入数学公式
Date: 2015-09-01 22:52
Modified: 2015-09-01 22:52
Tags: markdown, meachine_learning
Slug: write-math-formula-with-mathjax
Authors: Joey Huang
Summary: 本文介绍如何使用 Markdown + MathJax 书写数学公式


在书写数值计算类文章，特别是机器学习相关算法时，难免需要插入复杂的数学公式。一种是用图片在网页上展示，另外一种是使用 [MathJax][1] 来展示复杂的数学公式。它直接使用 Javascript 使用矢量字库或 SVG 文件来显示数学公式。优点是效果好，比如在 Retina 屏幕上也不会变得模糊。并且可以直接把公式写在 Markdown 文章里。本文介绍使用 MathJax 在 Markdown 文件里直接插入数学公式。并且附带一个简单的书写数学公式的 LaTex 教程。

## 工具

### 配置 Markdown Preview 来支持 MathJax

使用 Sublime + Markdown Preview 插件来写博客时。需要开启 Markdown Preview 对 MathJax 的支持，这样在预览界面才能正确地显示数学公式。方法是打开在 Markdown Preview 的用户配置文件 (Package Settings -> Markdown Preview -> Setting - User) 里添加如下内容：
	
```javascript
"enable_mathjax": true
```

### 配置 Pelican 主题模板来支持 MathJax

我使用的主题是 `foundation-default-colours`，它默认是支持 MathJax 的。我们可以在模板 `base.html` 找到如下内容：

```html
<!-- mathjax config similar to math.stackexchange -->
<script type="text/x-mathjax-config">
MathJax.Hub.Config({
	jax: ["input/TeX", "output/HTML-CSS"],
	tex2jax: {
		inlineMath: [ ['$', '$'] ],
		displayMath: [ ['$$', '$$']],
		processEscapes: true,
		skipTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
	},
	messageStyle: "none",
	"HTML-CSS": { preferredFont: "TeX", availableFonts: ["STIX","TeX"] }
});
</script>
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
```

如果模板不支持，也可以直接添加上面的脚本来支持 MathJax。

## LaTex 简明教程

### 例子

先来看个例子：

```markdown
$$
J(\theta) = \frac 1 2 \sum_{i=1}^m (h_\theta(x^{(i)})-y^{(i)})^2
$$
```

上面用 LaTex 格式书写的数学公式经过 MathJax 展示后效果如下：

$$
J(\theta) = \frac 1 2 \sum_{i=1}^m (h_\theta(x^{(i)})-y^{(i)})^2
$$

这个公式是线性回归算法里的成本函数。

### 规则

关于在 Markdown 书写 LaTex 数学公式有几个规则常用规则需要记住：

**行内公式**
行内公式使用 `$` 号作为公式的左右边界，如 $h(x) = \theta_0 + \theta_1 x$ 公式的 LaTex 内容如下

```markdown
$h(x) = \theta_0 + \theta_1 x$
```

**行间公式**
公式需要独立显示一行时，使用 `$$` 来作为公式的左右边界，如

$$
\theta_i = \theta_i - \alpha\frac\partial{\partial\theta_i}J(\theta)
$$

的 LaTex 代码为：

```markdown
$$
\theta_i = \theta_i - \alpha\frac\partial{\partial\theta_i}J(\theta)
$$
```

**常用 LaTex 代码**
需要记住的几个常用的符号，这样书写起来会快一点

编码      | 说明                               | 示例
---------|------------------------------------|----------
\frac    | 分子分母之间的横线                   | $\frac1x$
_        | 用下划线来表示下标                   | $x_i$
^        | 次方运算符来表示上标                 | $x^i$
\sum     | 累加器，上下标用上面介绍的编码来书写   | $\sum$
\alpha   | 希腊字母 alpha                      | $y := \alpha x$

记住这几个就差不多了，倒回去看一下线性回归算法的成本函数的公式及其 LaTex 代码，对着练习个10分钟基本就可以掌握常用公式的写法了。要特别注意公式里空格和 `{}` 的运用规则。基本原则是，空格可加可不加，但如果会引起歧义，最好加上空格。`{}` 是用来组成群组的。比如写一个分式时，分母是一个复杂公式时，可以用 `{}` 包含起来，这样整个复杂公式都会变成分母了。

### 几个非常有用的资源

* Github 上有个[在线 Markdown MathJax 编辑器][2]，可以在这里练习，平时写公式时也可以在这里先写好再拷贝到文章里
* 这是 [LaTex 完整教程][3]，包含完整的 LaTex 数学公式的内容，包括更高级的格式控制等
* 这是一份PDF 格式的 [MathJax 支持的数学符号表][4]，当需要书写复杂数学公式时，一些非常特殊的符号的转义字符可以从这里查到

好啦，这样差不多就可以写出优美的数学公式啦。


[1]: https://www.mathjax.org
[2]: https://kerzol.github.io/markdown-mathjax/editor.html
[3]: http://www.forkosh.com/mathtextutorial.html
[4]: http://mirrors.ctan.org/info/symbols/math/maths-symbols.pdf