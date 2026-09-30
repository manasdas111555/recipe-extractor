// @vitest-environment jsdom
import React from 'react';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, fireEvent, waitFor, cleanup } from '@testing-library/react';
import VaultLibrary from '../VaultLibrary';

describe('VaultLibrary Component (UPA-1209)', () => {
  const mockOnSelectRecipe = vi.fn();
  const mockOnClose = vi.fn();

  const MOCK_AFFILIATE_TAG = 'tag=MOCK_TAG';

  const mockLocalItems = [
    {
      id: 'local_item_1',
      title: 'Local Paneer Butter Masala',
      category: 'RECIPE',
      source_url: 'https://www.instagram.com/reel/C1234567890/',
      ingredients: [
        { name: 'Paneer', quantity: '200g' },
        { name: 'Butter', quantity: '2 tbsp' }
      ],
      instructions: ['Melt butter', 'Add paneer cubes', 'Simmer gravy'],
      created_at: '2026-09-20T10:00:00.000Z'
    }
  ];

  const mockRemoteItems = [
    {
      id: 'remote_item_2',
      source_url: 'https://www.instagram.com/reel/C9876543210/',
      platform: 'TRAVEL',
      recipe_data: {
        title: 'Hidden Waterfalls of Meghalaya',
        category: 'TRAVEL',
        domain: 'TRAVEL',
        places: ['Nohkalikai Falls', 'Rainbow Falls'],
        notes: 'Best visited during monsoon'
      },
      created_at: '2026-09-21T12:00:00.000Z'
    }
  ];

  const mockRehydrateSuccessResponse = {
    status: 'success',
    rehydrated: true,
    item: {
      id: 'local_item_1',
      title: 'Local Paneer Butter Masala',
      category: 'RECIPE',
      source_url: 'https://www.instagram.com/reel/C1234567890/',
      ingredients: [
        {
          name: 'Paneer',
          quantity: '200g',
          amazon_url: `https://www.amazon.in/dp/B001?${MOCK_AFFILIATE_TAG}`,
          blinkit_url: 'https://blinkit.com/s/?q=Paneer',
          zepto_url: 'https://zepto.now/search?q=Paneer'
        },
        {
          name: 'Butter',
          quantity: '2 tbsp',
          amazon_url: `https://www.amazon.in/dp/B002?${MOCK_AFFILIATE_TAG}`,
          blinkit_url: 'https://blinkit.com/s/?q=Butter',
          zepto_url: 'https://zepto.now/search?q=Butter'
        }
      ],
      instructions: ['Melt butter', 'Add paneer cubes', 'Simmer gravy'],
      created_at: '2026-09-20T10:00:00.000Z'
    }
  };

  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
    localStorage.setItem('upa_vault_items', JSON.stringify(mockLocalItems));

    global.fetch = vi.fn().mockImplementation(async (url: string, options?: any) => {
      const urlStr = String(url);
      if (urlStr.includes('/api/v1/library/rehydrate')) {
        return {
          ok: true,
          status: 200,
          json: async () => mockRehydrateSuccessResponse
        };
      }
      if (urlStr.includes('/api/v1/library')) {
        return {
          ok: true,
          status: 200,
          json: async () => ({
            status: 'success',
            items: mockRemoteItems
          })
        };
      }
      return {
        ok: true,
        status: 200,
        json: async () => ({})
      };
    });
  });

  afterEach(() => {
    cleanup();
  });

  it('renders nothing when isOpen is false', () => {
    const { container } = render(
      <VaultLibrary onSelectRecipe={mockOnSelectRecipe} isOpen={false} onClose={mockOnClose} />
    );
    expect(container.firstChild).toBeNull();
  });

  it('renders modal header, search input, and close button when isOpen is true', async () => {
    render(
      <VaultLibrary onSelectRecipe={mockOnSelectRecipe} isOpen={true} onClose={mockOnClose} />
    );

    expect(screen.getByText(/Universal Intelligence Vault/i)).toBeDefined();
    expect(screen.getByPlaceholderText(/Search by title/i)).toBeDefined();

    await waitFor(() => {
      expect(screen.getByText('Local Paneer Butter Masala')).toBeDefined();
    });

    // Close button triggers onClose
    const closeBtn = screen.getByText('✕');
    fireEvent.click(closeBtn);
    expect(mockOnClose).toHaveBeenCalledTimes(1);
  });

  it('loads local and remote items and displays them in the vault list', async () => {
    render(
      <VaultLibrary onSelectRecipe={mockOnSelectRecipe} isOpen={true} onClose={mockOnClose} />
    );

    await waitFor(() => {
      expect(screen.getByText('Local Paneer Butter Masala')).toBeDefined();
      expect(screen.getByText('Hidden Waterfalls of Meghalaya')).toBeDefined();
    });
  });

  it('filters items when user enters a search query', async () => {
    render(
      <VaultLibrary onSelectRecipe={mockOnSelectRecipe} isOpen={true} onClose={mockOnClose} />
    );

    await waitFor(() => {
      expect(screen.getByText('Local Paneer Butter Masala')).toBeDefined();
    });

    const searchInput = screen.getByPlaceholderText(/Search by title/i);
    fireEvent.change(searchInput, { target: { value: 'Meghalaya' } });
    fireEvent.keyDown(searchInput, { key: 'Enter', code: 'Enter' });

    await waitFor(() => {
      expect(screen.queryByText('Local Paneer Butter Masala')).toBeNull();
      expect(screen.getByText('Hidden Waterfalls of Meghalaya')).toBeDefined();
    });
  });

  it('selects and rehydrates legacy item with MOCK_TAG affiliate links when clicked', async () => {
    render(
      <VaultLibrary onSelectRecipe={mockOnSelectRecipe} isOpen={true} onClose={mockOnClose} />
    );

    await waitFor(() => {
      expect(screen.getByText('Local Paneer Butter Masala')).toBeDefined();
    });

    const itemCard = screen.getByText('Local Paneer Butter Masala').closest('.glass-card')!;
    fireEvent.click(itemCard);

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        '/api/v1/library/rehydrate',
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        })
      );
    });

    // Check that onSelectRecipe receives the rehydrated recipe with MOCK_TAG
    expect(mockOnSelectRecipe).toHaveBeenCalledTimes(1);
    const selectedData = mockOnSelectRecipe.mock.calls[0][0];
    expect(selectedData.ingredients[0].amazon_url).toContain(MOCK_AFFILIATE_TAG);
    expect(selectedData.ingredients[0].blinkit_url).toContain('blinkit.com');
    expect(selectedData.ingredients[0].zepto_url).toContain('zepto.now');
    expect(mockOnClose).toHaveBeenCalledTimes(1);
  });

  it('handles item export trigger', async () => {
    const originalOpen = window.open;
    window.open = vi.fn();

    render(
      <VaultLibrary onSelectRecipe={mockOnSelectRecipe} isOpen={true} onClose={mockOnClose} />
    );

    await waitFor(() => {
      expect(screen.getByText('Hidden Waterfalls of Meghalaya')).toBeDefined();
    });

    const exportBtn = screen.getAllByTitle(/Export Markdown/i)[0];
    fireEvent.click(exportBtn);

    expect(window.open).toHaveBeenCalledWith(
      expect.stringContaining('/api/v1/library/'),
      '_blank'
    );

    window.open = originalOpen;
  });

  it('handles item deletion from vault and local storage', async () => {
    const originalConfirm = window.confirm;
    window.confirm = vi.fn().mockReturnValue(true);

    render(
      <VaultLibrary onSelectRecipe={mockOnSelectRecipe} isOpen={true} onClose={mockOnClose} />
    );

    await waitFor(() => {
      expect(screen.getByText('Local Paneer Butter Masala')).toBeDefined();
    });

    const deleteBtn = screen.getAllByTitle(/Delete from Vault/i)[0];
    fireEvent.click(deleteBtn);

    await waitFor(() => {
      expect(screen.queryByText('Local Paneer Butter Masala')).toBeNull();
    });

    window.confirm = originalConfirm;
  });
});
