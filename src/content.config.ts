import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  // Astro 6+ Content Layer：从文件系统加载 Markdown，id 由文件名推导
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    date: z.date(),
    author: z.string().optional().default('Enki Yan'),
    tags: z.array(z.string()).optional().default([]),
  }),
});

export const collections = { blog };
