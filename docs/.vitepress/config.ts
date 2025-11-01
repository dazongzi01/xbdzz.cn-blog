import { defineConfig } from 'vitepress'

export default defineConfig({
  title: '大粽子',
  description: '大粽子',

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
      { text: '初步了解', link: '/01_初步了解/' },
    ],

    sidebar: {
      '/01_初步了解/': [
        {
          text: '初步了解',
          items: [
            { text: '快速了解', link: '/01_初步了解/01_快速了解' },
            { text: '本地运行', link: '/01_初步了解/02_本地运行' },
            { text: '服务购买和搭建', link: '/01_初步了解/03_服务购买和搭建' },
            { text: '域名购买和解析', link: '/01_初步了解/04_域名购买和解析' },
            { text: '宝塔安装高手可忽略', link: '/01_初步了解/05_宝塔安装高手可忽略' },
            { text: '服务器运行环境', link: '/01_初步了解/06_服务器运行环境' },
            { text: '创建站点并配置', link: '/01_初步了解/07_创建站点并配置' },
            { text: '代码-Java项目打包', link: '/01_初步了解/08_代码-Java项目打包' },
            { text: '代码-管理端打包', link: '/01_初步了解/09_代码-管理端打包' },
            { text: '代码H5打包', link: '/01_初步了解/10_代码H5打包' }
          ]
        }
      ],
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com' }
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
