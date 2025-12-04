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
      { text: '系统安装', link: '/02_系统安装/' },
      { text: '使用手册', link: '/03_使用手册/' },
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
            { text: '代码H5打包', link: '/01_初步了解/10_代码H5打包' },
            { text: 'App-基础配置', link: '/01_初步了解/11_App-基础配置' },
            { text: 'App-开发调试', link: '/01_初步了解/12_App-开发调试' },
            { text: 'App-打包配置', link: '/01_初步了解/13_App-打包配置' },
            { text: 'App-打包上线', link: '/01_初步了解/14_App-打包上线' },
            { text: 'App-隐私政策', link: '/01_初步了解/15_App-隐私政策' },
            { text: '微信小程序打包', link: '/01_初步了解/16_微信小程序打包' },
            { text: 'PC商城部署', link: '/01_初步了解/17_PC商城部署' }
          ]
        }
      ],
      '/02_系统安装/': [
        {
          text: '系统安装',
          items: [
            { text: '云存储配置指南', link: '/02_系统安装/02_云存储配置指南' },
            { text: '微信公众号支付配置', link: '/02_系统安装/03_微信公众号支付配置指南' },
            { text: '微信小程序配置指南', link: '/02_系统安装/04_微信小程序配置指南' },
            { text: '微信小程序支付配置', link: '/02_系统安装/05_微信小程序支付配置' },
            { text: '支付宝开通与支付配置', link: '/02_系统安装/06_支付宝开通和支付' },
            { text: 'wxJava框架配置', link: '/02_系统安装/07_wxJava正确配置' }
          ]
        }
      ],
      '/03_使用手册/': [
        {
          text: '使用手册',
          items: [
            { text: '圈层管理完全指南', link: '/03_使用手册/01_圈层介绍' },
            { text: '用户等级管理', link: '/03_使用手册/02_用户等级管理' },
            { text: '用户管理', link: '/03_使用手册/03_用户管理' },
            { text: '商户管理', link: '/03_使用手册/04_商户管理' },
            { text: '商品管理', link: '/03_使用手册/05_商品管理' },
            { text: '付费会员管理', link: '/03_使用手册/06_付费会员管理' },
            { text: '微信小程序直播', link: '/03_使用手册/07_小程序直播' },
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
