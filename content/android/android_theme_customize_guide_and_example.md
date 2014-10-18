Title: Android Theme结构分析与典型案例
Date: 2014-09-26 20:20
Modified: 2014-09-26 20:20
Tags: android, theme
Slug: android-theme-customize-guide-and-example
Authors: Joey Huang
Summary: 本文记录android源码平台通过theme来定制UI的典型案例，进而梳理出theme的整体结构


本文记录android源码平台通过theme来定制UI的典型案例，进而梳理出theme的整体结构。

##ActionBar外观样式结构

### 1. [attrs.xml][1]用ActionBar定义了外观属性

```xml
<declare-styleable name="ActionBar">
    ......
</declare-styleable>
```

### 2. [themes.xml][3]里的android:actionBarStyle定义了不同主题的ActionBar外观

```xml
<style name="Theme.Holo">
    <item name="actionBarStyle">@android:style/Widget.Holo.ActionBar</item>
</style>

<style name="Theme.Holo.Light">
    <item name="android:actionBarStyle">@android:style/Widget.Holo.Light.ActionBar.Solid</item>
</style>
```

### 3. [styles.xml][2]定义了具体的属性值

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

### 4. 典型属性说明
* android:background: ActionBar背景
* android:backgroundSplit: ActionBar拆分出来的在屏幕下部的背景
* android:homeAsUpIndicator: ActionBar上的返回图标
* android:titleTextStyle: ActionBar标题文本样式

### 5. 实例: 修改Theme.Holo.Light的ActionBar背景

在[styles.xml][2]里找到Widget.Holo.Light.ActionBar.Solid的定义，并且修改background和backgroundSplit的值即可。

```xml
<style name="Widget.Holo.Light.ActionBar.Solid">
    <item name="android:background">@android:drawable/ab_solid_light_holo</item>
    <item name="android:backgroundSplit">@android:drawable/ab_bottom_solid_light_holo</item>
</style>
```

## Preference外观样式

### 1. PreferenceCategory外观定义分析

PreferenceCategory由Theme里的PreferenceCategoryStyle决定其外观样式。在[theme.xml][3]里有如下定义：

```xml
<style name="Theme.Holo.Light" parent="Theme.Light">
    ...
    <item name="preferenceCategoryStyle">@android:style/Preference.Holo.Category</item>
    ...
</style>
```

`Preference.Holo.Category`在[style.xml][2]里定义如下：

```xml
<style name="Preference.Holo.Category">
    <item name="android:layout">@android:layout/preference_category_holo</item>
    <!-- The title should not dim if the category is disabled, instead only the preference children should dim. -->
    <item name="android:shouldDisableView">false</item>
    <item name="android:selectable">false</item>
</style>
```

`preference_category_holo`定义如下：

```xml
<!-- Layout used for PreferenceCategory in a PreferenceActivity. -->
<TextView xmlns:android="http://schemas.android.com/apk/res/android"
    style="?android:attr/listSeparatorTextViewStyle"
    android:id="@+android:id/title"
    android:paddingStart="@dimen/preference_item_padding_side"
    android:paddingEnd="@dimen/preference_item_padding_side" />
```

由此可见PreferenceCategory实际是一个TextView，它使用theme里定义的`listSeparatorTextViewStyle`的外观来定义自己的外观。`listSeparatorTextViewStyle`定义在[theme.xml][3]里：

```xml
<style name="Theme.Holo.Light" parent="Theme.Light">
    ...
    <item name="listSeparatorTextViewStyle">@android:style/Widget.Holo.Light.TextView.ListSeparator</item>
    ...
</style>
```

`Widget.Holo.Light.TextView.ListSeparator`定义在[style.xml][2]里：

```xml
<style name="Widget.Holo.Light.TextView.ListSeparator" parent="Widget.TextView.ListSeparator">
    <item name="android:background">@android:drawable/list_section_divider_holo_light</item>
    <item name="android:textAllCaps">true</item>
</style>
```

### 2. PreferenceCategory外观修改

如果想修改`PreferenceCategory`的背景和文字颜色，由上面的分析，我们只需要修改theme的`listSeparatorTextViewStyle`即可。定义一个新的背景图片即可实现：

```xml
<style name="MyListSeparator" parent="Widget.Holo.Light.TextView.ListSeparator">
    <item name="android:background">@drawable/my_list_section_divider_holo_light</item>
    <item name="android:textStyle">bold</item>
    <item name="android:textColor">@color/my_text_color_list_separator</item>
    <item name="android:textSize">16sp</item>
</style>
```

这样，定义一个theme，将其`listSeparatorTextViewStyle`设置成`MyListSeparator`即可。



## attrs详解
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
