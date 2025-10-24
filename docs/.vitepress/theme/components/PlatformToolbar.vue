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
const showRawHtml = ref(false)
const rawHtmlContent = ref('')

const platformNames: Record<string, string> = {
  wechat: '📱 微信公众号',
  juejin: '⚡ 掘金',
  csdn: '📝 CSDN',
  zhihu: '🎓 知乎',
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
    console.error('❌ 找不到文章内容元素，检查 DOM 结构...')
    // 调试：列出主要元素
    console.log('main:', document.querySelector('main'))
    console.log('article:', document.querySelector('article'))
    console.log('prose:', document.querySelector('.prose'))
    console.log('vp-doc:', document.querySelector('.vp-doc'))
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
  console.log('✓ 格式化结果预览:', formatted.substring(0, 200))
  console.log('✓ 完整格式化内容:', formatted)
  // 也打到 window 对象方便查看
  ;(window as any).__debugFormattedContent = formatted

  // 显示预览
  previewContent.value = formatted
  previewPlatform.value = platform
  showPreview.value = true

  // 调试：也存在 window 对象上，以便查看
  ;(window as any).__platformContent = formatted
  ;(window as any).__platformContentLength = formatted.length

  console.log('✅ 预览已设置，previewContent长度:', previewContent.value.length)
  console.log('✅ 也已存储在 window.__platformContent 上')
}

const copyToClipboard = async () => {
  console.log('📋 开始复制...')

  // 获取预览 DOM 元素中的真实内容
  const previewElement = document.getElementById('preview-content')
  console.log('✓ previewElement 找到:', !!previewElement)
  console.log('✓ previewElement.innerHTML 长度:', previewElement?.innerHTML.length)

  if (!previewElement) {
    console.error('❌ 找不到预览内容元素')
    alert('找不到预览内容，请刷新页面重试')
    return
  }

  // 首先检测浏览器和系统
  const userAgent = navigator.userAgent.toLowerCase()
  const isMac = /macintosh|macintel|macppc/.test(userAgent)
  const isSafari = /safari/.test(userAgent) && !/chrome/.test(userAgent)
  console.log('🖥️ 系统: macOS?', isMac, '| Safari?', isSafari)

  // 方案 1: 复制真实的 DOM 结构（最重要！）
  // 这样粘贴时会得到格式化的 HTML，而不是纯文本
  try {
    console.log('📝 方案1: 使用 Range + Selection 复制 DOM...')

    // 选择预览元素的内容
    const range = document.createRange()
    range.selectNodeContents(previewElement)

    const selection = window.getSelection()
    if (!selection) throw new Error('无法获取 Selection')

    selection.removeAllRanges()
    selection.addRange(range)

    console.log('✓ 已选中预览内容，范围:', range.toString().length, '字符')

    // 使用 execCommand 复制选中的内容
    const successful = document.execCommand('copy')
    console.log('✓ execCommand 返回:', successful)

    selection.removeAllRanges()

    if (successful) {
      showCopySuccess()
      console.log('✅ 复制成功！（DOM Range 方案）')
      return
    } else {
      throw new Error('execCommand 返回 false')
    }
  } catch (error) {
    console.error('❌ DOM Range 方案失败:', error)
  }

  // 方案 2: 为 macOS Safari 特别优化 - 使用 textarea 但保持 HTML 格式
  if (isMac && isSafari) {
    try {
      console.log('📝 方案2-macOS: 使用 macOS Safari 特殊方案...')
      const htmlContent = previewElement.innerHTML

      // 创建可见的临时容器以便 Safari 能够正确复制
      const tempContainer = document.createElement('div')
      tempContainer.id = '__temp-copy-container'
      tempContainer.innerHTML = htmlContent
      tempContainer.style.position = 'absolute'
      tempContainer.style.left = '-10000px'
      tempContainer.style.top = '-10000px'
      tempContainer.style.width = '1px'
      tempContainer.style.height = '1px'
      tempContainer.style.overflow = 'hidden'

      document.body.appendChild(tempContainer)

      // 创建选区并复制
      const range = document.createRange()
      range.selectNodeContents(tempContainer)
      const selection = window.getSelection()
      selection.removeAllRanges()
      selection.addRange(range)

      const result = document.execCommand('copy')
      selection.removeAllRanges()
      document.body.removeChild(tempContainer)

      if (result) {
        showCopySuccess()
        console.log('✅ 复制成功！（macOS Safari 方案）')
        return
      } else {
        throw new Error('macOS Safari execCommand 失败')
      }
    } catch (error) {
      console.error('❌ macOS Safari 方案失败:', error)
    }
  }

  // 方案 3: 如果 DOM 复制失败，尝试 Blob 方式
  try {
    console.log('📝 方案3: 使用 Blob + Clipboard API...')
    const htmlContent = previewElement.innerHTML

    const blob = new Blob([htmlContent], { type: 'text/html' })
    const data = [new ClipboardItem({ 'text/html': blob })]

    await navigator.clipboard.write(data)
    showCopySuccess()
    console.log('✅ 复制成功！（Blob 方案）')
    return
  } catch (error) {
    console.error('❌ Blob 方案失败:', error)
  }

  // 方案 4: 通用降级方案 - 创建临时容器并复制
  try {
    console.log('📝 方案4: 使用临时容器 + execCommand...')

    const tempContainer = document.createElement('div')
    tempContainer.style.position = 'fixed'
    tempContainer.style.left = '-9999px'
    tempContainer.style.top = '-9999px'
    tempContainer.style.pointerEvents = 'none'
    tempContainer.style.visibility = 'hidden'

    // 复制预览元素的所有子节点（保持 DOM 结构）
    previewElement.childNodes.forEach(node => {
      const clone = node.cloneNode(true)
      tempContainer.appendChild(clone)
    })

    document.body.appendChild(tempContainer)

    const range = document.createRange()
    range.selectNodeContents(tempContainer)

    const selection = window.getSelection()
    selection?.removeAllRanges()
    selection?.addRange(range)

    const successful = document.execCommand('copy')
    selection?.removeAllRanges()
    document.body.removeChild(tempContainer)

    if (successful) {
      showCopySuccess()
      console.log('✅ 复制成功！（临时容器方案）')
      return
    } else {
      throw new Error('execCommand 返回 false')
    }
  } catch (error) {
    console.error('❌ 临时容器方案失败:', error)
  }

  // 所有方案都失败
  console.error('❌ 所有复制方案都失败了')
  console.log('系统信息:', { isMac, isSafari, userAgent: navigator.userAgent })
  alert('⚠️ 复制失败，请点击"查看HTML"按钮查看内容并手动复制。\n\n也可以尝试：\n1. 在预览窗口中选中所有文本（Ctrl+A）\n2. 按 Cmd+C（Mac）或 Ctrl+C（Windows）复制\n3. 粘贴到编辑器中')
}

