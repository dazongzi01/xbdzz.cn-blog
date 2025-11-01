<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useData } from 'vitepress'
import {
  formatForWechat,
  formatForJuejin,
  formatForCSDN,
  formatForZhihu,
} from '../utils/formatters'

const { page } = useData()
const showToolbar = ref(false)
const previewContent = ref('')
const previewPlatform = ref('')
const showPreview = ref(false)

const platformNames: Record<string, string> = {
  wechat: '📱 微信公众号',
  juejin: '⚡ 掘金',
  csdn: '📝 CSDN',
  zhihu: '🎓 知乎',
}

const platformColors: Record<string, string> = {
  wechat: '#07c160',
  juejin: '#1e80ff',
  csdn: '#fc5531',
  zhihu: '#000000',
}

const formatters: Record<string, (content: string) => string> = {
  wechat: formatForWechat,
  juejin: formatForJuejin,
  csdn: formatForCSDN,
  zhihu: formatForZhihu,
}

onMounted(() => {
  // 检测魔法参数 ?dazongzi=666
  const params = new URLSearchParams(window.location.search)
  showToolbar.value = params.get('dazongzi') === '666'
})

const formatFor = (platform: string) => {
  console.log('📍 开始格式化，平台:', platform)

  // 尝试多种方式获取文章内容
  let articleEl = null

  // 方法1: 尝试获取 .prose 元素（VitePress 默认）
  articleEl = document.querySelector('.prose')
  console.log('✓ 方法1(.prose):', articleEl ? '找到' : '未找到')

  // 方法2: 如果没找到，尝试获取 main 下的 article
  if (!articleEl) {
    articleEl = document.querySelector('main article')
    console.log('✓ 方法2(main article):', articleEl ? '找到' : '未找到')
  }

  // 方法3: 尝试获取 .vp-doc 元素（VitePress v1.x）
  if (!articleEl) {
    articleEl = document.querySelector('.vp-doc')
    console.log('✓ 方法3(.vp-doc):', articleEl ? '找到' : '未找到')
  }

  // 方法4: 如果还是没找到，尝试获取 main 下的第一个有内容的 div
  if (!articleEl) {
    const main = document.querySelector('main')
    if (main) {
      const divs = main.querySelectorAll(':scope > div')
      console.log('✓ 方法4(main > div):', divs.length > 0 ? `找到 ${divs.length} 个 div` : '未找到')
      if (divs.length > 0) {
        articleEl = divs[0]
      }
    }
  }

  if (!articleEl) {
    console.error('❌ 找不到文章内容元素')
    alert('无法找到文章内容，请刷新页面重试')
    return
  }

  // 获取 HTML 内容
  const htmlContent = articleEl.innerHTML
  console.log('✓ 获取内容长度:', htmlContent.length, '字符')

  if (!htmlContent || htmlContent.trim().length === 0) {
    console.error('❌ 文章内容为空')
    alert('文章内容为空')
    return
  }

  // 根据平台格式化
  const formatter = formatters[platform]
  if (!formatter) {
    console.error('❌ 找不到格式化器:', platform)
    alert('找不到格式化器')
    return
  }

  console.log('📝 应用格式化器...')
  const formatted = formatter(htmlContent)
  console.log('✓ 格式化完成，长度:', formatted.length, '字符')

  // 显示预览
  previewContent.value = formatted
  previewPlatform.value = platform
  showPreview.value = true
}

const copyToClipboard = async () => {
  console.log('📋 开始复制...')

  // 获取预览 DOM 元素中的真实内容
  const previewElement = document.getElementById('preview-content')
  console.log('✓ previewElement 找到:', !!previewElement)

  if (!previewElement) {
    console.error('❌ 找不到预览内容元素')
    alert('找不到预览内容，请刷新页面重试')
    return
  }

  try {
    console.log('📝 方案1: 使用 Range + Selection 复制 DOM...')

    // 选择预览元素的内容
    const range = document.createRange()
    range.selectNodeContents(previewElement)

    // 获取当前选择并替换为我们的范围
    const selection = window.getSelection()
    if (selection) {
      selection.removeAllRanges()
      selection.addRange(range)
    }

    // 执行复制命令
    const successful = document.execCommand('copy')
    console.log('✓ 复制命令执行:', successful ? '成功' : '失败')

    if (successful) {
      // 清除选择
      if (selection) {
        selection.removeAllRanges()
      }
      alert('✅ 复制成功！可以粘贴到目标平台了')
      return
    }
  } catch (err) {
    console.error('❌ 方案1失败:', err)
  }

  // 降级方案：尝试 Clipboard API
  try {
    console.log('📝 方案2: 使用 Clipboard API...')

    // 如果浏览器支持，使用现代 API
    if (navigator.clipboard && navigator.clipboard.writeText) {
      // 获取纯文本（包含 HTML 标记）
      const htmlText = previewElement.innerHTML

      // 创建富文本格式
      const blob = new Blob([htmlText], { type: 'text/html' })
      const data = [new ClipboardItem({ 'text/html': blob })]

      // 尝试写入 HTML
      try {
        await navigator.clipboard.write(data)
        console.log('✓ HTML 已复制到剪贴板')
        alert('✅ 复制成功！可以粘贴到目标平台了')
        return
      } catch (err) {
        console.warn('⚠️ 无法复制 HTML，尝试纯文本...', err)
        // 回退到纯文本
        await navigator.clipboard.writeText(htmlText)
        alert('✅ 已复制（纯文本格式）')
        return
      }
    }
  } catch (err) {
    console.error('❌ Clipboard API 失败:', err)
  }

  alert('复制失败，请手动复制预览内容')
}

