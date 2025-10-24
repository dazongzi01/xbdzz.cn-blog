# Claude Code 项目规则

## 对话语言设置

**所有与我的对话都使用中文进行**

- 优先使用简体中文
- 代码注释可保持原语言或翻译为中文
- 变量名和函数名保持原样，不翻译
- 文档和输出信息使用中文

## 项目背景

这是一个 CRMEB 文档采集和发布系统，包含：
- VitePress 文档站点
- 多平台内容发布（WeChat, Juejin, CSDN, Zhihu）
- Web 爬虫采集系统
- 自动路径生成和分类

## 主要特性

### 1. 采集任务映射 (TODO_CAIJI.md)
- 维护采集链接的层级结构
- 支持模块和章节划分
- 自动跟踪采集进度

### 2. 自动采集爬虫 (smart_crawler_auto.py)
- 自动提取网页标题
- 智能分类和路径生成
- 完整日志和报告

### 3. 工作流程指南 (COLLECTION_WORKFLOW.md)
- 详细的使用步骤
- 常见问题解决
- 最佳实践

## 与用户沟通时

1. **代码示例**：用中文解释，代码保持原样
2. **文件操作**：详细说明文件路径和操作步骤
3. **错误处理**：用中文清晰地解释问题和解决方案
4. **技术术语**：可使用中英混合，保证清晰理解

## 常用目录

```
/Users/dazongzi/ZBKJ/CODEMANGER/My_Doc/
├── TODO_CAIJI.md              # 采集任务映射
├── COLLECTION_WORKFLOW.md     # 工作流程指南
├── AUTO_CRAWLER_GUIDE.md      # 自动爬虫指南
├── smart_crawler_auto.py      # 自动爬虫脚本
├── docs/                      # 采集结果输出
└── .claude/                   # Claude Code 配置
```
