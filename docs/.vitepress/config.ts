import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'CRMEB Java 文档',
  description: 'Java 多商户商城系统完整文档',

  ignoreDeadLinks: true,

  srcExclude: [
    '06_API文档/04_用户接口.md',
  ],

  head: [
    ['meta', { name: 'viewport', content: 'width=device-width, initial-scale=1.0' }],
    ['link', { rel: 'icon', href: '/logo.svg' }]
  ],

  themeConfig: {
    logo: '/logo.svg',

    nav: [
      { text: '首页', link: '/' },
      { text: '初步了解', link: '/docs/01_初步了解/index' },
    ],

    sidebar: {
      '/docs/01_初步了解/': [
        {
          text: '初步了解',
          items: [
            { text: '快速了解', link: '/docs/01_初步了解/01_快速了解' },
            { text: '写作规范指南', link: '/docs/01_初步了解/00_写作规范指南' },
            { text: '配图与排版指南', link: '/docs/01_初步了解/01_配图与排版指南' },
            { text: '跨平台发布指南', link: '/docs/01_初步了解/02_跨平台发布指南' },
            { text: '文章写作模板', link: '/docs/01_初步了解/03_文章写作模板' },
            { text: '方案对比示例', link: '/docs/01_初步了解/04_方案对比示例' }
          ]
        }
      ],
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com' }
    ],

    footer: {
      message: 'CRMEB Java 多商户商城系统',
      copyright: 'Copyright © 2024 CRMEB. All rights reserved.'
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
