/**
 * 多平台内容格式化工具
 * 支持：微信公众号、掘金、CSDN、知乎
 *
 * 核心策略：
 * - 提取原始 HTML
 * - 用正则表达式应用样式
 * - 包裹在标准容器中
 * - 输出最终的完整 HTML
 */

// ============================================
// 各平台的样式定义
// ============================================

const platformStyles = {
  wechat: {
    container: 'margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 10px; padding-right: 10px; background-attachment: scroll; background-clip: border-box; background-color: rgba(0, 0, 0, 0); background-image: none; background-origin: padding-box; background-position-x: 0%; background-position-y: 0%; background-repeat: no-repeat; background-size: auto; width: auto; font-family: Optima, \'Microsoft YaHei\', PingFangSC-regular, serif; font-size: 16px; color: rgb(0, 0, 0); line-height: 1.5em; word-spacing: 0em; letter-spacing: 0em; word-break: break-word; overflow-wrap: break-word; text-align: left;',
    h1: 'margin-top: 30px; margin-bottom: 15px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; display: flex; font-size: 24px; color: rgb(7, 193, 96); line-height: 1.5em; letter-spacing: 0em; font-weight: bold;',
    h2: 'margin-top: 30px; margin-bottom: 15px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; display: flex; font-size: 22px; color: rgb(7, 193, 96); line-height: 1.5em; letter-spacing: 0em; font-weight: bold;',
    h3: 'margin-top: 30px; margin-bottom: 15px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; display: flex; font-size: 20px; color: rgb(7, 193, 96); line-height: 1.5em; letter-spacing: 0em; font-weight: bold;',
    h4: 'margin-top: 20px; margin-bottom: 10px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; display: flex; font-size: 18px; color: rgb(7, 193, 96); line-height: 1.5em; letter-spacing: 0em; font-weight: bold;',
    h5: 'margin-top: 20px; margin-bottom: 10px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; display: flex; font-size: 16px; color: rgb(7, 193, 96); line-height: 1.5em; letter-spacing: 0em; font-weight: bold;',
    h6: 'margin-top: 20px; margin-bottom: 10px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; display: flex; font-size: 14px; color: rgb(7, 193, 96); line-height: 1.5em; letter-spacing: 0em; font-weight: bold;',
    p: 'color: rgb(89, 89, 89); font-size: 15px; line-height: 1.8em; letter-spacing: 0.04em; text-align: left; text-indent: 0em; margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; padding-top: 8px; padding-bottom: 8px; padding-left: 0px; padding-right: 0px;',
    li: 'color: rgb(89, 89, 89); font-size: 15px; line-height: 1.8em; margin: 8px 0;',
    code: 'background: #f5f5f5; padding: 2px 6px; border-radius: 3px; font-family: Consolas, Monaco, monospace; color: #e74c3c; font-size: 14px;',
    pre: 'background: #f8f8f8; padding: 15px; border-radius: 5px; overflow-x: auto; border-left: 3px solid #07c160; line-height: 1.6; font-size: 13px;',
    img: 'display: block; margin-top: 10px; margin-right: auto; margin-bottom: 10px; margin-left: auto; max-width: 100%; border-top-style: none; border-bottom-style: none; border-left-style: none; border-right-style: none; border-top-width: 3px; border-bottom-width: 3px; border-left-width: 3px; border-right-width: 3px; border-top-color: rgba(0, 0, 0, 0.4); border-bottom-color: rgba(0, 0, 0, 0.4); border-left-color: rgba(0, 0, 0, 0.4); border-right-color: rgba(0, 0, 0, 0.4); border-top-left-radius: 0px; border-top-right-radius: 0px; border-bottom-right-radius: 0px; border-bottom-left-radius: 0px;',
    blockquote: 'border-left: 4px solid #07c160; padding-left: 15px; margin: 15px 0; color: #666; font-style: italic;',
    table: 'width: 100%; border-collapse: collapse; margin: 15px 0;',
    tr: 'border-bottom: 1px solid #ddd;',
    th: 'background: #f0f0f0; padding: 10px; text-align: left; font-weight: bold; color: rgb(7, 193, 96);',
    td: 'padding: 10px; border-right: 1px solid #ddd;',
    ul: 'margin: 10px 0; padding-left: 20px;',
    ol: 'margin: 10px 0; padding-left: 20px;',
  },
  juejin: {
    container: 'margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 10px; padding-right: 10px; font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif; font-size: 16px; color: rgb(37, 43, 58); line-height: 1.6em; word-break: break-word;',
    h1: 'margin-top: 30px; margin-bottom: 15px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; display: flex; font-size: 24px; color: rgb(30, 128, 255); line-height: 1.5em; letter-spacing: 0em; font-weight: bold;',
    h2: 'margin-top: 30px; margin-bottom: 15px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; display: flex; font-size: 22px; color: rgb(30, 128, 255); line-height: 1.5em; letter-spacing: 0em; font-weight: bold;',
    h3: 'margin-top: 30px; margin-bottom: 15px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; display: flex; font-size: 20px; color: rgb(30, 128, 255); line-height: 1.5em; letter-spacing: 0em; font-weight: bold;',
    h4: 'margin-top: 20px; margin-bottom: 10px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; display: flex; font-size: 18px; color: rgb(30, 128, 255); line-height: 1.5em; letter-spacing: 0em; font-weight: bold;',
    h5: 'margin-top: 20px; margin-bottom: 10px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; display: flex; font-size: 16px; color: rgb(30, 128, 255); line-height: 1.5em; letter-spacing: 0em; font-weight: bold;',
    h6: 'margin-top: 20px; margin-bottom: 10px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; display: flex; font-size: 14px; color: rgb(30, 128, 255); line-height: 1.5em; letter-spacing: 0em; font-weight: bold;',
    p: 'color: rgb(37, 43, 58); font-size: 15px; line-height: 1.8em; letter-spacing: 0em; margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; padding-top: 8px; padding-bottom: 8px; padding-left: 0px; padding-right: 0px;',
    li: 'color: rgb(37, 43, 58); font-size: 15px; line-height: 1.8em; margin: 8px 0;',
    code: 'background: #f5f5f5; padding: 2px 6px; border-radius: 3px; font-family: monospace; color: #d73a49; font-size: 14px;',
    pre: 'background: #f5f5f5; padding: 15px; border-radius: 4px; overflow-x: auto; line-height: 1.6; font-size: 13px;',
    img: 'display: block; margin-top: 10px; margin-right: auto; margin-bottom: 10px; margin-left: auto; max-width: 100%; border-radius: 4px;',
    blockquote: 'border-left: 4px solid #1e80ff; padding-left: 15px; margin: 15px 0; color: #666;',
    table: 'width: 100%; border-collapse: collapse; margin: 15px 0;',
    tr: 'border-bottom: 1px solid #ddd;',
    th: 'background: #f0f0f0; padding: 10px; text-align: left; font-weight: bold; color: rgb(30, 128, 255);',
    td: 'padding: 10px; border-right: 1px solid #ddd;',
    ul: 'margin: 10px 0; padding-left: 20px;',
    ol: 'margin: 10px 0; padding-left: 20px;',
  },
  csdn: {
    container: 'margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 10px; padding-right: 10px; font-family: \'Segoe UI\', \'Microsoft YaHei\', sans-serif; font-size: 16px; color: rgb(51, 51, 51); line-height: 1.5em; word-break: break-word;',
    h1: 'margin-top: 30px; margin-bottom: 15px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; display: flex; font-size: 24px; color: rgb(252, 85, 49); line-height: 1.5em; font-weight: bold; border-bottom: 1px solid #fc5531;',
    h2: 'margin-top: 30px; margin-bottom: 15px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; display: flex; font-size: 22px; color: rgb(252, 85, 49); line-height: 1.5em; font-weight: bold;',
    h3: 'margin-top: 30px; margin-bottom: 15px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; display: flex; font-size: 20px; color: rgb(252, 85, 49); line-height: 1.5em; font-weight: bold;',
    h4: 'margin-top: 20px; margin-bottom: 10px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; display: flex; font-size: 18px; color: rgb(252, 85, 49); line-height: 1.5em; font-weight: bold;',
    h5: 'margin-top: 20px; margin-bottom: 10px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; display: flex; font-size: 16px; color: rgb(252, 85, 49); line-height: 1.5em; font-weight: bold;',
    h6: 'margin-top: 20px; margin-bottom: 10px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; display: flex; font-size: 14px; color: rgb(252, 85, 49); line-height: 1.5em; font-weight: bold;',
    p: 'color: rgb(51, 51, 51); font-size: 15px; line-height: 1.8em; margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; padding-top: 8px; padding-bottom: 8px; padding-left: 0px; padding-right: 0px;',
    li: 'color: rgb(51, 51, 51); font-size: 15px; line-height: 1.8em; margin: 8px 0;',
    code: 'background: #f5f5f5; padding: 2px 6px; border-radius: 3px; font-family: Consolas, Monaco, monospace; color: #e74c3c; font-size: 14px;',
    pre: 'background: #f5f5f5; padding: 15px; border-radius: 4px; overflow-x: auto; line-height: 1.6; font-size: 13px;',
    img: 'display: block; margin-top: 10px; margin-right: auto; margin-bottom: 10px; margin-left: auto; max-width: 100%; border-radius: 4px;',
    blockquote: 'border-left: 4px solid #fc5531; padding-left: 15px; margin: 15px 0; color: #666;',
    table: 'width: 100%; border-collapse: collapse; margin: 15px 0;',
    tr: 'border-bottom: 1px solid #ddd;',
    th: 'background: #f0f0f0; padding: 10px; text-align: left; font-weight: bold; color: rgb(252, 85, 49);',
    td: 'padding: 10px; border-right: 1px solid #ddd;',
    ul: 'margin: 10px 0; padding-left: 20px;',
    ol: 'margin: 10px 0; padding-left: 20px;',
  },
  zhihu: {
    container: 'margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 10px; padding-right: 10px; font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif; font-size: 16px; color: rgb(26, 26, 26); line-height: 1.6em; word-break: break-word;',
    h1: 'margin-top: 30px; margin-bottom: 15px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; display: flex; font-size: 24px; color: rgb(26, 26, 26); line-height: 1.5em; font-weight: 600; border-bottom: 1px solid #ddd;',
    h2: 'margin-top: 30px; margin-bottom: 15px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; display: flex; font-size: 22px; color: rgb(26, 26, 26); line-height: 1.5em; font-weight: 600;',
    h3: 'margin-top: 30px; margin-bottom: 15px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; display: flex; font-size: 20px; color: rgb(51, 51, 51); line-height: 1.5em; font-weight: 600;',
    h4: 'margin-top: 20px; margin-bottom: 10px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; display: flex; font-size: 18px; color: rgb(85, 85, 85); line-height: 1.5em; font-weight: 600;',
    h5: 'margin-top: 20px; margin-bottom: 10px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; display: flex; font-size: 16px; color: rgb(85, 85, 85); line-height: 1.5em; font-weight: 600;',
    h6: 'margin-top: 20px; margin-bottom: 10px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; display: flex; font-size: 14px; color: rgb(85, 85, 85); line-height: 1.5em; font-weight: 600;',
    p: 'color: rgb(26, 26, 26); font-size: 15px; line-height: 1.8em; margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; padding-top: 8px; padding-bottom: 8px; padding-left: 0px; padding-right: 0px;',
    li: 'color: rgb(26, 26, 26); font-size: 15px; line-height: 1.8em; margin: 8px 0;',
    code: 'background: #f5f5f5; padding: 2px 5px; border-radius: 2px; font-family: monospace; color: #d73a49; font-size: 14px;',
    pre: 'background: #f5f5f5; padding: 15px; border-radius: 4px; overflow-x: auto; line-height: 1.6; font-size: 13px;',
    img: 'display: block; margin-top: 10px; margin-right: auto; margin-bottom: 10px; margin-left: auto; max-width: 100%; border-radius: 4px;',
    blockquote: 'border-left: 4px solid #999; padding-left: 15px; margin: 15px 0; color: #666;',
    table: 'width: 100%; border-collapse: collapse; margin: 15px 0;',
    tr: 'border-bottom: 1px solid #ddd;',
    th: 'background: #f0f0f0; padding: 10px; text-align: left; font-weight: bold; color: rgb(26, 26, 26);',
    td: 'padding: 10px; border-right: 1px solid #ddd;',
    ul: 'margin: 10px 0; padding-left: 20px;',
    ol: 'margin: 10px 0; padding-left: 20px;',
  },
}

