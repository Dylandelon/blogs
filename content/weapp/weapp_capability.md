Title: 微信小程序兼容性问题
Date: 2017-1-19 22:52
Modified: 2017-1-19 22:52
Tags: weapp
Slug: weapp-capability
Authors: Joey Huang
Summary: 本文我们来谈变微信小程序系统兼容性的那些坑。

## 微信小程序兼容性问题

微信小程序发布一周多了，兼容性问题，特别是 Android 平台兼容性问题特别严重。据我观察，好多小程序掉到兼容性的坑里。掉坑里不要紧，更让人捉急的是，从坑里爬上来的时候，手刚抓到坑沿，又被微信官方踩到（紧急修复兼容性的版本没审核通过，被微信打回重审），再次跌落坑底，然后眼睁睁地看着后台用户在破口大骂“什么东西都没有啊~，什么破小程序”。

微信小程序的兼容性问题除了微信本身的 Bug 外，大部分是目标平台对 JavaScript 标准库支持程度不同造成的。

### 微信本身的 Bug 引起的

微信本身的 Bug 引发的兼容性问题有个现成的例子，就是 `wx.request()` 返回的状态码 `res.statusCode` 的值在 iOS 下是 int 型数据，而在 Android 6.0.1 上却是 String 型数据。如果你判断服务器的返回状态码方法不当，可能就踩到坑里了。

```javascript
wx.request({
    url: 'http://api.example.com',
    success: function (res) {
        if (res.statusCode === 200) {
            // success
        } else {
            // server failure
        }
    }
})
```

上述代码就踩坑了，正确的做法是使用 `==` 而不是使用 `===` 来判断。另外一个更规范的方法是使用 `parseInt(res.statusCode) === 200` 来实现。

### Javascript 标准库兼容性问题

比如 `Array.find()` 方法在 iOS 10.2/Android 7.0 上完美支持，但在 Android 6.0.1 上却不支持。如果代码里用到了这个接口，就会导致在 Android 6.0.1 上无法正常工作。通过对比发现，这类接口不支持的个数还是比较多的。特别是 Android 平台版本众多，兼容性问题就更严重，可能一不小小心就掉到坑里。

## 解决方法

微信本身 Bug 只能绕过去，但对 JavaScript 引擎的兼容性，可以有更优雅的解决方法。比如，我们可以打补丁，使用 polyfill 来实现这些不支持的标准库方法。比如，修复 Android 6.0.1 平台不支持 `String.startsWith()` 的问题，可以使用下面的 polyfill 代码：

```javascript
if (!String.prototype.startsWith) {
    console.warn('define polyfill for Array.prototype.startsWith');
    String.prototype.startsWith = function (searchString, position) {
      position = position || 0;
      return this.substr(position, searchString.length) === searchString;
  };
}
```

