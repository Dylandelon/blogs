Title: Android电话本核心数据结构
Date: 2014-11-27 22:00
Modified: 2014-11-27 23:20
Tags: android, contacts, contacts provider
Slug: android-contacts-provider
Authors: Joey Huang
Summary: 本文描述Contacts Provider的数据库结构；电话本数据的访问和修改以及电话本数据的元数据架构。阅读本文可对电话本数据结构有全貌的了解。如果你正在开发维护Contacts模块，本文是必读资料。它将帮助你理解Contacts模块的所有的数据相关的操作。

[TOC]

## 简介

Contact Provider是Android系统提供的一个功能强大且灵活的系统组件，用来管理系统里的所有联系人数据。我们在Android手机是看到的联系人信息的数据来源就是由Contact Provider提供的，我们也可以自己写程序来访问这些联系人数据，也可以把这些数据和我们自己的网络服务进行同步和备份。由于Contact Provider管理了相当多类型的数据源，对一个联系人又同时管理着非常多的信息，结果就导致Contact Provider组织结构异常复杂。本文包含以下内容来介绍Contact Provider：

* Contact Provider的基础数据结构
* 怎么样从Contact Provider里获取联系人数据
* 怎么样修改Contact Provider里的联系人数据
* 怎么样写一个同步适配器(sync adapter)来实现联系人数据的同步

本文假设你已经了解了Android的content provider机制。Android自带的一个示例程序SampleSyncAdapter很好地演示了如何写一个同步适配器，来把联系人数据同步到部署在Google Web Service上网络服务上。

## Contact Provider结构

Contact Provider是Android里的一个content provider组件。针对一个联系人，它维护三种类型的数据，分别用三个表来维护这些数据。三个表都定义在类`ContactsContract`里，它定义了每个表的content URL，列名称等常量。

* ContactsContract.Contacts
  这个表的每一行表示一个联系人，它是由`RawContacts`表里的数据聚合而来的。
* ContactsContract.RawContacts
  针对不同的帐户，这个表的第一行包含了一个联系人的概要信息。
* ContactsContract.Data
  这个表保存真正的联系人数据，比如电子邮件，电话号码等。

定义在`ContactsContract`里的其他表，用来辅助实现Contact Provider的其他功能。三个核心的表Contacts, RawContacts, Data的相互关系如下图所示：

