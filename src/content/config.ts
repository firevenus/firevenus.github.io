import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    date: z.date(),
    author: z.string().optional().default('Enki Yan'),
    tags: z.array(z.string()).optional().default([]),
  }),
});

export const collections = { blog };
