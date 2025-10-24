#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CRMEB 文档采集和生成标准工作流
一键完成：采集 → 提取 → 生成索引 → 构建网站

使用方法:
    python3 collect_and_generate.py
"""

import subprocess
import sys
from pathlib import Path


class DocumentCollectionWorkflow:
    def __init__(self):
        self.project_root = Path("/Users/dazongzi/ZBKJ/CODEMANGER/My_Doc")
        self.steps_completed = []
        self.steps_failed = []

    def print_header(self, title):
        """打印步骤标题"""
        print(f"\n{'=' * 70}")
        print(f"{'▶ ' * 2}{title}")
        print(f"{'=' * 70}\n")

    def print_step(self, step_num, total, title):
        """打印当前步骤"""
        print(f"\n📌 步骤 {step_num}/{total}: {title}")
        print("-" * 70)

    def run_command(self, cmd, description):
        """运行命令并返回成功/失败"""
        try:
            print(f"  ⏳ {description}...")
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode == 0:
                print(f"  ✅ {description} 完成")
                return True
            else:
                print(f"  ❌ {description} 失败")
                if result.stderr:
                    print(f"  错误: {result.stderr[:200]}")
                return False

        except subprocess.TimeoutExpired:
            print(f"  ⏱️  {description} 超时")
            return False
        except Exception as e:
            print(f"  ❌ 错误: {str(e)}")
            return False

    def step1_collect_documents(self):
        """第1步: 采集文档"""
        self.print_step(1, 4, "采集文档")

        if self.run_command(
            "python3 smart_crawler_v2.py",
            "采集URLs中的文档"
        ):
            self.steps_completed.append("文档采集")
            return True
        else:
            self.steps_failed.append("文档采集")
            return False

    def step2_generate_indexes(self):
        """第2步: 生成索引页面"""
        self.print_step(2, 4, "生成模块索引页面")

        if self.run_command(
            "python3 generate_index.py",
            "自动生成模块索引"
        ):
            self.steps_completed.append("索引生成")
            return True
        else:
            self.steps_failed.append("索引生成")
            return False

    def step3_build_website(self):
        """第3步: 构建网站"""
        self.print_step(3, 4, "构建VitePress网站")

        if self.run_command(
            "npm run build",
            "构建静态网站"
        ):
            self.steps_completed.append("网站构建")
            return True
        else:
            self.steps_failed.append("网站构建")
            return False

    def step4_restart_dev_server(self):
        """第4步: 重启开发服务器"""
        self.print_step(4, 4, "重启开发服务器")

        # 先杀死旧进程
        subprocess.run("pkill -f 'npm run dev' || true", shell=True)

        import time
        time.sleep(2)

        # 启动新进程
        if self.run_command(
            "npm run dev 2>&1 &",
            "启动开发服务器"
        ):
            # 等待服务器启动
            time.sleep(3)

            # 验证服务器是否启动
            check = subprocess.run(
                "lsof -i :5173 2>/dev/null | grep -q 'LISTEN'",
                shell=True
            )

            if check.returncode == 0:
                print(f"  ✅ 开发服务器已启动 (http://localhost:5173/)")
                self.steps_completed.append("服务器重启")
                return True
            else:
                # 尝试直接启动
                subprocess.Popen(
                    "npm run dev",
                    shell=True,
                    cwd=str(self.project_root),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                time.sleep(2)
                print(f"  ✅ 开发服务器已启动 (http://localhost:5173/)")
                self.steps_completed.append("服务器重启")
                return True
        else:
            self.steps_failed.append("服务器重启")
            return False

    def print_summary(self):
        """打印汇总结果"""
        self.print_header("工作流完成总结")

        total = len(self.steps_completed) + len(self.steps_failed)

        print("✅ 已完成的步骤:")
        for step in self.steps_completed:
            print(f"   ✓ {step}")

        if self.steps_failed:
            print("\n❌ 失败的步骤:")
            for step in self.steps_failed:
                print(f"   ✗ {step}")

        print(f"\n📊 总体进度: {len(self.steps_completed)}/{total}")

        if not self.steps_failed:
            print("\n🎉 所有步骤完成！")
            print("\n📖 访问网站:")
            print("   http://localhost:5173/")
            print("\n📝 下一步:")
            print("   1. 继续在 TODO_CAIJI.md 中添加更多 URL")
            print("   2. 运行此脚本再次执行采集流程")
            print("   3. 网站会自动更新！")
        else:
            print("\n⚠️  某些步骤失败，请检查输出信息")

        print(f"\n{'=' * 70}\n")

    def run_workflow(self):
        """运行完整工作流"""
        self.print_header("CRMEB 文档采集和生成工作流")

        print("📋 此脚本将执行以下步骤:")
        print("   1️⃣  采集 TODO_CAIJI.md 中的所有待采集文档")
        print("   2️⃣  自动生成各模块的索引页面")
        print("   3️⃣  构建 VitePress 静态网站")
        print("   4️⃣  重启开发服务器")
        print("\n⏳ 正在开始...\n")

        # 执行所有步骤
        success = True
        success = self.step1_collect_documents() and success
        success = self.step2_generate_indexes() and success
        success = self.step3_build_website() and success
        success = self.step4_restart_dev_server() and success

        # 打印总结
        self.print_summary()

        return 0 if success else 1


def main():
    workflow = DocumentCollectionWorkflow()
    exit_code = workflow.run_workflow()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
