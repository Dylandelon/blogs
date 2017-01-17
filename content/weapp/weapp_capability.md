Title: 微信小程序兼容性问题
Date: 2017-1-19 22:52
Modified: 2017-1-19 22:52
Tags: weapp
Slug: weapp-capability
Authors: Joey Huang
Summary: 本文我们来谈变微信小程序系统兼容性的那些坑。

## 兼容性问题由来

微信小程序发布一周多了，兼容性问题，特别是 Android 平台兼容性问题特别严重。据我观察，好多小程序掉到兼容性的坑里。掉坑里不要紧，更让人捉急的是，从坑里爬上来的时候，手刚抓到坑沿，又被微信官方踩到（紧急修复兼容性的版本没审核通过，被微信打回重审），再次跌落坑底，然后眼睁睁地看着后台用户在破口大骂“什么东西都没有啊~，什么破小程序”。

微信小程序的兼容性问题除了微信本身的 Bug 外，大部分是目标平台 JavaScript 引擎对标准库支持程度不同造成的。

### 微信本身的 Bug 引起的

微信本身的 Bug 引发的兼容性问题有个现成的例子，就是 `wx.request()` 返回值的 `res.statusCode` 的值，在 iOS 及开发工具下是 int 型数据，而在 Android 6.0.1 上却是 String 型数据。这样造成的兼容性问题就是，如果你判断服务器的返回状态码方法不当，可能就踩到坑里了。

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

### Javascript 引擎兼容性问题

比如 `Array.find()` 方法在 iOS 10.2/Android 7.0 上完美支持，但在 Android 6.0.1 上却不支持。如果代码里用到了这个接口，就会导致在 Android 6.0.1 上无法正常工作。通过对比发现，这类接口不支持的个数还是比较多的。特别是 Android 平台版本众多，兼容性问题就更严重，可能一不小小心就掉到坑里。

## 解决方法

微信本身 Bug 只能绕过去，但对 JavaScript 引擎的兼容性，可以有更优雅的解决方法。比如，我们可以打补丁，针对不支持特定接口的平台，使用 polyfill 来实现这些接口。