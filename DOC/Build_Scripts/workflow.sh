#!/bin/bash

###############################################################################
# 文章写作自动化工作流 - 主控制脚本
# 用法：bash workflow.sh {command} {article-name} [options]
###############################################################################

set -euo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 路径配置
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WORKFLOW_DIR="${SCRIPT_DIR}/.claude/workflow"
WORK_DIR="${SCRIPT_DIR}/.claude/work"  # 临时工作目录
DOCS_DIR="${SCRIPT_DIR}/docs/01_初步了解"  # 最终输出目录
PHASES_DIR="${WORKFLOW_DIR}/phases"
CONFIG_DIR="${WORKFLOW_DIR}/config"
TEMPLATES_DIR="${WORKFLOW_DIR}/templates"

# 检查Python环境
check_python() {
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}✗ 错误：未找到Python 3${NC}"
        exit 1
    fi
}

# 打印信息
log_info() {
    echo -e "${BLUE}ℹ ${1}${NC}"
}

log_success() {
    echo -e "${GREEN}✓ ${1}${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠ ${1}${NC}"
}

log_error() {
    echo -e "${RED}✗ ${1}${NC}"
}

# 打印帮助信息
print_help() {
    cat << 'EOF'

📝 文章写作自动化工作流

用法：bash workflow.sh {command} {article-name} [options]

命令：
  init <article-name>          初始化新文章
    选项：
      --title "标题"            文章标题
      --audiences "受众1,受众2" 目标受众（逗号分隔）
      --style "风格"            写作风格

  run <article-name>           运行完整工作流（所有5个阶段）
    选项：
      --phase N                 只运行第N个阶段
      --from N                  从第N个阶段开始
      --verbose                 显示详细输出

  phase <article-name> N        运行特定阶段（N=1-5）

  resume <article-name>         从上次中断处继续

  status <article-name>         显示文章进度状态

  validate <article-name>       验证文章完整性

  publish <article-name>        发布文章到docs目录

  clean <article-name>          清理工作文件

  list                         列出所有文章

选项：
  --verbose, -v               显示详细日志
  --dry-run                   模拟运行，不实际执行
  --help, -h                  显示此帮助信息

示例：
  # 初始化新文章
  bash workflow.sh init crmeb-intro --title "CRMEB系统简介" --audiences "技术,运营,产品"

  # 运行完整工作流
  bash workflow.sh run crmeb-intro

  # 只运行第2个阶段
  bash workflow.sh phase crmeb-intro 2

  # 从第3个阶段继续
  bash workflow.sh run crmeb-intro --from 3

  # 查看进度
  bash workflow.sh status crmeb-intro

  # 发布文章
  bash workflow.sh publish crmeb-intro

EOF
}

# 检查文章是否存在
check_article_exists() {
    local article_name=$1
    if [ ! -d "${ARTICLES_DIR}/${article_name}" ]; then
        log_error "文章目录不存在：${article_name}"
        log_info "请先运行：bash workflow.sh init ${article_name}"
        exit 1
    fi
}

# 初始化新文章
init_article() {
    local article_name=$1
    shift

    # 解析参数
    local title=""
    local audiences="技术人员,运营人员,产品经理"
    local style="俏皮有趣，专业准确"

    while [[ $# -gt 0 ]]; do
        case $1 in
            --title) title="$2"; shift 2 ;;
            --audiences) audiences="$2"; shift 2 ;;
            --style) style="$2"; shift 2 ;;
            *) shift ;;
        esac
    done

    # 如果没有提供标题，使用文章名
    if [ -z "$title" ]; then
        title="${article_name}"
    fi

    # 创建目录结构
    mkdir -p "${ARTICLES_DIR}/${article_name}/logs"

    # 创建配置文件
    cat > "${ARTICLES_DIR}/${article_name}/config.json" << EOJSON
{
  "article_name": "${article_name}",
  "title": "${title}",
  "audiences": [$(echo "$audiences" | sed 's/,/","/g' | sed 's/^/"/;s/$/"/')],
  "writing_style": "${style}",
  "created_at": "$(date -u +'%Y-%m-%dT%H:%M:%SZ')",
  "target_word_count": 5000,
  "required_illustrations": 4
}
EOJSON

    # 创建初始状态文件
    cat > "${ARTICLES_DIR}/${article_name}/status.json" << EOJSON
{
  "article_name": "${article_name}",
  "title": "${title}",
  "created_at": "$(date -u +'%Y-%m-%dT%H:%M:%SZ')",
  "updated_at": "$(date -u +'%Y-%m-%dT%H:%M:%SZ')",
  "phases": {
    "phase1": {"status": "pending", "output": "01-planning.md"},
    "phase2": {"status": "pending", "output": "02-draft.md"},
    "phase3": {"status": "pending", "output": "03-guidelines.md"},
    "phase4": {"status": "pending", "output": "04-checklist.md"},
    "phase5": {"status": "pending", "output": "05-final.md"}
  },
  "quality_score": null,
  "published": false,
  "logs": "logs/execution.log"
}
EOJSON

    # 创建原始输入文件
    cat > "${ARTICLES_DIR}/${article_name}/00-raw-input.md" << EOMD