推而广之，我们可以把平台不支持的标准库方法，使用 polyfill 实现。这就是 [minapp-polyfill](https://github.com/kamidox/minapp-polyfill) 这个项目的目的。

使用方法很简单，把 [minapp-polyfill](https://github.com/kamidox/minapp-polyfill) 项目里的 `polyfill.js` 拷贝到小程序源码目录下，在需要打补丁的 JavaScript 源文件头部引入如下代码即可：

```javascript
import 'path/to/polyfill.js'
```

**目前这个项目只是搭了个骨架，还需要很多方法需要实现。PR is welcome。**

## 各个平台对 JavaScript 标准库支持情况

条件限制，这里统计了四个平台对 JavaScript 标准库的支持情况，分别是 iOS 10.2, Android 6.0.1, Android 7.0, 微信开发者工具，具体数据如下：

Component.apiName  | iOS 10.2 | Android 6.0.1 | Android 7.0 | devtool
-------------------------------------|------------|------------|------------|------------
Array.toString                      | YES        | YES        | YES        | YES
Array.values                        | YES        | N/A        | YES        | N/A
Array.toLocaleString                | YES        | YES        | YES        | YES
Array.concat                        | YES        | YES        | YES        | YES
Array.fill                          | YES        | N/A        | YES        | YES
Array.join                          | YES        | YES        | YES        | YES
Array.pop                           | YES        | YES        | YES        | YES
Array.push                          | YES        | YES        | YES        | YES
Array.reverse                       | YES        | YES        | YES        | YES
Array.shift                         | YES        | YES        | YES        | YES
Array.slice                         | YES        | YES        | YES        | YES
Array.sort                          | YES        | YES        | YES        | YES
Array.splice                        | YES        | YES        | YES        | YES
Array.unshift                       | YES        | YES        | YES        | YES
Array.every                         | YES        | YES        | YES        | YES
Array.forEach                       | YES        | YES        | YES        | YES
Array.some                          | YES        | YES        | YES        | YES
Array.indexOf                       | YES        | YES        | YES        | YES
Array.lastIndexOf                   | YES        | YES        | YES        | YES
Array.filter                        | YES        | YES        | YES        | YES
Array.reduce                        | YES        | YES        | YES        | YES
Array.reduceRight                   | YES        | YES        | YES        | YES
Array.map                           | YES        | YES        | YES        | YES
Array.entries                       | YES        | N/A        | YES        | YES
Array.keys                          | YES        | N/A        | YES        | YES
Array.find                          | YES        | N/A        | YES        | YES
Array.findIndex                     | YES        | N/A        | YES        | YES
Array.includes                      | YES        | N/A        | N/A        | YES
Array.copyWithin                    | YES        | N/A        | YES        | YES
Array.constructor                   | YES        | YES        | YES        | YES
Buffer                              | N/A        | N/A        | N/A        | N/A
DataView.getInt8                    | YES        | YES        | YES        | YES
DataView.getUint8                   | YES        | YES        | YES        | YES
DataView.getInt16                   | YES        | YES        | YES        | YES
DataView.getUint16                  | YES        | YES        | YES        | YES
DataView.getInt32                   | YES        | YES        | YES        | YES
DataView.getUint32                  | YES        | YES        | YES        | YES
DataView.getFloat32                 | YES        | YES        | YES        | YES
DataView.getFloat64                 | YES        | YES        | YES        | YES
DataView.setInt8                    | YES        | YES        | YES        | YES
DataView.setUint8                   | YES        | YES        | YES        | YES
DataView.setInt16                   | YES        | YES        | YES        | YES
DataView.setUint16                  | YES        | YES        | YES        | YES
DataView.setInt32                   | YES        | YES        | YES        | YES
DataView.setUint32                  | YES        | YES        | YES        | YES
DataView.setFloat32                 | YES        | YES        | YES        | YES
DataView.setFloat64                 | YES        | YES        | YES        | YES
DataView.constructor                | YES        | YES        | YES        | YES
Date.toString                       | YES        | YES        | YES        | YES
Date.toISOString                    | YES        | YES        | YES        | YES
Date.toDateString                   | YES        | YES        | YES        | YES
Date.toTimeString                   | YES        | YES        | YES        | YES
Date.toLocaleString                 | YES        | YES        | YES        | YES
Date.toLocaleDateString             | YES        | YES        | YES        | YES
Date.toLocaleTimeString             | YES        | YES        | YES        | YES
Date.valueOf                        | YES        | YES        | YES        | YES
Date.getTime                        | YES        | YES        | YES        | YES
Date.getFullYear                    | YES        | YES        | YES        | YES
Date.getUTCFullYear                 | YES        | YES        | YES        | YES
Date.getMonth                       | YES        | YES        | YES        | YES
Date.getUTCMonth                    | YES        | YES        | YES        | YES
Date.getDate                        | YES        | YES        | YES        | YES
Date.getUTCDate                     | YES        | YES        | YES        | YES
Date.getDay                         | YES        | YES        | YES        | YES
Date.getUTCDay                      | YES        | YES        | YES        | YES
Date.getHours                       | YES        | YES        | YES        | YES
Date.getUTCHours                    | YES        | YES        | YES        | YES
Date.getMinutes                     | YES        | YES        | YES        | YES
Date.getUTCMinutes                  | YES        | YES        | YES        | YES
Date.getSeconds                     | YES        | YES        | YES        | YES
Date.getUTCSeconds                  | YES        | YES        | YES        | YES
Date.getMilliseconds                | YES        | YES        | YES        | YES
Date.getUTCMilliseconds             | YES        | YES        | YES        | YES
Date.getTimezoneOffset              | YES        | YES        | YES        | YES
Date.setTime                        | YES        | YES        | YES        | YES
Date.setMilliseconds                | YES        | YES        | YES        | YES
Date.setUTCMilliseconds             | YES        | YES        | YES        | YES
Date.setSeconds                     | YES        | YES        | YES        | YES
Date.setUTCSeconds                  | YES        | YES        | YES        | YES
Date.setMinutes                     | YES        | YES        | YES        | YES
Date.setUTCMinutes                  | YES        | YES        | YES        | YES
Date.setHours                       | YES        | YES        | YES        | YES
Date.setUTCHours                    | YES        | YES        | YES        | YES
Date.setDate                        | YES        | YES        | YES        | YES
Date.setUTCDate                     | YES        | YES        | YES        | YES
Date.setMonth                       | YES        | YES        | YES        | YES
Date.setUTCMonth                    | YES        | YES        | YES        | YES
Date.setFullYear                    | YES        | YES        | YES        | YES
Date.setUTCFullYear                 | YES        | YES        | YES        | YES
Date.setYear                        | YES        | YES        | YES        | YES
Date.getYear                        | YES        | YES        | YES        | YES
Date.toJSON                         | YES        | YES        | YES        | YES
Date.toUTCString                    | YES        | YES        | YES        | YES
Date.toGMTString                    | YES        | YES        | YES        | YES
Date.constructor                    | YES        | YES        | YES        | YES
Error.toString                      | YES        | YES        | YES        | YES
Error.constructor                   | YES        | YES        | YES        | YES
Float32Array.constructor            | YES        | YES        | YES        | YES
Float64Array.constructor            | YES        | YES        | YES        | YES
Function.constructor                | YES        | YES        | YES        | YES
Int16Array.constructor              | YES        | YES        | YES        | YES
Int32Array.constructor              | YES        | YES        | YES        | YES
Int8Array.constructor               | YES        | YES        | YES        | YES
Map.forEach                         | YES        | N/A        | YES        | YES
Map.clear                           | YES        | N/A        | YES        | YES
Map.delete                          | YES        | N/A        | YES        | YES
Map.get                             | YES        | N/A        | YES        | YES
Map.has                             | YES        | N/A        | YES        | YES
Map.set                             | YES        | N/A        | YES        | YES
Map.keys                            | YES        | N/A        | YES        | YES
Map.values                          | YES        | N/A        | YES        | YES
Map.entries                         | YES        | N/A        | YES        | YES
Map.constructor                     | YES        | N/A        | YES        | YES
Math.abs                            | YES        | YES        | YES        | YES
Math.acos                           | YES        | YES        | YES        | YES
Math.asin                           | YES        | YES        | YES        | YES
Math.atan                           | YES        | YES        | YES        | YES
Math.acosh                          | YES        | N/A        | YES        | YES
Math.asinh                          | YES        | N/A        | YES        | YES
Math.atanh                          | YES        | N/A        | YES        | YES
Math.atan2                          | YES        | YES        | YES        | YES
Math.cbrt                           | YES        | N/A        | YES        | YES
Math.ceil                           | YES        | YES        | YES        | YES
Math.clz32                          | YES        | N/A        | YES        | YES
Math.cos                            | YES        | YES        | YES        | YES
Math.cosh                           | YES        | N/A        | YES        | YES
Math.exp                            | YES        | YES        | YES        | YES
Math.expm1                          | YES        | N/A        | YES        | YES
Math.floor                          | YES        | YES        | YES        | YES
Math.fround                         | YES        | N/A        | YES        | YES
Math.hypot                          | YES        | N/A        | YES        | YES
Math.log                            | YES        | YES        | YES        | YES
Math.log10                          | YES        | N/A        | YES        | YES
Math.log1p                          | YES        | N/A        | YES        | YES
Math.log2                           | YES        | N/A        | YES        | YES
Math.max                            | YES        | YES        | YES        | YES
Math.min                            | YES        | YES        | YES        | YES
Math.pow                            | YES        | YES        | YES        | YES
Math.random                         | YES        | YES        | YES        | YES
Math.round                          | YES        | YES        | YES        | YES
Math.sign                           | YES        | N/A        | YES        | YES
Math.sin                            | YES        | YES        | YES        | YES
Math.sinh                           | YES        | N/A        | YES        | YES
Math.sqrt                           | YES        | YES        | YES        | YES
Math.tan                            | YES        | YES        | YES        | YES
Math.tanh                           | YES        | N/A        | YES        | YES
Math.trunc                          | YES        | N/A        | YES        | YES
Math.imul                           | YES        | YES        | YES        | YES
Object.toString                     | YES        | YES        | YES        | YES
Object.toLocaleString               | YES        | YES        | YES        | YES
Object.valueOf                      | YES        | YES        | YES        | YES
Object.hasOwnProperty               | YES        | YES        | YES        | YES
Object.propertyIsEnumerable         | YES        | YES        | YES        | YES
Object.isPrototypeOf                | YES        | YES        | YES        | YES
Object.\__defineGetter__             | YES        | YES        | YES        | YES
Object.\__defineSetter__             | YES        | YES        | YES        | YES
Object.\__lookupGetter__             | YES        | YES        | YES        | YES
Object.\__lookupSetter__             | YES        | YES        | YES        | YES
Object.constructor                  | YES        | YES        | YES        | YES
Promise.then                        | YES        | YES        | YES        | YES
Promise.catch                       | YES        | YES        | YES        | YES
Promise.constructor                 | YES        | YES        | YES        | YES
RegExp.compile                      | YES        | YES        | YES        | YES
RegExp.exec                         | YES        | YES        | YES        | YES
RegExp.toString                     | YES        | YES        | YES        | YES
RegExp.test                         | YES        | YES        | YES        | YES
RegExp.constructor                  | YES        | YES        | YES        | YES
Set.forEach                         | YES        | N/A        | YES        | YES
Set.add                             | YES        | N/A        | YES        | YES
Set.clear                           | YES        | N/A        | YES        | YES
Set.delete                          | YES        | N/A        | YES        | YES
Set.has                             | YES        | N/A        | YES        | YES
Set.entries                         | YES        | N/A        | YES        | YES
Set.values                          | YES        | N/A        | YES        | YES
Set.keys                            | YES        | N/A        | YES        | YES
Set.constructor                     | YES        | N/A        | YES        | YES
String.match                        | YES        | YES        | YES        | YES
String.padStart                     | YES        | N/A        | N/A        | N/A
String.padEnd                       | YES        | N/A        | N/A        | N/A
String.repeat                       | YES        | N/A        | YES        | YES
String.replace                      | YES        | YES        | YES        | YES
String.search                       | YES        | YES        | YES        | YES
String.split                        | YES        | YES        | YES        | YES
String.toString                     | YES        | YES        | YES        | YES
String.valueOf                      | YES        | YES        | YES        | YES
String.charAt                       | YES        | YES        | YES        | YES
String.charCodeAt                   | YES        | YES        | YES        | YES
String.codePointAt                  | YES        | N/A        | YES        | YES
String.concat                       | YES        | YES        | YES        | YES
String.indexOf                      | YES        | YES        | YES        | YES
String.lastIndexOf                  | YES        | YES        | YES        | YES
String.slice                        | YES        | YES        | YES        | YES
String.substr                       | YES        | YES        | YES        | YES
String.substring                    | YES        | YES        | YES        | YES
String.toLowerCase                  | YES        | YES        | YES        | YES
String.toUpperCase                  | YES        | YES        | YES        | YES
String.localeCompare                | YES        | YES        | YES        | YES
String.toLocaleLowerCase            | YES        | YES        | YES        | YES
String.toLocaleUpperCase            | YES        | YES        | YES        | YES
String.big                          | YES        | YES        | YES        | YES
String.small                        | YES        | YES        | YES        | YES
String.blink                        | YES        | YES        | YES        | YES
String.bold                         | YES        | YES        | YES        | YES
String.fixed                        | YES        | YES        | YES        | YES
String.italics                      | YES        | YES        | YES        | YES
String.strike                       | YES        | YES        | YES        | YES
String.sub                          | YES        | YES        | YES        | YES
String.sup                          | YES        | YES        | YES        | YES
String.fontcolor                    | YES        | YES        | YES        | YES
String.fontsize                     | YES        | YES        | YES        | YES
String.anchor                       | YES        | YES        | YES        | YES
String.link                         | YES        | YES        | YES        | YES
String.trim                         | YES        | YES        | YES        | YES
String.trimLeft                     | YES        | YES        | YES        | YES
String.trimRight                    | YES        | YES        | YES        | YES
String.startsWith                   | YES        | N/A        | YES        | YES
String.endsWith                     | YES        | N/A        | YES        | YES
String.includes                     | YES        | N/A        | YES        | YES
String.normalize                    | YES        | YES        | YES        | YES
String.constructor                  | YES        | YES        | YES        | YES
Symbol.toString                     | YES        | N/A        | YES        | YES
Symbol.valueOf                      | YES        | N/A        | N/A        | YES
Symbol.constructor                  | YES        | N/A        | YES        | YES
TypeError.toString                  | YES        | N/A        | N/A        | YES
TypeError.constructor               | YES        | YES        | YES        | YES
Uint16Array.constructor             | YES        | YES        | YES        | YES
Uint32Array.constructor             | YES        | YES        | YES        | YES
Uint8Array.constructor              | YES        | YES        | YES        | YES
Uint8ClampedArray.constructor       | YES        | YES        | YES        | YES
WeakMap.delete                      | YES        | YES        | YES        | YES
WeakMap.get                         | YES        | YES        | YES        | YES
WeakMap.has                         | YES        | YES        | YES        | YES
WeakMap.set                         | YES        | YES        | YES        | YES
WeakMap.constructor                 | YES        | YES        | YES        | YES

*N/A 表示这个标准库方法在平台上不支持*

**Q: 这些数据是怎么来的，靠谱吗？**
A: 这些数据是在真实小程序运行环境下运行，然后把 API 支持情况发送到服务器后台，再写个脚本把数据整理汇总后得来的。

**Q: 其他平台，比如 Android 5.0 的支持情况怎么样？**
A: 由于条件限制，手上没有 Android 5.0 的手机，有愿意配合收集数据的，私信留言。配合的方法很简单，用指定型号的手机打开一个微信小程序，按一个按钮即可。

**Q: 为什么不使用 [lodash](https://github.com/lodash/lodash) 之类效率更高的库，而使用的标准库？**
A: 使用 lodash 之类的确实效率更高，兼容性也更好。基于两个原因没有使用，一是 lodash 太大，而微信小程序限制在 1MB 以内。当然，可以用 lodash 模块化的版本来解决，但还有第二个原因，即 lodash 的一些 API 也有兼容性问题，比如我试过 [lodash.findIndex](https://www.npmjs.com/package/lodash.findindex) 这个包，结果在 Android 6.0.1 上也无法成功运行 (这一点未做深入验证，感兴趣的同学可以验证一下)。

## 总结

从后台数据来看，小程序刚发布的前三天，确实带来了非常可观的流量红利，但这部分偿鲜的用户，很快就消失了。三天过后，基本上保持了平衡的访问量。流量红利和广告一样，是催化剂，真正有价值的还是要做用户需要的产品。

在此顺手安利一下开发的两个小程序 [360好书推荐](https://minapp.com/miniapp/90/) 和 [51经典电影](https://minapp.com/miniapp/89/)，偶尔想用的时候打开，可能会偶遇一些小惊喜。但坦白讲，这两个小程序都和微信倡导的小程序价值观不符。微信还是希望通过小程序把线下低频的，服务成本高（这里应该主要是时间成本，即便利性）的场景，转化为线上快捷的使用方式。
