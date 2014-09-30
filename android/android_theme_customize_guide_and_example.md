Android Theme结构分析与典型案例
================================

[TOC]

本文记录android源码平台通过theme来定制UI的典型案例，进而梳理出theme的整体结构。

##ActionBar外观样式结构

###1. [attrs.xml][1]用ActionBar定义了外观属性

```xml
<declare-styleable name="ActionBar">
    ......
</declare-styleable>
```

###2. [themes.xml][3]里的android:actionBarStyle定义了不同主题的ActionBar外观

```xml
<style name="Theme.Holo">
    <item name="actionBarStyle">@android:style/Widget.Holo.ActionBar</item>
</style>

<style name="Theme.Holo.Light">
    <item name="android:actionBarStyle">@android:style/Widget.Holo.Light.ActionBar.Solid</item>
</style>
```

###3. [styles.xml][2]定义了具体的属性值

```xml
<style name="Widget.Holo.Light.ActionBar" parent="Widget.Holo.ActionBar">
    <item name="android:titleTextStyle">@android:style/TextAppearance.Holo.Widget.ActionBar.Title</item>
    <item name="android:subtitleTextStyle">@android:style/TextAppearance.Holo.Widget.ActionBar.Subtitle</item>
    <item name="android:background">@android:drawable/ab_transparent_light_holo</item>
    <item name="android:backgroundStacked">@android:drawable/ab_stacked_transparent_light_holo</item>
    <item name="android:backgroundSplit">@android:drawable/ab_bottom_transparent_light_holo</item>
    <item name="android:homeAsUpIndicator">@android:drawable/ic_ab_back_holo_light</item>
    <item name="android:progressBarStyle">@android:style/Widget.Holo.Light.ProgressBar.Horizontal</item>
    <item name="android:indeterminateProgressStyle">@android:style/Widget.Holo.Light.ProgressBar</item>
</style>
```

###4. 典型属性说明
* android:background: ActionBar背景
* android:backgroundSplit: ActionBar拆分出来的在屏幕下部的背景
* android:homeAsUpIndicator: ActionBar上的返回图标
* android:titleTextStyle: ActionBar标题文本样式

###5. 实例: 修改Theme.Holo.Light的ActionBar背景

在[styles.xml][2]里找到Widget.Holo.Light.ActionBar.Solid的定义，并且修改background和backgroundSplit的值即可。

```xml
<style name="Widget.Holo.Light.ActionBar.Solid">
    <item name="android:background">@android:drawable/ab_solid_light_holo</item>
    <item name="android:backgroundSplit">@android:drawable/ab_bottom_solid_light_holo</item>
</style>
```

##attrs详解
* dialogTitleIconsDecorLayout: 用来定义对话框窗口标题的装饰器。修改对话框标题样式时，可定制这个属性。参阅@layout/dialog_title_icons_holo

##参考内容
* [属性的定义][1]
* [样式的定义][2]
* [主题的定义][3]
* [窗口组件的代码流程][4]

[1]: https://android.googlesource.com/platform/frameworks/base/+/android-sdk-4.4.2_r1.0.1/core/res/res/values/attrs.xml
[2]: https://android.googlesource.com/platform/frameworks/base/+/android-sdk-4.4.2_r1.0.1/core/res/res/values/styles.xml
[3]: https://android.googlesource.com/platform/frameworks/base/+/android-sdk-4.4.2_r1.0.1/core/res/res/values/themes.xml
[4]: https://android.googlesource.com/platform/frameworks/base/+/android-sdk-4.4.2_r1.0.1/policy/src/com/android/internal/policy/impl/PhoneWindow.java
