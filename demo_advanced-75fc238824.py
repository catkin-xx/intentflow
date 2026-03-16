"""
IntentFlow 高级特性演示
展示复合任务、工作流 DSL、智能体协作、可观测性
"""

import asyncio
from intentflow_advanced import (
    AdvancedAdaptiveEngine, CompositeNode,
    WorkflowDSL, TelemetrySystem
)
from intentflow_nodes import QueryNode, GenerateNode, DecideNode
from intentflow_core import IntentContext, ModalityType


async def main():
    print("=" * 80)
    print("IntentFlow 高级特性演示")
    print("=" * 80)
    print()

    # 1. 创建高级引擎
    engine = AdvancedAdaptiveEngine()

    # 2. 注册所有节点（包括复合节点）
    engine.register_node(QueryNode())
    engine.register_node(GenerateNode())
    engine.register_node(DecideNode())
    engine.register_node(CompositeNode())

    print("✓ 节点注册完成：query, generate, decide, composite")
    print()

    # 3. 定义工作流 DSL
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
                    "on_failure": "query"
                },
                "query": {
                    "type": "query",
                    "on_success": "end"
                },
                "composite": {
                    "type": "composite",
                    "next": "end"
                }
            }
        }
    )

    engine.dsl.define_workflow(
        "creative_workflow",
        {
            "start": "generate",
            "nodes": {
                "generate": {
                    "type": "generate",
                    "on_success": "query"
                },
                "query": {
                    "type": "query",
                    "on_success": "end"
                }
            }
        }
    )

    print("✓ 工作流定义完成：intelligent_query, creative_workflow")
    print()

    # 4. 设置智能体协作规则
    engine.set_collaboration_rule(
        "query_handler",
        ["decide_handler"]
    )

    print("✓ 智能体协作规则设置完成：query_handler ←→ decide_handler")
    print()

    # 5. 场景演示
    scenarios = [
        {
            "name": "场景 1：使用工作流 DSL - 简单查询",
            "input": "什么是 IntentFlow？",
            "workflow": "intelligent_query"
        },
        {
            "name": "场景 2：使用工作流 DSL - 复合任务",
            "input": "这是一个复杂的任务，需要多步骤处理",
            "workflow": "intelligent_query"
        },
        {
            "name": "场景 3：创作工作流 - 图像生成 + 查询",
            "input": "画一只海滩上的猫",
            "workflow": "creative_workflow"
        },
        {
            "name": "场景 4：智能体协作 - 带协作的查询",
            "input": "分析一下当前情况",
            "use_collaboration": True
        }
    ]

    for i, scenario in enumerate(scenarios, 1):
        print("-" * 80)
        print(scenario["name"])
        print("-" * 80)
        print(f"用户输入：{scenario['input']}")
        print()

        # 创建上下文
        context = IntentContext(
            user_input=scenario["input"],
            input_modality=ModalityType.TEXT
        )

        # 执行编排
        if "workflow" in scenario:
            print(f"使用工作流：{scenario['workflow']}")
            results = await engine.orchestrate_with_collaboration(
                context,
                start_node="decide_handler",
                workflow_name=scenario["workflow"]
            )
        else:
            print("使用智能体协作模式")
            results = await engine.orchestrate_with_collaboration(
                context,
                start_node="query_handler"
            )

        # 展示结果
        print("\n执行链路：")
        for j, result in enumerate(results, 1):
            print(f"\n  步骤 {j}:")
            print(f"    成功：{'✓' if result.success else '✗'}")
            print(f"    内容：{result.content[:100]}...")
            if result.next_intent:
                print(f"    下一步意图：{result.next_intent.value}")
            if result.metadata:
                print(f"    元数据：{result.metadata}")

        print()

    # 6. 显示监控仪表板
    print("=" * 80)
    print("监控仪表板")
    print("=" * 80)
    print(engine.get_dashboard())
    print()

    # 7. 核心特性总结
    print("=" * 80)
    print("IntentFlow 四大核心特性")
    print("=" * 80)
    features = [
        {
            "feature": "意图节点抽象",
            "desc": "内置意图识别，从'执行'升级到'理解-自适应'"
        },
        {
            "feature": "多模态支持",
            "desc": "原生支持文本、图像、音频、视频的统一处理"
        },
        {
            "feature": "工作流 DSL",
            "desc": "声明式定义复杂工作流，无需硬编码"
        },
        {
            "feature": "可观测性",
            "desc": "完整的链路追踪和性能监控系统"
        }
    ]

    for feature in features:
        print(f"\n🔹 {feature['feature']}")
        print(f"   {feature['desc']}")

    print()
    print("✓ 高级特性演示完成！")


if __name__ == "__main__":
    asyncio.run(main())
