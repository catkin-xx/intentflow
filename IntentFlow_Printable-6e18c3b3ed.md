---
# IntentFlow 演示文稿（打印版）
> **打印说明**：建议使用 A4 纸张，双面打印，每页 3 张幻灯片（布局设置）

---

# IntentFlow 使用指南演示文稿

---

## 封面页

**IntentFlow**
### 下一代多模态智能体编排框架

从"执行链"到"意图节点"的范式升级

---

## 目录

1. **为什么需要 IntentFlow**
2. **核心概念解析**
3. **快速上手**
4. **深度特性**
5. **生产环境部署**
6. **最佳实践**
7. **Q&A**

---

## 1. 为什么需要 IntentFlow？

### 当前痛点

| 问题 | 表现 |
|------|------|
| **路由僵化** | LangChain 需要硬编码连接关系 |
| **多模态困难** | 文本、图像、音频需要分别处理 |
| **可观测性弱** | 难以追踪复杂工作流 |
| **协作成本高** | 智能体间协作需要大量手动代码 |

---

## 1. 为什么需要 IntentFlow？

### IntentFlow 的解决方案

```
┌─────────────┐
│  用户输入   │  文本 | 图像 | 音频 | 视频
└──────┬──────┘
       │
       ↓
┌─────────────────────┐
│   意图节点理解      │  ← 核心：自适应意图识别
└──────┬──────────────┘
       │
       ↓
┌─────────────────────┐
│   自适应路由        │  ← 动态决策，无需硬编码
└──────┬──────────────┘
       │
       ↓
┌─────────────────────┐
│   智能体协作        │  ← 自动触发协作节点
└──────┬──────────────┘
       │
       ↓
┌─────────────────────┐
│   可观测性追踪      │  ← 完整链路监控
└─────────────────────┘
```

---

## 1. 为什么需要 IntentFlow？

### 对比 LangChain

| 特性 | LangChain | IntentFlow |
|------|-----------|------------|
| **核心抽象** | Chain（链） | IntentNode（意图节点） |
| **路由方式** | 静态配置 | 自适应意图识别 |
| **多模态** | 有限支持 | 原生支持 |
| **编排方式** | 线性链式 | 动态图状编排 |
| **可观测性** | 基础日志 | 完整链路追踪 |
| **智能体协作** | 手动实现 | 自动协作 |

---

## 2. 核心概念解析

### 意图节点（IntentNode）

**定义**：IntentFlow 的最小执行单元，内置意图理解能力

**核心方法**：

```python
class IntentNode:
    async def understand_intent(context) -> IntentType:
        """理解用户意图"""
        pass

    async def execute(context) -> IntentResult:
        """执行业务逻辑"""
        pass
```

**设计理念**：
- 理解 → 决策 → 自适应

---

## 2. 核心概念解析

### 意图类型

```python
class IntentType(Enum):
    QUERY      = "query"      # 查询类
    GENERATE   = "generate"   # 生成类
    DECIDE     = "decide"     # 决策类
    INTERACT   = "interact"   # 交互类
    COMPOSITE  = "composite"  # 复合类
```

### 模态类型

```python
class ModalityType(Enum):
    TEXT       = "text"       # 文本
    IMAGE      = "image"      # 图像
    AUDIO      = "audio"      # 音频
   VIDEO      = "video"      # 视频
    MULTIMODAL = "multimodal" # 多模态
```

---

## 2. 核心概念解析

### 上下文管理

```python
@dataclass
class IntentContext:
    user_input: str
    input_modality: ModalityType
    conversation_history: List[Dict]
    state: Dict[str, Any]
    metadata: Dict[str, Any]

    def update_state(key, value):
        """更新状态"""

    def add_to_history(role, content):
        """添加对话历史"""
```

**作用**：携带整个工作流的上下文信息

---

## 2. 核心概念解析

### 自适应路由

```
用户输入："分析并决定下一步"
         ↓
    [DecideNode]
         ↓
   理解意图：复杂任务
         ↓
   返回 next_intent = COMPOSITE
         ↓
   自动路由到 [CompositeNode]
         ↓
   执行复合任务
```

**优势**：无需硬编码路由逻辑

---

## 2. 核心概念解析

### 工作流 DSL

**定义复杂工作流**：

```python
engine.dsl.define_workflow(
    "intelligent_query",
    {
        "start": "decide",
        "nodes": {
            "decide": {
                "conditions": {
                    "复杂": "composite",
                    "简单": "query"
                }
            }
        }
    }
)
```

**优势**：声明式、可读性强

---

## 3. 快速上手

### 安装方式

**方式 1：PyPI 安装**
```bash
pip install intentflow
```

**方式 2：Docker**
```bash
docker pull intentflow/intentflow:latest
docker run -p 8080:8080 intentflow/intentflow
```

**依赖要求**：
- Python 3.8+
- asyncio 运行时

---

## 3. 快速上手

### Hello World

```python
from intentflow import IntentFlow
from intentflow.nodes import QueryNode
from intentflow.types import IntentContext, ModalityType

engine = IntentFlow()
engine.register_node(QueryNode())

context = IntentContext(
    user_input="什么是 IntentFlow？",
    input_modality=ModalityType.TEXT
)

results = await engine.orchestrate(context, "query_handler")
print(results[0].content)
```

