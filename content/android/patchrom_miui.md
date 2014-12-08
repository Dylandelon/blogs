Title: 使用 patchrom 移植 MIUI
Date: 2014-12-06 23:00
Modified: 2014-12-06 23:00
Tags: android, patchrom, miui
Slug: patchrom-miui
Authors: Joey Huang
Summary: 本文介绍使用 patchrom 移植 MIUI 的方法。记录整个过程中遇到问题的调试方法及其解决方案。

[TOC]

## 开篇

MIUI 使用代码插桩的方式来移植。即 MIUI 把他们基于 AOSP 的修改的代码全部用 smali 开放出来。这样我们通过对比 MIUI 的 smali 代码和 AOSP 的 smali　代码就可以知道 MIUI 修改了哪些内容，把这些内容移植过去即可完成 MIUI的移植。本文以 jellybean42-mtk 为例，描述使用 patchrom 移植 MIUI的方法以及在过程中遇到的问题及其调试方法。

## 移植过程

可以查阅 [MIUI 移植的文档][1]了解一些背景知识。这里将主体步骤描述如下：

### 下载 MIUI patchrom

下载 repo 工具

    :::shell
    mkdir ~/bin
    curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
    chmod a+x ~/bin/repo

下载 MIUI patchrom 代码

    :::shell
    mkdir ~/work/patchrom
    cd ~/work/patchrom
    repo init -u git://github.com/MiCode/patchrom.git -b jellybean42-mtk
    repo sync

`repo sync` 命令需要很长的时间才能把代码下载完，代码总量大于10G。所以，基本上可以玩儿去了，不要傻傻地等了。

代码下载完成后，我们就可以开始移植工作了。实际的代码目录树结构和内容和文档里描述的会有出入，我们可以忽略文档里的，以实际代码为准。本文使用2014-12-04下载的代码为准。

### 准备移植目录

在 patchrom 根目录下创建一个产品的工作目录用来移植时使用。

    :::shell
    cd ~/work/patchrom
    source build/envsetup.sh
    mkdir ~/work/patchrom/mtk6582
    cd mtk6582

### 准备一个 OTA 升级包

我们直接拿一个要当作底包的 OTA 升级包来作为 stockrom.zip。对这个底包有以下的要求：

1. 这个底包必须是 user 版本且足够稳定。因为根据底包移植完的软件是直接拿来当产品使用的。
2. 这个底包可以直接在手机里通过 recovery 模式升级。这个对后面移植完手的 miui-ota 包的烧录有帮助。

这样，我们直接把这个 OTA 升级包 stockrom.zip 放在刚刚我们创建的 mtk6582 目录下。除此之外，我们还需要一台内核 root 过的手机，以便配合整个移植过程。

!!! Note "关于stockrom.zip"
    patchrom 官方移植教程是使用 `../tools/ota_target_from_phone -r` 来直接从移植手机里生成 stockrom.zip 。这个命令要求手机先运行在 recovery 模式下。我自己验证过无法运行，没去深究。所以，直接拿一个 OTA 升级包来作为移植的底包。

user 版本的 OTA 升级包里，apk 文件都是经过 odex 优化的。而 smali 反汇编又需要优化前的 apk　文件。怎么样解决这个问题呢？

1. 打开 stockrom.zip 文件，把 system/framework 下的 pacheCoder.jar, gcm.jar, hpe.jar 从 zip 包里删除。这是因为这三个 jar 包没有经过 odex 优化。即找不到相应的 odex 包。这样的情况在下面的步骤处理时会出错。
2. 在 patchrom/mtk6582 目录下，执行如下命令　`../tools/deodex.sh stockrom.zip` ，执行结束后，原 OTA 包会被覆盖掉，而且里面的 odex 文件将全部被打包回 apk 文件里。
3. 把步骤 1 删除掉的 3 个 jar 包放回 zip 包里。然后运行下面命令对zip包进行重新签名 `java -Xmx2048m -jar signapk.jar -w testkey.x509.pem testkey.pk8 stockrom.zip stockrom-signed.zip`。
4. 把新生成的 ota zip 包放在手机 SD 卡里，进 recovery 模式进行升级。确保制作出来的包没有问题。

### 准备一个 makefile

