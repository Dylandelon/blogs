Title: Android数据同步和帐户管理
Date: 2014-11-28 22:00
Modified: 2014-11-28 23:20
Tags: android, SyncAdapter, AccountManager
Slug: android-syncadapter-accountmanager
Authors: Joey Huang
Summary: 本文分析平台自带的 SimpleSyncAdapter 来介绍 Android 平台数据同步相关的框架及帐户管理相关的话题。最后总结出实现一个自己的帐户以及在这个帐户下同步电话本数据所需要的技术和资源。
Status: draft

## 开篇

上一篇关于电话本的文章，我们总结了电话本数据库的关键数据结构。本篇文章重点介绍要实现一个电话本同步功能的步骤和方法。同步功能需要客户端和服务器，本文重点介绍客户端的实现机制和方法。

Contacts Provider 被设计成很容易处理在设备和服务器之间**同步**数据。可以让用户从服务器下载数据到一个新设备上，也可以让用户把设备上的数据上传到服务器上。同步机制保证了用户可以时刻在设备上拥有最新的数据，不管这些数据是修改的，添加的。

虽然有各种各样的方式来同步数据，但 Android 平台提供了一个同步框架让实现数据同步变得更加简单。这个框架会完成下面的事情：

* 检查网络是否可用
* 根据用户的偏好来调度并执行数据同步
* 重新执行意外停止的同步操作

要利用 Android 框架实现数据同步，你只需要提供一个**同步适配器**，每个同步适配器都唯一地对应一个特定的服务和内容，可以处理同一服务下的多个帐户的数据同步。框架也允许多个同步适配器对应一个服务和内容。

## 实现同步适配器

要给电话本实现一个同步适配器，你可以创建一个包含下面内容的应用程序：

* 实现一个同步适配器服务来响应系统的绑定同步适配器的请求
  当系统要执行数据同步时，它调用 Service 的 `onBind()` 方法来获取同步适配器的 `IBinder` 接口。这样系统就可以用 `IBinder` 接口进行跨进程调用同步适配器里定义的方法。在 SampleSyncAdapter 这个示例应用里，`com.example.android.samplesync.syncadapter.SyncService` 类实现了这个服务。
* 从 `AbstractThreadedSyncAdapter` 类继承来实现一个实际的同步适配器
  这个类完成真正从服务器下载数据的任务，从设备上传数据到服务器以及解决冲突等功能。这个类的关键方法是 `onPerformSync()` ，在这个方法里完成所有的工作。这个类必须被实现成**单例**。在 SampleSyncAdapter 这个示例应用里，`com.example.android.samplesync.syncadapter.SyncAdapter` 类就是实际的同步适配器。
* 实现 `Application` 子类
  这个类会作为同步适配器单例的工厂类，在其 `onCreate()` 方法里创建同步适配器单例，然后提供一个静态的 getter 方法来返回这个同步适配器单例。同步适配器服务里的 `onBind()` 方法会调用这个 getter 函数来获取同步适配器，并把这个适配器作为 `IBinder` 接口返回给系统。
* 实现一个用户鉴权服务来响应系统的鉴权请求（可选）
  `AccountManager` 会启动这个服务来完成鉴权。服务的 `onCreate()` 方法鉴权实例。当系统想为同步适配器的用户帐户进行鉴权时，系统会调用服务的 `onBind()` 方法来获取一个 `IBinder` 接口，这样系统就可以用 `IBinder` 接口进行跨进程调用来完成鉴权工作。在 SimpleSyncAdapter 示例代码里，实现这个功能的类是 `com.example.android.samplesync.authenticator.AuthenticationService`。
* 继承 `AbstractAccountAuthenticator` 来实现一个处理鉴权请求的类（可选）
  `AccountManager` 会调用这个类提供的接口以完成用户鉴权。完成鉴权的方法各异，取决于服务器使用的技术。在 SimpleSyncAdapter 示例代码里，这个类由 `com.example.android.samplesync.authenticator.Authenticator` 实现。
* 向系统注册同步适配器和帐户鉴权的 XML 文件
  前面描述的同步适配器和鉴权服务通过 `<service>` 标签在应用程序的 `AndroidManifest.xml` 里定义。在服务声明标签里，通过 `<meta-data>` 标签来给系统提供特殊的数据。在 SimpleSyncAdapter 示例代码里，包含两个 XML 文件：同步适配器描述文件 `res/xml/syncadapter.xml` ，这个文件描述了同步的服务器地址以和帐户类型。帐户鉴权描述文件 `res/xml/authenticator.xml` 。这个文件描述了这个帐户支持的鉴权帐户类型。以及在鉴权过程中会显示的 UI 资源。这里描述的帐户类型和同步适配器里描述的帐户类型必须相同。

!!! Note "关于帐户和同步适配器"
    一般情况下，一个帐户下会有多种同步服务，比如 GOOGLE 帐户可以支持电话本，日程表，书签，照片等同步服务。所以帐户一般不会和同步适配器放在同一个应用程序里，而是单独放在一个应用程序里，比如 GOOGLE 帐户就放在开机向导 SetupWizard 里，而同步适配器则是实现在相应的应用程序里。帐户和同步适配器的关联关系就是靠上文提到的 XML 里的帐户类型。当系统调用同步适配器来同步数据时，会在系统里找这个同步适配器帐户类型指定的帐户来进行鉴权。

## 用同步适配器打造电话本的社交数据

