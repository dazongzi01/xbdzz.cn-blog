#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
过滤未采集的文档 - 用于构建前清理
- 读取 TODO_CAIJI.md 找出未采集的文档
- 生成排除列表用于 VitePress 构建
- 只输出已采集成功的文档（状态为 [✅]）
- 动态生成侧边栏菜单（只包含已采集的文档）

使用方法:
    python3 scripts/filter-collected-docs.py
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime


def parse_todo_file(todo_file):
    """解析 TODO_CAIJI.md 文件，提取文档路径和状态"""
    collected_files = []  # 已采集的文件
    uncollected_files = []  # 未采集的文件

    with open(todo_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_task = None
    current_status = None
    current_path = None

    for line in lines:
        line = line.strip()

        # 检测任务标题 #### ### xxx
        if line.startswith('#### ###'):
            # 保存上一个任务
            if current_path:
                if current_status == '[✅]':
                    collected_files.append(current_path)
                else:
                    uncollected_files.append(current_path)

            # 重置
            current_task = line
            current_status = None
            current_path = None

        # 提取状态
        elif line.startswith('- 采集状态:'):
            status_match = re.search(r'\[([ x✅❌])\]', line)
            if status_match:
                status_char = status_match.group(1)
                if status_char == '✅':
                    current_status = '[✅]'
                elif status_char == 'x':
                    current_status = '[x]'
                else:
                    current_status = '[ ]'

        # 提取输出路径
        elif line.startswith('- 输出路径:'):
            path_match = re.search(r'`([^`]+)`', line)
            if path_match:
                current_path = path_match.group(1)

    # 处理最后一个任务
    if current_path:
        if current_status == '[✅]':
            collected_files.append(current_path)
        else:
            uncollected_files.append(current_path)

    return collected_files, uncollected_files


def generate_exclude_patterns(uncollected_files, project_root):
    """生成 VitePress 排除模式"""
    exclude_patterns = []

    for file_path in uncollected_files:
        # 转换为相对于 docs 目录的路径
        if file_path.startswith('docs/'):
            rel_path = file_path[5:]  # 去掉 'docs/' 前缀
            exclude_patterns.append(rel_path)

    return exclude_patterns


def generate_sidebar_config(collected_files):
    """根据已采集的文档生成侧边栏配置"""
    # 按模块分组
    modules = {}

    for file_path in collected_files:
        if not file_path.startswith('docs/'):
            continue

        # 解析路径: docs/01_快速开始/1_快速开始/01_系统简介.md
        parts = file_path.replace('docs/', '').split('/')

        if len(parts) >= 3:
            module = parts[0]  # 01_快速开始
            chapter = parts[1]  # 1_快速开始
            filename = parts[2]  # 01_系统简介.md

            if module not in modules:
                modules[module] = {}

            if chapter not in modules[module]:
                modules[module][chapter] = []

            # 生成菜单项
            doc_name = filename.replace('.md', '')
            link = f"/{module}/{chapter}/{doc_name}"  # 去掉 .md 后缀

            modules[module][chapter].append({
                'name': doc_name,
                'link': link
            })

    return modules


def generate_vitepress_config(exclude_patterns, collected_files):
    """生成完整的 VitePress 配置文件"""

    modules = generate_sidebar_config(collected_files)

    # 生成排除列表
    exclude_list = ""
    if exclude_patterns:
        exclude_list = "  srcExclude: [\n"
        for pattern in exclude_patterns:
            exclude_list += f"    '{pattern}',\n"
        exclude_list += "  ],\n\n"

    # 生成导航栏（只包含有文档的模块）
    nav_items = ["      { text: '首页', link: '/' },"]
    for module in sorted(modules.keys()):
        module_name = module.split('_', 1)[1] if '_' in module else module
        nav_items.append(f"      {{ text: '{module_name}', link: '/{module}/' }},")
    nav_config = "\n".join(nav_items)

    # 生成侧边栏
    sidebar_items = []
    for module, chapters in sorted(modules.items()):
        module_name = module.split('_', 1)[1] if '_' in module else module

        sidebar_items.append(f"      '/{module}/': [")
        sidebar_items.append(f"        {{")
        sidebar_items.append(f"          text: '{module_name}',")
        sidebar_items.append(f"          items: [")

        for chapter, docs in sorted(chapters.items()):
            chapter_name = chapter.split('_', 1)[1] if '_' in chapter else chapter
            sidebar_items.append(f"            {{")
            sidebar_items.append(f"              text: '{chapter_name}',")
            sidebar_items.append(f"              items: [")

            for doc in sorted(docs, key=lambda x: x['name']):
                doc_title = doc['name'].split('_', 1)[1] if '_' in doc['name'] else doc['name']
                sidebar_items.append(f"                {{ text: '{doc_title}', link: '{doc['link']}' }},")

            sidebar_items.append(f"              ]")
            sidebar_items.append(f"            }},")

        sidebar_items.append(f"          ]")
        sidebar_items.append(f"        }}")
        sidebar_items.append(f"      ],")

    sidebar_config = "\n".join(sidebar_items)

    # 生成完整配置
    config = f"""import {{ defineConfig }} from 'vitepress'

export default defineConfig({{
  title: 'CRMEB Java 文档',
  description: 'Java 多商户商城系统完整文档',

  ignoreDeadLinks: true,

{exclude_list}  head: [
    ['meta', {{ name: 'viewport', content: 'width=device-width, initial-scale=1.0' }}],
    ['link', {{ rel: 'icon', href: '/logo.svg' }}]
  ],

  themeConfig: {{
    logo: '/logo.svg',

    nav: [
{nav_config}
    ],

    sidebar: {{
{sidebar_config}
    }},

    socialLinks: [
      {{ icon: 'github', link: 'https://github.com' }}
    ],

    footer: {{
      message: 'CRMEB Java 多商户商城系统',
      copyright: 'Copyright © 2024 CRMEB. All rights reserved.'
    }},

    search: {{
      provider: 'local'
    }},

    docFooter: {{
      prev: '上一页',
      next: '下一页'
    }},

    outline: {{
      label: '页面导航'
    }}
  }},

  markdown: {{
    lineNumbers: true,
    theme: 'github-dark',
    breaks: true
  }}
}})
"""

    return config


def main():
    project_root = Path("/Users/dazongzi/ZBKJ/CODEMANGER/My_Doc")
    todo_file = project_root / "TODO_CAIJI.md"
    config_file = project_root / "docs" / ".vitepress" / "config.ts"
    docs_dir = project_root / "docs"

    print("====================================")
    print("   🔍 过滤未采集的文档")
    print("====================================\n")

    if not todo_file.exists():
        print(f"❌ 错误: {todo_file} 不存在")
        return

    # 解析 TODO 文件
    print("📖 正在读取采集任务...")
    collected_files, uncollected_files = parse_todo_file(todo_file)

    print(f"  ✅ 已采集: {len(collected_files)} 个文档")
    print(f"  ⏭️  未采集: {len(uncollected_files)} 个文档\n")

    if uncollected_files:
        print("📝 未采集的文档列表:")
        for file_path in uncollected_files[:10]:  # 只显示前10个
            print(f"  - {file_path}")
        if len(uncollected_files) > 10:
            print(f"  ... 还有 {len(uncollected_files) - 10} 个\n")
        print()

    # 生成排除模式
    print("🔧 生成排除配置...")
    exclude_patterns = generate_exclude_patterns(uncollected_files, project_root)

    # 输出到 JSON 文件供其他工具使用
    exclude_file = project_root / "scripts" / "exclude-patterns.json"
    exclude_file.parent.mkdir(parents=True, exist_ok=True)

    with open(exclude_file, 'w', encoding='utf-8') as f:
        json.dump({
            'collected_count': len(collected_files),
            'uncollected_count': len(uncollected_files),
            'exclude_patterns': exclude_patterns,
            'collected_files': collected_files,
            'uncollected_files': uncollected_files
        }, f, ensure_ascii=False, indent=2)

    print(f"  ✅ 排除配置已保存: {exclude_file}\n")

    # 生成并写入 VitePress 配置
    if config_file.exists() or True:  # 总是生成
        print("📝 生成 VitePress 配置...")
        config_content = generate_vitepress_config(exclude_patterns, collected_files)

        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(config_content)

        print(f"  ✅ 已更新 VitePress 配置（排除列表 + 动态侧边栏）\n")

    print("====================================")
    print("   ✅ 配置完成")
    print("====================================")
    print(f"\n📊 统计:")
    print(f"  - 将构建: {len(collected_files)} 个文档")
    print(f"  - 将跳过: {len(uncollected_files)} 个文档")
    print("\n💡 现在可以运行构建命令了:")
    print("   npm run build")
    print()


if __name__ == "__main__":
    main()
