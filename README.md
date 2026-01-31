---
marp: true
theme: gaia
---

# Prompt Engineering Design Patterns

#### Concepts and Practices


@Huang, Baochen

---

# Definitions

- agent/rules： 事先定义好的行为的东西（As a/an xxx）
    - subagent: 子agent，用来区分上下文
- rules/instructions： 实现定义好得规范和行为
- commands: 斜杠命令，重复性很高的一串行为
- skills: 实现定义好的工具

---

# Principles

- 减少上下文
    - 减少token使用
    - 过多上下文，容易遗忘需求
- 记忆
- 可迭代
- 范围控制
    - 防止修改范围过大/破坏功能
- 增加功能

---

# 设计模式 - Agentic模式

- 任务拆解： 一个agent做一件事/一类事


### 理由：

- 减少上下文
    - 让每个agent的需求降低
- 范围控制
    - 让每个agent只在某个文件夹里工作
- 可迭代
    - 多总结每次的功能让其越来越符合需求

---

# 设计模式 - rules模式

- 讲需求按层次拆分，维护在不同的文件中
- 组合使用


### 理由：

- 通过 组合 + 按需调用 减少上下文
- 可迭代


---

# 设计模式 - Workflow模式

- 用workflow规范agent的执行步骤，并且指定相关分支。

---

# 设计模型 - Agent模式/rules模式技巧

- 重申：避免遗忘
  - > 重新阅读自己的需求
- 知识自总结
  - > 阅读外部/内部文档，总结成需要的内容
- 反思
  - > 将刚才的错误总结道 xxx开发需求里


--- 

# Agent + rules 的例子

#### Agent

- 使用@manager管理ai-related的文档
- 使用@dev来开发
- 使用@formatter来格式化代码

#### rules分层

- 所有agent需要遵循的规则
- python开发需要遵循的规则

---

# 设计模式 - commands模式

- 将重复性很高的一串行为，封装成一个命令

### 理由：

- 可迭代

---

# Commands 模式例子

- /list-agents


---

# 设计模式 - Skills模式

- 增加agent的功能（agent其实是通过工具来跟世界交互）

## 理由：

- 一些工具反复使用，让agent可能每次都产生大量代码
- 增加功能


---

# 设计模式 - 需求拆分模式

- 以文件夹、文件文档和方法文档的方式分层整理需求
- 文件夹维护 requirements.md 文件
- OPTIONAL: 创建TO-DO.md文件，方便中断后继续执行
- OPTIONAL: 增加change-log.md文件，方便ai回滚

---

## Skill 模式例子

- 维护一个读取pdf的skill

---

## 设计模式 - 可验证可回归

- 建立unit-test agent。

