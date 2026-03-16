"""
IntentFlow 节点连接可视化
展示自适应工作流如何动态构建执行链路
"""

import asyncio
from intentflow_advanced import AdvancedAdaptiveEngine
from intentflow_nodes import QueryNode, GenerateNode, DecideNode, CompositeNode
from intentflow_core import IntentContext, ModalityType, IntentType


class VisualEngine(AdvancedAdaptiveEngine):
    """带可视化输出的引擎"""

    def __init__(self):
        super().__init__()
        self.execution_trace = []  # 记录执行轨迹

    async def orchestrate_with_visualization(
        self,
        context: IntentContext,
        start_node: str,
        workflow_name=None
    ):
        """带可视化的编排"""
        self.execution_trace = []
        results = []
        current_node = self.nodes[start_node]
        step = 0

        print(f"\n{'='*80}")
        print(f"开始执行自适应工作流")
        print(f"{'='*80}")
        print(f"初始节点: {start_node}")
        print(f"用户输入: {context.user_input}")
        print()

        while current_node and step < 10:
            # 执行前快照
            snapshot = {
                "step": step + 1,
                "node": current_node.name,
                "intent": current_node.intent_type.value,
                "input": context.user_input
            }

            # 执行节点
            result = await current_node(context)
            results.append(result)

            # 记录执行轨迹
            snapshot["success"] = result.success
            snapshot["output_summary"] = result.content[:50] + "..."
            snapshot["next_intent"] = result.next_intent.value if result.next_intent else None

            # 检查协作
            if current_node.name in self.collaboration_rules:
                snapshot["collaborators"] = self.collaboration_rules[current_node.name]

            self.execution_trace.append(snapshot)

            # 可视化输出
            self._visualize_step(snapshot)

            # 路由决策
            if result.next_intent:
                next_node = self._find_node_by_intent(result.next_intent)
                if next_node:
                    print(f"    └─→ 路由到: {next_node.name} ({result.next_intent.value})")
                    current_node = next_node
                else:
                    print(f"    └─× 找不到匹配的节点，流程结束")
                    break
            else:
                print(f"    └─∎ 没有下一步，流程结束")
                break

            step += 1

        print(f"\n{'='*80}")
        print(f"执行完成，共 {len(results)} 个步骤")
        print(f"{'='*80}\n")

        return results

    def _visualize_step(self, snapshot):
        """可视化单步执行"""
        print(f"步骤 {snapshot['step']}:")
        print(f"  执行节点: {snapshot['node']} ({snapshot['intent']})")
        print(f"  输入: {snapshot['input']}")
        print(f"  结果: {'✓' if snapshot['success'] else '✗'}")

        if "collaborators" in snapshot:
            print(f"  触发协作: {', '.join(snapshot['collaborators'])}")

        print(f"  输出: {snapshot['output_summary']}")

        if snapshot['next_intent']:
            print(f"  下一步意图: {snapshot['next_intent']}")

        print()


async def demonstrate_connections():
    """演示不同的连接模式"""

    # 1. 创建引擎
    engine = VisualEngine()

    # 2. 注册节点
    query_node = QueryNode()
    generate_node = GenerateNode()
    decide_node = DecideNode()
    composite_node = CompositeNode()

    engine.register_node(query_node)
    engine.register_node(generate_node)
    engine.register_node(decide_node)
    engine.register_node(composite_node)

    print("✓ 节点注册完成")

    # 3. 设置协作规则
    engine.set_collaboration_rule("query_handler", ["decide_handler"])
    print("✓ 协作规则设置: query_handler ←→ decide_handler\n")

    # 4. 演示场景
    scenarios = [
        {
            "name": "场景 1: 简单自适应路由",
            "input": "什么是 LangChain？",
            "start": "query_handler"
        },
        {
            "name": "场景 2: 复合任务自适应",
            "input": "这是一个复杂的任务，需要多步骤处理",
            "start": "decide_handler"
        },
        {
            "name": "场景 3: 带协作的查询",
            "input": "查询一下当前状态",
            "start": "query_handler"
        }
    ]

    for scenario in scenarios:
        print(f"\n{'#'*80}")
        print(f"# {scenario['name']}")
        print(f"# {'#'*78}")
        print(f"# 输入: {scenario['input']}")
        print(f"# 起始: {scenario['start']}")
        print(f"{'#'*80}\n")

        context = IntentContext(
            user_input=scenario['input'],
            input_modality=ModalityType.TEXT
        )

        await engine.orchestrate_with_visualization(
            context,
            scenario['start']
        )

    # 5. 输出完整执行轨迹
    print(f"\n{'='*80}")
    print("完整执行轨迹汇总")
    print(f"{'='*80}\n")

    for i, trace in enumerate(engine.execution_trace, 1):
        print(f"轨迹 {i}:")
        print(f"  节点: {trace['node']} ({trace['intent']})")
        print(f"  状态: {'成功' if trace['success'] else '失败'}")
        if trace.get('next_intent'):
            print(f"  路由到: {trace['next_intent']}")
        if trace.get('collaborators'):
            print(f"  协作节点: {', '.join(trace['collaborators'])}")
        print()


async def main():
    print("=" * 80)
    print("IntentFlow 节点连接机制可视化")
    print("=" * 80)
    print()

    await demonstrate_connections()

    print("\n" + "=" * 80)
    print("总结：IntentFlow 节点连接的三大机制")
    print("=" * 80)
    print("""
1. 自适应路由（Adaptive Routing）
   - 节点返回 next_intent，引擎自动找到匹配的节点
   - 无需硬编码连接关系，根据实时上下文动态决策

2. 智能体协作（Agent Collaboration）
   - 通过 set_collaboration_rule 定义节点间的协作关系
   - 执行一个节点时，自动触发协作节点

3. 工作流 DSL（Workflow DSL）
   - 通过 define_workflow 定义静态工作流
   - 支持条件路由、失败降级等复杂逻辑

这种设计让 IntentFlow 相比 LangChain 具备更强的灵活性和自适应性。
    """)


if __name__ == "__main__":
    asyncio.run(main())
