# IntentFlow 使用指南

## 目录

- [1. 简介](#1-简介)
  - [1.1 什么是 IntentFlow](#11-什么是-intentflow)
  - [1.2 核心设计理念](#12-核心设计理念)
  - [1.3 与 LangChain 的对比](#13-与-langchain-的对比)
  - [1.4 适用场景](#14-适用场景)
- [2. 快速开始](#2-快速开始)
  - [2.1 安装方式](#21-安装方式)
  - [2.2 Hello World 示例](#22-hello-world-示例)
  - [2.3 第一个多模态应用](#23-第一个多模态应用)
  - [2.4 常见安装问题](#24-常见安装问题)
- [3. 核心概念](#3-核心概念)
  - [3.1 意图节点](#31-意图节点)
  - [3.2 模态类型](#32-模态类型)
  - [3.3 上下文管理](#33-上下文管理)
  - [3.4 自适应路由](#34-自适应路由)
  - [3.5 工作流 DSL](#35-工作流-dsl)
- [4. 基础教程](#4-基础教程)
  - [4.1 查询类节点](#41-查询类节点)
  - [4.2 生成类节点](#42-生成类节点)
  - [4.3 决策类节点](#43-决策类节点)
  - [4.4 复合节点](#44-复合节点)
  - [4.5 节点连接与编排](#45-节点连接与编排)
- [5. 高级特性](#5-高级特性)
  - [5.1 多模态适配器](#51-多模态适配器)
  - [5.2 智能体协作](#52-智能体协作)
  - [5.3 工作流定义](#53-工作流定义)
  - [5.4 可观测性系统](#54-可观测性系统)
  - [5.5 自定义节点开发](#55-自定义节点开发)
- [6. 生产环境部署](#6-生产环境部署)
  - [6.1 Docker 容器化](#61-docker-容器化)
  - [6.2 Kubernetes 部署](#62-kubernetes-部署)
  - [6.3 Serverless 集成](#63-serverless-集成)
  - [6.4 性能优化](#64-性能优化)
  - [6.5 安全与合规](#65-安全与合规)
- [7. API 参考](#7-api-参考)
  - [7.1 核心 API](#71-核心-api)
  - [7.2 节点 API](#72-节点-api)
  - [7.3 适配器 API](#73-适配器-api)
  - [7.4 事件与回调](#74-事件与回调)
- [8. 最佳实践](#8-最佳实践)
  - [8.1 节点设计原则](#81-节点设计原则)
  - [8.2 工作流模式](#82-工作流模式)
  - [8.3 错误处理](#83-错误处理)
  - [8.4 性能调优](#84-性能调优)
  - [8.5 测试策略](#85-测试策略)
- [9. 常见问题](#9-常见问题)
  - [9.1 安装与配置](#91-安装与配置)
  - [9.2 开发问题](#92-开发问题)
  - [9.3 部署问题](#93-部署问题)
  - [9.4 性能问题](#94-性能问题)
- [10. 生态与社区](#10-生态与社区)
  - [10.1 插件开发](#101-插件开发)
  - [10.2 贡献指南](#102-贡献指南)
  - [10.3 社区资源](#103-社区资源)
  - [10.4 路线图](#104-路线图)
- [附录](#附录)
  - [A. 术语表](#a-术语表)
  - [B. 更新日志](#b-更新日志)
  - [C. 许可证](#c-许可证)
  - [D. 致谢](#d-致谢)

---

## 1. 简介

### 1.1 什么是 IntentFlow

IntentFlow 是**下一代多模态智能体编排框架**，专注于解决复杂 AI 应用的自适应工作流问题。

#### 核心特性

- **意图优先**：从"执行链"升级到"意图节点"，内置意图理解能力
- **原生多模态**：统一处理文本、图像、音频、视频，无需额外扩展
- **自适应编排**：动态路由、智能体协作、自动优化
- **完整可观测性**：链路追踪、性能监控、实时仪表板
- **工作流 DSL**：声明式定义复杂工作流，无需硬编码

#### 适用对象

- AI 应用开发者
- 企业级解决方案架构师
- 多模态 AI 研究人员
- 低代码/无代码平台开发者

---

### 1.2 核心设计理念

#### 意图驱动架构

传统框架（如 LangChain）采用"执行链"模式，开发者需要预先定义完整的执行路径。IntentFlow 引入"意图节点"概念：

1. **理解**：节点内置意图识别能力
2. **决策**：根据上下文动态选择下一步
3. **自适应**：支持回环、分支、并行等复杂模式

#### 可组合性

每个节点都是独立的、可复用的单元，通过声明式组合构建复杂应用：

```python
# 简单组合
engine.register_node(QueryNode())
engine.register_node(GenerateNode())

# 复杂组合（工作流 DSL）
engine.dsl.define_workflow("complex_task", {
    "start": "decide",
    "nodes": {
        "decide": {
            "conditions": {
                "复杂": "composite",
                "简单": "query"
            }
        }
    }
})
```

#### 渐进式增强

- **入门**：使用预设节点，5 分钟上手
- **进阶**：自定义节点，扩展能力
- **专家**：插件开发，生态共建

---

### 1.3 与 LangChain 的对比

| 特性              | LangChain                          | IntentFlow                          |
|-------------------|------------------------------------|-------------------------------------|
| **核心抽象**      | Chain（链）                        | IntentNode（意图节点）              |
| **路由方式**      | 静态配置/硬编码                    | 自适应意图识别                      |
| **多模态支持**    | 有限支持（需额外扩展）             | 原生支持                            |
| **编排方式**      | 线性链式                          | 动态图状编排（支持并行、回环）      |
| **可观测性**      | 基础日志                          | 完整链路追踪 + 性能仪表板           |
| **工作流定义**    | Python 代码                        | DSL（领域特定语言）                 |
| **智能体协作**    | 手动实现                          | 自动协作机制                        |
| **学习曲线**      | 中等                              | 低（预设节点） + 高（深度定制）     |

#### 何时选择 IntentFlow？

✅ **适合 IntentFlow 的场景：**
- 需要处理多模态输入（图像、音频、视频）
- 复杂的多步骤任务（需要自适应路由）
- 需要实时监控和性能优化
- 团队希望降低开发复杂度

✅ **适合 LangChain 的场景：**
- 纯文本应用
- 简单的线性工作流
- 已经基于 LangChain 构建的现有系统

---

### 1.4 适用场景

#### 智能客服系统

```
用户输入（文字/语音/图片）
    ↓
意图识别（QueryNode）
    ↓
知识库检索 OR 智能体协作
    ↓
答案生成（GenerateNode）
```

#### 多模态创作平台

```
用户需求："生成一张海滩日落的图片"
    ↓
意图理解（GenerateNode）
    ↓
多模态适配器（文本 → 图像）
    ↓
图像生成（调用 DALL-E / Midjourney）
    ↓
结果返回 + 历史记录
```

#### 企业决策支持系统

```
输入：复杂的业务分析请求
    ↓
意图理解（DecideNode）
    ↓
任务分解（CompositeNode）
    ↓
并行执行多个子任务
    ↓
结果聚合 + 可视化
```

#### 边缘计算 AI

```
IoT 设备采集数据
    ↓
本地意图识别（轻量级节点）
    ↓
决策（本地 OR 上云端）
    ↓
低延迟响应
```

---

## 2. 快速开始

### 2.1 安装方式

#### 方式一：从 PyPI 安装（推荐）

```bash
pip install intentflow
```

#### 方式二：从源码安装

```bash
git clone https://github.com/yourusername/intentflow.git
cd intentflow
pip install -e .
```

#### 方式三：Docker 部署

```bash
docker pull intentflow/intentflow:latest
docker run -p 8080:8080 intentflow/intentflow
```

#### 依赖要求

- Python 3.8+
- 异步运行时（asyncio）
- 可选依赖：
  - `transformers`（用于意图识别）
  - `pillow`（图像处理）
  - `pydub`（音频处理）

---

### 2.2 Hello World 示例

#### 最简单的查询示例

```python
import asyncio
from intentflow import IntentFlow
from intentflow.nodes import QueryNode
from intentflow.types import IntentContext, ModalityType

async def main():
    # 1. 创建引擎
    engine = IntentFlow()

    # 2. 注册节点
    query_node = QueryNode()
    engine.register_node(query_node)

    # 3. 创建上下文
    context = IntentContext(
        user_input="什么是 IntentFlow？",
        input_modality=ModalityType.TEXT
    )

    # 4. 执行编排
    results = await engine.orchestrate(context, "query_handler")

    # 5. 输出结果
    for result in results:
        print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
```

#### 输出

```
📚 IntentFlow: 一个用于构建多模态智能体应用的框架，核心抽象是意图节点。
```

---

### 2.3 第一个多模态应用

#### 图像生成示例

```python
import asyncio
from intentflow import IntentFlow
from intentflow.nodes import GenerateNode
from intentflow.types import IntentContext, ModalityType

async def main():
    engine = IntentFlow()
    engine.register_node(GenerateNode())

    context = IntentContext(
        user_input="生成一张海滩日落的图片",
        input_modality=ModalityType.TEXT
    )

    results = await engine.orchestrate(context, "generate_handler")

    for result in results:
        print(result.content)
        print(f"模态: {result.modality.value}")

if __name__ == "__main__":
    asyncio.run(main())
```

#### 输出

```
🎨 正在生成图像：海滩日落的图片
（这是一个模拟输出，实际会调用图像生成模型）

模态: image
```

---

### 2.4 常见安装问题

#### 问题 1：Python 版本不兼容

```
ERROR: Python 3.7 is not supported
```

**解决方案**：升级到 Python 3.8+

```bash
# 使用 pyenv 安装 Python 3.10
pyenv install 3.10.0
pyenv local 3.10.0
```

#### 问题 2：依赖冲突

```
ERROR: pip's dependency resolver does not currently take into account...
```

**解决方案**：使用虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

pip install intentflow
```

#### 问题 3：权限问题

```
ERROR: Could not install packages due to an EnvironmentError: [Errno 13]
```

**解决方案**：使用 `--user` 参数

```bash
pip install --user intentflow
```

---

## 3. 核心概念

### 3.1 意图节点

IntentNode 是 IntentFlow 的核心抽象，代表一个可执行的业务逻辑单元。

#### 基本结构

```python
from abc import ABC, abstractmethod

class IntentNode(ABC):
    def __init__(self, name: str, intent_type: IntentType):
        self.name = name
        self.intent_type = intent_type
        self.adaptive = True  # 是否启用自适应模式

    @abstractmethod
    async def understand_intent(self, context: IntentContext) -> IntentType:
        """理解用户意图"""
        pass

    @abstractmethod
    async def execute(self, context: IntentContext) -> IntentResult:
        """执行意图"""
        pass

    async def __call__(self, context: IntentContext) -> IntentResult:
        """统一的调用接口"""
        if self.adaptive:
            detected_intent = await self.understand_intent(context)
            if detected_intent != self.intent_type:
                return IntentResult(
                    success=False,
                    content=f"Intent mismatch",
                    next_intent=detected_intent
                )
        return await self.execute(context)
```

#### 意图类型

```python
from enum import Enum

class IntentType(Enum):
    QUERY = "query"          # 查询类：检索信息、回答问题
    GENERATE = "generate"    # 生成类：创作内容、生成图像/视频
    DECIDE = "decide"        # 决策类：分析、判断、路由
    INTERACT = "interact"    # 交互类：对话、工具调用
    COMPOSITE = "composite"  # 复合类：多意图组合
```

---

### 3.2 模态类型

IntentFlow 原生支持多种模态的输入和输出。

#### 支持的模态

```python
class ModalityType(Enum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    MULTIMODAL = "multimodal"
```

#### 多模态上下文

```python
from intentflow.types import IntentContext, ModalityType

# 文本输入
context1 = IntentContext(
    user_input="你好",
    input_modality=ModalityType.TEXT
)

# 图像输入（模拟）
context2 = IntentContext(
    user_input="image_data_base64",
    input_modality=ModalityType.IMAGE
)

# 多模态输入
context3 = IntentContext(
    user_input="文本 + 图像 + 音频",
    input_modality=ModalityType.MULTIMODAL
)
```

---

### 3.3 上下文管理

IntentContext 携带整个工作流的上下文信息。

#### 结构

```python
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class IntentContext:
    """意图上下文"""
    user_input: str
    input_modality: ModalityType
    conversation_history: List[Dict] = field(default_factory=list)
    state: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def update_state(self, key: str, value: Any):
        """更新状态"""
        self.state[key] = value

    def add_to_history(self, role: str, content: str):
        """添加对话历史"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
```

#### 使用示例

```python
# 创建上下文
context = IntentContext(
    user_input="查询昨天销售额",
    input_modality=ModalityType.TEXT
)

# 更新状态
context.update_state("last_query", "销售额")
context.update_state("date_range", "yesterday")

# 添加历史
context.add_to_history("user", "查询昨天销售额")
context.add_to_history("assistant", "好的，正在查询...")
```

---

### 3.4 自适应路由

IntentFlow 支持根据执行结果动态路由到不同节点。

#### 路由机制

1. 节点返回 `next_intent`
2. 引擎查找匹配该意图的节点
3. 动态切换到下一个节点

#### 示例

```python
# DecideNode 返回不同的 next_intent
async def execute(self, context: IntentContext) -> IntentResult:
    task = context.user_input

    if "复杂" in task:
        return IntentResult(
            success=True,
            content="检测到复杂任务",
            next_intent=IntentType.COMPOSITE  # 路由到复合节点
        )
    elif "查询" in task:
        return IntentResult(
            success=True,
            content="检测到查询意图",
            next_intent=IntentType.QUERY     # 路由到查询节点
        )

    return IntentResult(success=True, content="无法确定下一步")
```

---

### 3.5 工作流 DSL

使用声明式语言定义复杂工作流，无需硬编码。

#### 基本语法

```python
engine.dsl.define_workflow(
    "workflow_name",
    {
        "start": "start_node",
        "nodes": {
            "start_node": {
                "type": "query",
                "on_success": "next_node",
                "on_failure": "fallback_node"
            },
            "next_node": {
                "type": "generate",
                "next": "end"
            },
            "fallback_node": {
                "type": "query",
                "next": "end"
            }
        }
    }
)
```

#### 条件路由

```python
engine.dsl.define_workflow(
    "conditional_workflow",
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
            "composite": {
                "type": "composite",
                "next": "end"
            },
            "query": {
                "type": "query",
                "next": "end"
            },
            "fallback": {
                "type": "query",
                "next": "end"
            }
        }
    }
)
```

---

## 4. 基础教程

### 4.1 查询类节点

QueryNode 用于处理信息检索和问答。

#### 基本使用

```python
from intentflow.nodes import QueryNode
from intentflow.types import IntentContext, ModalityType

# 创建节点
query_node = QueryNode()

# 配置知识库
query_node.knowledge_base = {
    "IntentFlow": "多模态智能体编排框架",
    "LangChain": "LLM 应用开发框架"
}

# 使用
context = IntentContext(
    user_input="什么是 IntentFlow？",
    input_modality=ModalityType.TEXT
)

result = await query_node(context)
print(result.content)
```

#### 自定义查询逻辑

```python
class CustomQueryNode(QueryNode):
    async def execute(self, context: IntentContext) -> IntentResult:
        query = context.user_input

        # 调用外部 API
        response = await self.call_search_api(query)

        return IntentResult(
            success=True,
            content=response,
            modality=ModalityType.TEXT
        )
```

---

### 4.2 生成类节点

GenerateNode 用于内容生成（文本、图像、音频等）。

#### 文本生成

```python
from intentflow.nodes import GenerateNode

generate_node = GenerateNode()

context = IntentContext(
    user_input="写一首关于春天的诗",
    input_modality=ModalityType.TEXT
)

result = await generate_node(context)
print(result.content)
```

#### 图像生成

```python
# 注意：实际使用需要配置图像生成模型
context = IntentContext(
    user_input="画一只海滩上的猫",
    input_modality=ModalityType.TEXT
)

result = await generate_node(context)
print(result.metadata)  # 包含图像生成参数
```

---

### 4.3 决策类节点

DecideNode 用于分析、判断和路由。

#### 基本使用

```python
from intentflow.nodes import DecideNode

decide_node = DecideNode()

context = IntentContext(
    user_input="分析一下当前情况",
    input_modality=ModalityType.TEXT
)

result = await decide_node(context)
print(result.content)

if result.next_intent:
    print(f"下一步: {result.next_intent.value}")
```

#### 自定义决策规则

```python
class CustomDecideNode(DecideNode):
    async def execute(self, context: IntentContext) -> IntentResult:
        task = context.user_input

        # 自定义决策逻辑
        if len(task) > 100:
            next_intent = IntentType.COMPOSITE
        elif "?" in task:
            next_intent = IntentType.QUERY
        else:
            next_intent = IntentType.GENERATE

        return IntentResult(
            success=True,
            content=f"决策完成，下一步: {next_intent.value}",
            next_intent=next_intent
        )
```

---

### 4.4 复合节点

CompositeNode 用于处理多步骤复杂任务。

#### 基本使用

```python
from intentflow.nodes import CompositeNode

composite_node = CompositeNode()

context = IntentContext(
    user_input="这是一个复杂的任务，需要多步骤处理",
    input_modality=ModalityType.TEXT
)

result = await composite_node(context)
print(result.content)
```

#### 任务分解

```python
class CustomCompositeNode(CompositeNode):
    def __init__(self):
        super().__init__()
        self.decomposition_rules = {
            r"复杂.*任务": ["analyze", "plan", "execute", "review"],
            r"多步骤.*流程": ["step1", "step2", "step3"]
        }

    async def execute(self, context: IntentContext) -> IntentResult:
        task = context.user_input

        # 分解任务
        steps = self.decompose_task(task)

        # 执行子任务
        results = []
        for step in steps:
            result = await self.execute_step(step, context)
            results.append(result)

        # 聚合结果
        return IntentResult(
            success=True,
            content=f"复合任务完成: {len(results)} 个步骤",
            modality=ModalityType.TEXT
        )
```

---

### 4.5 节点连接与编排

#### 基本编排

```python
from intentflow import IntentFlow

engine = IntentFlow()

# 注册节点
engine.register_node(QueryNode())
engine.register_node(GenerateNode())
engine.register_node(DecideNode())

# 执行编排
context = IntentContext(
    user_input="查询信息并生成报告",
    input_modality=ModalityType.TEXT
)

results = await engine.orchestrate(context, start_node="query_handler")
```

#### 自适应路由

```python
# DecideNode 会根据结果动态路由
context = IntentContext(
    user_input="分析并决定下一步",
    input_modality=ModalityType.TEXT
)

results = await engine.orchestrate(context, start_node="decide_handler")
```

#### 智能体协作

```python
# 设置协作规则
engine.set_collaboration_rule(
    "query_handler",
    ["decide_handler", "generate_handler"]
)

# 执行时会自动触发协作节点
results = await engine.orchestrate_with_collaboration(
    context,
    start_node="query_handler"
)
```

---

## 5. 高级特性

### 5.1 多模态适配器

MultimodalAdapter 统一处理不同模态的输入输出。

#### 基本结构

```python
from abc import ABC, abstractmethod

class MultimodalAdapter(ABC):
    @abstractmethod
    async def to_semantic(self, raw_input: Any, modality: ModalityType) -> str:
        """将原始输入转换为语义表示"""
        pass

    @abstractmethod
    async def from_semantic(self, semantic: str, target_modality: ModalityType) -> Any:
        """从语义表示生成目标模态的输出"""
        pass
```

#### 自定义适配器

```python
class ImageAdapter(MultimodalAdapter):
    async def to_semantic(self, raw_input: Any, modality: ModalityType) -> str:
        """图像 → 语义"""
        # 调用图像识别模型
        description = await self.describe_image(raw_input)
        return description

    async def from_semantic(self, semantic: str, target_modality: ModalityType) -> Any:
        """语义 → 图像"""
        # 调用图像生成模型
        image = await self.generate_image(semantic)
        return image
```

#### 注册适配器

```python
engine.register_adapter(ModalityType.IMAGE, ImageAdapter())
```

---

### 5.2 智能体协作

多个节点可以协作完成任务。

#### 设置协作规则

```python
# 查询节点协作决策节点
engine.set_collaboration_rule(
    "query_handler",
    ["decide_handler"]
)

# 生成节点协作多个节点
engine.set_collaboration_rule(
    "generate_handler",
    ["query_handler", "decide_handler"]
)
```

#### 协作执行

```python
# 自动触发协作节点
results = await engine.orchestrate_with_collaboration(
    context,
    start_node="query_handler"
)
```

---

### 5.3 工作流定义

#### 完整示例

```python
engine.dsl.define_workflow(
    "intelligent_query",
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
            "composite": {
                "type": "composite",
                "next": "end"
            },
            "query": {
                "type": "query",
                "next": "end"
            },
            "fallback": {
                "type": "query",
                "next": "end"
            }
        }
    }
)
```

#### 执行工作流

```python
results = await engine.orchestrate_with_collaboration(
    context,
    start_node="decide_handler",
    workflow_name="intelligent_query"
)
```

---

### 5.4 可观测性系统

实时监控执行链路和性能指标。

#### 启用可观测性

```python
# 高级引擎内置可观测性
from intentflow_advanced import AdvancedAdaptiveEngine

engine = AdvancedAdaptiveEngine()

# 执行编排（自动追踪）
results = await engine.orchestrate_with_collaboration(context, start_node)

# 获取指标
metrics = engine.telemetry.get_metrics()
print(f"成功率: {metrics['success_rate']:.1%}")
print(f"平均延迟: {metrics['avg_latency']:.3f}s")
```

#### 查看仪表板

```python
dashboard = engine.get_dashboard()
print(dashboard)
```

#### 输出示例

```
================================================================================
IntentFlow 监控仪表板
================================================================================

📊 执行统计
  - 总执行次数: 100
  - 成功率: 98.5%
  - 平均延迟: 0.125s
  - 错误次数: 1

🤖 智能体协作
  - query_handler ←→ decide_handler

📝 已注册工作流
  - 数量: 2
  - intelligent_query
  - creative_workflow
================================================================================
```

---

### 5.5 自定义节点开发

#### 创建自定义节点

```python
from intentflow_core import IntentNode, IntentType, IntentContext, IntentResult, ModalityType

class MyCustomNode(IntentNode):
    def __init__(self, name: str = "my_custom_node"):
        super().__init__(name, IntentType.QUERY)

    async def understand_intent(self, context: IntentContext) -> IntentType:
        """理解意图"""
        # 自定义意图识别逻辑
        if "特殊关键词" in context.user_input:
            return IntentType.GENERATE
        return IntentType.QUERY

    async def execute(self, context: IntentContext) -> IntentResult:
        """执行业务逻辑"""
        # 自定义执行逻辑
        result = await self.my_business_logic(context)

        return IntentResult(
            success=True,
            content=result,
            modality=ModalityType.TEXT,
            next_intent=None  # 或者指定下一步意图
        )

    async def my_business_logic(self, context: IntentContext) -> str:
        """你的业务逻辑"""
        # 调用 API、数据库、模型等
        return "处理完成"
```

#### 注册自定义节点

```python
# 创建节点
custom_node = MyCustomNode()

# 注册到引擎
engine.register_node(custom_node)

# 使用
results = await engine.orchestrate(context, "my_custom_node")
```

---

## 6. 生产环境部署

### 6.1 Docker 容器化

#### Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 暴露端口
EXPOSE 8080

# 启动服务
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

#### requirements.txt

```txt
intentflow>=1.0.0
uvicorn[standard]
fastapi
```

#### 构建与运行

```bash
# 构建镜像
docker build -t intentflow-app .

# 运行容器
docker run -p 8080:8080 intentflow-app
```

---

### 6.2 Kubernetes 部署

#### deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: intentflow-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: intentflow
  template:
    metadata:
      labels:
        app: intentflow
    spec:
      containers:
      - name: intentflow
        image: intentflow-app:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
```

#### service.yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: intentflow-service
spec:
  selector:
    app: intentflow
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: LoadBalancer
```

#### 部署

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

---

### 6.3 Serverless 集成

#### AWS Lambda

```python
# lambda_function.py
from intentflow import IntentFlow
from intentflow.nodes import QueryNode
from intentflow.types import IntentContext, ModalityType

# 初始化引擎（全局，避免冷启动）
engine = IntentFlow()
engine.register_node(QueryNode())

def lambda_handler(event, context):
    """AWS Lambda 入口"""
    user_input = event.get("input", "")
    modality = event.get("modality", "text")

    # 创建上下文
    intent_context = IntentContext(
        user_input=user_input,
        input_modality=ModalityType(modality)
    )

    # 执行编排
    results = await engine.orchestrate(intent_context, "query_handler")

    return {
        "statusCode": 200,
        "body": {
            "results": [r.content for r in results]
        }
    }
```

---

### 6.4 性能优化

#### 并发执行

```python
import asyncio

async def execute_multiple(contexts):
    """并发执行多个请求"""
    tasks = [
        engine.orchestrate(ctx, "query_handler")
        for ctx in contexts
    ]
    results = await asyncio.gather(*tasks)
    return results
```

#### 缓存策略

```python
from functools import lru_cache

class CachedQueryNode(QueryNode):
    @lru_cache(maxsize=1000)
    async def execute(self, context: IntentContext) -> IntentResult:
        """缓存查询结果"""
        # 原有逻辑
        return await super().execute(context)
```

#### 资源限制

```python
engine = IntentFlow(max_concurrent_requests=10, timeout=30)
```

---

### 6.5 安全与合规

#### 输入验证

```python
class SecureQueryNode(QueryNode):
    async def execute(self, context: IntentContext) -> IntentResult:
        # 验证输入
        if self.is_malicious(context.user_input):
            return IntentResult(
                success=False,
                content="Invalid input",
                modality=ModalityType.TEXT
            )

        # 原有逻辑
        return await super().execute(context)

    def is_malicious(self, input_str: str) -> bool:
        """检测恶意输入"""
        # 实现你的安全检查逻辑
        return False
```

#### 敏感数据处理

```python
class PrivacyAwareNode(IntentNode):
    async def execute(self, context: IntentContext) -> IntentResult:
        # 脱敏处理
        sanitized_input = self.sanitize(context.user_input)

        # 执行
        result = await self.process(sanitized_input)

        return IntentResult(
            success=True,
            content=result,
            modality=ModalityType.TEXT
        )
```

---

## 7. API 参考

### 7.1 核心 API

#### IntentFlow

```python
class IntentFlow:
    def __init__(self, max_concurrent_requests: int = 10, timeout: int = 30):
        """初始化引擎"""

    def register_node(self, node: IntentNode):
        """注册节点"""

    async def orchestrate(self, context: IntentContext, start_node: str) -> List[IntentResult]:
        """执行编排"""
```

#### AdvancedAdaptiveEngine

```python
class AdvancedAdaptiveEngine(AdaptiveEngine):
    def set_collaboration_rule(self, primary_node: str, collaborator_nodes: List[str]):
        """设置协作规则"""

    async def orchestrate_with_collaboration(
        self,
        context: IntentContext,
        start_node: str,
        workflow_name: Optional[str] = None
    ) -> List[IntentResult]:
        """带协作的编排"""

    def get_dashboard(self) -> str:
        """获取监控仪表板"""
```

---

### 7.2 节点 API

#### IntentNode

```python
class IntentNode(ABC):
    def __init__(self, name: str, intent_type: IntentType):
        """初始化节点"""

    @abstractmethod
    async def understand_intent(self, context: IntentContext) -> IntentType:
        """理解意图"""

    @abstractmethod
    async def execute(self, context: IntentContext) -> IntentResult:
        """执行业务逻辑"""

    async def __call__(self, context: IntentContext) -> IntentResult:
        """调用接口"""
```

#### 内置节点

- `QueryNode` - 查询节点
- `GenerateNode` - 生成节点
- `DecideNode` - 决策节点
- `CompositeNode` - 复合节点

---

### 7.3 适配器 API

#### MultimodalAdapter

```python
class MultimodalAdapter(ABC):
    @abstractmethod
    async def to_semantic(self, raw_input: Any, modality: ModalityType) -> str:
        """原始输入 → 语义表示"""

    @abstractmethod
    async def from_semantic(self, semantic: str, target_modality: ModalityType) -> Any:
        """语义表示 → 目标模态"""
```

---

### 7.4 事件与回调

#### 注册回调

```python
engine.on_execution_start(lambda ctx: print("开始执行"))
engine.on_execution_complete(lambda ctx, res: print("执行完成"))
engine.on_error(lambda ctx, err: print(f"错误: {err}"))
```

---

## 8. 最佳实践

### 8.1 节点设计原则

1. **单一职责**：每个节点只做一件事
2. **幂等性**：多次执行结果一致
3. **可观测**：清晰的日志和指标
4. **可测试**：易于单元测试

#### 示例

```python
class WellDesignedNode(IntentNode):
    def __init__(self, name: str):
        super().__init__(name, IntentType.QUERY)
        self.logger = logging.getLogger(__name__)

    async def execute(self, context: IntentContext) -> IntentResult:
        try:
            # 记录开始
            self.logger.info(f"开始执行: {context.user_input}")

            # 执行业务逻辑
            result = await self.do_work(context)

            # 记录完成
            self.logger.info(f"执行完成: {result}")

            return IntentResult(success=True, content=result, modality=ModalityType.TEXT)
        except Exception as e:
            # 记录错误
            self.logger.error(f"执行失败: {e}", exc_info=True)

            return IntentResult(success=False, content=str(e), modality=ModalityType.TEXT)
```

---

### 8.2 工作流模式

#### 模式 1：线性链式

```python
# 适用于简单流程
query → generate → end
```

#### 模式 2：条件分支

```python
# 适用于需要决策的场景
decide → [复杂 → composite, 简单 → query]
```

#### 模式 3：并行协作

```python
# 适用于需要多个节点协同的场景
query ←→ [decide, generate]
```

#### 模式 4：回环重试

```python
# 适用于需要重试的场景
execute → [成功 → end, 失败 → retry]
```

---

### 8.3 错误处理

#### 全局错误处理

```python
engine.on_error(lambda ctx, err: print(f"全局错误: {err}"))
```

#### 节点级错误处理

```python
async def execute(self, context: IntentContext) -> IntentResult:
    try:
        # 业务逻辑
        result = await self.do_work(context)
        return IntentResult(success=True, content=result, modality=ModalityType.TEXT)
    except Exception as e:
        # 错误处理
        return IntentResult(
            success=False,
            content=f"处理失败: {e}",
            modality=ModalityType.TEXT,
            next_intent=IntentType.QUERY  # 降级到查询节点
        )
```

---

### 8.4 性能调优

#### 1. 减少序列化开销

```python
# 避免频繁序列化大对象
# 推荐：传递引用
context.state["large_data"] = large_object
```

#### 2. 异步优先

```python
# 使用异步 I/O
async def execute(self, context: IntentContext) -> IntentResult:
    # 好的：异步调用
    result = await api_call_async()
    # 坏的：同步调用
    result = api_call_sync()
```

#### 3. 连接池

```python
# 复用连接
class ConnectionPoolNode(IntentNode):
    def __init__(self):
        super().__init__("pool_node", IntentType.QUERY)
        self.connection_pool = ConnectionPool(size=10)

    async def execute(self, context: IntentContext) -> IntentResult:
        conn = await self.connection_pool.acquire()
        try:
            result = await self.do_work(conn, context)
            return IntentResult(success=True, content=result, modality=ModalityType.TEXT)
        finally:
            await self.connection_pool.release(conn)
```

---

### 8.5 测试策略

#### 单元测试

```python
import pytest
from intentflow.nodes import QueryNode
from intentflow.types import IntentContext, ModalityType

@pytest.mark.asyncio
async def test_query_node():
    node = QueryNode()
    context = IntentContext(
        user_input="测试",
        input_modality=ModalityType.TEXT
    )

    result = await node(context)

    assert result.success == True
    assert result.modality == ModalityType.TEXT
```

#### 集成测试

```python
@pytest.mark.asyncio
async def test_workflow():
    engine = IntentFlow()
    engine.register_node(QueryNode())
    engine.register_node(GenerateNode())

    context = IntentContext(
        user_input="测试",
        input_modality=ModalityType.TEXT
    )

    results = await engine.orchestrate(context, "query_handler")

    assert len(results) > 0
    assert results[0].success == True
```

---

## 9. 常见问题

### 9.1 安装与配置

#### Q1: 安装失败怎么办？

**A**: 检查 Python 版本（需要 3.8+），使用虚拟环境：

```bash
python -m venv venv
source venv/bin/activate
pip install intentflow
```

#### Q2: 依赖冲突如何解决？

**A**: 使用 `pip-tools` 锁定依赖版本：

```bash
pip install pip-tools
pip-compile requirements.in
pip-sync
```

---

### 9.2 开发问题

#### Q1: 如何调试节点？

**A**: 启用详细日志：

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# 或者在节点中打印
print(f"调试信息: {context.user_input}")
```

#### Q2: 自定义节点不工作？

**A**: 检查以下几点：

1. 是否正确继承 `IntentNode`
2. 是否实现了 `understand_intent` 和 `execute` 方法
3. 是否正确注册到引擎

---

### 9.3 部署问题

#### Q1: Docker 容器无法访问网络？

**A**: 检查 Docker 网络配置：

```bash
docker network create intentflow-net
docker run --network intentflow-net intentflow-app
```

#### Q2: Kubernetes Pod 启动失败？

**A**: 查看日志：

```bash
kubectl logs <pod-name>
kubectl describe pod <pod-name>
```

---

### 9.4 性能问题

#### Q1: 执行速度慢？

**A**: 优化建议：

1. 启用缓存
2. 使用异步 I/O
3. 增加并发数
4. 使用连接池

#### Q2: 内存占用高？

**A**: 检查是否有内存泄漏：

```python
import tracemalloc
tracemalloc.start()

# 执行你的代码
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)
```

---

## 10. 生态与社区

### 10.1 插件开发

#### 创建插件

```python
# intentflow_my_plugin/__init__.py
from intentflow import IntentNode, IntentType, IntentContext, IntentResult, ModalityType

class MyPluginNode(IntentNode):
    def __init__(self):
        super().__init__("my_plugin", IntentType.QUERY)

    async def execute(self, context: IntentContext) -> IntentResult:
        # 插件逻辑
        return IntentResult(success=True, content="插件输出", modality=ModalityType.TEXT)

# setup.py
from setuptools import setup, find_packages

setup(
    name="intentflow-my-plugin",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["intentflow>=1.0.0"],
    entry_points={
        "intentflow.plugins": [
            "my_plugin = intentflow_my_plugin:MyPluginNode",
        ],
    },
)
```

#### 安装插件

```bash
pip install intentflow-my-plugin
```

---

### 10.2 贡献指南

#### 提交 PR

1. Fork 仓库
2. 创建功能分支：`git checkout -b feature/my-feature`
3. 提交更改：`git commit -m "Add my feature"`
4. 推送到分支：`git push origin feature/my-feature`
5. 创建 Pull Request

#### 代码规范

- 遵循 PEP 8
- 添加单元测试
- 更新文档
- 通过 CI 检查

---

### 10.3 社区资源

#### 官方资源

- GitHub: https://github.com/yourusername/intentflow
- 文档: https://docs.intentflow.dev
- Discord: https://discord.gg/intentflow

#### 社区贡献

- 示例项目: https://github.com/yourusername/intentflow-examples
- 插件市场: https://plugins.intentflow.dev
- 博客: https://blog.intentflow.dev

---

### 10.4 路线图

#### v1.1（规划中）

- 增强可视化工作流编辑器
- 支持更多 LLM 模型
- 性能优化

#### v2.0（长期）

- 分布式编排
- 跨语言支持（JavaScript、Go）
- 商业云服务

---

## 附录

### A. 术语表

| 术语 | 定义 |
|------|------|
| IntentNode | 意图节点，IntentFlow 的核心抽象 |
| IntentContext | 意图上下文，携带状态和信息 |
| IntentResult | 意图执行结果 |
| AdaptiveEngine | 自适应引擎，负责编排和路由 |
| MultimodalAdapter | 多模态适配器，处理不同模态的输入输出 |
| Workflow DSL | 工作流领域特定语言，用于定义复杂工作流 |

---

### B. 更新日志

#### v1.0.0（当前版本）

- ✨ 初始版本发布
- ✨ 核心功能：意图节点、自适应路由、多模态支持
- ✨ 工作流 DSL
- ✨ 可观测性系统
- 📖 完整文档

---

### C. 许可证

MIT License

Copyright (c) 2026 IntentFlow Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

### D. 致谢

感谢以下项目的启发：
- LangChain
- LangSmith
- Flowise
- n8n

感谢所有贡献者的支持！

---

**有问题？欢迎加入我们的 [Discord 社区](https://discord.gg/intentflow) 或提交 [GitHub Issue](https://github.com/yourusername/intentflow/issues)**
