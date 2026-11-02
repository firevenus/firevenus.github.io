import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://firevenus.github.io',
  base: '/',
  integrations: [sitemap()],
  // 本地沙箱环境 shiki 安装不完整时用：ASTRO_NO_SHIKI=1 npm run build
  ...(process.env.ASTRO_NO_SHIKI ? { markdown: { syntaxHighlight: false } } : {}),
});
