# IntentFlow

**Next-Generation Multimodal Agent Orchestration Framework**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/yourusername/intentflow?style=social)](https://github.com/yourusername/intentflow)
[![GitHub Issues](https://img.shields.io/github/issues/yourusername/intentflow)](https://github.com/yourusername/intentflow/issues)

---

## 🚀 Quick Start

### Installation

```bash
pip install intentflow
```

### Hello World

```python
import asyncio
from intentflow import IntentFlow
from intentflow.nodes import QueryNode
from intentflow.types import IntentContext, ModalityType

async def main():
    engine = IntentFlow()
    engine.register_node(QueryNode())

    context = IntentContext(
        user_input="What is IntentFlow?",
        input_modality=ModalityType.TEXT
    )

    results = await engine.orchestrate(context, "query_handler")
    print(results[0].content)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## ✨ Features

### 🎯 Intent-Driven Architecture

- **IntentNode**: Core abstraction with built-in intent understanding
- **Adaptive Routing**: Dynamic decision-making based on context
- **No Hard-coding**: Routes adapt automatically to user needs

### 🌐 Native Multimodal Support

- **Text**: Natural language processing
- **Image**: Visual understanding and generation
- **Audio**: Speech recognition and synthesis
- **Video**: Video understanding and creation

### 🤖 Agent Collaboration

```python
engine.set_collaboration_rule(
    "query_handler",
    ["decide_handler", "generate_handler"]
)
```

### 📊 Full Observability

- **Execution Tracing**: Complete request lifecycle tracking
- **Performance Metrics**: Latency, success rate, error analysis
- **Real-time Dashboard**: Live monitoring of all workflows

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [User Guide](IntentFlow_User_Guide.md) | Complete usage guide |
| [Presentation](IntentFlow_Presentation.md) | Slide deck for demos |
| [Slides HTML](IntentFlow_Slides.html) | Interactive HTML slides |
| [API Reference](IntentFlow_User_Guide.md#7-api-reference) | Full API documentation |

---

## 💡 Usage Examples

### Query Node

```python
from intentflow.nodes import QueryNode

query_node = QueryNode()
context = IntentContext(
    user_input="What is LangChain?",
    input_modality=ModalityType.TEXT
)

result = await query_node(context)
print(result.content)
```

### Generate Node

```python
from intentflow.nodes import GenerateNode

generate_node = GenerateNode()
context = IntentContext(
    user_input="Generate an image of a sunset beach",
    input_modality=ModalityType.TEXT
)

result = await generate_node(context)
print(result.content)
```

### Workflow DSL

```python
engine.dsl.define_workflow(
    "intelligent_query",
    {
        "start": "decide",
        "nodes": {
            "decide": {
                "conditions": {
                    "complex": "composite",
                    "simple": "query"
                }
            }
        }
    }
)
```

---

## 🏗️ Architecture

```
User Input (Text | Image | Audio | Video)
    ↓
Intent Understanding (IntentNode)
    ↓
Adaptive Routing (Dynamic Decision)
    ↓
Agent Collaboration (Multi-node Orchestration)
    ↓
Observability Tracking (Telemetry System)
```

---

## 🆚 IntentFlow vs LangChain

| Feature | LangChain | IntentFlow |
|---------|-----------|------------|
| Core Abstraction | Chain | IntentNode |
| Routing | Static configuration | Adaptive intent recognition |
| Multimodal | Limited support | Native support |
| Orchestration | Linear chains | Dynamic graph orchestration |
| Observability | Basic logging | Complete tracing + dashboard |
| Agent Collaboration | Manual implementation | Automatic collaboration |

---

## 🛠️ Installation

### From PyPI

```bash
pip install intentflow
```

### From Source

```bash
git clone https://github.com/yourusername/intentflow.git
cd intentflow
pip install -e .
```

### Using Docker

```bash
docker pull intentflow/intentflow:latest
docker run -p 8080:8080 intentflow/intentflow
```

---

## 🚀 Deployment

### Kubernetes

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

### AWS Lambda

See [User Guide](IntentFlow_User_Guide.md#63-serverless-integration) for detailed instructions.

### Docker Compose

```bash
docker-compose up -d
```

---

## 📚 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain) for inspiring the orchestration concept
- [Flowise](https://github.com/FlowiseAI/Flowise) for the visual workflow editor idea
- [n8n](https://github.com/n8n-io/n8n) for the workflow automation patterns

---

## 📞 Support

- 📖 [Documentation](IntentFlow_User_Guide.md)
- 💬 [Discord Community](https://discord.gg/intentflow)
- 🐛 [Report Issues](https://github.com/yourusername/intentflow/issues)
- ✉️ Email: support@intentflow.dev

---

## 🔮 Roadmap

### v1.1 (Planned)
- Enhanced visual workflow editor
- Support for more LLM models
- Performance optimizations

### v2.0 (Long-term)
- Distributed orchestration
- Cross-language support (JavaScript, Go)
- Commercial cloud service

---

## ⭐ Star History

If you find IntentFlow helpful, please consider giving it a star on GitHub!

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/intentflow&type=Date)](https://star-history.com/#yourusername/intentflow&Date)

---

**Made with ❤️ by the IntentFlow community**