Contact Provider 使用 `ContactsContract.StreamItems` 和 `ContactsContract.StreamItemPhotos` 来管理来自社交网络的数据。你可以写一个同步适配器来从你的服务器上下载社交数据，并保存在这两个表里。你也可以从这两个表里读取数据，然后显示在你自己的应用程序里。使用这个机制，可以让你的社交网络服务和应用程序无缝地集成进 Android 系统里，跟原生电话本应用绑定起来。比如，可以在 Android 电话本里看到好友的微博信息以及头象等等。

### 社交文本信息流

信息流和 RawContact 里的某个记录是关联的，通过 `ContactsContract.StreamItems.RAW_CONTACT_ID` 来和 RawContact 表里的 _ID 值关联起来。RawContact 里的帐户类型和帐户名称也保存在 ` ContactsContract.StreamItems` 表里的记录里。下表是 StreamItems 表的一些关键字段。

字段名称            | 必填字段   | 说明
--------------------|------------|---------------
ACCOUNT_TYPE        | 是         | 信息流所属的帐户类型，与其关联的 RawContact 里的帐户类型一致
ACCOUNT_NAME        | 是         | 信息流所属的帐户名，与其关联的 RawContact 里帐户名一致
CONTACT_ID          | 是         | 作为外键与 Contacts 表里的 _ID 字段关联
CONTACT_LOOKUP_KEY  | 是         | 作为外键与 Contacts 表里的 LOOKUP_KEY 字段关联
RAW_CONTACT_ID      | 是         | 作为外键与 RawContacts 表里的 _ID 字段关联
COMMENTS            | 否         | 在信息流之前显示的一段可选的文本描述
TEXT                | 是         | 信息流的文本内容。内容可以是 HTML 格式的，系统通过 `fromHtml()` 函数来展示内容。系统还可能会对太长的内容进行裁剪，但会尽量避免破坏 HTML 的 TAB。
TIMESTAMP           | 是         | 信息更新的时间，用1970年1月1日开始的毫秒数表示。由同步适配器维护，Contact Provider 不会维护这个字段。相反，当超出空间限制后，系统会根据这个字段，挑出最早的信息流进行删除。

StreamItems 表还包含 SYNC1 - SYNC4 等字段来给同步适配器使用。

### 社交照片流

 Contact Provider 里的 `ContactsContract.StreamItemPhotos` 表用来保存与信息流相关联的照片信息。这个表的 STREAM_ITEM_ID 字段通过外键与 `ContactsContract.StreamItems` 表的 _ID 字段关联起来。这个表的关键字段如下：

字段名称            | 说明
--------------------|---------------
STREAM_ITEM_ID      | 通过外键与 StreamItems 关联，表示所尾的信息流
PHOTO               | 这个二进制 blob 字段由 Contact Provider 维护，用来保存图片的 thumbnail 信息。这个字段是为了向后兼容而存在的。
PHOTO_FILE_ID       | RawContacts 里照片的数字索引值。把这个值串在 `DisplayPhoto.CONTENT_URI` 后面，这样就得到了一个指向照片文件的 Uri，再调用 `openAssetFileDescriptor()` 来获取照片文件的句柄。
PHOTO_URI           | 直接指向照片文件的 Uri，可以直接调用 `openAssetFileDescriptor()` 来打开文件。

### 使用社交信息流表的限制

当使用 `ContactsContract.StreamItems` 和 `ContactsContract.StreamItemPhotos` 等社交信息表时，有一些额外的限制。

* 权限
  这些表需要额外的权限，要从这些表中读取内容，你的应用程序需要申请 `READ_SOCIAL_STREAM` 权限。要修改它们，需要 `WRITE_SOCIAL_STREAM` 权限。
* 容量限制
  对 `ContactsContract.StreamItems` 表的使用有容量限制，针对一个 RawContacts 记录，保存在这个表里的数据条数有限制。当达到条数限制后，Contact Provider 会根据 `TIMESTAMP` 字段的值把旧的数据删除掉，以便腾出空间给新插入的数据。要获取容量限制，可以用 `CONTENT_LIMIT_URI` 发起一个查询，查询的结果只会包含一条记录，从 `StreamItem.MAX_ITEMS` 这个字段里可以读到条数限制。

### 社交信息流的交互

由 Contact Provider 管理起来的社交信息流结合系统原生的电话本应用，可以让你的社交数据与设备的联系人产生很强的关联关系。通过同步适配器让你的社交数据和 Contact Provider 结合可以提供以下的附加功能：

* 可以把用户联系人的动态信息保存在 `ContactsContract.StreamItems` 和 `ContactsContract.StreamItemPhotos` 表里以便后续需要时使用。
* 除了普通的同步功能之外，当用户查看某个联系人时，可以触发同步适配器去获取关于这个联系人的额外数据，这样就可以在用户查看联系人时，可以看到联系人的高清照片以及最近的动态信息流。
* 通过 Contact Provider 向设备的联系人应用程序注册一个通知，这样当用户打开联系人查看时，可以收到和个 Intent ，这时你可以通过同步适配器去获取用户的状态信息（是否在线等）然后显示出来。这种策略比全部同步一遍要更省带宽和时间。
* 用户在查看联系人信息时，可以邀请联系人加入你的社交网络。要实现这个功能，需要启用邀请联系人的机制，你需要实现一个 Activity 来处理现有的联系人加入社交网络的功能。然后把这个 Activity 通过 XML 的方式告诉设备的联系人应用程序。

### 查看联系人事件及社交信息流查看

为了当用户打开一个联系人查看时同步适配器能收到通知，需要通过下面的步骤来完成一些配置：



