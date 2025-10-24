import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'CRMEB Java 文档',
  description: 'Java 多商户商城系统完整文档',

  ignoreDeadLinks: true,

  head: [
    ['meta', { name: 'viewport', content: 'width=device-width, initial-scale=1.0' }],
    ['link', { rel: 'icon', href: '/logo.svg' }]
  ],

  themeConfig: {
    logo: '/logo.svg',

    nav: [
      { text: '首页', link: '/' },
      { text: '快速开始', link: '/01_快速开始/' },
      { text: '系统配置', link: '/02_系统配置/' },
      { text: '商城功能', link: '/03_商城功能/' },
      { text: '商户管理', link: '/04_商户管理/' },
      { text: '交易订单', link: '/05_交易订单/' },
      { text: 'API文档', link: '/06_API文档/' }
    ],

    sidebar: {
      '/01_快速开始/': [
        {
          text: '快速开始',
          items: [
            { text: '模块概览', link: '/01_快速开始/' }
          ]
        }
      ],
      '/02_系统配置/': [
        {
          text: '系统配置',
          items: [
            { text: '模块概览', link: '/02_系统配置/' }
          ]
        }
      ],
      '/03_商城功能/': [
        {
          text: '商城功能',
          items: [
            { text: '模块概览', link: '/03_商城功能/' }
          ]
        }
      ],
      '/04_商户管理/': [
        {
          text: '商户管理',
          items: [
            { text: '模块概览', link: '/04_商户管理/' }
          ]
        }
      ],
      '/05_交易订单/': [
        {
          text: '交易订单',
          items: [
            { text: '模块概览', link: '/05_交易订单/' }
          ]
        }
      ],
      '/06_API文档/': [
        {
          text: 'API文档',
          items: [
            { text: '模块概览', link: '/06_API文档/' }
          ]
        }
      ]
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
