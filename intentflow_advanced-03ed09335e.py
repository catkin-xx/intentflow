"""
IntentFlow 高级特性：智能体协作、工作流 DSL、实时可观测性
解决前面演示中的循环问题，展示真正的自适应编排
"""

import asyncio
import re
from typing import Dict, Any, List, Optional, Callable
from dataclasses import field
from intentflow_core import (
    IntentNode, IntentType, ModalityType,
    IntentContext, IntentResult, MultimodalAdapter, AdaptiveEngine
)


class CompositeNode(IntentNode):
    """复合意图节点：处理多步骤复杂任务"""

    def __init__(self, name: str = "composite_handler"):
        super().__init__(name, IntentType.COMPOSITE)
        # 定义子任务分解规则
        self.decomposition_rules = {
            r"复杂.*任务": ["decide", "plan", "execute", "review"],
            r"多步骤|流程": ["analyze", "step1", "step2", "conclude"],
            r"比较|对比": ["collect", "compare", "recommend"]
        }

    async def understand_intent(self, context: IntentContext) -> IntentType:
        """理解是否为复合意图"""
        text = context.user_input.lower()

        for pattern in self.decomposition_rules:
            if re.search(pattern, text):
                return IntentType.COMPOSITE

        return IntentType.COMPOSITE

    async def execute(self, context: IntentContext) -> IntentResult:
        """执行复合任务"""
        task = context.user_input

        # 识别任务类型
        steps = []
        task_type = "standard"

        for pattern, task_steps in self.decomposition_rules.items():
            if re.search(pattern, task):
                steps = task_steps
                task_type = pattern
                break

        if not steps:
            steps = ["analyze", "execute", "verify"]

        # 模拟多步骤执行
        execution_log = []
        for i, step in enumerate(steps, 1):
            execution_log.append(f"  ✓ 步骤 {i}: {step}")

        return IntentResult(
            success=True,
            content=f"🔄 复合任务执行中...\n任务类型：{task_type}\n\n执行步骤：\n" + "\n".join(execution_log) + f"\n\n✓ 复合任务完成",
            modality=ModalityType.TEXT,
            metadata={
                "task_type": task_type,
                "steps": steps,
                "step_count": len(steps)
            }
        )


class WorkflowDSL:
    """
    工作流 DSL（领域特定语言）
    允许用声明式方式定义工作流，而非硬编码
    """

    def __init__(self):
        self.workflows: Dict[str, Dict] = {}

    def define_workflow(self, name: str, definition: Dict):
        """
        定义工作流

        示例：
        {
            "start": "query",
            "nodes": {
                "query": {
                    "type": "query",
                    "on_success": "decide",
                    "on_failure": "fallback"
                },
                "decide": {
                    "type": "decide",
                    "conditions": {
                        "complex": "composite",
                        "simple": "end"
                    }
                },
                "composite": {
                    "type": "composite",
                    "next": "end"
                }
            }
        }
        """
        self.workflows[name] = definition

    def parse_workflow(self, name: str) -> Dict:
        """解析工作流"""
        if name not in self.workflows:
            raise ValueError(f"Workflow '{name}' not found")

        workflow = self.workflows[name]

        # 验证工作流结构
        if "start" not in workflow or "nodes" not in workflow:
            raise ValueError("Invalid workflow structure")

        return workflow


class TelemetrySystem:
    """
    可观测性系统
    提供实时监控、性能分析、错误追踪
    """

    def __init__(self):
        self.metrics: Dict[str, List[Dict]] = {
            "executions": [],
            "latencies": [],
            "errors": []
        }
        self.active_traces: Dict[str, Dict] = {}

    def start_trace(self, trace_id: str, node_name: str, context: IntentContext):
        """开始追踪"""
        self.active_traces[trace_id] = {
            "node": node_name,
            "start_time": asyncio.get_event_loop().time(),
            "input": context.user_input,
            "modality": context.input_modality.value,
            "steps": []
        }

    def end_trace(self, trace_id: str, result: IntentResult):
        """结束追踪"""
        if trace_id in self.active_traces:
            trace = self.active_traces[trace_id]
            end_time = asyncio.get_event_loop().time()
            latency = end_time - trace["start_time"]

            self.metrics["executions"].append({
                "node": trace["node"],
                "success": result.success,
                "latency": latency
            })

            self.metrics["latencies"].append(latency)

            if not result.success:
                self.metrics["errors"].append({
                    "node": trace["node"],
                    "error": result.content
                })

            del self.active_traces[trace_id]

    def get_metrics(self) -> Dict:
        """获取指标"""
        return {
            "total_executions": len(self.metrics["executions"]),
            "success_rate": sum(1 for e in self.metrics["executions"] if e["success"]) / len(self.metrics["executions"]) if self.metrics["executions"] else 0,
            "avg_latency": sum(self.metrics["latencies"]) / len(self.metrics["latencies"]) if self.metrics["latencies"] else 0,
            "error_count": len(self.metrics["errors"])
        }


