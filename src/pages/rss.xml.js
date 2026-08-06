import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const posts = await getCollection('blog');
  const items = posts
    .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf())
    .map((post) => ({
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.date,
      link: `/blog/${post.slug}/`,
      categories: post.data.tags || [],
    }));

  return rss({
    title: '奥尔特云 | Enki Yan',
    description: '游戏开发 · 技术笔记 · 产业观察 — 冻土回声 Enki Yan',
    site: context.site,
    items,
    customData: '<language>zh-cn</language>',
  });
}