**输出**：
```
📚 IntentFlow: 多模态智能体编排框架
```

---

## 3. 快速上手

### 第一个多模态应用

```python
context = IntentContext(
    user_input="生成一张海滩日落的图片",
    input_modality=ModalityType.TEXT
)

results = await engine.orchestrate(context, "generate_handler")
print(results[0].content)
```

**输出**：
```
🎨 正在生成图像：海滩日落的图片
模态: image
```

---

## 4. 深度特性

### 智能体协作

**定义协作关系**：

```python
engine.set_collaboration_rule(
    "query_handler",
    ["decide_handler", "generate_handler"]
)
```

**执行时自动触发**：
```
[QueryNode] 执行完成
    ↓
  自动触发
    ↓
[DecideNode] ←→ [GenerateNode]
```

**优势**：无需手动编排

---

## 4. 深度特性

### 可观测性系统

**实时监控执行链路**：

```python
engine = AdvancedAdaptiveEngine()

results = await engine.orchestrate_with_collaboration(
    context, start_node
)

# 获取指标
metrics = engine.telemetry.get_metrics()
print(f"成功率: {metrics['success_rate']:.1%}")
print(f"平均延迟: {metrics['avg_latency']:.3f}s")
```

---

## 4. 深度特性

### 监控仪表板

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

## 5. 生产环境部署

### Docker 容器化

**Dockerfile**：
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

**构建与运行**：
```bash
docker build -t intentflow-app .
docker run -p 8080:8080 intentflow-app
```

---

## 5. 生产环境部署

### Kubernetes 部署

**deployment.yaml**：
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
```

---

## 5. 生产环境部署

### Serverless 集成

**AWS Lambda**：
```python
def lambda_handler(event, context):
    intent_context = IntentContext(
        user_input=event.get("input", ""),
        input_modality=ModalityType(event.get("modality", "text"))
    )

    results = await engine.orchestrate(intent_context, "query_handler")

    return {
        "statusCode": 200,
        "body": {"results": [r.content for r in results]}
    }
```

---

## 6. 最佳实践

### 节点设计原则

1. **单一职责**：每个节点只做一件事
2. **幂等性**：多次执行结果一致
3. **可观测**：清晰的日志和指标
4. **可测试**：易于单元测试

### 错误处理

```python
try:
    result = await self.do_work(context)
    return IntentResult(success=True, content=result)
except Exception as e:
    logger.error(f"执行失败: {e}")
    return IntentResult(success=False, content=str(e))
```

---

## 6. 最佳实践

### 性能优化

| 优化策略 | 说明 |
|----------|------|
| **异步优先** | 使用 `async/await` |
| **连接池** | 复用数据库/API 连接 |
| **缓存** | 缓存重复查询结果 |
| **并发执行** | 使用 `asyncio.gather` |

### 测试策略

```python
@pytest.mark.asyncio
async def test_query_node():
    node = QueryNode()
    context = IntentContext(
        user_input="测试",
        input_modality=ModalityType.TEXT
    )
    result = await node(context)
    assert result.success == True
```

---

## 7. Q&A

### 常见问题

**Q1: IntentFlow 与 LangChain 的主要区别？**

**A**: IntentFlow 的核心是"意图节点"，支持自适应路由和原生多模态；LangChain 的核心是"执行链"，需要硬编码路由逻辑。

**Q2: 如何自定义节点？**

**A**: 继承 `IntentNode`，实现 `understand_intent` 和 `execute` 方法，然后注册到引擎。

**Q3: 生产环境如何部署？**

**A**: 推荐 Docker + Kubernetes 或 Serverless（AWS Lambda、阿里云函数计算）。

**Q4: 性能如何优化？**

**A**: 启用缓存、使用异步 I/O、增加并发数、使用连接池。

---

## 7. Q&A

### 更多资源

| 资源类型 | 链接 |
|----------|------|
| **GitHub** | https://github.com/yourusername/intentflow |
| **文档** | https://docs.intentflow.dev |
| **Discord** | https://discord.gg/intentflow |
| **示例** | https://github.com/yourusername/intentflow-examples |

---

## 8. 开始使用 IntentFlow

### 三步上手

1. **安装**
   ```bash
   pip install intentflow
   ```

2. **创建第一个应用**
   ```python
   from intentflow import IntentFlow
   engine = IntentFlow()
   ```

3. **加入社区**
   - Discord: https://discord.gg/intentflow
   - GitHub: https://github.com/yourusername/intentflow

---

## 谢谢！

### 感兴趣吗？

- 📖 阅读 [完整使用指南](IntentFlow_User_Guide.md)
- 💻 查看 [示例代码](intentflow_core.py)
- 🚀 开始 [构建你的应用](demo_intentflow.py)

---

## 附录

### 技术栈

- **核心**：Python 3.8+, asyncio
- **依赖**：pydantic, aiohttp
- **可选**：transformers, pillow, pydub

### 开源协议

MIT License

### 贡献者

欢迎贡献！查看 [CONTRIBUTING.md](CONTRIBUTING.md)

---

**有问题？欢迎联系：**

- GitHub Issues: https://github.com/yourusername/intentflow/issues
- Discord: https://discord.gg/intentflow
- Email: support@intentflow.dev
