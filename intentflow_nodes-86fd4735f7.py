"""
IntentFlow 实现节点
包含具体的意图节点实现和多模态适配器
"""

from intentflow_core import (
    IntentNode, IntentType, ModalityType,
    IntentContext, IntentResult, MultimodalAdapter
)
from typing import Optional, Any
import re


class QueryNode(IntentNode):
    """查询类意图节点：处理信息检索、问答"""

    def __init__(self, name: str = "query_handler"):
        super().__init__(name, IntentType.QUERY)
        self.knowledge_base = {
            "LangChain": "一个用于构建 LLM 应用的框架，由 Harrison Chase 于 2022 年创建",
            "IntentFlow": "下一代多模态智能体编排框架，核心抽象是意图节点",
            "GPT": "由 OpenAI 开发的大型语言模型系列",
        }

    async def understand_intent(self, context: IntentContext) -> IntentType:
        """理解是否为查询意图"""
        query_patterns = [
            r"什么是|什么是|what is|explain|解释|介绍",
            r"怎么|如何|how to|怎么用",
            r"查询|搜索|查找|search"
        ]
        text = context.user_input.lower()

        for pattern in query_patterns:
            if re.search(pattern, text):
                return IntentType.QUERY

        # 默认返回自身类型
        return IntentType.QUERY

    async def execute(self, context: IntentContext) -> IntentResult:
        """执行查询"""
        query = context.user_input

        # 简单的关键词匹配
        for key, value in self.knowledge_base.items():
            if key.lower() in query.lower():
                return IntentResult(
                    success=True,
                    content=f"📚 {key}: {value}",
                    modality=ModalityType.TEXT
                )

        return IntentResult(
            success=True,
            content=f"我理解你想查询关于「{query}」的信息，但我目前的知识库中没有相关内容。",
            modality=ModalityType.TEXT
        )


class GenerateNode(IntentNode):
    """生成类意图节点：创作内容、生成多媒体"""

    def __init__(self, name: str = "generate_handler"):
        super().__init__(name, IntentType.GENERATE)

    async def understand_intent(self, context: IntentContext) -> IntentType:
        """理解是否为生成意图"""
        generate_patterns = [
            r"生成|创建|画|写一首|write a poem|generate|create",
            r"创作|compose|design"
        ]
        text = context.user_input.lower()

        for pattern in generate_patterns:
            if re.search(pattern, text):
                return IntentType.GENERATE

        return IntentType.GENERATE

    async def execute(self, context: IntentContext) -> IntentResult:
        """执行生成"""
        request = context.user_input

        # 简单的生成逻辑（实际会调用 LLM 或图像生成模型）
        if "画" in request or "image" in request.lower():
            description = request.replace("画", "").replace("生成", "").strip()
            return IntentResult(
                success=True,
                content=f"🎨 正在生成图像：{description}\n（这是一个模拟输出，实际会调用图像生成模型）",
                modality=ModalityType.IMAGE,
                metadata={"generation_type": "image", "description": description}
            )
        elif "诗" in request or "poem" in request.lower():
            return IntentResult(
                success=True,
                content=f"📝 正在创作诗歌...\n\n题目：{request}\n\n（这是一个模拟输出，实际会调用 LLM 生成完整诗歌）",
                modality=ModalityType.TEXT,
                metadata={"generation_type": "poem"}
            )
        else:
            return IntentResult(
                success=True,
                content=f"📝 正在生成内容：{request}\n（这是一个模拟输出，实际会调用 LLM）",
                modality=ModalityType.TEXT
            )


class DecideNode(IntentNode):
    """决策类意图节点：分析、判断、路由"""

    def __init__(self, name: str = "decide_handler"):
        super().__init__(name, IntentType.DECIDE)
        self.decision_rules = {
            "复杂": IntentType.COMPOSITE,
            "简单": IntentType.QUERY,
            "创意": IntentType.GENERATE
        }

    async def understand_intent(self, context: IntentContext) -> IntentType:
        """理解是否为决策意图"""
        decide_patterns = [
            r"应该|哪个|更好|比较|recommend|should",
            r"选择|决策|分析|analyze"
        ]
        text = context.user_input.lower()

        for pattern in decide_patterns:
            if re.search(pattern, text):
                return IntentType.DECIDE

        return IntentType.DECIDE

    async def execute(self, context: IntentContext) -> IntentResult:
        """执行决策"""
        request = context.user_input

        # 简单的决策逻辑
        for keyword, next_intent in self.decision_rules.items():
            if keyword in request:
                return IntentResult(
                    success=True,
                    content=f"🤔 分析中...\n\n检测到「{keyword}」特征，建议下一步：{next_intent.value}",
                    modality=ModalityType.TEXT,
                    next_intent=next_intent
                )

        return IntentResult(
            success=True,
            content=f"🤔 正在分析：「{request}」\n（这是一个模拟输出，实际会进行深度分析）",
            modality=ModalityType.TEXT
        )


class SimpleTextAdapter(MultimodalAdapter):
    """简单的文本模态适配器"""

    async def to_semantic(self, raw_input: Any, modality: ModalityType) -> str:
        """将输入转换为语义表示"""
        if modality == ModalityType.TEXT:
            return str(raw_input)
        elif modality == ModalityType.IMAGE:
            return f"[图像输入: {raw_input}]"
        elif modality == ModalityType.AUDIO:
            return f"[音频输入: {raw_input}]"
        else:
            return str(raw_input)

    async def from_semantic(self, semantic: str, target_modality: ModalityType) -> Any:
        """从语义表示生成输出"""
        if target_modality == ModalityType.TEXT:
            return semantic
        elif target_modality == ModalityType.IMAGE:
            return f"[图像生成: {semantic}]"
        elif target_modality == ModalityType.AUDIO:
            return f"[音频生成: {semantic}]"
        else:
            return semantic