# ${title}

在这里粘贴你的原始内容、大纲或笔记。

系统将自动：
1. 分析和规划内容结构
2. 生成完整的初稿
3. 创建配图制作指南
4. 生成排版优化清单
5. 创建发布检查清单

---

## 你的内容从这里开始

（替换这个部分为你的原始内容）

EOMD

    log_success "文章已初始化：${article_name}"
    log_info "下一步："
    echo "  1. 编辑文件：${ARTICLES_DIR}/${article_name}/00-raw-input.md"
    echo "  2. 运行工作流：bash workflow.sh run ${article_name}"
}

# 显示进度状态
show_status() {
    local article_name=$1
    check_article_exists "$article_name"

    local config_file="${ARTICLES_DIR}/${article_name}/config.json"
    local status_file="${ARTICLES_DIR}/${article_name}/status.json"

    if [ ! -f "$status_file" ]; then
        log_error "进度文件不存在"
        exit 1
    fi

    # 使用Python读取JSON并显示
    python3 << EOPY
import json
from pathlib import Path

config = json.load(open('${config_file}'))
status = json.load(open('${status_file}'))

print(f"\n📄 文章：{config['title']}")
print(f"📅 创建时间：{config['created_at']}")

completed = sum(1 for p in status['phases'].values() if p['status'] == 'completed')
total = len(status['phases'])

print(f"📊 进度：{completed}/{total} 完成")
print(f"\n阶段状态：")

for phase_name, phase_info in status['phases'].items():
    phase_num = phase_name.replace('phase', '')
    symbol = "✅" if phase_info['status'] == 'completed' else ("⏳" if phase_info['status'] == 'in_progress' else "⭕")
    print(f"  {symbol} Phase {phase_num}: {phase_info['status']}")

if status.get('quality_score'):
    print(f"\n⭐ 质量评分：{status['quality_score']}/100")

EOPY
}

# 运行完整工作流
run_workflow() {
    local article_name=$1
    shift

    check_article_exists "$article_name"

    # 解析参数
    local start_phase=1
    local end_phase=5
    local verbose=0

    while [[ $# -gt 0 ]]; do
        case $1 in
            --from) start_phase="$2"; shift 2 ;;
            --phase) start_phase="$2"; end_phase="$2"; shift 2 ;;
            --verbose|-v) verbose=1; shift ;;
            *) shift ;;
        esac
    done

    log_info "开始工作流：${article_name}"
    echo ""

    # 运行各个阶段
    for phase in $(seq $start_phase $end_phase); do
        log_info "======================================="
        log_info "运行 Phase ${phase}..."
        log_info "======================================="

        run_phase "$article_name" "$phase" "$verbose"

        echo ""
    done

    log_success "工作流完成！"
    show_status "$article_name"
}

# 运行单个阶段
run_phase() {
    local article_name=$1
    local phase=$2
    local verbose=$3

    check_article_exists "$article_name"

    local phase_script="${PHASES_DIR}/phase${phase}-*.py"

    # 查找对应的脚本
    local script=$(ls ${phase_script} 2>/dev/null | head -1)

    if [ -z "$script" ]; then
        log_error "找不到Phase ${phase}的脚本"
        exit 1
    fi

    local log_file="${ARTICLES_DIR}/${article_name}/logs/phase${phase}.log"

    # 运行Python脚本
    python3 "$script" \
        --article "${article_name}" \
        --work-dir "${ARTICLES_DIR}/${article_name}" \
        --config "${ARTICLES_DIR}/${article_name}/config.json" \
        $([ "$verbose" = "1" ] && echo "--verbose") \
        2>&1 | tee "$log_file"

    if [ ${PIPESTATUS[0]} -eq 0 ]; then
        log_success "Phase ${phase} 完成"

        # 更新状态文件
        update_phase_status "$article_name" "$phase" "completed"
    else
        log_error "Phase ${phase} 失败，详见日志：$log_file"
        update_phase_status "$article_name" "$phase" "failed"
        exit 1
    fi
}

