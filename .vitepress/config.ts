import { defineConfig } from 'vitepress'

export default defineConfig({
  lang: 'zh-CN',
  title: '奥尔特云',
  description: '游戏开发、技术笔记与产业观察',
  cleanUrls: false,
  lastUpdated: true,

  sitemap: {
    hostname: 'https://firevenus.github.io'
  },

  head: [
    ['meta', { name: 'author', content: 'Enki Yan' }],
    ['meta', { name: 'keywords', content: '游戏开发, MCP, 微信公众号, AI, 东北, 独立游戏, 冻土回声' }],
    ['meta', { property: 'og:site_name', content: '奥尔特云' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { name: 'twitter:card', content: 'summary_large_image' }],
    ['link', { rel: 'alternate', type: 'application/rss+xml', title: '奥尔特云', href: '/rss.xml' }]
  ],

  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '文章', link: '/posts/mcp-wechat-publish' },
      {
        text: 'GitHub',
        link: 'https://github.com/firevenus'
      }
    ],

    sidebar: {
      '/posts/': [
        {
          text: '技术笔记',
          items: [
            { text: '想用AI写完文章之后直接发到微信，该怎么做？', link: '/posts/mcp-wechat-publish' }
          ]
        }
      ]
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/firevenus' }
    ],

    footer: {
      message: ' Released under the MIT License.',
      copyright: 'Copyright © 2026 Enki Yan'
    },

    outline: {
      label: '本页目录',
      level: [2, 3]
    },

    docFooter: {
      prev: '上一篇',
      next: '下一篇'
    },

    lastUpdatedText: '最后更新',

    search: {
      provider: 'local',
      options: {
        translations: {
          button: {
            buttonText: '搜索文章',
            buttonAriaLabel: '搜索文章'
          },
          modal: {
            noResultsText: '无法找到相关结果',
            resetButtonTitle: '清除查询条件',
            footer: {
              selectText: '选择',
              navigateText: '切换'
            }
          }
        }
      }
    }
  }
})
