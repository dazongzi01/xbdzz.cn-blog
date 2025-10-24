#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
模块索引页面生成器
根据采集的文档内容自动生成 index.md
"""

import os
import re
from pathlib import Path


class IndexGenerator:
    def __init__(self):
        self.docs_path = Path("/Users/dazongzi/ZBKJ/CODEMANGER/My_Doc/docs")

    def extract_title_and_description(self, markdown_file):
        """从Markdown文件中提取标题和核心内容"""
        try:
            with open(markdown_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 提取第一个h1标题
            title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else "文档"

            # 提取核心内容部分的要点
            core_section = re.search(
                r'## 📋 核心内容\s*\n((?:- .+\n?)+)',
                content
            )

            key_points = []
            if core_section:
                points_text = core_section.group(1)
                points = re.findall(r'- (.+)', points_text)
                # 过滤掉Vue模板占位符，取前4个有效要点
                key_points = [
                    p.strip() for p in points
                    if p.strip() and not p.strip().startswith('{{')
                ][:4]

            return {
                'title': title,
                'key_points': key_points
            }

        except Exception as e:
            print(f"❌ 提取文件失败 {markdown_file}: {str(e)}")
            return {'title': '文档', 'key_points': []}

    def get_module_docs(self, module_path):
        """获取模块下的所有文档（排除index.md）"""
        docs = []
        module_dir = self.docs_path / module_path

        if not module_dir.exists():
            return docs

        # 获取所有.md文件，排除index.md
        md_files = sorted([
            f for f in module_dir.glob('*.md')
            if f.name != 'index.md' and not f.name.startswith('.')
        ])

        for i, md_file in enumerate(md_files, 1):
            doc_name = md_file.stem  # 文件名不含.md
            info = self.extract_title_and_description(md_file)

            docs.append({
                'number': i,
                'filename': md_file.name,
                'doc_name': doc_name,
                'title': info['title'],
                'key_points': info['key_points']
            })

        return docs

    def generate_index_markdown(self, module_path, module_title):
        """生成模块索引页面"""
        docs = self.get_module_docs(module_path)

        if not docs:
            print(f"⚠️  模块 {module_path} 下没有文档")
            return None

        # 构建Markdown内容
        markdown = f"# {module_title}\n\n"

        # 简介
        markdown += f"本模块包含与 {module_title} 相关的 {len(docs)} 个文档。\n\n"

        # 已有文档列表
        markdown += "## 📋 本模块已有的文档\n\n"

        for doc in docs:
            # 文档链接
            markdown += f"### {doc['number']}. [{doc['title']}](./{doc['filename']}) ✅\n"

            # 核心内容描述
            if doc['key_points']:
                for point in doc['key_points']:
                    markdown += f"- {point}\n"
            else:
                # 当没有有效的key_points时，使用默认描述
                markdown += f"- 查看 {doc['title']} 了解详情\n"

            markdown += "\n"

        # 学习路径
        markdown += "## 🎯 学习路径\n\n"
        markdown += "```\n"
        markdown += f"开始学习 {module_title}\n"
        markdown += "    ↓\n"

        for doc in docs:
            markdown += f"{doc['number']}️⃣ {doc['title']}\n"
            markdown += "    ↓\n"

        markdown += f"✅ 完成 {module_title}！\n"
        markdown += "```\n\n"

        # 推荐阅读顺序
        markdown += "## 💡 推荐阅读顺序\n\n"
        markdown += "| 顺序 | 文档 | 内容 |\n"
        markdown += "|------|------|------|\n"

        for doc in docs:
            if doc['key_points']:
                key_point = doc['key_points'][0]
            else:
                key_point = f"查看 {doc['title']} 的详细内容"
            markdown += f"| {doc['number']} | {doc['title']} | {key_point} |\n"

        markdown += "\n"

        # 下一步
        markdown += "## ➡️ 下一步\n\n"
        markdown += "完成本模块学习后，您可以：\n\n"
        markdown += "- 返回 [首页](/) 查看其他模块\n"
        markdown += "- 根据需要深入学习相关模块\n"
        markdown += "- 访问 [API文档](/06_API文档/) 了解开发接口\n\n"

        markdown += "---\n\n"
        markdown += f"**本页面由智能生成器自动创建，基于实际采集的文档内容。**\n"

        return markdown

    def save_index(self, module_path, content):
        """保存索引文件"""
        index_file = self.docs_path / module_path / "index.md"

        try:
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✅ 已生成: {index_file}")
            return True

        except Exception as e:
            print(f"❌ 保存失败 {index_file}: {str(e)}")
            return False

    def generate_all_modules(self):
        """生成所有模块的索引页面"""
        modules = [
            ('01_快速开始', '快速开始'),
            ('02_系统配置', '系统配置'),
            ('03_商城功能', '商城功能'),
            ('04_商户管理', '商户管理'),
            ('05_交易订单', '交易订单'),
            ('06_API文档', 'API文档'),
        ]

        print("=" * 70)
        print("🚀 模块索引页面生成器启动")
        print("=" * 70)

        success_count = 0

        for module_path, module_title in modules:
            print(f"\n📝 生成: {module_title}")

            markdown = self.generate_index_markdown(module_path, module_title)

            if markdown:
                if self.save_index(module_path, markdown):
                    success_count += 1
            else:
                print(f"⏭️  跳过: {module_path} (没有文档或生成失败)")

        print(f"\n{'=' * 70}")
        print(f"✅ 生成完成！")
        print(f"   成功: {success_count}/{len(modules)}")
        print(f"   请运行 'npm run build' 来重新生成网站")
        print("=" * 70)


def main():
    generator = IndexGenerator()
    generator.generate_all_modules()


if __name__ == "__main__":
    main()
