# Contributing to IntentFlow

Thank you for your interest in contributing to IntentFlow! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)

---

## 🤝 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other contributors

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- pip

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/intentflow.git
cd intentflow

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

### Verify Installation

```bash
python -c "from intentflow import IntentFlow; print('Success!')"
```

---

## 🔧 Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Changes

- Write clean, readable code
- Follow coding standards (see below)
- Add tests for new features
- Update documentation

### 3. Test Your Changes

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=. --cov-report=html

# Run linter
flake8 .
black --check .
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: add new feature"
# or
git commit -m "fix: resolve issue #123"
```

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then go to GitHub and create a Pull Request.

---

## 📝 Coding Standards

### Python Code Style

We follow PEP 8 with some modifications:

```python
# Good
async def execute(self, context: IntentContext) -> IntentResult:
    """Execute the intent."""
    return IntentResult(
        success=True,
        content="Hello",
        modality=ModalityType.TEXT
    )

# Bad
async def execute(self, context):
    return IntentResult(success=True, content="Hello", modality=ModalityType.TEXT)
```

### Naming Conventions

- **Classes**: `PascalCase` (e.g., `IntentNode`)
- **Functions**: `snake_case` (e.g., `execute`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`)
- **Private members**: `_leading_underscore` (e.g., `_internal_method`)

### Type Hints

All public APIs should include type hints:

```python
from typing import List, Optional

def orchestrate(
    self,
    context: IntentContext,
    start_node: str
) -> List[IntentResult]:
    """Orchestrate the workflow."""
    pass
```

### Documentation

Every public function/class should have a docstring:

```python
class IntentNode:
    """
    Core abstraction for IntentFlow.

    An IntentNode represents a single executable unit with built-in
    intent understanding capabilities.

    Attributes:
        name: Node name for identification
        intent_type: Type of intent this node handles
        adaptive: Whether to enable adaptive mode
    """

    async def execute(self, context: IntentContext) -> IntentResult:
        """
        Execute the intent.

        Args:
            context: The intent context with user input and metadata

        Returns:
            IntentResult: The execution result with content and status

        Raises:
            ValueError: If context is invalid
        """
        pass
```

---

## 🧪 Testing

### Test Structure

```
tests/
├── __init__.py
├── test_core.py
├── test_nodes.py
├── test_adapters.py
└── test_integration.py
```

### Writing Tests

```python
import pytest
from intentflow import IntentFlow
from intentflow.nodes import QueryNode
from intentflow.types import IntentContext, ModalityType

@pytest.mark.asyncio
async def test_query_node():
    """Test QueryNode execution."""
    node = QueryNode()
    context = IntentContext(
        user_input="test",
        input_modality=ModalityType.TEXT
    )

    result = await node(context)

    assert result.success == True
    assert result.modality == ModalityType.TEXT
    assert "test" in result.content.lower()
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_nodes.py

# Run with coverage
pytest --cov=. --cov-report=html

# Run with verbose output
pytest -v
```

### Test Requirements

- All new features must have tests
- Test coverage should not decrease
- All tests must pass before merging

---

## 📚 Documentation

### Documentation Structure

```
docs/
├── api-reference.md
├── tutorials/
│   ├── quick-start.md
│   └── advanced-features.md
└── guides/
    ├── deployment.md
    └── best-practices.md
```

### Writing Documentation

- Use clear, concise language
- Include code examples
- Add diagrams where helpful
- Keep it up to date

### Markdown Style

```markdown
# Heading 1

## Heading 2

### Heading 3

**Bold text**
*Italic text*
`Code inline`

```
Code block
```

- List item 1
- List item 2

| Table Header 1 | Table Header 2 |
|---------------|---------------|
| Cell 1        | Cell 2        |

> Blockquote

[Link text](https://example.com)
```

---

## 📤 Submitting Changes

### Pull Request Checklist

Before submitting a PR, ensure:

- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] New tests added (if applicable)
- [ ] Documentation updated
- [ ] Commit messages follow conventional commits
- [ ] PR description is clear and comprehensive

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Test additions or changes
- `chore`: Maintenance tasks

**Examples:**

```
feat(core): add adaptive routing

Implement dynamic routing based on intent detection.
Nodes can now return next_intent to control flow.

Closes #123
```

```
fix(nodes): resolve memory leak in QueryNode

Fix issue where query results were not being cleaned up
properly, causing memory to accumulate over time.

Fixes #456
```

### PR Description Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Fixes #123
Related to #456

## How Has This Been Tested?
- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated
```

---

## 🏷️ Release Process

Releases are managed by maintainers using semantic versioning:

1. Increment version in `__version__.py`
2. Update CHANGELOG.md
3. Create git tag: `git tag v1.0.0`
4. Push tag: `git push origin v1.0.0`
5. Create GitHub Release

---

## 🆘 Getting Help

If you need help:

- 📖 Check the [documentation](README.md#-documentation)
- 💬 Join our [Discord](https://discord.gg/intentflow)
- 🐛 Open an [issue](https://github.com/yourusername/intentflow/issues)
- ✉️ Email: support@intentflow.dev

---

## 📜 Legal

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to IntentFlow!** 🎉