const showCopySuccess = () => {
  const btn = document.querySelector('.btn-copy')
  if (!btn) return

  const originalText = btn.textContent
  btn.textContent = '✅ 已复制！'
  btn.classList.add('copied')

  setTimeout(() => {
    btn.textContent = originalText
    btn.classList.remove('copied')
  }, 2000)
}

const closePreview = () => {
  showPreview.value = false
}

const viewRawHtml = () => {
  rawHtmlContent.value = (window as any).__platformContent || previewContent.value
  showRawHtml.value = true
}

const closeRawHtml = () => {
  showRawHtml.value = false
}

// ESC 键关闭预览
onMounted(() => {
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && showPreview.value) {
      closePreview()
    }
  })
})
</script>

<template>
  <!-- 平台工具栏 -->
  <div v-if="showToolbar" class="platform-toolbar">
    <div class="toolbar-buttons">
      <button
        v-for="(name, platform) in platformNames"
        :key="platform"
        @click="formatFor(platform)"
        :class="`btn btn-${platform}`"
      >
        {{ name }}
      </button>
    </div>
    <div class="toolbar-hint">✨ 点击平台按钮预览并复制</div>
  </div>

  <!-- 预览弹窗 -->
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="showPreview" class="preview-modal-overlay" @click="closePreview">
        <div class="preview-modal" @click.stop>
          <!-- 预览头部 -->
          <div class="preview-header">
            <h3 class="preview-title">
              {{ platformNames[previewPlatform] }} 预览
            </h3>
            <div class="preview-actions">
              <button class="btn-copy" @click="copyToClipboard">
                📋 复制全文
              </button>
              <button class="btn-view-html" @click="viewRawHtml" title="查看原始HTML">
                🔍 查看HTML
              </button>
              <button class="btn-close" @click="closePreview">
                ✕
              </button>
            </div>
          </div>

          <!-- 预览内容 -->
          <div class="preview-body">
            <div id="preview-content" v-html="previewContent"></div>
          </div>

          <!-- 预览脚注 -->
          <div class="preview-footer">
            <p>💡 内容已格式化，点击"复制全文"后可直接粘贴到{{ platformNames[previewPlatform] }}编辑器</p>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>

  <!-- HTML 查看器 -->
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="showRawHtml" class="preview-modal-overlay" @click="closeRawHtml">
        <div class="preview-modal" @click.stop style="width: 95%; max-width: 1000px;">
          <div class="preview-header">
            <h3 class="preview-title">📄 原始 HTML 代码</h3>
            <button class="btn-close" @click="closeRawHtml">✕</button>
          </div>
          <div class="preview-body" style="font-family: monospace; white-space: pre-wrap; word-break: break-all; font-size: 12px;">
            {{ rawHtmlContent }}
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
/* 工具栏容器 */
.platform-toolbar {
  position: fixed;
  top: 70px;
  right: 20px;
  z-index: 1000;
  background: white;
  padding: 12px 16px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border: 1px solid #eee;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.toolbar-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.toolbar-hint {
  font-size: 12px;
  color: #999;
  text-align: right;
  white-space: nowrap;
}