const closePreview = () => {
  showPreview.value = false
}
</script>

<template>
  <!-- 平台工具栏 -->
  <div v-if="showToolbar" class="platform-toolbar">
    <div class="toolbar-header">📢 一键复制到多平台</div>
    <div class="toolbar-buttons">
      <button
        v-for="(name, key) in platformNames"
        :key="key"
        class="platform-btn"
        :style="{ borderColor: platformColors[key] }"
        @click="formatFor(key)"
      >
        {{ name }}
      </button>
    </div>
  </div>

  <!-- 预览窗口 -->
  <div v-if="showPreview" class="preview-modal">
    <div class="preview-container">
      <!-- 标题栏 -->
      <div class="preview-header">
        <div class="preview-title">
          {{ platformNames[previewPlatform] }} 预览
        </div>
        <button class="close-btn" @click="closePreview">✕</button>
      </div>

      <!-- 预览内容 -->
      <div class="preview-content-wrapper">
        <div id="preview-content" class="preview-content" v-html="previewContent"></div>
      </div>

      <!-- 底部操作栏 -->
      <div class="preview-footer">
        <button class="copy-btn" @click="copyToClipboard">
          📋 复制全文
        </button>
        <div class="preview-tips">
          ✨ 复制后直接粘贴到 {{ platformNames[previewPlatform] }} 编辑器即可
        </div>
      </div>
    </div>
  </div>

  <!-- 背景遮罩 -->
  <div v-if="showPreview" class="preview-overlay" @click="closePreview"></div>
</template>

<style scoped>
/* 工具栏样式 */
.platform-toolbar {
  position: fixed;
  top: 70px;
  right: 20px;
  z-index: 900;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  padding: 12px;
  min-width: 280px;
}

.toolbar-header {
  font-size: 13px;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
  text-align: center;
}

.toolbar-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.platform-btn {
  padding: 8px 12px;
  border: 2px solid;
  border-radius: 6px;
  background: white;
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.platform-btn:hover {
  background: #f0f0f0;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 预览窗口 */
.preview-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
  width: 85%;
  max-width: 800px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

.preview-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #e5e7eb;
  background: #f9fafb;
}

.preview-title {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #6b7280;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #e5e7eb;
  color: #1f2937;
}

.preview-content-wrapper {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: white;
}

.preview-content {
  line-height: 1.6;
  color: #374151;
  font-size: 14px;
}

/* 预览内容样式 */
:deep(.preview-content h1),
:deep(.preview-content h2),
:deep(.preview-content h3),
:deep(.preview-content h4),
:deep(.preview-content h5),
:deep(.preview-content h6) {
  margin-top: 20px;
  margin-bottom: 12px;
}

:deep(.preview-content p) {
  margin-bottom: 12px;
}

:deep(.preview-content code) {
  background: #f3f4f6;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
}

:deep(.preview-content pre) {
  background: #1f2937;
  color: #f3f4f6;
  padding: 12px;
  border-radius: 6px;
  overflow-x: auto;
  margin: 12px 0;
}

:deep(.preview-content pre code) {
  background: none;
  color: inherit;
  padding: 0;
}

:deep(.preview-content blockquote) {
  border-left: 4px solid #d1d5db;
  padding-left: 12px;
  margin: 12px 0;
  color: #6b7280;
  font-style: italic;
}

:deep(.preview-content table) {
  width: 100%;
  border-collapse: collapse;
  margin: 12px 0;
}

:deep(.preview-content th),
:deep(.preview-content td) {
  border: 1px solid #e5e7eb;
  padding: 8px 12px;
  text-align: left;
}

:deep(.preview-content th) {
  background: #f3f4f6;
  font-weight: 600;
}

.preview-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-top: 1px solid #e5e7eb;
  background: #f9fafb;
}

.copy-btn {
  padding: 10px 20px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
}

.copy-btn:hover {
  background: #2563eb;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.copy-btn:active {
  transform: translateY(0);
}

.preview-tips {
  font-size: 12px;
  color: #6b7280;
}

/* 背景遮罩 */
.preview-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

/* 响应式 */
@media (max-width: 768px) {
  .platform-toolbar {
    top: auto;
    bottom: 20px;
    right: 10px;
    left: 10px;
    max-width: none;
  }

  .preview-modal {
    width: 95%;
    max-height: 90vh;
  }
}
</style>