class AdvancedAdaptiveEngine(AdaptiveEngine):
    """
    高级自适应引擎
    集成工作流 DSL、可观测性、智能体协作
    """

    def __init__(self):
        super().__init__()
        self.dsl = WorkflowDSL()
        self.telemetry = TelemetrySystem()
        self.collaboration_rules: Dict[str, List[str]] = {}

    def set_collaboration_rule(self, primary_node: str, collaborator_nodes: List[str]):
        """设置协作规则：定义节点间的协作关系"""
        self.collaboration_rules[primary_node] = collaborator_nodes

    async def orchestrate_with_collaboration(
        self,
        context: IntentContext,
        start_node: str,
        workflow_name: Optional[str] = None
    ) -> List[IntentResult]:
        """
        带协作功能的编排
        支持工作流定义和智能体协作
        """
        results = []
        current_node = self.nodes[start_node]
        trace_id = f"{start_node}_{asyncio.get_event_loop().time()}"

        # 开始追踪
        self.telemetry.start_trace(trace_id, start_node, context)

        try:
            # 如果指定了工作流，按工作流执行
            if workflow_name:
                workflow = self.dsl.parse_workflow(workflow_name)
                results = await self._execute_workflow(context, workflow, trace_id)
            else:
                # 否则按自适应逻辑执行
                max_steps = 10
                step = 0

                while current_node and step < max_steps:
                    # 执行当前节点
                    result = await current_node(context)
                    results.append(result)

                    # 检查是否需要协作
                    if current_node.name in self.collaboration_rules:
                        collaborator_results = await self._execute_collaborators(
                            context, current_node.name
                        )
                        results.extend(collaborator_results)

                    # 自适应路由
                    if result.next_intent and result.next_intent != current_node.intent_type:
                        current_node = self._find_node_by_intent(result.next_intent)
                    else:
                        break

                    step += 1

        finally:
            # 结束追踪
            if results:
                self.telemetry.end_trace(trace_id, results[-1])

        return results

    async def _execute_workflow(
        self,
        context: IntentContext,
        workflow: Dict,
        trace_id: str
    ) -> List[IntentResult]:
        """按工作流定义执行"""
        results = []
        current_node_name = workflow["start"]
        visited = set()

        while current_node_name and current_node_name not in visited:
            visited.add(current_node_name)

            if current_node_name not in self.nodes:
                break

            node = self.nodes[current_node_name]
            result = await node(context)
            results.append(result)

            # 根据工作流定义决定下一步
            if current_node_name in workflow["nodes"]:
                node_config = workflow["nodes"][current_node_name]

                if result.success:
                    current_node_name = node_config.get("on_success")
                else:
                    current_node_name = node_config.get("on_failure")

                # 检查条件路由
                if "conditions" in node_config and result.metadata:
                    for condition, next_node in node_config["conditions"].items():
                        if condition in str(result.metadata):
                            current_node_name = next_node
                            break
            else:
                break

        return results

    async def _execute_collaborators(
        self,
        context: IntentContext,
        primary_node_name: str
    ) -> List[IntentResult]:
        """执行协作节点"""
        results = []

        if primary_node_name in self.collaboration_rules:
            for collaborator_name in self.collaboration_rules[primary_node_name]:
                if collaborator_name in self.nodes:
                    collaborator = self.nodes[collaborator_name]
                    result = await collaborator(context)
                    results.append(result)

        return results

    def _find_node_by_intent(self, intent_type: IntentType) -> Optional[IntentNode]:
        """根据意图类型查找节点"""
        for node in self.nodes.values():
            if node.intent_type == intent_type:
                return node
        return None

    def get_dashboard(self) -> str:
        """生成监控仪表板"""
        metrics = self.telemetry.get_metrics()

        dashboard = f"""
{'=' * 80}
IntentFlow 监控仪表板
{'=' * 80}

📊 执行统计
  - 总执行次数: {metrics['total_executions']}
  - 成功率: {metrics['success_rate']:.1%}
  - 平均延迟: {metrics['avg_latency']:.3f}s
  - 错误次数: {metrics['error_count']}

🤖 智能体协作
"""
        for primary, collaborators in self.collaboration_rules.items():
            dashboard += f"  - {primary} ←→ {', '.join(collaborators)}\n"

        dashboard += f"""
📝 已注册工作流
  - 数量: {len(self.dsl.workflows)}
"""
        for name in self.dsl.workflows:
            dashboard += f"  - {name}\n"

        dashboard += "=" * 80

        return dashboard
