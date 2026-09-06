'use client';

import React, { useState, useEffect } from 'react';
import { BookOpen, Search, Trash2, Download, ExternalLink, RefreshCw, Sparkles, ChefHat } from 'lucide-react';

interface LibraryItem {
  id: string;
  source_url: string;
  platform?: string;
  recipe_data?: {
    recipe_title?: string;
    title?: string;
    cooking_time?: string;
    prep_time?: string;
    servings?: number;
    ingredients?: any[];
    instructions?: string[];
  };
  cached_at?: string;
  created_at?: string;
}

interface VaultLibraryProps {
  onSelectRecipe: (recipe: any) => void;
  isOpen: boolean;
  onClose: () => void;
}

export default function VaultLibrary({ onSelectRecipe, isOpen, onClose }: VaultLibraryProps) {
  const [items, setItems] = useState<LibraryItem[]>([]);
  const [search, setSearch] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const fetchLibrary = async (query = '') => {
    setLoading(true);
    setError(null);
    try {
      const url = query
        ? `/api/v1/library?search=${encodeURIComponent(query)}&limit=20`
        : `/api/v1/library?limit=20`;
      const res = await fetch(url);
      if (!res.ok) {
        throw new Error(`Failed to load vault library: ${res.statusText}`);
      }
      const data = await res.json();
      setItems(data.items || []);
    } catch (err: any) {
      setError(err.message || 'Error fetching recipes');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchLibrary(search);
    }
  }, [isOpen]);

  const handleDelete = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!confirm('Are you sure you want to remove this recipe from your personal vault?')) {
      return;
    }
    try {
      const res = await fetch(`/api/v1/library/${id}`, { method: 'DELETE' });
      if (res.ok) {
        setItems((prev) => prev.filter((it) => it.id !== id));
      } else {
        alert('Failed to delete item.');
      }
    } catch (err) {
      console.error(err);
      alert('Network error deleting item.');
    }
  };

  const handleExport = (id: string, format: 'markdown' | 'txt' | 'json', e: React.MouseEvent) => {
    e.stopPropagation();
    window.open(`/api/v1/library/${id}/export?format=${format}`, '_blank');
  };

  if (!isOpen) return null;

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        backdropFilter: 'blur(8px)',
        zIndex: 1000,
        display: 'flex',
        justifyContent: 'flex-end',
      }}
      onClick={onClose}
    >
      <div
        style={{
          width: '100%',
          maxWidth: '560px',
          height: '100%',
          background: 'var(--bg-base)',
          borderLeft: '1px solid var(--border-subtle)',
          display: 'flex',
          flexDirection: 'column',
          boxShadow: '-10px 0 30px rgba(0, 0, 0, 0.5)',
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Vault Header */}
        <div
          style={{
            padding: '1.25rem 1.5rem',
            borderBottom: '1px solid var(--border-subtle)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
            <BookOpen size={22} color="var(--accent-emerald)" />
            <div>
              <h2 style={{ fontSize: '1.15rem', fontWeight: 700 }}>Personal Recipe Vault</h2>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                Saved extractions & synchronized pantry lists
              </p>
            </div>
          </div>
          <button onClick={onClose} className="btn-ghost" style={{ padding: '0.35rem 0.65rem' }}>
            ✕
          </button>
        </div>

        {/* Search & Filter Bar */}
        <div style={{ padding: '1rem 1.5rem', borderBottom: '1px solid var(--border-subtle)' }}>
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              background: 'rgba(255, 255, 255, 0.05)',
              border: '1px solid var(--border-subtle)',
              borderRadius: 'var(--radius-sm)',
              padding: '0.5rem 0.75rem',
            }}
          >
            <Search size={16} color="var(--text-muted)" />
            <input
              type="text"
              placeholder="Search by title, dish or platform..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && fetchLibrary(search)}
              style={{
                background: 'transparent',
                border: 'none',
                color: 'var(--text-primary)',
                outline: 'none',
                width: '100%',
                fontSize: '0.875rem',
              }}
            />
            <button
              onClick={() => fetchLibrary(search)}
              className="btn-ghost"
              style={{ padding: '0.2rem 0.5rem', fontSize: '0.75rem' }}
            >
              Search
            </button>
          </div>
        </div>

        {/* Recipe Cards List */}
        <div style={{ flex: 1, overflowY: 'auto', padding: '1rem 1.5rem' }}>
          {loading ? (
            <div style={{ textAlign: 'center', padding: '3rem 1rem', color: 'var(--text-muted)' }}>
              <RefreshCw size={24} className="animate-pulse-subtle" style={{ margin: '0 auto 0.75rem' }} />
              <p>Loading your recipe archive...</p>
            </div>
          ) : error ? (
            <div style={{ textAlign: 'center', padding: '2rem 1rem', color: 'var(--accent-rose)' }}>
              <p>{error}</p>
            </div>
          ) : items.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '4rem 1rem', color: 'var(--text-muted)' }}>
              <ChefHat size={40} style={{ margin: '0 auto 1rem', opacity: 0.4 }} />
              <p style={{ fontWeight: 600, color: 'var(--text-primary)' }}>No recipes in vault yet</p>
              <p style={{ fontSize: '0.85rem', marginTop: '0.35rem' }}>
                Extract any Instagram Reel, TikTok, or YouTube Short to archive it here!
              </p>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {items.map((item) => {
                const title =
                  item.recipe_data?.recipe_title ||
                  item.recipe_data?.title ||
                  'Untitled Recipe Extraction';
                const ingredientsCount = item.recipe_data?.ingredients?.length || 0;
                const platform = item.platform || 'Social Reel';

                return (
                  <div
                    key={item.id}
                    className="glass-card"
                    style={{
                      cursor: 'pointer',
                      display: 'flex',
                      flexDirection: 'column',
                      gap: '0.5rem',
                      transition: 'transform 0.15s ease, border-color 0.15s ease',
                    }}
                    onClick={() => {
                      onSelectRecipe(item.recipe_data);
                      onClose();
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between' }}>
                      <div>
                        <span className="badge-pill badge-emerald" style={{ marginBottom: '0.35rem' }}>
                          {platform}
                        </span>
                        <h3 style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-primary)' }}>
                          {title}
                        </h3>
                      </div>

                      {/* Actions */}
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                        <button
                          onClick={(e) => handleExport(item.id, 'markdown', e)}
                          className="btn-ghost"
                          style={{ padding: '0.25rem 0.45rem', fontSize: '0.7rem' }}
                          title="Export Markdown"
                        >
                          <Download size={13} />
                        </button>
                        <button
                          onClick={(e) => handleDelete(item.id, e)}
                          className="btn-ghost"
                          style={{ padding: '0.25rem 0.45rem', fontSize: '0.7rem', color: '#FDA4AF' }}
                          title="Delete from Vault"
                        >
                          <Trash2 size={13} />
                        </button>
                      </div>
                    </div>

                    <div
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        fontSize: '0.75rem',
                        color: 'var(--text-secondary)',
                        marginTop: '0.25rem',
                      }}
                    >
                      <span>🛒 {ingredientsCount} ingredients indexed</span>
                      <span style={{ color: 'var(--accent-emerald)', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                        Open in Chef View <ExternalLink size={11} />
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