// ============================================
// 核心格式化函数
// ============================================

function applyStylesWithRegex(html: string, styles: typeof platformStyles.wechat): string {
  let result = html

  // 为各个标签添加 style 属性（包括表格和列表标签）
  const tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'code', 'pre', 'img', 'blockquote', 'table', 'tr', 'td', 'th', 'ul', 'ol']

  tags.forEach(tag => {
    if (styles[tag as keyof typeof styles]) {
      const style = styles[tag as keyof typeof styles]
      const regex = new RegExp(`<${tag}([^>]*)>`, 'g')
      result = result.replace(regex, (match, attrs) => {
        if (attrs.includes('style=')) {
          return match
        }
        return `<${tag}${attrs} style="${style}" data-tool="markdown-nice">`
      })
    }
  })

  return result
}

// ============================================
// 各平台格式化函数
// ============================================

export function formatForWechat(htmlContent: string): string {
  let html = htmlContent
  html = applyStylesWithRegex(html, platformStyles.wechat)
  return `<section id="nice" data-tool="mdnice编辑器" data-website="https://www.mdnice.com" style="${platformStyles.wechat.container}">
${html}
</section>`
}

export function formatForJuejin(htmlContent: string): string {
  let html = htmlContent
  html = applyStylesWithRegex(html, platformStyles.juejin)
  return `<section id="nice" data-tool="mdnice编辑器" data-website="https://www.mdnice.com" style="${platformStyles.juejin.container}">
${html}
</section>`
}

export function formatForCSDN(htmlContent: string): string {
  let html = htmlContent
  html = applyStylesWithRegex(html, platformStyles.csdn)
  return `<section id="nice" data-tool="mdnice编辑器" data-website="https://www.mdnice.com" style="${platformStyles.csdn.container}">
${html}
</section>`
}

export function formatForZhihu(htmlContent: string): string {
  let html = htmlContent
  html = applyStylesWithRegex(html, platformStyles.zhihu)
  return `<section id="nice" data-tool="mdnice编辑器" data-website="https://www.mdnice.com" style="${platformStyles.zhihu.container}">
${html}
</section>`
}

// ============================================
// 辅助函数
// ============================================

export function extractPlainText(html: string): string {
  const fragment = document.createElement('div')
  fragment.innerHTML = html
  return fragment.textContent || ''
}

export function sanitizeHtml(html: string): string {
  // 移除脚本和样式
  html = html.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
  html = html.replace(/<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>/gi, '')
  // 移除危险属性
  html = html.replace(/\s*on\w+\s*=\s*[\"'][^\"']*[\"']/gi, '')
  return html
}
