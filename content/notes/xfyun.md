Title: 迅飞语义识别集成向导
Date: 2015-12-15 15:36
Modified: 2015-12-15 15:36
Slug: xfyun
Authors: Joey Huang
Summary: 迅飞语义识别集成向导
Status: draft

## 如何集成迅飞语义识别向导

[TOC]

### 准备工作

* [申请开发者账号][1]
* 新建应用

### 开启语义识别服务

* [启用服务][2]
* [配置语义][3]，打开[语义管理][4]，在`通用语义场景`点击`设置`，配置智能家居的语义场景，目前是配置五个：**窗帘，灯，空调，电视，开关**

### 下载 SDK

[下载 SDK][5]，查看里面的 Demo 完成语义识别 Demo 开发。

比如，针对 Android 平台的代码如下：

```java
//1.创建文本语义理解对象
SpeechUnderstander understander = SpeechUnderstander.createUnderstander(context, null);
//2.设置参数，语义场景配置请登录http://osp.voicecloud.cn/
understander.setParameter(SpeechConstant.LANGUAGE, "zh_cn");
//3.开始语义理解
understander.startUnderstanding(mUnderstanderListener);
// XmlParser为结果解析类，见SpeechDemo
private SpeechUnderstanderListener mUnderstanderListener = new SpeechUnderstanderListener(){
public void onResult(UnderstanderResult result) {
            String text = result.getResultString();
}
    public void onError(SpeechError error) {}//会话发生错误回调接口
    public void onBeginOfSpeech() {}//开始录音
    public void onVolumeChanged(int volume){} //音量值0~30
    public void onEndOfSpeech() {}//结束录音
    public void onEvent(int eventType, int arg1, int arg2, Bundle obj) {}//扩展用接口
};
```

语义识别的结果是个 Json 字符串，比如：

```json
{
  "semantic": {
    "slots": {
      "location": {
        "type": "LOC_HOUSE",
        "room": "客厅"
      },
      "onOff": "OPEN"
    }
  },
  "rc": 0,
  "device": "airControl",
  "service": "smartHome",
  "operation": "OPEN",
  "text": "把客厅的空调打开"
}
```

### 查阅智能家居语义开发文档

查阅《语义开放平台_智能家居场景协议规范文档_v1.0.pdf》文档。

* 2.1 应答消息格式
* 2.2 应答消息字段定义
* 3.2 地点描述相关协议
* 4 设备服务协议
    * 4.2 窗帘
    * 4.3 灯
    * 4.7 电视
    * 4.18 空调
    * 4.30 开关

### 语义识别举例

#### 能正确识别的语义

* 把客厅的空调打开
* 把厕所的灯打开
* 把楼上的灯打开
* 把客厅的电视关掉
* 把二楼洗手间的灯打开
* 把窗帘打开一半
* 太热了
* 太冷了
* 把客厅的空调温度调高一点

#### 不能正确识别的语义

* 房间里太亮了
* 打开离家模式

### 实现策略

语音控制主要有两个要素，一是**设备**，如客厅的空调，书房的空调，厕所的电灯，餐厅的开关等等。二是**动作**，如打开，关闭，打开一半，调高温度等等。

1. 使用语义接口来实现（text）
2. 设备定位：
  2.1 设备列表（灯光1，冰箱1，灯光5）
  2.2 遍历设备列表，去 text 里找 （第一优先级），如果找到，就直接使用这个设备来作为控制对象
  2.3 动作：从语义识别（第一优先级），比如打开，关闭，调高，调低等。
  2.4 动作：自定义的动作（调亮，调暗），根据自定义动作的关键词，从 text 里找。
  2.5 人性化动作：比如，用户说太热了，语义识别会识别出打开空调，但是哪个空调呢？如果只有一个空调，那我就直接打开空调。再比如，用户说打开电视。如果只有一个电视，就直接打开。如果有多个电视，报错。
  2.6 使用地点定位：比如“打开一楼客厅灯光”，如果一楼只有一个客厅，且客厅只有一个灯光，就打开。否则提示用户错误。


[1]: http://www.xfyun.cn/
[2]: http://www.xfyun.cn/index.php/services/osp
[3]: http://osp.voicecloud.cn/
[4]: http://osp.voicecloud.cn/index.php/default/app/control
[5]: http://www.xfyun.cn/sdk/dispatcher
