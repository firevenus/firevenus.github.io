# Enki's Blog · 奥尔特云

个人博客 — 独立游戏、技术笔记与产业观察

## 技术栈

- [Astro](https://astro.build/) - 静态站点生成器
- GitHub Pages - 免费托管 (gh-pages 分支)
- Cloudflare Pages - CDN 加速 (enki-yan.pages.dev)
- GitHub Actions - 自动构建部署

## 本地开发

```bash
npm install
npm run dev
```

## 构建部署

```bash
npm run build
```

推送到 `main` 分支后：
1. Cloudflare Pages 自动构建部署 → enki-yan.pages.dev
2. GitHub Actions 构建并推送 `dist/` 到 `gh-pages` 分支 → firevenus.github.io

## 独立页面

| 路径 | 说明 |
|:--|:--|
| `/juyi-weight-lab/` | 居易指数 · 权重实验室 — 交互式100城排名工具 |

## 文章列表

- [想用AI写完文章之后直接发到微信，该怎么做？](src/content/posts/mcp-wechat-publish.md) - 14个微信公众号MCP Server全景对比
