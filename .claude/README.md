# Claude Code 配置目录

这个目录包含 Claude Code 项目的配置文件。

## 文件说明

### config.json
项目的基础配置，包含：
- 语言设置：中文 (zh-CN)
- 对话语言：中文

### rules.md
项目规则和通信标准：
- **对话语言**：所有对话都使用简体中文
- **项目背景**：CRMEB 文档采集和发布系统
- **主要特性**：采集系统、爬虫、自动路径生成
- **常用目录**：项目结构说明

### settings.local.json
本地设置文件

### todos.md
项目待办事项

## 使用说明

这些配置文件会被 Claude Code 自动加载，您不需要手动修改它们，除非需要：

1. **更改对话语言**：编辑 `config.json` 中的 `language` 字段
2. **更新项目规则**：编辑 `rules.md` 文件
3. **修改本地设置**：编辑 `settings.local.json`

## 关键配置项

✅ **对话语言**：中文 (Simplified Chinese)
✅ **编码**：UTF-8
✅ **时区**：中国 (Asia/Shanghai)
✅ **文档风格**：中文技术文档

## 相关项目文件

- `TODO_CAIJI.md` - 采集任务映射文件
- `COLLECTION_WORKFLOW.md` - 采集工作流程指南
- `AUTO_CRAWLER_GUIDE.md` - 自动爬虫使用指南
- `smart_crawler_auto.py` - 智能自动爬虫脚本

---

**最后更新**：2025-10-24
