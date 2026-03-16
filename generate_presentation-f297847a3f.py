#!/usr/bin/env python3
"""
IntentFlow 演示文稿生成器
将 Markdown 幻灯片转换为多种格式（HTML、PDF、PPTX）
"""

import os
import sys
from pathlib import Path


def generate_html_slides(md_file: str, output_file: str = "IntentFlow_Slides.html"):
    """生成 HTML 幻灯片（使用 Reveal.js）"""

    reveal_js_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IntentFlow 使用指南</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/reveal.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/theme/black.min.css">
    <style>
        body {{
            font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
        }}
        .reveal h1 {{
            font-size: 2.5em;
            margin-bottom: 0.5em;
        }}
        .reveal h2 {{
            font-size: 1.8em;
            margin-bottom: 0.5em;
        }}
        .reveal h3 {{
            font-size: 1.3em;
            margin-bottom: 0.5em;
        }}
        .reveal p {{
            font-size: 1.1em;
            line-height: 1.6;
            margin-bottom: 0.8em;
        }}
        .reveal ul, .reveal ol {{
            font-size: 1.1em;
            line-height: 1.6;
            margin-bottom: 0.8em;
        }}
        .reveal pre {{
            font-size: 0.8em;
            line-height: 1.4;
            margin: 1em 0;
        }}
        .reveal code {{
            font-family: 'Fira Code', 'Consolas', monospace;
        }}
        .reveal pre code {{
            max-height: 500px;
        }}
        .reveal table {{
            font-size: 0.9em;
            border-collapse: collapse;
            margin: 1em 0;
        }}
        .reveal table th, .reveal table td {{
            border: 1px solid #666;
            padding: 0.5em;
            text-align: left;
        }}
        .reveal blockquote {{
            border-left: 4px solid #42affa;
            padding-left: 1em;
            margin: 1em 0;
            color: #ccc;
        }}
        .reveal .highlight {{
            color: #42affa;
            font-weight: bold;
        }}
        .reveal .code-block {{
            background: #1e1e1e;
            padding: 1em;
            border-radius: 8px;
            margin: 1em 0;
        }}
        .reveal .diagram {{
            font-family: 'Courier New', monospace;
            background: #2a2a2a;
            padding: 1.5em;
            border-radius: 8px;
            margin: 1em 0;
            font-size: 0.85em;
            line-height: 1.8;
        }}
    </style>
</head>
<body>
    <div class="reveal">
        <div class="slides">
"""

    # 读取 Markdown 文件
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 转换 Markdown 到 Reveal.js 格式
    lines = md_content.split('\n')
    current_slide = []
    in_code_block = False
    slide_count = 0

    for line in lines:
        line = line.rstrip()

        # 检测幻灯片分隔符
        if line.startswith('---'):
            if current_slide:
                # 生成当前幻灯片 HTML
                slide_html = convert_to_html('\n'.join(current_slide))
                reveal_js_html += slide_html
                current_slide = []
                slide_count += 1
            continue

        current_slide.append(line)

    # 最后一页
    if current_slide:
        slide_html = convert_to_html('\n'.join(current_slide))
        reveal_js_html += slide_html
        slide_count += 1

    # 添加 Reveal.js 脚本
    reveal_js_html += """
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/reveal.min.js"></script>
    <script>
        Reveal.initialize({
            hash: true,
            transition: 'slide',
            progress: true,
            center: true,
            slideNumber: true,
            width: 1200,
            height: 700,
            margin: 0.04,
            minScale: 0.2,
            maxScale: 2.0,
        });
    </script>
</body>
</html>
"""

    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(reveal_js_html)

    print(f"✓ 生成 HTML 幻灯片: {output_file}")
    print(f"  共 {slide_count} 页")
    print(f"  在浏览器中打开即可演示")


def convert_to_html(md_text: str) -> str:
    """将 Markdown 文本转换为 HTML（用于单页幻灯片）"""

    html = "<section>\n"
    lines = md_text.split('\n')

    in_code_block = False
    in_diagram = False
    in_table = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        # 代码块
        if stripped.startswith('```'):
            if not in_code_block:
                in_code_block = True
                html += '<pre class="code-block"><code>'
            else:
                in_code_block = False
                html += '</code></pre>\n'
            continue

        if in_code_block:
            # 转义 HTML 特殊字符
            escaped = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            html += escaped + '\n'
            continue

        # 标题
        if stripped.startswith('##'):
            level = len(stripped) - len(stripped.lstrip('#'))
            title = stripped.lstrip('#').strip()
            html += f'<h{level}>{title}</h{level}>\n'
        elif stripped.startswith('#'):
            title = stripped.lstrip('#').strip()
            html += f'<h2>{title}</h2>\n'

        # 列表
        elif stripped.startswith('- '):
            item = stripped[2:]
            html += f'<li>{item}</li>\n'
        elif stripped.startswith('* '):
            item = stripped[2:]
            html += f'<li>{item}</li>\n'
        elif len(stripped) > 0 and stripped[0].isdigit() and '. ' in stripped:
            # 处理数字列表
            item = stripped[stripped.index('.') + 2:]
            html += f'<li>{item}</li>\n'

        # 表格
        elif '|' in stripped:
            if not in_table:
                html += '<table>\n'
                in_table = True
            if stripped.startswith('|-'):
                continue  # 分隔线
            cells = [cell.strip() for cell in stripped.split('|')]
            cells = cells[1:-1]  # 去掉首尾空元素
            html += '<tr>\n'
            for cell in cells:
                html += f'<td>{cell}</td>\n'
            html += '</tr>\n'

        # 空行
        elif not stripped:
            if in_table:
                html += '</table>\n'
                in_table = False
            html += '<br>\n'

        # 普通段落
        else:
            if in_table:
                html += '</table>\n'
                in_table = False
            html += f'<p>{stripped}</p>\n'

    if in_table:
        html += '</table>\n'

    html += "</section>\n"
    return html


def generate_printable_guide(md_file: str, output_file: str = "IntentFlow_Printable.md"):
    """生成可打印的演示文稿（大字号、优化打印）"""

    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 添加打印友好的样式说明
    print_header = """---
