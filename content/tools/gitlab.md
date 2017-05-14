Title: 基于 Gitlab 的源代码管理及开发模型
Date: 2017-05-14 20:20
Modified: 2017-05-14 20:20
Tags: tools
Slug: gitlab
Authors: Joey Huang
Summary: 团队准备从 SVN 切换到自建的 Git 开发模型，选择了 Gitlab CE 版本作为源码管理平台。本文描述的开发模型适用于嵌入式开发领域，这与 Web 相关产品开发模型有较大差别。

[Gitlab CE](https://about.gitlab.com/products/) 是一个开源的基于 Git 的源代码管理软件，本文介绍基于 Gitlab 的源代码管理规范及典型工作流程。关于 Gitlab 的安装，可参阅[官方文档](https://about.gitlab.com/installation/)。Gitlab 是一个非常强大的系统，基本上可以搭建一个类似 Github 这样的私有网站了。本文描述的，只是针对嵌入式开发领域，进行项目管理，权限管理，代码评审，产品分支管理等有限领域的一些实践规则。

## 1 用户管理

Gitlab 安装完成后，会自动创建一个 root 帐户，这个帐户是系统管理员。系统管理员有最高的系统权限，可以查看所有的项目，并给适当的项目分配权限。当系统管理员第一次登录时，系统会强制要求修改密码。

用户可以自己注册，也可以由系统管理员创建用户。这里推荐由系统管理员创建用户，并设置初始密码，然后告诉用户。用户第一次登录时，系统要求修改密码。推荐用户登录后，修改个人头像，并使用真实头像，这样后续查看修改记录时可以一眼看出哪个人修改了什么内容。

![创建用户](https://raw.githubusercontent.com/kamidox/blogs/master/https://raw.githubusercontent.com/kamidox/blogs/master/images/git_create_user.png)

操作演练（建议实际安装完成后，演练一遍下面的任务）：

1. 在 Gitlab 系统上创建四个用户，分别是 user1, user2, user3, user4
2. 使用 user1 登录系统

## 2 项目管理

对正式的项目，推荐由系统管理员来进行项目管理工作，并分配权限。系统管理员账户一般由软件开发经理持有，这样确保不会有人能随意修改系统，也不会有人能看到全部的项目相关资料。

### 2.1 创建项目

创建项目推荐在 Gitlab 网页上操作，简单易懂。需要注意，创建项目时，一定要选择 “Private” 的项目。Public 的项目注册用户都可以看得到。而 Private 的项目只有经过明确邀请的用户才能看得到这个项目。这对项目的权限管理有极大的帮助。

![创建项目](https://raw.githubusercontent.com/kamidox/blogs/master/images/git_create_project.png)

操作演练：由系统管理员创建一个示例项目 demo

### 2.2 设置项目成员

不同的帐户具有不同的项目权限。Gitlab 有多种角色的帐户，还可以基于 Group 来进行权限管理。在需求不是特别复杂的情况下，我们推荐采用最简单的权限模型来管理项目权限。

* Master 账户是这个项目的主要负责人，他可以直接修改代码并提交，不需要经过审核。除此之外，Master 用户还可以对 Developer 提交的代码进行评审，并最终决定是合并进主干还是退回重新修改。
* Developer 账户是这个项目的贡献者，它可以查看代码并下载代码，但不能直接提交代码，提交的代码需要经过 Master 审核后才能合并进主干。
* 其他的角色可根据实际情况酌情使用，比如可以给 SQA 开通 Reporter 角色的账户，用来 report issue 。

Gitlab 默认的角色列表项目权限可参阅官方文档[项目角色与权限](https://docs.gitlab.com/ce/user/permissions.html#project)。需要注意，这里的 Master 指的是用户在项目上的角色，而不是指代码的主干。

![设置项目组成员](https://raw.githubusercontent.com/kamidox/blogs/master/images/git_project_member.png)

操作演练：

1. 添加一个用户作为 Master 账户
2. 添加一个用户作为 Developer 帐户

## 3 Git Flow

Git Flow 是一种基于 Git 的开发流程。其主要思想是，以 Master 为主线，所有的新功能开发在 Branch 上完成，等开发完成后，合并到 Master 里。

原则：**Master 里包含的永远是稳定（至少经过初步测试和代码评审）的源代码。可以直接在 Master 上把代码进行部署（编译并发布给测试部的版本）。**

![Git Flow](https://raw.githubusercontent.com/kamidox/blogs/master/images/git_flow.png)

主要分成几个步骤：

1. 创建分支
2. 在分支上提交代码
3. 创建 Merge Request
4. 代码评审
5. 合并到主干

接下来，我们来讨论几个典型的场景下的 Git FLow 开发模型。熟悉 Github 的同学可能对 Merge Request 这个称呼感到奇怪，实际上它就是 Pull Request，不同的叫法而已。

### 3.1 Master 用户直接在主干上开发

这种开发模式一般用在一些**不需要团队协作**的小功能的开发上。这种开发模式和 SVN 开发模式基本相同。

**1. 下载代码**

```shell
git clone http://user1@192.168.56.101/user1/demo.git
```

**2. 编写代码，验证后提交**

```shell
git commit -am "My feature is ready"
```

**3. 推送到主干**

```shell
git push
```

便捷与安全有时是相互矛盾的。这种开发模式虽然简洁，但没有强制的代码评审，是否采用需要根据实际情况考量。

操作演练：由 Master 用户直接提交代码修改到主干

### 3.2 新功能分支开发流程

这种工作一般在一个较大的新功能开发时使用，一般需要进行团队协作，即由几个人共同来开发。这是最经典的 Git Flow 开发流程，在 Bug Fix 时也可以使用这个开发模式。典型步骤如下：

**1. 创建功能开发分支**

创建新功能分支，并把分支推送到远程代码仓库。这个动作也可以在 Gitlab 网页上操作。

```shell
git clone http://user1@192.168.56.101/user1/demo.git
cd demo
git checkout -b feature2
git push origin feature2
```

**2. 其他开发人员下载代码，并在分支上开发新功能**

```shell
git clone http://user2@192.168.56.101/user1/demo.git
git checkout feature2
git config user.name "user2"
git config user.email "user2@example.com"
```

**3. 测试新功能并提交**

```shell
git commit -am "Developer user2 for Feature 2"
git push
```

**4. 创建 Merge Request**

步骤 2 和 3 可以无限制次数地进行，直到新功能开发完成，并完成单元测试为止。当新功能开发完成后，需要在 Gitlab 网页上创建合并请求。提交 Merge Request 的目的是为了发起代码评审流程。

![合并请求](https://raw.githubusercontent.com/kamidox/blogs/master/images/git_merge_request.png)

**5. 代码评审**

合并请求可以指定具有 Master 角色的用户进行 Review。如果 Review 通过，则直接会把新功能合并进代码主干。如果 Review 不通过，则评审人员可以直接关闭这个 Merge Request。等待开发者重新修改代码，并重新提交 Merge Request。

![代码评审](https://raw.githubusercontent.com/kamidox/blogs/master/images/git_code_review.png)

评审过程中，可以直接在 Gitlab 网页上，对着代码写上评审意见。这些评审意见对应的开发者都会看到。

![代码评审意见](https://raw.githubusercontent.com/kamidox/blogs/master/images/git_code_review_comments.png)

**6. 更新本地代码副本**

当新功能合并到代码主干后，其他开发人员可以更新服务器上的最新代码到自己本地的工作副本中。

```shell
git pull
```

操作演练：

1. Master 用户创建一个远程分支
2. Developer user2 下载代码，切换到开发分支，并提交代码到开发分支
3. Developer user3 下载代码，切换到开发分支，并提交代码到开发分支
4. Master user1 下载代码，切换到开发分支，并提交代码到开发分支
5. 创建合并请求
6. 代码评审
7. 评审不过，发回重新修改
8. Developer user2 重新修改代码，并提交到开发分支
9. 重新发起合并请求
10. 代码评审
11. 评审通过，合并到代码主干
12. 删除开发分支
13. 开发者更新本地代码

### 3.3 Developer 用户直接在主干上开发

这种开发模式一般用在一些**不需要协作**的小功能开发或 Bug 修复上。由于 **Developer 用户没有权限把修改的代码直接提交到主干**上。所以，需要先 Fork 一个本地分支，然后本地修改后，发起一个 Merge Request ，由 Master 用户进行代码评审，合格后由 Master 用户把代码合并到主干。

**1. 开发者 Fork 一份基线**

这一步骤必须在 Gitlab 网页端进行。比如，我们使用 user2 Fork 一个由 user1 创建的 demo 项目，则其 Git 地址为：

```shell
http://user2@192.168.56.101/user2/demo.git
```

注意和原来直接从 user1 的 demo 项目的 Git 地址比较 `http://user2@192.168.56.101/user1/demo.git` 。

**2. 开发者下载 Fork 的基线代码**

```shell
git clone http://user2@192.168.56.101/user2/demo.git
```

**3. 开发者修改代码，测试，并提交**

```shell
git push origin master
```

**4. 提交 Merge Request**

这一步骤必须在 Gitlab 网页上进行。点击 `Merge Requests` -> `New Merge Request` 来创建一个合并请求。需要指定合并请求的源分支和目的分支。

![合并请求](https://raw.githubusercontent.com/kamidox/blogs/master/images/git_merge_request.png)

**5. 代码评审**

指定的代码评审者可以查看这个合并请求，并选择直接关闭或者合并到主干。如果关闭，则一般会写上评审不通过的理由，然后由开发者重新修改，并重新提交合并请求。如果通过评审，则代码会合并到主干上。

**6. 开发者更新本地代码**

当 Developer 角色的开发者 Fork 了一份代码后，本地 Git 仓库里实际是“追踪”开发者 Fork 出来的这份代码，而不是原始的代码仓库里的代码。如下所示：

```shell
$ git remote -v
origin  http://user2@192.168.56.101/user2/demo.git (fetch)
origin  http://user2@192.168.56.101/user2/demo.git (push)
```

此时要怎么样把原始的代码仓库里的代码更新到本地呢？比如，另外一个开发者合并了一个新的功能到原始代码的主干上，怎么样把这个代码更新到本地呢？进而更新到 Fork 出来的代码仓库里呢？可以使用以下的方法：

首先，把原始的 Git 代码仓库地址添加到本地：

```shell
$ git remote add upstream http://user2@192.168.56.101/user1/demo.git
```

查看添加后的情况：

```shell
$ git remote -v
origin  http://user2@192.168.56.101/user2/demo.git (fetch)
origin  http://user2@192.168.56.101/user2/demo.git (push)
upstream  http://user2@192.168.56.101/user1/demo.git (fetch)
upstream  http://user2@192.168.56.101/user1/demo.git (push)
```

接着，把原始 Git 代码仓库里的代码下载下来，只是把数据库下载下来而已，并没有合并到本地分支：

```shell
git fetch upstream
```

下一步，把下载下来的代码合并到本地分支：

```shell
git merge upstream/master
```

执行这一步时需要注意，需要确保本地没有未提交的修改，否则到时处理代码冲突会比较麻烦。上面的两条指令也可以由一条完成，即 `git pull upstream master` 。

最后，把从原始 Git 代码仓库合并下来的代码，提交到 Fork 出来的远程代码仓库里。

```shell
git commit -am "Merge from upstream"
git push origin master
```

操作演练：

1. 开发者 Fork 一份基线
2. 开发者下载 Fork 出来的基线代码到本地
3. 开发者修改代码并提交
4. 开发者再次修改代码，并再次提交
5. 开发者推送本地提交到 Fork 出来的远程代码仓库上
6. 开发者发起 Merge Request
7. 代码评审，不通过，关闭 Merge Request
8. 开发者根据评审意见重新修改代码，并提交，然后推送到远程代码仓库
9. 开发者发起 Merge Request
10. 代码评审，通过，合并到主干
11. 其他开发者提交代码到主干
12. 开发者更新本地代码到原始主干，并且使 Fork 出来的远程代码仓库与原始主干保持同步

## 4 分支及标签管理

分支的目的是为了做代码隔离。典型的代码隔离如前面介绍的新功能开发分支，另外一个典型的目的是为己发布的产品拉独立的分支来维护，或者虽然产品还没发布，但由于并行开发多个产品线，在产品测试后期，就拉出独立分支，隔离主干的频繁变动。这背后的原因是由于不同的分支代码的质量和稳定性是不一样的。一般来讲，新功能开发分支稳定性最差，因为只有开发者做了单元测试而已。其次是主干，做了代码评审，如果有自动化测试系统，那么还会做设备自动测试和系统自动测试。一般情况下，产品的集成测试版本以及前面几个系统测试版本会在主干上直接编译。最稳定的是产品分支，己发布或即将发布的产品的测试力度和强度是最大的，其稳定性也是最好的。综上，我们开发流程里采用的分支类型包含：

* 开发分支：为了开发新功能而临时创建的，当合并进主干后，这种分支可以删除
* 代码主干：一直存在，且在 Gitlab 里具有**保护属性**，即普通的 Developer 要修改这个分支上的代码时需要经过评审
* 产品分支：产品即将发布或发布后创建，然后一直存在，且在 Gitlab 里具有保护属性

### 4.1 产品分支管理

假设，我们有一个产品已经经过了 8 轮的系统测试，目前软件整体上比较稳定，按计划再测试 2 轮即会正式发布。而当前，主干上频繁地有新功能合并进来，这些新功能又是这个产品不需要的。产品软件负责人经过讨论，决定拉出独立的产品分支来管理，以避免新合并进来的新功能由于稳定性较差，测试不全面，影响即将发布的产品的质量。

在创建功能开发分支时，我们介绍了命令行创建远程分支的方法，实际上在 Gitlab 网页上操作更简单。

![创建分支](https://raw.githubusercontent.com/kamidox/blogs/master/images/git_create_branch.png)

需要注意，默认情况下创建出来的分支是不处于保护状态的。即任何的 Developer 角色的人都可以推送代码到这个分支，这是我们不希望看到的。越到项目后期，代码的修改越需要谨慎地进行评审。所以，创建完分支，需要把分支设置为 Proteced 属性，这样可以对产品分支的代码修改进行严格地控制。

![产品分支保护](https://raw.githubusercontent.com/kamidox/blogs/master/images/git_branch_protected.png)

大家可以看到，这里设置的**保护级别比主干更高**，即没有人能直接推送代码到这个分支上。任何人，包括 Master 角色的开发者提交代码时，也只能通过创建 Bug Fix 分支，然后在分支上修改代码，验证，最后通过创建 Merge Request 来强制进行代码评审。当然，Master 角色的开发者可以自己评审自己的代码，但起码强制进行了二次确认。相应地，为了安全，也可以把主干的保护级别设置成和产品分支的保护级别一样，这样就没有人能直接向主干推送代码，都必须通过 Merge Request 进行代码评审后才可以合并代码到主干上。

创建完分支后，后续**这个产品的版本就直接从这个分支上编译，而不再从主干上编译**。假设，这个时候这个产品上修改了一个 Bug，并提交到了这个分支上。那么这个提交要不要也合并到主干上呢？答案是原则上需要合并到主干上，但也不能强制要求。如果这个 Bug 只和这个产品相关，而和其他产品无关，而且**提交到主干上需要考虑不同产品的兼容性问题，复杂度增加很多**，此时可以允许不提交到主干。如果是最终决策不提交到主干，这个提交需要在 commit log 里注明 **PSBF:** (Product Specific Bug Fix) 前缀，以方便以后根据前缀来查询。但如果这个 Bug 是个普遍存在的 Bug ，主干上的其他衍生产品也会有这样的 Bug，则这个 Bug 的修改**必须**合并到主干上。由于提交到产品分支的修改必须强制经过评审，所以在评审的时候可以告诉开发者是否需要把这个修改合并进主干。

另外一个问题，如果一个新功能分支合并到主干上了，这个时候一般是不需要合并到产品分支的。但如果主干上合并进了一个 Bug Fix 修改，此时要不要合并进产品分支呢？答案是看情况，不能一概而论。如果这个 Bug Fix 和具体的产品无关，则不需要合并进产品分支。如果这个 Bug Fix 和具体的产品相关，但不严重，属于 normal 或 minor 级别的 Bug，则根据产品的生命周期判断，可以合并也可以不合并进产品分支。如果这个 Bug Fix 和具体的产品相关，且非常严重，则**必须**合并进产品分支。经过讨论后，还可能需要马上发起一个 ECR/ECN 流程来下发新软件。

![合并到产品分支](https://raw.githubusercontent.com/kamidox/blogs/master/images/git_merge_to_product_branch.png)

操作演练：

1. 创建一个产品分支，并设置相应的保护级别
2. Master 角色的用户提交 Bug 修改流程，演示强制代码评审的效果
3. 主干上合并了一个严重的问题修改，同时也需要合并到产品分支

### 4.2 标签管理

标签的目的是为了做标记，它能唯一地标识代码仓库中某个“时刻”的代码。典型地，所有的正式发布的软件版本会都会打上标签，以方便以后追溯。再如特单版本正式发布后，也会打上标签。**标签的命名和软件命名采用相同的规则**，这样方便从己发布的软件直接找到对应的源码。

![代码对比](https://raw.githubusercontent.com/kamidox/blogs/master/images/git_tags.png)

## 5 其他

有一个非常重要的原则，需要强调，开发者需要尽量确保自己 Fork 出来的基线以及本地的代码副本和原基线的主干保持同步。即需要经常更新主干上的代码。否则，会给后续的代码评审以及代码合并造成很大的无谓的工作量。其次，为了减少代码合并时的工作量，推荐开发者在提交 Merge Request 前，把自己的工作分支更新到主干代码上，解决完冲突，验证完代码有效性后，再提交 Merge Request。这里也提醒代码评审者注意，如果评审一个 Merge Request 时，发现代码有冲突，不能进行 Fast-Forward 合并，而需要手动合并冲突，则开发者必定没有在提交 Merge Request 时更新到最新的主干上。此时代码评审者完全可以拒绝这个合并请求，并要求开发者更新到最新主干上，合并完冲突，验证通过后重新提交 Merge Request。

推荐阅读阮一峰的两篇关于 Git 的博客，简洁明了，清晰易懂。分别是[《Git 工作流程》](http://www.ruanyifeng.com/blog/2015/12/git-workflow.html)和[《Git远程操作详解》](http://www.ruanyifeng.com/blog/2014/06/git_remote.html)。

关于 Git 的系统性基础知识，可参阅 [Pro Git](https://git-scm.com/book/zh/v2) 这本开源图书。关于 Windows 平台的 Git 客户端，如果喜欢命令行的用户，可使用 [Git for windows](https://git-for-windows.github.io)。对于习惯 TortoiseSVN 客户端的用户，推荐使用 [TortoiseGit](https://tortoisegit.org)。

（完）