下面的 makefile 可以作为模板，里面有详细的注释说明每个字段的含义。

    :::makefile
    #
    # Makefile for mtk6582
    #

    # 指定我们要移植的手机的底包，就是上一步骤里准备的 stockrom.zip
    local-zip-file     := stockrom.zip

    # 编译我们移植好的 MIUI ROM 时的输出文件名
    local-out-zip-file := MIUI_MTK6582.zip

    # 制作升级差异包时所需要的上一个版本的 ota 包目录，我们暂时还用不着
    local-previous-target-dir := ~/work/ota_base/mtk6582

    # All apps from original ZIP, but has smali files chanded
    local-modified-apps :=

    local-modified-jars :=

    # 哪些 MIUI 模块不包含在最终生成的 MIUI ROM 里。这里我们默认包含所有的 MIUI 模块。
    local-miui-removed-apps :=

    # 我们在移植过程中，使用了 MIUI 的 Phone 模块，但对 MIUI 的这个模块进行反编译并修改了部分 smali 代码使其功能正常。
    # 针对 jellybean42-mtk 这个分支，所有的 MIUI 模块定义在 patchrom/build/jellybean42-mtk.mk 文件里。
    local-miui-modified-apps := Phone

    # density define
    local-density := XHDPI

    include phoneapps.mk

    # To include the local targets before and after zip the final ZIP file,
    # and the local-targets should:
    # (1) be defined after including porting.mk if using any global variable(see porting.mk)
    # (2) the name should be leaded with local- to prevent any conflict with global targets
    local-pre-zip := local-pre-zip-misc
    local-after-zip:= local-put-to-phone

    # The local targets after the zip file is generated, could include 'zip2sd' to
    # deliver the zip file to phone, or to customize other actions

    include $(PORT_BUILD)/porting.mk

    # To define any local-target
    updater := $(ZIP_DIR)/META-INF/com/google/android/updater-script
    pre_install_data_packages := $(TMP_DIR)/pre_install_apk_pkgname.txt
    local-pre-zip-misc:
	    rm -rf $(pre_install_data_packages)
	    for apk in $(ZIP_DIR)/data/media/preinstall_apps/*.apk; do\
		    $(AAPT) d --values resources $$apk | grep 'id=127 packageCount' | sed -e "s/^.*name=//" >> $(pre_install_data_packages);\
	    done
	    more $(pre_install_data_packages) | wc -l > $(ZIP_DIR)/system/etc/enforcecopyinglibpackages.txt
	    more $(pre_install_data_packages) >> $(ZIP_DIR)/system/etc/enforcecopyinglibpackages.txt

    out/framework2.jar : out/framework.jar

    %.phone : out/%.jar
	    @echo push -- to --- phone
	    adb remount
	    adb push $< /system/framework
	    adb shell chmod 644 /system/framework/$*.jar

    %.sign-plat : out/%
	    java -jar $(TOOL_DIR)/signapk.jar $(PORT_ROOT)/build/security/platform.x509.pem $(PORT_ROOT)/build/security/platform.pk8  $< $<.signed
	    @echo push -- to --- phone
	    adb remount
	    adb push $<.signed /system/app/$*
	    adb shell chmod 644 /system/app/$*

### make workspace

在 patchrom/mtk6582 目录下运行 `make workspace` 命令。这个命令会把 stockrom.zip 文件解压，并且反编译里面的 jar/apk 来作为移植的基础。在上述 makefile 内容下，会生成下面几个文件夹：

1. android.policy.jar.out
2. framework.jar.out
3. framework-res
4. mediatek-framework.jar.out
5. secondary-framework.jar.out
6. services.jar.out

!!! Note "深入理解make workspace"
    可以阅读 patchrom/build　目录下的 makefile 文件来深入理解 patchrom　的编译系统。对 `make workspace` 命令，实际上是根据 jellybean42-mtk.mk 里的 private-miui-jars，以及 framework-res.apk　和 makefile　里定义的 local-modified-apps 来决定反编译哪些内容的。

### make firstpatch

在 patchrom/mtk6582 目录下运行 `make firstpatch` 命令。这个命令偿试自动合并 smali 文件。如果无法合并，会在 reject 目录下生成有冲突的文件。所以，运行这个命令后，我们只需要合并 reject 目录下的有冲突的文件即可完成 MIUI ROM 的移植工作。

这个命令在 patchrom/mtk6582/temp 目录下生成的文件树如下：

    :::shell
    ├── dst_smali_orig # 这个是底包 stockrom.zip 里反编译出来的系统 smali 文件
    │   ├── android.policy.jar.out
    │   ├── framework.jar.out
    │   ├── mediatek-framework.jar.out
    │   ├── secondary-framework.jar.out
    │   └── services.jar.out
    ├── dst_smali_patched　# 这个是程序自动合并的目标 smali 文件
    │   ├── android.policy.jar.out
    │   ├── framework.jar.out
    │   ├── mediatek-framework.jar.out
    │   ├── secondary-framework.jar.out
    │   └── services.jar.out
    ├── new_smali # 这个是 MIUI ROM 里反编译出来的系统 smali 文件
    │   ├── android.policy.jar.out
    │   ├── framework.jar.out
    │   ├── mediatek-framework.jar.out
    │   ├── secondary-framework.jar.out
    │   └── services.jar.out
    ├── old_smali　# 这个是 AOSP 里反编译出来的系统 smali 文件
    │   ├── android.policy.jar.out
    │   ├── framework.jar.out
    │   ├── mediatek-framework.jar.out
    │   ├── secondary-framework.jar.out
    │   └── services.jar.out
    └── reject　# 这个是由于冲突程序无法自动合并，需要手动合并的 smali 文件
        ├── android.policy.jar.out
        ├── framework.jar.out
        ├── secondary-framework.jar.out
        └── services.jar.out

可以阅读 patchrom/build 和 patchrom/tools 两个目录下的 makefile 和 shell 源码来理解 make firstpatch 过程到底做了什么事情。

!!! Note "关于自动合并"
    自动合并会把一些差异自动合并进 dst_smali_patched 目录。这个合并过程是怎么样的呢？可以阅读 patchrom/tools/patch_miui_framework.sh 文件来获取详细信息。这里总结自动合并的过程如下：1) 用 diff 命令计算 old_smali 和 new_smali 两个文件夹下的每个文件的补丁 .diff 文件。2) 用 patch 命令把计算出来的 .diff 文件逐个给 dst_smali_orig 目录下的对应文件打补丁，自动合并成功的文件最终生成成 dst_smali_patched 目录下。

### 手动合并 reject 目录

看起来好简单，其实挑战刚刚开始，要手动合并 reject 目录下的内容不是件容易的事情。即使合并完，后面的调试过程也是痛苦异常。不过也别灰心。办法总比困难多。掌握了基本原理，那么合并过程和调试过程其实还是有规律可以遵循的。在开始这个痛苦过程前，需要先掌握 smali 语法以及 Dalvik　虚拟机的字节码的函义。关于 Dalvik 虚拟机字节码，这个[文档][2]可以查阅。

手动合并 smali 代码的流程是这样的：

1. 用文本编辑器逐个打开 `reject` 目录下的所有文件，找出冲突的代码块
2. 用 BeyondCompare/Meld 工具去比较 old_smali 和 new_smali，找出冲突代码块的位置
3. 通过比较阅读 smali 文件理解 MIUI 在 AOSP 的基础修改了什么逻辑
4. 用 BeyondCompare/Meld 工具去比较 dst_smali_orig 和 dst_smali_patched，找出冲突代码块的位置
5. 根据步骤 3 的逻辑修改，把这个修改合并进 dst_smali_patched 目录

这个过程刚做很痛苦，但有做几次积累一定经验后，就轻松了。过程中可能还要结合 AOSP 的 JAVA 源码阅读来理解逻辑。

目标 smali 代码合并进 dst_smali_patched 之后，还需要把这个结果合并回 patchrom/mtk6582 目录下的相应 smali 文件里。比如，需要把 patchrom/mtk6582/android.policy.jar.out 目录和 patchrom/mtk6582/temp/dst_smali_patched/android.policy.jar.out 目录相比较，把最终结果合并进 patchrom/mtk6582/android.policy.jar.out　里。因为 patchrom 编译工具在生成这些需要合并的文件时，把 smali 文件里的行号删除了。这样有利于自动合并和手动合并，而不会被行号干扰。而我们合并完真正进行编译时，实际上参加编译的是 patchrom/mtk6582/android.policy.jar.out 下的 smali 文件。所以必须合并回去才能真正把 MIUI 合并过去。

### make fullota

合并完成后，可以在 patchrom/mtk6582 目录下运行 `make fullota` 来生成目标文件 MIUI_MTK6582.zip。如果你人品足够好，那么可能一步就生成了。但基本上没有这么好的运气。过程中会有 smali 错误。需要根据提示去做适当的修改。编译通过后，就可以把 MIUI_MTK6582.zip 文件通过 recovery 方式升级到手机看移植后的效果。

## 结语

本文分析了使用 patchrom 移植 MIUI 的全过程，详细解释了 patchrom 编译系统及步骤。这个对理解 patchrom 移植的原理有比较大的帮助。移植过程中可能会碰到各种各样的问题。这些问题都需要一些丰富的知识去识别和解决。下一篇准备介绍一下移植过程中遇到的一些问题，解决方法以及找到解决方法的分析过程。

[1]: http://pan.baidu.com/s/1o6yq4I2
[2]: http://pallergabor.uw.hu/androidblog/dalvik_opcodes.html

