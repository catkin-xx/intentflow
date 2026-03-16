"""
IntentFlow:下一代多模态智能体编排框架
核心抽象：意图节点
设计哲学：从"执行链"到"理解-自适应"编排
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, TypedDict
from dataclasses import dataclass, field
from enum import Enum
import json
import asyncio


class IntentType(Enum):
    """意图类型枚举"""
    QUERY = "query"          # 查询类：检索信息、回答问题
    GENERATE = "generate"    # 生成类：创作内容、生成图像/视频
    DECIDE = "decide"        # 决策类：分析、判断、路由
    INTERACT = "interact"    # 交互类：对话、工具调用
    COMPOSITE = "composite"  # 复合类：多意图组合


class ModalityType(Enum):
    """模态类型枚举"""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    MULTIMODAL = "multimodal"


@dataclass
class IntentContext:
    """意图上下文：携带状态、历史、元数据"""
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
        self.conversation_history.append({"role": role, "content": content})


@dataclass
class IntentResult:
    """意图执行结果"""
    success: bool
    content: str
    modality: ModalityType
    next_intent: Optional[IntentType] = None
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class IntentNode(ABC):
    """
    核心抽象：意图节点
    相比 LangChain 的 Chain，IntentNode 增加了：
    1. 意图理解能力（识别用户真实需求）
    2. 自适应能力（根据上下文调整行为）
    3. 多模态支持（统一处理不同输入）
    """

    def __init__(self, name: str, intent_type: IntentType):
        self.name = name
        self.intent_type = intent_type
        self.adaptive = True  # 是否启用自适应模式

    @abstractmethod
    async def understand_intent(self, context: IntentContext) -> IntentType:
        """
        理解用户意图
        可以是简单的规则匹配，也可以是 LLM 驱动的意图识别
        """
        pass

    @abstractmethod
    async def execute(self, context: IntentContext) -> IntentResult:
        """
        执行意图
        返回结果和可能的下一步意图
        """
        pass

    async def __call__(self, context: IntentContext) -> IntentResult:
        """统一的调用接口"""
        # 1. 理解意图（如果启用了自适应）
        if self.adaptive:
            detected_intent = await self.understand_intent(context)
            # 如果检测到的意图与当前节点类型不匹配，可以动态路由
            if detected_intent != self.intent_type:
                return IntentResult(
                    success=False,
                    content=f"Intent mismatch: expected {self.intent_type}, detected {detected_intent}",
                    modality=ModalityType.TEXT,
                    next_intent=detected_intent
                )

        # 2. 执行
        return await self.execute(context)


class MultimodalAdapter(ABC):
    """
    多模态适配器：统一处理不同模态的输入
    将图像/音频/视频转换为统一的语义表示
    """

    @abstractmethod
    async def to_semantic(self, raw_input: Any, modality: ModalityType) -> str:
        """
        将原始输入转换为语义表示
        例如：图像 -> "一张日落海滩的照片"
        """
        pass

    @abstractmethod
    async def from_semantic(self, semantic: str, target_modality: ModalityType) -> Any:
        """
        从语义表示生成目标模态的输出
        例如："一只猫" -> 图像生成
        """
        pass


class AdaptiveEngine:
    """
    自适应编排引擎
    相比 LangChain 的静态链式编排，AdaptiveEngine 支持动态路由和自我调整
    """

    def __init__(self):
        self.nodes: Dict[str, IntentNode] = {}
        self.adapters: Dict[ModalityType, MultimodalAdapter] = {}

    def register_node(self, node: IntentNode):
        """注册意图节点"""
        self.nodes[node.name] = node

    def register_adapter(self, modality: ModalityType, adapter: MultimodalAdapter):
        """注册模态适配器"""
        self.adapters[modality] = adapter

    async def orchestrate(self, context: IntentContext, start_node: str) -> List[IntentResult]:
        """
        编排执行流程
        支持动态路由和自我调整
        """
        results = []
        current_node = self.nodes[start_node]
        max_steps = 10  # 防止无限循环
        step = 0

        while current_node and step < max_steps:
            # 执行当前节点
            result = await current_node(context)
            results.append(result)

            # 如果失败且检测到新意图，动态路由
            if not result.success and result.next_intent:
                # 找到匹配的节点
                for node in self.nodes.values():
                    if node.intent_type == result.next_intent:
                        current_node = node
                        break
            # 如果成功且有下一步意图，继续
            elif result.success and result.next_intent:
                for node in self.nodes.values():
                    if node.intent_type == result.next_intent:
                        current_node = node
                        break
            else:
                break

            step += 1

        return results

    def visualize_flow(self, context: IntentContext, start_node: str):
        """
        可视化执行流程
        生成流程图或描述
        """
        return f"""
IntentFlow Visualization:
Start: {start_node}
Input: {context.user_input} ({context.input_modality.value})
Available Nodes: {[node.name for node in self.nodes.values()]}
""" + "\n".join([f"- {name}: {node.intent_type.value}" for name, node in self.nodes.items()])