![contacts_structure](https://raw.githubusercontent.com/kamidox/blogs/master/images/contacts_structure.png)

### RawContacts表

一个raw contacts表示一个来自特定帐户类型和名称的联系人数据。因为Contact Provider允许多个在线服务作为数据的来源，所以Contact Provider允许多个raw contacts来对应同一个联系人。用户也可以从多个帐户中合并多个raw contacts来生成一个联系人数据。

raw contact的大部分数据不保存在`RawContacts`表里，而是通过一行或多行数据保存在`ContactsContract.Data`表里。`Data`表里的每行数据都有一个`Data.RAW_CONTACT_ID`，它与表`RawContacts`的` RawContacts._ID`是对应的。即表`Data`里所有满足`Data.RAW_CONTACT_ID == RawContacts._ID`的记录，都属于表`RawContacts`里由`RawContacts._ID`指定的这条记录的数据。

#### raw contact的重要字段

下表是raw contact的表的一些重要字段。

字段名称      | 用途           | 备注
--------------|----------------|------------
ACCOUNT_NAME  | raw contact的数据来源的帐户名称。比如对Google帐户而言，这个字段的值就是用户的Gmail地址。 | 这个字段的数据格式是由帐户类型决定的，不一定要电子邮件地址。只要服务提供方能保证帐户名的唯一性即可。
ACCOUNT_TYPE  | raw contact的数据来源的帐户类型。比如Google帐户的帐户类型是**com.google**，这个值由一般由帐户提供方的域名来保证唯一性，不和别的帐户冲突。 | 一个帐户类型一般会和一个同步适配器关联起来，来提供数据同步服务。
DELETED       | 删除标志位 | Contact Provider使用这个标志位来管理用户删除，但还没同步到服务器上的记录。当同步适配器开始同步，从服务器上删除了这个记录之后，这条记录才在本地删除。

#### 注意事项

下面是关于`RawContacts`表的重要的注意事项：

* 联系人名称并不保存在`ContactsContract.RawContacts`表里，而是保存在`ContactsContract.Data`表里。它的数据类型是`ContactsContract.CommonDataKinds.StructuredName`。而且每个联系人在Data表里只有一行表示联系人名字的数据。
* 要在raw contact表里保存属于指定帐户数据，必须先通过`AccountManager`注册帐户。可以通过提示用户添加帐户类型和帐户名称到系统里来实现注册帐户的目的。如果你不这样做，Contact Provider会自动删除raw contact表里属于这个帐户的数据。
  例如，如果你需要你的应用程序维护来自你的网络服务`"com.example.dataservice"`的联系人数据，帐户的用户名是`"user@dataservice.example.com"`。用户必须先在手机里新建一个帐户，其帐户类型是`"com.example.dataservice"`，帐户名是`"user@dataservice.example.com"`。添加帐户成功后，你的应用程序才能添加属于这个帐户的联系人数据到raw contact表里。

#### 一个例子

为了更好的理解raw contact的机制，我们假设有个用户叫"Emily Dickinson"，她在设备里添加了下面三个帐户：

* `emily.dickinson@gmail.com`
* `emilyd@gmail.com`
* `Twitter account "belle_of_amherst"`

并且都启用了自动同步功能。

假设Emily在电脑上打开浏览器，用`emily.dickinson@gmail.com`登录Gmail，打开通讯录，添加了"Thomas Higginson"。过了一会儿，她又用`emilyd@gmail.com`登录Gmail，然后向"Thomas Higginson"发了封电子邮件，这个操作会自动把"Thomas Higginson"添加进联系人里。她也在Twitter上关注了"colonel_tom" (Thomas Higginson's Twitter ID) 。

上面的操作，会导致Contacts Provider创建了三个raw contacts:

* 第一个是和`emily.dickinson@gmail.com`帐户关联的叫"Thomas Higginson"的联系人。这个联系人所属的帐户类型是Google。
* 第二个是和`emilyd@gmail.com`帐户关联的叫"Thomas Higginson"的raw contact。这个联系人的帐户类型也是Google。虽然第二个联系人和第一个的名字一样，但它属于另外一个帐户名下的联系人。
* 第三个是和Twitter帐户"belle_of_amherst"关联的叫"Thomas Higginson"的联系人。它的帐户类型是Twitter.

### Data表

前面提过，Data表是用来保存联系人数据的，通过`Data.RAW_CONTACT_ID`和raw contact里的`RawContacts._ID`关联起来。这样就允许一个raw contact可以有多个相同类型的数据保存在Data表里，比如一个联系人可以有多个电子邮件地址，多个电话号码等。例如，属于`emilyd@gmail.com`帐户的联系人"Thomas Higginson"有一个家庭电子邮件`thigg@gmail.com`以及一个工作电子邮件`thomas.higginson@gmail.com`，Contact Provider保存这两个电子邮件地址在Data表里，并通过`Data.RAW_CONTACT_ID`和`RawContacts`表里的数据关联。

需要注意，不同类型的数据全部保存在`Data`表里。联系人名字，邮件地址，电话号码，照片，网址等等，全部是保存在`Data`表里的。为了实现这样的目的，Data表里包含一些描述性的字段来描述数据。还包含了一些真正的用来保存数据的字段。

#### 描述性字段

* RAW_CONTACT_ID
  用来和`RawContacts._ID`字段进行关联，以表示行数据是属于哪个raw contact的。
* MIMETYPE
  数据类型，Contact Provider使用定义`ContactsContract.CommonDataKinds`里的子类来区别不同的数据类型。
* IS_PRIMARY
  如果一个数据类型可以出现多次，则这个字段用来标示出这种数据类型的主数据。比如一个联系人有多个电话号码，则其中一个的IS_PRIMARY可以设置为非零值，则这个号码就是主电话号码。有些应用程序可以利用这一特性地优先选择主电话号码来拨号等。

#### 通用数据字段

一个Data表里的记录，总共有15个通用数据字段，从DATA1到DATA15。同时还有4个只能给同步适配器使用的字段SYNC1到SYNC4。

DATA1字段会被索引起来，Contact Provider默认问题认为这个字段保存的是最经常被访问的数据，比如对Email数据而言，这个字段保存的就是Email地址。

通常情况下，DATA15被用来保存二进制数据(BLOB)，比如照片的二进制数据等。

#### 类型相关的字段

DATA表里的每一行保存一种类型的数据，为了方便地访问不同类型的数据，Contact Provider也提供了访问具体类型数据的字段的方法，这些类型相关的字段别名由定义在`ContactsContract.CommonDataKinds`里的子类来定义。

例如，`ContactsContract.CommonDataKinds.Email`类定义了MIME Type为`Email.CONTENT_ITEM_TYPE`的数据，要访问Email地址时，可以直接访问`Email.ADDRESS`，它的值其实就是"data1"，就是通用数据字段的DATA1字段。

!!! CAUTION "警告"
    当向`ContactsContract.Data`表中添加自定义数据时，不要使用`ContactsContract.CommonDataKinds`里预定义的MIME类型。否则你可以丢失数据或引起Contact Provider不能正常工作。例如，你**不能**向Data表里添加一行数据，然后其MIME type定义为`Email.CONTENT_ITEM_TYPE`，其值保存在字段DATA1上，且其值是用户名而不是Email地址。

下图就是类型相关字段别名和通用数据字段的关联关系图：

![data_columns](https://raw.githubusercontent.com/kamidox/blogs/master/images/data_columns.png)

#### 类型相关的字段名类

下表列出了最常用的类型相关的别名字段类

别名类名称                                      | 数据类型      | 备注
------------------------------------------------|---------------|-----------------------
ContactsContract.CommonDataKinds.StructuredName | 名字          | 只能有一个名字
ContactsContract.CommonDataKinds.Photo          | 照片          | 只能有一个照片
ContactsContract.CommonDataKinds.Email          | 电子邮件      | 可以有多个电子邮件地址
ContactsContract.CommonDataKinds.GroupMembership| 联系人所在的组| 联系人的组是可选项

### Contacts表

Contact Provider会从RawContacts和Data表里收集数据，组合生成一个记录放在Contacts表里。Contact Provider负责在这个表里生成记录，合并数据。应用程序和同步适配器都不能向这个表里添加记录，Contacts表里的一些字段还是只读的。

!!! Hint "注意"
    如果你试图通过ContentResolve的insert()方法向Contacts表里添加记录，会得到一个`UnsupportedOperationException`的错误。如果试图修改只读的字段，也会被忽略。

Contact Provider会根据raw contact自动向Contacts表里添加一条记录。如果raw contact数据改变，导致Contacts表里原先和raw contact关联记录不复存在了，那么Contact Provider也会自动向Contacts里自动添加一条记录。如果应用程序或同步适配器添加了一条raw contact记录，且这条记录与Contacts表里的某条记录是一样的，那么Contact Provider会负责把这条新增加的记录和原来那条记录合并。

Contact Provider通过`Contacts._ID`和`RawContacts.CONTACT_ID`把Contacts表和RawContacts表的数据关联起来。即一个Contacts表里的记录可以与多个RawContacts表里的记录对应。给定`Contacts._ID`的值，所有`RawContacts.CONTACT_ID`为这个值的记录都与Contacts里的这条记录关联。

`ContactsContract.Contacts`表还包含了一个`LOOKUP_KEY`字段，这个字段永久地和某个特定的联系人关联起来。这个字段存在的意义在于，Contacts表是由Contacts Provider自动维护的，当发生数据合并或同步适配器修改raw contacts时，Contacts._ID的值是会发生变化的。而`Contacts.LOOKUP_KEY`在这个过程中，是不会发生变化的。`Contacts.CONTENT_LOOKUP_URI`和`LOOKUP_KEY`字段组合起来所代表的联系人依然指向了原来的联系人。所以，我们可以用`LOOKUP_KEY`来连接一个我们感兴趣的联系人。

下图阐明了三个主要的表之间的关系：

![contacts_tables](https://raw.githubusercontent.com/kamidox/blogs/master/images/contacts_tables.png)

### 从同步适配器来的数据

用户可以在设备里直接输入联系人数据，联系人数据也可以通过同步适配器自动地在设备和云端进行同步。同步适配器在系统后台运行，由系统控制，通过ContentResolver来管理数据。

在Android系统上，同步适配器的云端服务是由帐户类型来区分的。一个同步适配器对应一个帐户类型。但同步适配器可以支持同一个帐户类型下的多个帐户名，就象可以在设备上登录多个Google帐户一样。下面的文字描述了帐户类型和帐户名称与同步适配器的关系。

* 帐户类型
  唯一地标识了用户存储数据的云端服务。大多数时候，用户必须通过云端服务鉴权才能使用服务。例如，Google联系人就是一个值为"com.google"的帐户类型。这个值与AccountManager类里的帐户类型的值是一样的。
* 帐户名称
  唯一地标识了某个帐户类型的一个特定的帐户。Google联系人帐户和Google帐户是相同的，它们都用Gmail地址作为帐户名称。其他的云端服务可能使用一个字符串或一个数字来表示帐户名称，但必须注意的是，云端服务必须保证在同一个帐户类型里，帐户名称可以唯一地区分一个帐户。

帐户类型可以不唯一，即一个设备里可以有多个相同帐户类型的帐户。比如，设备可以登录多个Google帐户。帐户名称一般是唯一的，至少在同一个帐户类型里必须是唯一的。帐户类型和帐户名称结合起来，通过同步适配器，共同标识了一个在Contact Provider和云端服务之间的一个特定同步数据流。

如果你想在你的云端服务和Contact Provider之间同步数据，你必须实现一个同步适配器。后面章节的文章会提到这个话题。

### 需要的权限

需要访问Contact Provider的应用程序必须取得下面的权限：

* 读权限
  需要在应用程序的AndroidManifest.xml里，添加`<uses-permission android:name="android.permission.READ_CONTACTS">`
* 写权限
  需要在应用程序的AndroidManifest.xml里，添加`<uses-permission android:name="android.permission.WRITE_CONTACTS">`

这两个权限不包含User Profile数据的读写。user profile使用单独的权限来控制读写。

### User Profile

User Profile就是在设备联系人应用程序里看到的"我的个人资料"，用来描述本设备所有人信息的一个数据。`ContactsContract.Contacts`表里有一行数据用来表现user profile。这个数据用来描述设备所有人本身，而不是设备所有人的联系人。

读写user profile除了读写联系人数据外，还需要额外的权限，他们是"android.permission.READ_PROFILE"和"android.permission.WRITE_PROFILE"。这两个都是在API 14的时候才加进去的。

要获取user profile，可以使用ContentResolver通过`ContactsContract.Profile.CONTENT_URI`来获取，下面是获取user profile的示例代码：

    :::java
    // Sets the columns to retrieve for the user profile
    mProjection = new String[]
        {
            Profile._ID,
            Profile.DISPLAY_NAME_PRIMARY,
            Profile.LOOKUP_KEY,
            Profile.PHOTO_THUMBNAIL_URI
        };

    // Retrieves the profile from the Contacts Provider
    mProfileCursor = getContentResolver().query(
                    Profile.CONTENT_URI,
                    mProjection ,
                    null,
                    null,
                    null);

### Contacts Provider元数据

Contacts Provider管理了本地的所有联系人数据，追踪他们的状态。这些元数据就是为了实现这些功能所需要的。这些元数据保存在RawContacts，Contacts, Data等表格记录里，同时还保存在`ContactsContract.Settings`和`ContactsContract.SyncState`表里。下面汇总了这些元数据的位置及其作用。

表名称                       | 字段名称     | 字段值              | 含义
-----------------------------|--------------|---------------------|----------------
ContactsContract.RawContacts | DIRTY        | 0: 数据没变化；1: 上次同步以来数据变化了 | 这个数据由Contact Provider维护。当用户修改记录时，这个值自动变为1；而当同步适配器修改记录时，在其修改数据的URI上，会带上`CALLER_IS_SYNCADAPTER`参数，以表示是同步适配器修改的，不需要标记为脏数据。
ContactsContract.RawContacts | VERSION      | 数据的版本          | 当RawContacts表里的记录数据改变时，Contacts Provider自动增加这个值。
ContactsContract.Data        | DATA_VERSION | 数据的版本          | 当Data表里的记录数据改变时，Contacts Provider自动增加这个值。
ContactsContract.RawContacts | SOURCE_ID    | 字符串，用来唯一标识这个记录来自哪个帐户的。 | 当同步适配器添加记录时，这个字段必须设置为服务器端针对这个记录的唯一标识。当设备端用户添加记录时，这个字段为空，这样就告诉同步适配器这个字段是用户新增的，必须在服务器端新建一条记录，并用这条记录的SOURCE_ID值来更新用户添加的这条记录。特别地，这个字段必须在一个帐户里保持全局唯一性，且必须在同步过程中保持不变。即同步前后，这个字段需要标识出相同的记录。
ContactsContract.Groups      | GROUP_VISIBLE | 0: 属于这个值的记录在应用程序里不可见；1: 这个组的联系人可见 | 这个字段可以让服务端设置组的可见性。
ContactsContract.Settings    | UNGROUPED_VISIBLE | 0: 未分组的联系人不可见；1: 未分组的联系人可见 | 默认情况下，未分组的联系人是不可见的。通过修改`ContactsContract.Settings`表里的这个字段，可以设置应用程序显示未分组的联系人。
ContactsContract.SyncState   | 所有字段     | 使用这个表来保存同步适配器的元数据 | 用这个表格来保存同步后的状态信息以及所有和同步相关的数据，比如时间戳等。

## 读写Contacts Provider

本节内容描述如何访问Contacts Provider的数据，主要集中在下面几个话题：

* 联系人记录查询
* 分批修改数据
* 通过Intent来获取或修改记录
* 数据完整性检查

通过同步适配器修改联系人数据将在下面的章节中单独描述。

### 查询记录

因为Contacts Provider数据是按照三个核心表(Contacts, RawContacts, Data)按照层次结构组织起来的，应用程序经常需要获取一个联系人的所有信息，这就需要从这三个表里里去联合查询。比如从Contacts表里找到一个记录，然后根据Contacts._ID从RawContacts表里关联RawContacts.CONTACT_ID去查询与这个Contacts记录关联的RawContacts记录。接着，再根据找到的关联的RawContacts记录的RawContacts._ID的值从Data表里，根据Data.RAW_CONTACTS_ID去查询所有的关联记录。再把这些记录组合起来，最后得到了一个完整的联系人信息。为了达成这个目的，Contact Provider提供了*ContactsContract.Contacts.Entity*类来实现这个功能，自动实现了这些表的联合查询。

一个entity表是从Contacts, RawContacts, Data三个表里把关联的记录合并起来，从中选择一些列来组合起来的。当从entity表里查询数据时，需要提供一个感兴趣的字段列表(projection)，查询结果是一个游标(cursor)，里面包含一个个联系人的所有信息数据。例如，指定一个联系人的名字，查询出这个联系人的所有电子邮件，那么你将得到包含一行数据的游标，这行数据里有名字以及多个电子邮件的数据。

entity表让查询操作更简单。你可以一次从不同的表里获取出联系人的所有信息。而不需要先从父表里查询数据，得到ID，再根据ID去子表里查询。而且，Contacts Provider把这些联合查询操作在一个事务里完成，这样保证了查询到的数据的一致性。

!!! Note "注意"
    一个entity一般没有包含Contacts表及其子表的所有字段，如果试图访问这些不在entity表里的字段，会有异常抛出。

下面的代码演示了如何从entity里获取记录数据。一个联系人应用程序一般有个列表显示联系人，点击后显示这个记录的详细信息，下面的代码是显示详细信息的一部分代码。即根据联系人的ID去获取所有的联系人信息。

    :::java
        /*
         * Appends the entity path to the URI. In the case of the Contacts Provider, the
         * expected URI is content://com.google.contacts/#/entity (# is the ID value).
         */
        mContactUri = Uri.withAppendedPath(
                mContactUri,
                ContactsContract.Contacts.Entity.CONTENT_DIRECTORY);

        // Initializes the loader identified by LOADER_ID.
        getLoaderManager().initLoader(
                LOADER_ID,  // The identifier of the loader to initialize
                null,       // Arguments for the loader (in this case, none)
                this);      // The context of the activity

        // Creates a new cursor adapter to attach to the list view
        mCursorAdapter = new SimpleCursorAdapter(
                this,                        // the context of the activity
                R.layout.detail_list_item,   // the view item containing the detail widgets
                mCursor,                     // the backing cursor
                mFromColumns,                // the columns in the cursor that provide the data
                mToViews,                    // the views in the view item that display the data
                0);                          // flags

        // Sets the ListView's backing adapter.
        mRawContactList.setAdapter(mCursorAdapter);
        ...
    @Override
    public Loader<Cursor> onCreateLoader(int id, Bundle args) {

        /*
         * Sets the columns to retrieve.
         * RAW_CONTACT_ID is included to identify the raw contact associated with the data row.
         * DATA1 contains the first column in the data row (usually the most important one).
         * MIMETYPE indicates the type of data in the data row.
         */
        String[] projection =
            {
                ContactsContract.Contacts.Entity.RAW_CONTACT_ID,
                ContactsContract.Contacts.Entity.DATA1,
                ContactsContract.Contacts.Entity.MIMETYPE
            };

        /*
         * Sorts the retrieved cursor by raw contact id, to keep all data rows for a single raw
         * contact collated together.
         */
        String sortOrder =
                ContactsContract.Contacts.Entity.RAW_CONTACT_ID +
                " ASC";

        /*
         * Returns a new CursorLoader. The arguments are similar to
         * ContentResolver.query(), except for the Context argument, which supplies the location of
         * the ContentResolver to use.
         */
        return new CursorLoader(
                getApplicationContext(),  // The activity's context
                mContactUri,              // The entity content URI for a single contact
                projection,               // The columns to retrieve
                null,                     // Retrieve all the raw contacts and their data rows.
                null,                     //
                sortOrder);               // Sort by the raw contact ID.
    }

当数据加载结束，LoaderManager 会调用 Activity 的 onLoadFinish() 回调函数。这个回调函数的参数之一是 Cursor 对象，它包含了查询的结果集。应用程序可以从 Cursor 对象里获取数据并显示出来。

### 批量操作

在操作电话数据的增加，删除，修改时，尽量使用批量操作，通过创建一个 ArrayList 列表，列表里放 ContactProviderOperation 类的实例，最后再调用 ContentResolver.applyPatch() 方法来执行批量操作。Contact Provider 将把一次 applyPatch() 里的所有操作当成一个事务来执行，这样你的修改就不会造成数据不一致性。新建一个电话本记录时，批量操作也会把插入 RawContact 表里的数据和插入 Data 表里的数据放在一个事务里执行，确保数据的一致性。

#### 释放点

当指操作包含大量的操作时，执行起来虽然不会阻塞 UI 纯种，但系统整体很繁忙，会阻塞其它的进程。这样就会导致用户体验下降。一个解决方法是把所有操作通过合理的安排，放进几个独立的 ArrayList 对象里，同时为了不阻塞其他进程，可以在操作之间放一个**释放点**，释放点也是一个 ContentProviderOperation 实例，它的 isyieldAllowed() 会返回 true 。当 Contact Provider 执行这些操作时，遇到释放点后，它会停止事务，暂停操作，以便让其他程序运行。等到 Contact Provider 再次运行时，它将创建新的事务从上次暂停的地方继续执行操作。

释放点会导致在一批操作被分隔成多个事务。正因为如此，你需要把释放点放在一批相关数据操作的结尾处。比如，你需要把释放点放在添加 RawContact 记录和添加相应的 Data 记录之后。以确保释放点之间的操作的数据一致性。

释放点之间也是一个原子操作单元。所有在释放点之间的操作要么全部成功要么全部失败。如果没有设置释放点，那么整个批量操作都将作为一个原子操作，要么全部成功要么全部失败。使用释放点可以避免让系统性能受到挑战，同时又兼顾了数据操作的原子性。

#### 反向引用

当你把向 RawContact 里插入一条记录，以及把其相应的数据插入到 Data 表里作为一个批量操作时，你需要把 Data 表里的 RAW_CONTACT_ID 的值填成 RawContact 表里新插入的记录的 ID 值。而由于你还没有让 Contact Provider 去执行这个批量操作，即记录还没有在 RawContact 里生成，它的 ID 值是不可用的。为了解决这个问题， ContentProviderOperation.Builder 类提供了 withValueBackReference() 方法，用来让前一个操作的返回值作为当前操作的某个字段的值。

withValueBackReference() 方法有两个参数：

* key
  键值对里的键值，它的值必须是要引用前一个操作返回值作为当前字段值的字段名称
* previousResult
  applyPatch() 函数返回的 ContentProviderResult 实例数组的索引值，这个索引值从0开始计数。当一个批量操作被 applyPatch() 执行时，每个操作都会有个返回值，其值是一个 ContentProviderResult 实例，通过数组组织起来返回。previousResult 是这个返回数组的索引值，用这个索引值获取到 ContentProviderResult，并把结果保存在由 key 指定的当前操作的字段上。这样就允许我们在插入 Data 表时，把其 RAW_CONTACT_ID 的值作为反向引用，引用之前的插入 RawContact 操作的返回值上。appyPatch() 调用时，其结果数组一次性被创建，数组的大小就是操作的个数。结果数组的值全部被设置为 null。所以，当反向引用一个还未执行的操作的结果上时， withValueBackReference() 会抛出一个异常。

下面的代码演示如何向 raw contact 和 data 表里利用反向引用批量地插入数据。这个代码在 ContactManager 例子里。

    #!java
    /**
     * Creates a contact entry from the current UI values in the account named by mSelectedAccount.
     */
    protected void createContactEntry() {
        // Get values from UI
        String name = mContactNameEditText.getText().toString();
        String phone = mContactPhoneEditText.getText().toString();
        String email = mContactEmailEditText.getText().toString();
        int phoneType = mContactPhoneTypes.get(
                mContactPhoneTypeSpinner.getSelectedItemPosition());
        int emailType = mContactEmailTypes.get(
                mContactEmailTypeSpinner.getSelectedItemPosition());;

        // Prepare contact creation request
        //
        // Note: We use RawContacts because this data must be associated with a particular account.
        //       The system will aggregate this with any other data for this contact and create a
        //       coresponding entry in the ContactsContract.Contacts provider for us.
        ArrayList<ContentProviderOperation> ops = new ArrayList<ContentProviderOperation>();
        ops.add(ContentProviderOperation.newInsert(ContactsContract.RawContacts.CONTENT_URI)
                .withValue(ContactsContract.RawContacts.ACCOUNT_TYPE, mSelectedAccount.getType())
                .withValue(ContactsContract.RawContacts.ACCOUNT_NAME, mSelectedAccount.getName())
                .build());
        ops.add(ContentProviderOperation.newInsert(ContactsContract.Data.CONTENT_URI)
                .withValueBackReference(ContactsContract.Data.RAW_CONTACT_ID, 0)
                .withValue(ContactsContract.Data.MIMETYPE,
                        ContactsContract.CommonDataKinds.StructuredName.CONTENT_ITEM_TYPE)
                .withValue(ContactsContract.CommonDataKinds.StructuredName.DISPLAY_NAME, name)
                .build());
        ops.add(ContentProviderOperation.newInsert(ContactsContract.Data.CONTENT_URI)
                .withValueBackReference(ContactsContract.Data.RAW_CONTACT_ID, 0)
                .withValue(ContactsContract.Data.MIMETYPE,
                        ContactsContract.CommonDataKinds.Phone.CONTENT_ITEM_TYPE)
                .withValue(ContactsContract.CommonDataKinds.Phone.NUMBER, phone)
                .withValue(ContactsContract.CommonDataKinds.Phone.TYPE, phoneType)
                .build());
        ops.add(ContentProviderOperation.newInsert(ContactsContract.Data.CONTENT_URI)
                .withValueBackReference(ContactsContract.Data.RAW_CONTACT_ID, 0)
                .withValue(ContactsContract.Data.MIMETYPE,
                        ContactsContract.CommonDataKinds.Email.CONTENT_ITEM_TYPE)
                .withValue(ContactsContract.CommonDataKinds.Email.DATA, email)
                .withValue(ContactsContract.CommonDataKinds.Email.TYPE, emailType)
                .build());

        /*
         * Demonstrates a yield point. At the end of this insert, the batch operation's thread
         * will yield priority to other threads. Use after every set of operations that affect a
         * single contact, to avoid degrading performance.
         */
        op.withYieldAllowed(true);

        // Ask the Contact provider to create a new contact
        Log.i(TAG,"Selected account: " + mSelectedAccount.getName() + " (" +
                mSelectedAccount.getType() + ")");
        Log.i(TAG,"Creating contact: " + name);
        try {
            getContentResolver().applyBatch(ContactsContract.AUTHORITY, ops);
        } catch (Exception e) {
            // Display warning
            Context ctx = getApplicationContext();
            CharSequence txt = getString(R.string.contactCreationFailure);
            int duration = Toast.LENGTH_SHORT;
            Toast toast = Toast.makeText(ctx, txt, duration);
            toast.show();

            // Log exception
            Log.e(TAG, "Exceptoin encoutered while inserting contact: " + e);
        }
    }

* LINE 6 - 12 从编辑框里获取名字，电话，邮件以及电话类型和邮件类型。
* LINE 19 - 23 构建一个操作，这个操作向 RawContact 插入一条记录。然后将这个操作放在批量操作列表里。记住，这个操作的索引值是 0 。
* LINE 24 - 43 构建三个操作，分别向 Data 表里插入名字，电话和邮件。在这三个操作时，每个操作对 RAW_CONTACT_ID 的处理都使用了反向引用的原理，引用索引值为 0，即插入 RawContact 这个操作的返回值作为 Data 表里 RAW_CONTACT_ID 的值。
* LINE 50 插入一个释放点。当 Contact Provider 执行到这里时可以把CPU释放出来给别的进程执行。
* LINE 57 把这个批量操作列表提交给 Contact Provider 作为一个事务来执行。

批量操作也可以用来**优化并发控制**，它让一个事务执行时不用对数据库加锁。要使用这个方法，你可以执行这个事务，然后检查其它的修改是否同时发生了。如果发现数据不一致，则回滚整个事务，然后重试。

优化并发控制对手机设备特别有用，因为手机设备大部分情况下只有一个用户在使用，同时并发操作数据库的情景比较少。因为没有用锁来控制数据操作，所以不需要花时间来请求锁和释放锁，这样整个系统性能会比较好。要使用**优化并发控制**来修改一行 RawContact 的数据，可以用下面的步骤来进行：

1. 获取 RawContact 的数据时，把 VERSION 字段也一并获取出来
2. 使用 newAssertQuery(Uri) 静态方法来创建 ContentProviderOperation.Builder 实例，其 Uri 参数使用 RawContacts.CONTENT_URI 加 RawContact._ID组合起来。
3. 对创建出来的 ContentProviderOperation.Builder 实例，使用 withValue() 来和步骤 1 获取出来的 VERSION 字段值进行比较。
4. 对同一个 ContentProviderOperation.Builder 实例，使用 withExpectedCount() 来保证获得出来的记录有且只有一条。
5. 调用 build() 方法来创建 ContentProviderOperation 实例，并把它添加到批量操作列表的第一项。
6. 调用 applyPatch() 来执行这个事务。

如果一个潜在的修改在你获取数据和修改数据之间发生，那么 VERSION 值将会自动递增，这样步骤 4 的断言动作就会失败，从而整个事务都会回退。这样你可以选择重试或其它操作，总之数据会保持一致。下面的代码演示如何使用 CursorLoader 来创建包含**断言**的 ContentProviderOperation 实例。

    #!java
    /*
     * The application uses CursorLoader to query the raw contacts table. The system calls this method
     * when the load is finished.
     */
    public void onLoadFinished(Loader<Cursor> loader, Cursor cursor) {

        // Gets the raw contact's _ID and VERSION values
        mRawContactID = cursor.getLong(cursor.getColumnIndex(BaseColumns._ID));
        mVersion = cursor.getInt(cursor.getColumnIndex(SyncColumns.VERSION));
    }

    ...

        // Sets up a Uri for the assert operation
        Uri rawContactUri = ContentUris.withAppendedId(RawContacts.CONTENT_URI, mRawContactID);

        // Creates a builder for the assert operation
        ContentProviderOperation.Builder assertOp = ContentProviderOperation.netAssertQuery(rawContactUri);

        // Adds the assertions to the assert operation: checks the version and count of rows tested
        assertOp.withValue(SyncColumns.VERSION, mVersion);
        assertOp.withExpectedCount(1);

        // Creates an ArrayList to hold the ContentProviderOperation objects
        ArrayList ops = new ArrayList<ContentProviderOperationg>;

        ops.add(assertOp.build());

        // You would add the rest of your batch operations to "ops" here

        ...

        // Applies the batch. If the assert fails, an Exception is thrown
        try
            {
                ContentProviderResult[] results =
                        getContentResolver().applyBatch(AUTHORITY, ops);

            } catch (OperationApplicationException e) {

                // Actions you want to take if the assert operation fails go here
            }

## 结语

联系人的数据结构特别复杂。把握住了本文介绍的这几个核心数据结构及操作。基本上原电话本就会有一个全面的了解。下一篇关于电话本的文章，我们将结合 Android 的示例程序 SampleSyncAdapter 来介绍如何做一个电话本同步服务器以及如何在手机端添加一个同步适配器来同步自己的电话本数据。

