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
    let localItems: LibraryItem[] = [];
    try {
      const rawLocal = localStorage.getItem('upa_vault_items');
      if (rawLocal) {
        const parsed = JSON.parse(rawLocal);
        if (Array.isArray(parsed)) {
          localItems = parsed.map((it: any, idx: number) => ({
            id: it.id || `local_${idx}_${it.created_at || Date.now()}`,
            source_url: it.source_url || it.url || '#',
            platform: it.category || 'Saved Extraction',
            recipe_data: it,
            created_at: it.created_at || new Date().toISOString()
          }));
        }
      }
    } catch (e) {
      console.warn('Error reading local vault items:', e);
    }

    try {
      const url = query
        ? `/api/v1/library?search=${encodeURIComponent(query)}&limit=20`
        : `/api/v1/library?limit=20`;
      const res = await fetch(url);
      if (res.ok) {
        const data = await res.json();
        const remoteItems = data.items || [];
        const merged = [...localItems];
        const existingUrls = new Set(localItems.map(i => i.source_url));
        for (const rItem of remoteItems) {
          if (!existingUrls.has(rItem.source_url)) {
            merged.push(rItem);
          }
        }
        if (query.trim()) {
          const qLower = query.toLowerCase();
          setItems(merged.filter(it => 
            (it.recipe_data?.title || it.recipe_data?.recipe_title || '').toLowerCase().includes(qLower) ||
            it.source_url.toLowerCase().includes(qLower)
          ));
        } else {
          setItems(merged);
        }
      } else {
        setItems(localItems);
      }
    } catch (err: any) {
      setItems(localItems);
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
      const rawLocal = localStorage.getItem('upa_vault_items');
      if (rawLocal) {
        const parsed = JSON.parse(rawLocal);
        const updated = parsed.filter((it: any, idx: number) => `local_${idx}_${it.created_at || ''}` !== id && it.id !== id);
        localStorage.setItem('upa_vault_items', JSON.stringify(updated));
      }
      setItems((prev) => prev.filter((it) => it.id !== id));
      if (!id.startsWith('local_')) {
        await fetch(`/api/v1/library/${id}`, { method: 'DELETE' }).catch(() => {});
      }
    } catch (err) {
      setItems((prev) => prev.filter((it) => it.id !== id));
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
              <h2 style={{ fontSize: '1.15rem', fontWeight: 700 }}>📖 Universal Intelligence Vault</h2>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                Saved extractions, travel itineraries, workout plans & shoppable finds
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
              placeholder="Search by title, travel destination, dish or platform..."
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

        {/* Intelligence Cards List */}
        <div style={{ flex: 1, overflowY: 'auto', padding: '1rem 1.5rem' }}>
          {loading ? (
            <div style={{ textAlign: 'center', padding: '3rem 1rem', color: 'var(--text-muted)' }}>
              <RefreshCw size={24} className="animate-pulse-subtle" style={{ margin: '0 auto 0.75rem' }} />
              <p>Loading your intelligence archive...</p>
            </div>
          ) : error ? (
            <div style={{ textAlign: 'center', padding: '2rem 1rem', color: 'var(--accent-rose)' }}>
              <p>{error}</p>
            </div>
          ) : items.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '4rem 1rem', color: 'var(--text-muted)' }}>
              <Sparkles size={40} style={{ margin: '0 auto 1rem', opacity: 0.4, color: 'var(--accent-emerald)' }} />
              <p style={{ fontWeight: 600, color: 'var(--text-primary)' }}>No extractions saved in vault yet</p>
              <p style={{ fontSize: '0.85rem', marginTop: '0.35rem' }}>
                Extract any Instagram Reel, TikTok, or YouTube Short across recipes, travel guides, workouts, or product finds to archive it here!
              </p>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {items.map((item) => {
                const rData = item.recipe_data || {};
                const title =
                  rData.recipe_title ||
                  rData.title ||
                  'Untitled Extraction';
                
                // Multi-genre badge determination
                const catStr = ((rData as any).category || (rData as any).domain || item.platform || '').toUpperCase();
                const titleUpper = title.toUpperCase();
                let badgeLabel = '⚡ SAVED EXTRACTION';
                let badgeClass = 'badge-emerald';

                if (catStr.includes('TRAVEL') || catStr.includes('ITINERARY') || titleUpper.includes('ITINERARY') || titleUpper.includes('TRAVEL') || titleUpper.includes('VARKALA') || titleUpper.includes('BALI')) {
                  badgeLabel = '✈️ TRAVEL GUIDE';
                  badgeClass = 'badge-emerald';
                } else if (catStr.includes('WORKOUT') || catStr.includes('FITNESS') || titleUpper.includes('WORKOUT')) {
                  badgeLabel = '🏋️ WORKOUT ROUTINE';
                  badgeClass = 'badge-amber';
                } else if (catStr.includes('PRODUCT') || catStr.includes('KITCHEN_FIND') || titleUpper.includes('FIND') || titleUpper.includes('UNBOXING')) {
                  badgeLabel = '📦 PRODUCT FINDS';
                  badgeClass = 'badge-rose';
                } else if (catStr.includes('TUTORIAL') || catStr.includes('TECH') || titleUpper.includes('TUTORIAL')) {
                  badgeLabel = '💻 TUTORIAL';
                  badgeClass = 'badge-emerald';
                } else if (catStr.includes('EDUCATIONAL') || catStr.includes('EXPLAINER')) {
                  badgeLabel = '🎓 EDUCATIONAL';
                  badgeClass = 'badge-emerald';
                } else if (catStr.includes('BEAUTY') || catStr.includes('FASHION')) {
                  badgeLabel = '💄 BEAUTY & FASHION';
                  badgeClass = 'badge-rose';
                } else if (catStr.includes('RECIPE') || catStr.includes('COOK')) {
                  badgeLabel = '🍳 RECIPE';
                  badgeClass = 'badge-emerald';
                }

                // Dynamic Metadata line and Action button text
                let metaText = `🛒 ${(rData.ingredients?.length || 0)} ingredients indexed`;
                let actionText = `Open in Chef View`;

                if (badgeLabel.includes('TRAVEL')) {
                  const mapsCount = (rData as any).google_maps_locations?.length || 0;
                  metaText = mapsCount > 0 ? `📍 ${mapsCount} locations mapped` : `✈️ Travel Itinerary & Spots`;
                  actionText = `Open Travel Guide`;
                } else if (badgeLabel.includes('WORKOUT')) {
                  const stepsCount = rData.instructions?.length || (rData as any).steps?.length || 0;
                  metaText = stepsCount > 0 ? `🏋️ ${stepsCount} exercises / steps` : `🏋️ Fitness Workout Plan`;
                  actionText = `Open Workout View`;
                } else if (badgeLabel.includes('PRODUCT')) {
                  const productsCount = (rData as any).products?.length || 0;
                  metaText = productsCount > 0 ? `🛒 ${productsCount} shoppable products` : `📦 Product Finds`;
                  actionText = `Open Product Finds`;
                } else if (badgeLabel.includes('TUTORIAL') || badgeLabel.includes('EDUCATIONAL')) {
                  const stepsCount = rData.instructions?.length || (rData as any).steps?.length || 0;
                  metaText = stepsCount > 0 ? `💡 ${stepsCount} guide steps` : `💻 Tutorial Guide`;
                  actionText = `Open Tutorial View`;
                }

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
                    onClick={async () => {
                      let targetData = rData;
                      const rDataAny = rData as any;
                      const hasAffiliate = Array.isArray(rDataAny.ingredients) && rDataAny.ingredients.some((ing: any) => typeof ing === 'object' && (ing?.amazon_url || ing?.blinkit_url));
                      const urlToRehydrate = rDataAny.source_url || rDataAny.url || item.source_url;
                      if (!hasAffiliate && urlToRehydrate && urlToRehydrate !== '#') {
                        try {
                          const res = await fetch('/api/v1/library/rehydrate', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                              extraction_id: item.id,
                              canonical_url: urlToRehydrate,
                              item: rData
                            })
                          });
                          const data = await res.json();
                          if (data.status === 'success' && data.item) {
                            targetData = data.item;
                          }
                        } catch (e) {}
                      }
                      onSelectRecipe(targetData);
                      onClose();
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between' }}>
                      <div>
                        <span className={`badge-pill ${badgeClass}`} style={{ marginBottom: '0.35rem' }}>
                          {badgeLabel}
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
                      <span>{metaText}</span>
                      <span style={{ color: 'var(--accent-emerald)', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                        {actionText} <ExternalLink size={11} />
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
