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
      { text: '快速开始', link: '/01_快速开始/' },
    ],

    sidebar: {
      '/01_快速开始/': [
        {
          text: '快速开始',
          items: [
            {
              text: '快速入门',
              items: [
                { text: 'Hello_World', link: '/01_快速开始/1_快速入门/01_Hello_World' },
                { text: '环境准备', link: '/01_快速开始/1_快速入门/02_环境准备' },
                { text: '第一个应用', link: '/01_快速开始/1_快速入门/03_第一个应用' },
              ]
            },
            {
              text: '快速开始',
              items: [
                { text: '系统简介', link: '/01_快速开始/1_快速开始/01_系统简介' },
                { text: '环境配置', link: '/01_快速开始/1_快速开始/02_环境配置' },
              ]
            },
            {
              text: '核心概念',
              items: [
                { text: '架构概述', link: '/01_快速开始/2_核心概念/01_架构概述' },
                { text: '系统设计', link: '/01_快速开始/2_核心概念/02_系统设计' },
              ]
            },
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