# 更新阶段状态
update_phase_status() {
    local article_name=$1
    local phase=$2
    local status=$3

    python3 << EOPY
import json
from datetime import datetime

status_file = '${ARTICLES_DIR}/${article_name}/status.json'
with open(status_file, 'r') as f:
    data = json.load(f)

phase_key = f'phase${phase}'
data['phases'][phase_key]['status'] = '${status}'
data['phases'][phase_key]['completed_at'] = datetime.utcnow().isoformat() + 'Z'
data['updated_at'] = datetime.utcnow().isoformat() + 'Z'

with open(status_file, 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

EOPY
}

# 发布文章
publish_article() {
    local article_name=$1
    check_article_exists "$article_name"

    local work_dir="${ARTICLES_DIR}/${article_name}"
    local final_file="${work_dir}/05-final.md"
    local config_file="${work_dir}/config.json"

    if [ ! -f "$final_file" ]; then
        log_error "最终文件不存在：$final_file"
        log_info "请先运行完整工作流：bash workflow.sh run ${article_name}"
        exit 1
    fi

    # 获取标题
    local title=$(grep '^# ' "$final_file" | head -1 | sed 's/^# //')
    local target_file="${DOCS_DIR}/${article_name}.md"

    # 复制文件
    cp "$final_file" "$target_file"

    # 更新状态
    python3 << EOPY
import json

status_file = '${work_dir}/status.json'
with open(status_file, 'r') as f:
    data = json.load(f)

data['published'] = True
data['published_at'] = '$(date -u +'%Y-%m-%dT%H:%M:%SZ')'
data['published_to'] = '${target_file}'

with open(status_file, 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

EOPY

    log_success "文章已发布"
    log_info "位置：${target_file}"
}

# 列出所有文章
list_articles() {
    if [ ! -d "$ARTICLES_DIR" ]; then
        log_warning "还没有创建过文章"
        return
    fi

    echo ""
    echo "📚 现有文章列表："
    echo ""

    for article_dir in "${ARTICLES_DIR}"/*; do
        if [ -d "$article_dir" ]; then
            article_name=$(basename "$article_dir")
            config_file="${article_dir}/config.json"
            status_file="${article_dir}/status.json"

            if [ -f "$config_file" ] && [ -f "$status_file" ]; then
                python3 << EOPY
import json
config = json.load(open('${config_file}'))
status = json.load(open('${status_file}'))
completed = sum(1 for p in status['phases'].values() if p['status'] == 'completed')
total = len(status['phases'])
print(f"  • {config['title']:<40} [{completed}/{total}] {'✅' if status['published'] else '⭕'}")
EOPY
            fi
        fi
    done

    echo ""
}

# 主程序入口
main() {
    check_python

    if [ $# -eq 0 ]; then
        print_help
        exit 0
    fi

    local command=$1
    shift

    case $command in
        init)
            [ $# -lt 1 ] && { log_error "缺少参数：article-name"; exit 1; }
            init_article "$@"
            ;;
        run)
            [ $# -lt 1 ] && { log_error "缺少参数：article-name"; exit 1; }
            run_workflow "$@"
            ;;
        phase)
            [ $# -lt 2 ] && { log_error "缺少参数：article-name phase-number"; exit 1; }
            run_phase "$1" "$2" 0
            ;;
        resume)
            [ $# -lt 1 ] && { log_error "缺少参数：article-name"; exit 1; }
            article_name=$1
            check_article_exists "$article_name"
            # 找出第一个未完成的阶段
            start_phase=$(python3 << EOPY
import json
status = json.load(open('.claude/articles/${article_name}/status.json'))
for i in range(1, 6):
    if status['phases'][f'phase{i}']['status'] != 'completed':
        print(i)
        break
else:
    print(6)
EOPY
)
            if [ "$start_phase" -lt 6 ]; then
                run_workflow "$article_name" --from "$start_phase"
            else
                log_success "所有阶段都已完成"
            fi
            ;;
        status)
            [ $# -lt 1 ] && { log_error "缺少参数：article-name"; exit 1; }
            show_status "$1"
            ;;
        publish)
            [ $# -lt 1 ] && { log_error "缺少参数：article-name"; exit 1; }
            publish_article "$1"
            ;;
        list)
            list_articles
            ;;
        -h|--help|help)
            print_help
            ;;
        *)
            log_error "未知命令：$command"
            print_help
            exit 1
            ;;
    esac
}

# 运行主程序
main "$@"
