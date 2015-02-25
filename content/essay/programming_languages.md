Title: 学习一种新编程语言时，我们到底是要学什么
Date: 2015-01-08 23:20
Modified: 2015-01-08 23:20
Tags: thought
Slug: programe-languages
Authors: Joey Huang
Summary: 编程语言不下千种，即使是最主流的编程语言也有很多种，我们学习一种编程语言时，到底是要学习什么？只是语法的不同吗？
Status: draft

### 语言的特性

对 Java 程序员而言，Swift 里的 `Optional` 应该算是一种新的特性。在 The Swift Programming Language 里有这样的描述：

> Swift also introduces optional types, which handle the absence of a value. Optionals say either “there is a value, and it equals x” or “there isn’t a value at all”. Optionals are similar to using nil with pointers in Objective-C, but they work for any type, not just classes. Optionals are safer and more expressive than nil pointers in Objective-C and are at the heart of many of Swift’s most powerful features.

看这一句话并不能理解 `Optional` 的强大威力。但如果翻阅 Cocoa Touch 的 API 文档，你会发现大部分函数返回值都是 `Optional` 的，连很多类的属性也是 `Optional`。再深入学习，就会发现 `Optional` 基本上是 Swift 语言里的**错误处理机制**。至少到目前为止，Swift 还没有类似 try catch 这种错误处理方式。

类似的概念还有闭包 (Closure)。Java 8 之前是没有闭包的，如果闭包对你而言是个新概念，那么就值得深入去学习它的作用和最佳实践。我们可以在内心保持一种对优秀编程语言的敬畏：设计一种优秀编程语言的人都是一群极客，他们发明了这样的概念一定是为了解决某种编程过程中的痛点的。当然，如果你学习过 Python，可能闭包对你就不是什么新概念，但实际上你会发现 Swift 里的闭包的写法是可以是非常地简洁。因为 Swift 是一种非常年轻的语言，它在设计阶段一定会去参考其他编程语言优缺点。

### 语言的陷阱

语言的陷阱和特性一样重要。我们看下面一个简单的例子：


```swift
var array = Array<Int>()
array.append(1)
array.append(2)
array.append(3)

func changeSomeThing(a: Array<Int>) {
	a[0] = 100
}

changeSomeThing(array)

println("\(array)")
```

上面的代码会输出什么内容？实际上，这个代码无法编译通过。第 7 行代码会出错，提示数组是只读的。因为对 Swift 设计者而言，这种陷阱一定会在 Java 程序员身上发生，

### 语言的应用场景

我们总是可以问这样的问题：为什么要设计这样一种这个语言？他的设计目标是什么？在什么场景下使用？通过搜索资料，我们不难找出这种语言的应用场景。

**编程语言三个要素**
语法；标准库；应用框架。

**今日推荐**
今天推荐一个小工具[LiceCap][1]。它可以把你的屏幕操作录制成 GIF 动画。

> LICEcap can capture an area of your desktop and save it directly to .GIF or .LCF


