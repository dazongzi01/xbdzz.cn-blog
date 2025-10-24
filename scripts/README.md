# 脚本说明

## 📁 脚本列表

### 1. filter-collected-docs.py
**功能**: 过滤未采集的文档，生成构建排除列表

**作用**:
- 读取 `TODO_CAIJI.md` 文件
- 识别所有状态为 `[✅]` 的已采集文档
- 生成排除列表，确保只有已采集的文档被构建
- 更新 VitePress 配置的 `srcExclude` 选项

**使用方法**:
```bash
# 直接运行
python3 scripts/filter-collected-docs.py

# 或使用 npm 命令
npm run filter
```

**输出**:
- `scripts/exclude-patterns.json` - 排除配置文件
- 更新 `docs/.vitepress/config.ts` - VitePress 配置

---

## 🚀 使用流程

### 采集文档
```bash
# 运行采集脚本
./caiji.sh

# 或直接运行 Python 脚本
python3 smart_crawler_three_level.py
```

### 构建文档
```bash
# 方式1: 使用自动化脚本（推荐）
./build.sh

# 方式2: 使用 npm 命令（自动过滤）
npm run build

# 方式3: 强制构建所有文档（不过滤）
npm run build:force
```

### 预览文档
```bash
npm run preview
```

---

## 📊 构建流程

```
1. 采集文档
   └─> 运行 caiji.sh
       └─> 执行 smart_crawler_three_level.py
           └─> 更新 TODO_CAIJI.md 状态为 [✅]

2. 过滤未采集文档
   └─> 运行 filter-collected-docs.py
       └─> 读取 TODO_CAIJI.md
       └─> 生成排除列表
       └─> 更新 VitePress 配置

3. 构建 HTML
   └─> 运行 vitepress build
       └─> 只构建已采集的文档（状态为 [✅]）
       └─> 输出到 docs/.vitepress/dist
```

---

## 📝 配置文件说明

### TODO_CAIJI.md
采集任务配置文件，记录所有文档的采集状态：

- `[ ]` - 未采集（不会构建）
- `[x]` - 已采集（不会构建）
- `[✅]` - 采集成功（**会构建**）
- `[❌]` - 采集失败（不会构建）

### exclude-patterns.json
过滤脚本生成的排除列表，包含：
- `collected_count` - 已采集文档数量
- `uncollected_count` - 未采集文档数量
- `exclude_patterns` - 排除模式列表
- `collected_files` - 已采集文件列表
- `uncollected_files` - 未采集文件列表

---

## ⚙️ 自定义配置

### 修改项目根目录
编辑脚本中的 `project_root` 变量：

```python
project_root = Path("/your/project/path")
```

### 修改 TODO 文件路径
```python
todo_file = project_root / "YOUR_TODO_FILE.md"
```

---

## 🔧 故障排查

### 问题1: 构建时包含了未采集的文档
**原因**: 可能没有运行过滤脚本
**解决**:
```bash
npm run filter
npm run build:force
```

### 问题2: 过滤脚本找不到文件
**原因**: 路径配置错误
**解决**: 检查 `project_root` 配置是否正确

### 问题3: VitePress 配置未更新
**原因**: 权限问题或文件被锁定
**解决**:
```bash
chmod 644 docs/.vitepress/config.ts
python3 scripts/filter-collected-docs.py
```

---

## 📖 常见用法

### 只过滤不构建
```bash
npm run filter
```

### 查看排除列表
```bash
cat scripts/exclude-patterns.json | python3 -m json.tool
```

### 清理构建缓存
```bash
rm -rf docs/.vitepress/dist
rm -rf docs/.vitepress/cache
```

---

**最后更新**: 2025-10-24
