"""
IntentFlow 演示：多模态智能体编排实战
展示意图理解、自适应路由、动态编排的核心能力
"""

import asyncio
from intentflow_core import (
    AdaptiveEngine, IntentContext, IntentType, ModalityType
)
from intentflow_nodes import (
    QueryNode, GenerateNode, DecideNode, SimpleTextAdapter
)


async def main():
    print("=" * 80)
    print("IntentFlow: 下一代多模态智能体编排框架")
    print("核心抽象：意图节点（Intent Node）")
    print("=" * 80)
    print()

    # 1. 创建自适应引擎
    engine = AdaptiveEngine()

    # 2. 注册意图节点
    query_node = QueryNode()
    generate_node = GenerateNode()
    decide_node = DecideNode()

    engine.register_node(query_node)
    engine.register_node(generate_node)
    engine.register_node(decide_node)

    # 3. 注册多模态适配器
    text_adapter = SimpleTextAdapter()
    engine.register_adapter(ModalityType.TEXT, text_adapter)

    print("✓ 框架初始化完成")
    print("  - 已注册节点：query_handler, generate_handler, decide_handler")
    print("  - 已注册适配器：text_adapter")
    print()

    # 4. 运行多个场景演示
    scenarios = [
        {
            "name": "场景 1：查询类意图",
            "input": "什么是 LangChain？",
            "modality": ModalityType.TEXT,
            "start_node": "query_handler"
        },
        {
            "name": "场景 2：生成类意图（图像）",
            "input": "画一只在海滩上看日落的猫",
            "modality": ModalityType.TEXT,
            "start_node": "generate_handler"
        },
        {
            "name": "场景 3：决策类意图 -> 自适应路由",
            "input": "这是一个复杂的任务，应该选择哪种方式处理？",
            "modality": ModalityType.TEXT,
            "start_node": "decide_handler"
        },
        {
            "name": "场景 4：意图不匹配 -> 动态路由",
            "input": "生成一首关于春天的诗",
            "modality": ModalityType.TEXT,
            "start_node": "query_handler"  # 故意从错误的节点开始
        }
    ]

    for scenario in scenarios:
        print("-" * 80)
        print(scenario["name"])
        print("-" * 80)
        print(f"用户输入：{scenario['input']}")
        print(f"输入模态：{scenario['modality'].value}")
        print(f"起始节点：{scenario['start_node']}")
        print()

        # 创建上下文
        context = IntentContext(
            user_input=scenario["input"],
            input_modality=scenario["modality"]
        )

        # 执行编排
        results = await engine.orchestrate(context, scenario["start_node"])

        # 展示结果
        print("执行结果：")
        for i, result in enumerate(results, 1):
            print(f"\n  步骤 {i}:")
            print(f"    成功：{'✓' if result.success else '✗'}")
            print(f"    内容：{result.content}")
            print(f"    输出模态：{result.modality.value}")
            if result.next_intent:
                print(f"    下一步意图：{result.next_intent.value}")
            if result.metadata:
                print(f"    元数据：{result.metadata}")

        print()

    # 5. 可视化框架
    print("=" * 80)
    print("框架可视化")
    print("=" * 80)
    context = IntentContext(
        user_input="演示输入",
        input_modality=ModalityType.TEXT
    )
    print(engine.visualize_flow(context, "query_handler"))
    print()

    # 6. 核心优势对比
    print("=" * 80)
    print("IntentFlow vs LangChain 核心优势")
    print("=" * 80)
    advantages = [
        ["特性", "LangChain", "IntentFlow"],
        ["核心抽象", "链", "意图节点"],
        ["意图理解", "无", "内置"],
        ["自适应路由", "有限", "强"],
        ["多模态支持", "有限", "原生"],
        ["编排方式", "静态配置", "动态自适应"],
        ["场景适配", "文本为主", "多模态智能体"]
    ]

    for row in advantages:
        print(f"{row[0]:<15} | {row[1]:<20} | {row[2]:<20}")

    print()
    print("✓ 演示完成！IntentFlow 框架已成功实现")
    print()


if __name__ == "__main__":
    asyncio.run(main())
