import { defineConfig } from 'vitepress'
import { readFileSync, existsSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'

// 博客侧边栏由 vault 的发布脚本生成（blog-sidebar.json）。
// 文件不存在时降级为空数组，保证 build 不会因此失败。
const __dir = dirname(fileURLToPath(import.meta.url))
const sidebarFile = resolve(__dir, 'blog-sidebar.json')
const blogSidebar = existsSync(sidebarFile)
  ? JSON.parse(readFileSync(sidebarFile, 'utf-8'))
  : []

export default defineConfig({
  title: '大粽子',
  description: '电商全链路实战：支付接入、多端交付、后端性能、AI 落地。所有步骤都自己跑过一遍。',

  ignoreDeadLinks: true,

  // SEO：生成 sitemap.xml，供搜索引擎和 AI 爬虫发现全站内容
  sitemap: {
    hostname: 'https://xbdzz.cn'
  },


  head: [
    ['meta', { name: 'viewport', content: 'width=device-width, initial-scale=1.0' }],
    ['link', { rel: 'icon', href: '/logo.svg' }]
  ],

  themeConfig: {
    logo: '/logo.svg',

    nav: [
      { text: '首页', link: '/' },
      { text: '博客', link: '/blog/' },
    ],

    sidebar: {
      // 由发布脚本生成，不要手改
      '/blog/': blogSidebar,
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/dazongzi01/xbdzz.cn-blog' }
    ],

    footer: {
      message: '大粽子',
      copyright: ''
    },

    search: {
      provider: 'local'
    },

    docFooter: {
      prev: '上一页',
      next: '下一页'
    },

    outline: {
      label: '页面导航'
    }
  },

  markdown: {
    lineNumbers: true,
    theme: 'github-dark',
    breaks: true
  }
})
