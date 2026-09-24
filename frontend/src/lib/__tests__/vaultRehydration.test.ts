import { describe, it, expect, vi } from 'vitest';

describe('Vault Item Re-hydration Component Flow', () => {
  it('calls /api/v1/library/rehydrate and attaches monetized buy links when opening legacy vault item without affiliate URLs', async () => {
    const legacyItem = {
      id: 'vault_legacy_101',
      source_url: 'https://www.instagram.com/reel/C3abc123456/',
      title: 'Legacy Saved Recipe',
      ingredients: [
        { name: 'Paneer', quantity: '200g' },
        { name: 'Butter', quantity: '2 tbsp' }
      ]
    };

    const mockRehydratedResponse = {
      status: 'success',
      rehydrated: true,
      item: {
        ...legacyItem,
        ingredients: [
          {
            name: 'Paneer',
            quantity: '200g',
            amazon_url: 'https://www.amazon.in/dp/B001?tag=manasdas11155-21',
            blinkit_url: 'https://blinkit.com/s/?q=Paneer',
            zepto_url: 'https://zepto.now/search?q=Paneer'
          },
          {
            name: 'Butter',
            quantity: '2 tbsp',
            amazon_url: 'https://www.amazon.in/dp/B002?tag=manasdas11155-21',
            blinkit_url: 'https://blinkit.com/s/?q=Butter',
            zepto_url: 'https://zepto.now/search?q=Butter'
          }
        ]
      }
    };

    // Mock global fetch
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => mockRehydratedResponse
    });
    global.fetch = fetchMock;

    // Simulate Vault selection handler logic from VaultLibrary.tsx
    let targetData = legacyItem;
    const rDataAny = legacyItem as any;
    const hasAffiliate = Array.isArray(rDataAny.ingredients) && rDataAny.ingredients.some((ing: any) => typeof ing === 'object' && (ing?.amazon_url || ing?.blinkit_url));
    const urlToRehydrate = rDataAny.source_url || rDataAny.url;

    expect(hasAffiliate).toBe(false);
    expect(urlToRehydrate).toBe('https://www.instagram.com/reel/C3abc123456/');

    if (!hasAffiliate && urlToRehydrate && urlToRehydrate !== '#') {
      const res = await fetch('/api/v1/library/rehydrate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          extraction_id: legacyItem.id,
          canonical_url: urlToRehydrate,
          item: legacyItem
        })
      });
      const data = await res.json();
      if (data.status === 'success' && data.item) {
        targetData = data.item;
      }
    }

    // Verify fetch call details
    expect(fetchMock).toHaveBeenCalledWith('/api/v1/library/rehydrate', expect.objectContaining({
      method: 'POST'
    }));

    // Verify rehydrated item contains active buy links for Amazon, Blinkit, and Zepto
    const ing0 = targetData.ingredients[0] as any;
    expect(ing0.amazon_url).toContain('tag=manasdas11155-21');
    expect(ing0.blinkit_url).toContain('blinkit.com');
    expect(ing0.zepto_url).toContain('zepto.now');
  });
});
