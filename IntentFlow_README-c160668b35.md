# IntentFlow - 下一代多模态智能体编排框架

## Overview

IntentFlow是在LangChain基础上演进的下一代框架，核心抽象从"执行链"升级到"意图节点"，专注于**多模态智能体编排**和**自适应工作流**。

## 核心创新点

### 1. 从"执行"到"理解-自适应"
- **LangChain**：静态链式执行，依赖开发者硬编码路由逻辑
- **IntentFlow**：核心抽象为**意图节点**，内置意图识别能力

### 2. 原生多模态支持
- 统一处理文本、图像、音频、视频
- 多模态适配器将不同输入转换为统一语义表示

### 3. 自适应编排引擎
- 支持动态路由和智能体协作
- 可观测性系统实时监控执行链路

## 框架架构

### 核心模块

| 模块                | 职责                                  |
|---------------------|---------------------------------------|
| IntentType          | 意图类型枚举（查询、生成、决策、复合） |
| ModalityType        | 模态类型枚举（文本、图像、音频、视频） |
| IntentContext       | 上下文管理                            |
| IntentResult        | 执行结果返回                          |
| IntentNode          | 意图节点抽象                          |
| MultimodalAdapter   | 多模态适配器                          |
| AdaptiveEngine      | 自适应编排引擎                        |

### 节点类型

#### QueryNode
- **职责**：处理信息检索、问答
- **理解模式**：识别包含"什么是"、"如何"、"查询"等关键词的意图
- **执行策略**：知识库匹配 + 语义理解

#### GenerateNode
- **职责**：生成类内容（文本、图像、音频）
- **理解模式**：识别包含"生成"、"创作"、"画"等关键词的意图
- **执行策略**：路由到对应的生成模型

#### DecideNode
- **职责**：决策、分析、路由
- **理解模式**：识别包含"应该"、"哪个"、"更好"等关键词的意图
- **执行策略**：规则匹配 + 置信度分析

#### CompositeNode
- **职责**：处理复杂多步骤任务
- **理解模式**：识别包含"复杂"、"多步骤"、"流程"等关键词的意图
- **执行策略**：任务分解 + 多节点协作

## 高级特性

### 工作流 DSL（领域特定语言）
允许通过声明式配置定义复杂工作流
```python
engine.dsl.define_workflow(
    "multistep_analysis",
    {
        "start": "decide",
        "nodes": {
            "decide": {
                "type": "decide",
                "conditions": {
                    "复杂": "composite",
                    "简单": "query"
                },
                "on_failure": "fallback"
            },
            "query": {"type": "query", "on_success": "end"},
            "composite": {"type": "composite", "next": "end"}
        }
    }
)
```

### 智能体协作机制
定义节点间的协作关系，实现自动协作
```python
engine.set_collaboration_rule(
    "query_handler",
    ["decide_handler", "generate_handler"]
)
```

### 可观测性系统
- 实时执行链路追踪
- 性能指标监控
- 错误日志分析
- 可视化仪表板

## Quick Start

### 1. 创建并配置引擎
```python
from intentflow_advanced import AdvancedAdaptiveEngine
from intentflow_nodes import QueryNode, GenerateNode, DecideNode
from intentflow_core import ModalityType

# 高级引擎（包含可观测性和工作流DSL）
engine = AdvancedAdaptiveEngine()

# 注册节点
engine.register_node(QueryNode())
engine.register_node(GenerateNode())
engine.register_node(DecideNode())
```

### 2. 执行查询
```python
context = IntentContext(
    user_input="什么是 LangChain？",
    input_modality=ModalityType.TEXT
)

results = await engine.orchestrate(context, "query_handler")
```

### 3. 执行复合任务
```python
from intentflow_advanced import CompositeNode
engine.register_node(CompositeNode())

context = IntentContext(
    user_input="这是一个复杂的任务，需要多步骤处理",
    input_modality=ModalityType.TEXT
)

results = await engine.orchestrate(context, "decide_handler")
```

### 4. 查看监控
```python
print(engine.get_dashboard())
```

## 相比LangChain的优势

| 特性              | LangChain            | IntentFlow          |
|-------------------|----------------------|---------------------|
| 核心抽象          | 链（Chain）          | 意图节点（IntentNode）| 
| 意图理解          | 需硬编码             | 内置意图识别        |
| 自适应路由        | 有限支持             | 完整内置            |
| 多模态支持        | 有限                 | 原生多模态          |
| 编排方式          | 静态链式编排         | 动态自适应编排      |
| 可观测性          | 基础日志             | 完整链路追踪        |
| 智能体协作        | 手动实现             | 自动协作机制        |
| 领域适配          | 文本为主             | 多模态智能体        |

## 适用场景

1. **智能客服系统**：统一处理文字、语音、图像输入
2. **多模态创作平台**：支持文生图、图生文、音频生成
3. **复杂决策系统**：多节点协作分析复杂问题
4. **企业级工作流**：自适应流程编排
5. **数字人平台**：多模态交互系统

## Roadmap

### 短期目标
- 集成大模型（LLaMA、Qwen）实现更强大的意图识别
- 支持更多模态（3D模型、AR）
- 图形化工作流编辑器

### 长期愿景
- 真正的自主智能体系统
- 跨模态理解与生成
- 自我优化的自适应引擎