Title: SDIP notes
Date: 2015-09-01 09:36
Modified: 2015-09-01 09:36
Slug: sdip-notes
Authors: Joey Huang
Summary: SDIP notes
Status: draft

## SDIP Overview

### Project Life Cycle Phases

1. Initiation
2. Planning
	* Gathering of Requirements (Major Tasks and activities)
	* Analysis of Scope (Major Tasks and activities)
	* Create the Test Environment (Entry/Exit criteria)
3. Execution
	* Alpha (Mainstones)
	* Beta (Mainstones)
	* Release Candidate (Mainstones)
	* Close Sev 1/2 Defects	(Entry/Exit criteria)
4. Closure

### Software Development Life Cycle (SDLC)
1. Planning
2. Analysis -> documented product requirements and end user needs
3. Design -> documented design document to skilled programmers
4. Develop/Implementation -> coding and publish to testing team
5. Testing -> software is ready
6. Deployment -> software training, support and deployment communications
7. Maintaince 

### Different Main Development Life Cycles

1. Waterfall
2. V-Model
3. Agile: Agile with Scrum; Agile with RAD; Agile with XP;
4. Prototyping
5. Spiral

Difference: when these activities (Analysis, Design; Implement, Test) occur

### Project Release Life Cycles

1. System/Product Release
2. Component Release
3. Standalone/Service Pack Release
4. Maintenance Release

### Managing Life Cycles in Projects

1. Select Life Cycles
2. Combine different Life Cycles
3. Work Breakdown Structure (WBS)

## Leading Product Development Improvments

### Lesson 1: Effective and Efficient Product Development

* People: 
* Process: To connect People
* Technology: To support Process

### Lesson 2: Leading Change

Change Cycle: http://work911.com/articles/changecycle.htm
Need for Change + Leadership & Direction + Planning of Communication

### Lesson 3: Management Responsibilities

### Lession 5: Improvement Cycles

Monthly: SDIP Improvement Progress Report
Quaterly: SDIP Practice Implemention Report

Yearly re-planning

Oct: SDIP Information about new practices, tools, etc
Nov: Define Improvement Goals for BU
Dec: Define Improvement Plans for BU
Jan: Approve Goals, Plans, Budget and Resources

## Software Architecture

### Requirements Architecture Define

* Architecture View Point: 视角，从不同的视角看到的系统架构是不一样的。比如用户视角，商业视角，开发者视角等
* Architecture View: 视图，用来描述从不同视角看到的系统架构

**Most common used architectural views:**

* **Functional/Logic View -> UML Component Diagram**
  从功能和逻辑角度出发，根据数据和分层设计原则来描述系统
* **Code/Module View -> UML Package Diagram**
  这是个静态视图，描述服务器/模块之间如何连接
* **Development/Implementation View -> UML Package Diagram**
  从开发角度来描述系统，是软件经理关心的视图
* **Concurrency/Process View -> UML Component Diagram**
  从动态角度来描述系统，关心系统的运行时指标，包括并发，组件交互等
* **Physical/Deployment View -> UML Deployment Diagram**
  从系统工程师的角度来描述系统，从物理层（服务器，硬件组件 etc.）角度来描述系统，关心系统的可靠性，容错性，扩展性
* **Data View -> Entity Relationship Model**
  从数据关系的角度来描述系统，描述系统的数据库，数据连接，网络环境等。主要为了描述数据结构，数据关联，数据迁移等方面的问题。

**Quality Properties：**

* Availability
* Confidentiality
* Maintainability
* Reliability
* Performance
* Safety
* Security
* Usability

### Architecture Process/Strategy

** Architecture Process**

* **Elicitation**
  识别出系统的所有相关者，引导他们去表达需求和担忧点，以此来完善整体需求，从而在设计阶段把问题考虑全面。可以使用用例图，软件质量指标，原型等方法来达成这个目的。
* **Design**
	* System Structure -> Topology of components
	* Functional behaviour -> Responsibilities of components
	* System-Level Interaction -> Flow between components
	* Non-Functional Properties -> Quality Properties
	* System Implementation -> Technology choices
* **Documentation**
  从所有相关者的视角来描述系统。可以使用 UML 等。也需要把系统设计的妥协因素写进去。
* **Evaluation**
  从完整度，一致性，与现有系统兼容性，是否满足用户需求的角度来评估系统设计
* **Enforcement**
  通过代码级别的分析，来发现工程师的实现与系统架构设计相违背的地方。比如层次设计，耦合规则等
* **Validation**
  这里主要是进行产品和用户层面的验证，用是否符合用户需求来评价系统设计的优劣性。同时从典型用便场景出发，也可以从其他有经验的专家的角度来评估系统，发现系统的薄弱环节和设计缺陷。

**Architecture Strategy**

* Define the objectives of each architecture phase
	* Determine methods and tools to be used
	* Determine technologies to be used
	* Document architecture design rationale
* Prepare the architecture evolution
	* Create a roadmap for future extensions
	* Define and evaluate likely future change scenarios
	* Assess potential for reuse by adopting a product line approach
	* Prepare measures to avoid architectural erosion

### Using Methods and Tools to improve architecture

**Elicitation**

* ATAM (Architecture TrAde-off Method): 通过评估架构决策的结果来发现质量和系统架构之间的妥协和平衡。
	* 输入
		* 系统概要需求和商业模型
		* 各个视角的系统架构图
		* 至少包含非正式的系统的关键质量要求
	* 输出
		* 系统与商业目标的连接点
		* 从各个典型场景收集的系统质量要求
		* 把架构决策和质量要求对应起来
		* 系统薄弱环节和妥协平衡点
		* 风险列表
* QAW (Quality Attribute Workshop): 通过分析系统的非功能性关键质量指标来找出系统潜在的需求点。
	* 输入
		* 系统概要需求和商业模型
		* 各个视角的系统架构图
		* 至少包含非正式的系统的关键质量要求
	* 输出
		* 系统与商业目标的连接点
		* 从各个典型场景收集的系统质量要求
		* 把架构决策和质量要求对应起来
		* 系统薄弱环节和妥协平衡点
		* 风险列表

**Design**

* ADD (Attribute-Driven Design): 把系统解构成不同的组件
  从 质量要求，设计限制，功能要求 出发来解构
* Styles: 系统模型
	* 分层设计
	* 发布/订阅模型
	* MVC 模型
	* 客户端/服务器模型
	* 点对点通讯模型
	* etc. etc.
* Pattern: 设计模式
	* Composite 组合模式
	* Builder 构建模式
	* Decorator 装饰模式
	* etc. etc.

**Documentation**

* UML: 用来描述不同视角的系统框架图
* SysML: 是 UML 的一个扩展子集

**Evaluation**

* ARID (Active Reviews for Intermidiate Design)
	* 会前准备
		* 确认参加评审的人员列表
		* 准备设计演示文稿
		* 准备典型需求场景文档
		* 评审会议准备
	* 评审会议
		* 演示 ARID 方法
		* 演示设计文档
		* 头脑风暴/确认场景优先级和重要性
		* 进行评审
		* 展示评审结论

**Enforcement**

* DSM (Dependency Struct Matrix)
  通过分析代码来检查系统实现是否违背系统架构的分层设计。使用 LDM （[Lattix][1] 公司的一个软件架构管理解决方案，这里有一个[介绍文档][2]）工具来对代码进行静态分析，以发现一些非法的跨层引用。

**Validation**

* 通过 ARID 方法来验证架构
* 通过 ATAM 方法来验证架构

[1]: http://lattix.com/
[2]: http://edageek.com/2007/01/04/lattix-ldm-dependency-structure-matrix/