# IntentFlow 演示文稿（打印版）
> **打印说明**：建议使用 A4 纸张，双面打印，每页 3 张幻灯片（布局设置）

---

"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(print_header)
        f.write(content)

    print(f"✓ 生成可打印版本: {output_file}")


def main():
    print("=" * 80)
    print("IntentFlow 演示文稿生成器")
    print("=" * 80)
    print()

    md_file = "IntentFlow_Presentation.md"

    if not os.path.exists(md_file):
        print(f"✗ 错误：找不到文件 {md_file}")
        sys.exit(1)

    # 生成 HTML 幻灯片
    print("1. 生成 HTML 幻灯片（Reveal.js）")
    generate_html_slides(md_file, "IntentFlow_Slides.html")
    print()

    # 生成可打印版本
    print("2. 生成可打印版本")
    generate_printable_guide(md_file, "IntentFlow_Printable.md")
    print()

    # 生成讲义模式（包含演讲者备注）
    print("3. 生成讲义模式")
    generate_speaker_notes(md_file, "IntentFlow_Speaker_Notes.md")
    print()

    print("=" * 80)
    print("✓ 所有文件生成完成！")
    print("=" * 80)
    print()
    print("文件列表：")
    print("  1. IntentFlow_Slides.html      - 在浏览器中演示（推荐）")
    print("  2. IntentFlow_Printable.md     - 可打印版本")
    print("  3. IntentFlow_Speaker_Notes.md - 包含演讲者备注")
    print()
    print("使用建议：")
    print("  • 在线演示：用浏览器打开 IntentFlow_Slides.html")
    print("  • 离线演示：下载后无需网络即可使用")
    print("  • 分享链接：部署到 GitHub Pages 或 Vercel")
    print()


def generate_speaker_notes(md_file: str, output_file: str):
    """生成包含演讲者备注的版本"""

    speaker_notes = {
        "封面页": """
**演讲者备注**：
- 开场白：大家好，今天我要介绍的是 IntentFlow，下一代多模态智能体编排框架
- 核心卖点：从"执行链"到"意图节点"的范式升级
- 时间：1 分钟
""",
        "目录": """
**演讲者备注**：
- 快速过一遍目录，让听众对整体结构有预期
- 重点强调：核心概念和快速上手两部分
- 时间：30 秒
""",
        "为什么需要 IntentFlow？": """
**演讲者备注**：
- 先抛出痛点，引发共鸣
- 使用表格对比，清晰直观
- 强调当前方案的局限性
- 时间：2 分钟
""",
        "核心概念解析": """
**演讲者备注**：
- 这是技术核心部分，需要讲清楚
- 使用图示展示自适应路由
- 强调"理解→决策→自适应"的循环
- 时间：3 分钟
""",
        "快速上手": """
**演讲者备注**：
- 展示 Hello World 代码
- 强调只需要 3 步就能上手
- 时间：2 分钟
""",
        "深度特性": """
**演讲者备注**：
- 展示智能体协作的威力
- 演示监控仪表板
- 强调生产级可观测性
- 时间：3 分钟
""",
        "生产环境部署": """
**演讲者备注**：
- 提供多种部署方案
- 强调灵活性：从 Docker 到 Serverless
- 时间：2 分钟
""",
        "最佳实践": """
**演讲者备注**：
- 分享经验教训
- 强调节点设计原则
- 时间：1 分钟
""",
        "Q&A": """
**演讲者备注**：
- 准备好回答常见问题
- 鼓励提问
- 时间：2 分钟
""",
        "开始使用": """
**演讲者备注**：
- 呼吁行动
- 提供明确的下一步指引
- 时间：1 分钟
""",
        "谢谢": """
**演讲者备注**：
- 感谢聆听
- 提供联系方式和资源链接
- 时间：30 秒
"""
    }

    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    output_content = content + "\n\n---\n\n# 演讲者备注\n\n"

    for section, notes in speaker_notes.items():
        output_content += f"## {section}\n{notes}\n\n"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_content)


if __name__ == "__main__":
    main()
