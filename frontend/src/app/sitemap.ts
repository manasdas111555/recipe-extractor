import type { MetadataRoute } from 'next';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = 'https://universalpro.ai';

  const defaultRoutes: MetadataRoute.Sitemap = [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1.0
    },
    {
      url: `${baseUrl}/pricing`,
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 0.8
    }
  ];

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  try {
    const res = await fetch(`${apiUrl}/api/v1/public/sitemap?limit=500`, {
      next: { revalidate: 86400 }
    });
    if (res.ok) {
      const data = await res.json();
      const dynamicUrls: MetadataRoute.Sitemap = (data.urls || []).map((item: any) => ({
        url: item.url || `${baseUrl}/r/${item.slug}`,
        lastModified: item.last_modified ? new Date(item.last_modified) : new Date(),
        changeFrequency: 'weekly',
        priority: 0.7
      }));
      return [...defaultRoutes, ...dynamicUrls];
    }
  } catch (e) {
    console.warn('Backend sitemap endpoint unreachable, returning default routes.');
  }

  return defaultRoutes;
}