/* 工具栏按钮 */
.btn {
  padding: 8px 14px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.3s ease;
  color: white;
  white-space: nowrap;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.btn:active {
  transform: translateY(0);
}

.btn-wechat {
  background: #07c160;
}

.btn-wechat:hover {
  background: #05a450;
}

.btn-juejin {
  background: #1e80ff;
}

.btn-juejin:hover {
  background: #0052cc;
}

.btn-csdn {
  background: #fc5531;
}

.btn-csdn:hover {
  background: #e63412;
}

.btn-zhihu {
  background: #0084ff;
}

.btn-zhihu:hover {
  background: #0052cc;
}

/* 预览弹窗背景 */
.preview-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  backdrop-filter: blur(2px);
}

/* 预览弹窗 */
.preview-modal {
  background: white;
  width: 100%;
  max-width: 800px;
  max-height: 90vh;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

/* 预览头部 */
.preview-header {
  padding: 16px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fafafa;
  flex-shrink: 0;
}

.preview-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.preview-actions {
  display: flex;
  gap: 8px;
}

.btn-copy {
  padding: 6px 12px;
  background: #07c160;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.3s;
}

.btn-copy:hover {
  background: #05a450;
}

.btn-copy.copied {
  background: #666;
}

.btn-view-html {
  padding: 6px 12px;
  background: #9e9e9e;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.3s;
}

.btn-view-html:hover {
  background: #757575;
}

.btn-close {
  padding: 6px 12px;
  background: #f0f0f0;
  color: #666;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.3s;
}

.btn-close:hover {
  background: #ddd;
  color: #333;
}

/* 预览内容区域 */
.preview-body {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  font-size: 15px;
  line-height: 1.6;
  color: #333;
  background: white;
}

/* 预览内容样式 */
#preview-content {
  word-wrap: break-word;
}

#preview-content h1,
#preview-content h2,
#preview-content h3,
#preview-content h4,
#preview-content h5,
#preview-content h6 {
  margin-top: 0;
  margin-bottom: 0.5em;
}

#preview-content p {
  margin-bottom: 1em;
}

#preview-content img {
  max-width: 100%;
  height: auto;
}

#preview-content code {
  font-family: Consolas, Monaco, 'Courier New', monospace;
}

#preview-content pre {
  overflow-x: auto;
  margin: 1em 0;
}

#preview-content ul,
#preview-content ol {
  margin: 1em 0;
}

#preview-content li {
  margin: 0.5em 0;
}

#preview-content table {
  border-collapse: collapse;
}

#preview-content th,
#preview-content td {
  text-align: left;
}

/* 预览脚注 */
.preview-footer {
  padding: 12px 20px;
  background: #f0f9ff;
  border-top: 1px solid #e0f0ff;
  font-size: 12px;
  color: #0066cc;
  flex-shrink: 0;
}

.preview-footer p {
  margin: 0;
}

/* 动画 */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-active .preview-modal {
  animation: slideUp 0.3s ease;
}

.modal-leave-active .preview-modal {
  animation: slideDown 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes slideDown {
  from {
    transform: translateY(0);
    opacity: 1;
  }
  to {
    transform: translateY(20px);
    opacity: 0;
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .platform-toolbar {
    top: auto;
    bottom: 20px;
    right: 10px;
    left: 10px;
    width: auto;
  }

  .toolbar-buttons {
    justify-content: center;
  }

  .btn {
    padding: 6px 10px;
    font-size: 12px;
  }

  .preview-modal {
    max-width: 95vw;
    max-height: 95vh;
  }

  .preview-body {
    padding: 15px;
    font-size: 14px;
  }
}
</style>
