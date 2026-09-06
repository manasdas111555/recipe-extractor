'use client';

import React, { useState, useEffect, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import {
  Sparkles,
  Play,
  Clock,
  Flame,
  ChefHat,
  ShoppingCart,
  Share2,
  BookOpen,
  ArrowRight,
  ShieldCheck,
  Zap,
  CheckCircle2,
  AlertCircle,
  ExternalLink,
} from 'lucide-react';
import ServingAdjuster from '../components/ServingAdjuster';
import VaultLibrary from '../components/VaultLibrary';

interface ExtractionResult {
  recipe_title?: string;
  title?: string;
  dish_type?: string;
  prep_time?: string;
  cooking_time?: string;
  servings?: number;
  ingredients?: any[];
  instructions?: string[];
  equipment_needed?: string[];
  chef_tips?: string[];
  media_url?: string;
  thumbnail_url?: string;
  cached?: boolean;
}

function RecipeDashboard() {
  const searchParams = useSearchParams();
  const [url, setUrl] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [loadingPhase, setLoadingPhase] = useState<string>('Ready');
  const [result, setResult] = useState<ExtractionResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isVaultOpen, setIsVaultOpen] = useState<boolean>(false);
  const [quotaRemaining, setQuotaRemaining] = useState<number>(10);

  // Detect platform from URL
  const detectPlatform = (inputUrl: string) => {
    if (!inputUrl) return null;
    if (inputUrl.includes('instagram.com')) return { name: 'Instagram Reel', color: '#E1306C' };
    if (inputUrl.includes('tiktok.com')) return { name: 'TikTok', color: '#00F2FE' };
    if (inputUrl.includes('youtube.com') || inputUrl.includes('youtu.be'))
      return { name: 'YouTube Short', color: '#FF0000' };
    if (inputUrl.includes('facebook.com')) return { name: 'Facebook Reel', color: '#1877F2' };
    return { name: 'Social Video', color: '#10B981' };
  };

  const platformInfo = detectPlatform(url);

  // Support autostart from Web Share Target
  useEffect(() => {
    const initialUrl = searchParams.get('url');
    const autostart = searchParams.get('autostart');
    if (initialUrl) {
      setUrl(initialUrl);
      if (autostart === '1') {
        handleExtract(initialUrl);
      }
    }
  }, [searchParams]);

  const handleExtract = async (targetUrl = url) => {
    if (!targetUrl.trim()) {
      setError('Please paste a valid video URL from Instagram, TikTok, or YouTube.');
      return;
    }

    setError(null);
    setIsLoading(true);
    setLoadingPhase('Verifying Cloud Ingestion Cache...');

    try {
      // Simulate quick phase telemetry for user feedback
      setTimeout(() => setLoadingPhase('Analyzing Multimodal Audio & Frames...'), 800);
      setTimeout(() => setLoadingPhase('Gemini 3.8 Flash Synthesizing Recipe...'), 1800);

      const response = await fetch('/api/v1/extract', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: targetUrl }),
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.detail || 'Extraction failed. Please check the URL.');
      }

      const data = await response.json();
      setResult(data);
      setQuotaRemaining((prev) => Math.max(0, prev - 1));
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'Unable to complete recipe extraction.');
    } finally {
      setIsLoading(false);
      setLoadingPhase('Ready');
    }
  };

  const sampleUrls = [
    { label: 'Butter Chicken Reel', url: 'https://www.instagram.com/reel/C8ButterChickenSample/' },
    { label: 'Crispy Smashed Potatoes', url: 'https://www.tiktok.com/@chef/video/738291040182' },
    { label: '10-Min Garlic Noodles', url: 'https://youtube.com/shorts/GarlicNoodlesSample' },
  ];

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Top Navigation Bar */}
      <header
        style={{
          borderBottom: '1px solid var(--border-subtle)',
          background: 'rgba(10, 14, 26, 0.85)',
          backdropFilter: 'blur(16px)',
          position: 'sticky',
          top: 0,
          zIndex: 100,
          padding: '0.85rem 1.5rem',
        }}
      >
        <div
          style={{
            maxWidth: '1280px',
            margin: '0 auto',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div
              style={{
                width: '36px',
                height: '36px',
                borderRadius: '10px',
                background: 'linear-gradient(135deg, #10B981, #059669)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 0 15px rgba(16, 185, 129, 0.4)',
              }}
            >
              <ChefHat size={20} color="#FFFFFF" />
            </div>
            <div>
              <span style={{ fontSize: '1.15rem', fontWeight: 800, letterSpacing: '-0.02em' }}>
                UNIVERSAL <span className="gradient-text">PRO AI</span>
              </span>
              <span
                className="badge-pill badge-emerald"
                style={{ marginLeft: '0.5rem', fontSize: '0.65rem' }}
              >
                v1.4 Flagship
              </span>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
            {/* Tiered Quota Badge */}
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.4rem',
                background: 'rgba(255, 255, 255, 0.04)',
                border: '1px solid var(--border-subtle)',
                padding: '0.35rem 0.75rem',
                borderRadius: 'var(--radius-full)',
                fontSize: '0.75rem',
              }}
            >
              <Zap size={13} color="var(--accent-emerald)" />
              <span style={{ color: 'var(--text-secondary)' }}>Daily Quota:</span>
              <strong style={{ color: 'var(--accent-emerald)' }}>{quotaRemaining} left</strong>
            </div>

            {/* Vault Library Button */}
            <button
              onClick={() => setIsVaultOpen(true)}
              className="btn-ghost"
              style={{ padding: '0.45rem 0.85rem' }}
            >
              <BookOpen size={16} color="var(--accent-emerald)" />
              <span>Recipe Vault</span>
            </button>
          </div>
        </div>
      </header>

      {/* Hero Ingestion Section */}
      <main style={{ flex: 1, maxWidth: '1280px', margin: '0 auto', width: '100%', padding: '2rem 1.5rem' }}>
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <div
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.5rem',
              padding: '0.3rem 0.85rem',
              background: 'rgba(16, 185, 129, 0.1)',
              border: '1px solid rgba(16, 185, 129, 0.25)',
              borderRadius: 'var(--radius-full)',
              marginBottom: '1rem',
            }}
          >
            <Sparkles size={14} color="var(--accent-emerald)" />
            <span style={{ fontSize: '0.75rem', fontWeight: 600, color: '#34D399' }}>
              Sub-3s Social Extraction • Native Web Share PWA
            </span>
          </div>

          <h1
            style={{
              fontSize: '2.5rem',
              fontWeight: 800,
              lineHeight: 1.15,
              marginBottom: '0.75rem',
              letterSpacing: '-0.03em',
            }}
          >
            Turn Any Cooking Video into a <br />
            <span className="gradient-text">Structured Recipe & Pantry Cart</span>
          </h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '1rem', maxWidth: '640px', margin: '0 auto' }}>
            Paste any Instagram Reel, TikTok, or YouTube Short. Universal Pro AI extracts verified
            ingredients, scales serving yields, and links direct checkout in seconds.
          </p>
        </div>

        {/* Input Bar Card */}
        <div
          className="glass-panel"
          style={{
            maxWidth: '780px',
            margin: '0 auto 1.5rem',
            padding: '0.75rem',
            boxShadow: '0 10px 40px rgba(0, 0, 0, 0.4)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            {platformInfo && (
              <span
                style={{
                  fontSize: '0.75rem',
                  fontWeight: 600,
                  padding: '0.35rem 0.65rem',
                  borderRadius: '6px',
                  background: 'rgba(255, 255, 255, 0.08)',
                  color: platformInfo.color,
                  whiteSpace: 'nowrap',
                }}
              >
                {platformInfo.name}
              </span>
            )}
            <input
              type="text"
              placeholder="Paste Instagram Reel, TikTok, or YouTube Short link..."
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleExtract()}
              style={{
                flex: 1,
                background: 'transparent',
                border: 'none',
                color: 'var(--text-primary)',
                fontSize: '1rem',
                outline: 'none',
                padding: '0.5rem 0.5rem',
              }}
            />
            <button
              onClick={() => handleExtract()}
              disabled={isLoading || !url}
              className="btn-emerald"
            >
              {isLoading ? (
                <>
                  <Zap size={16} className="animate-pulse-subtle" />
                  <span>Extracting...</span>
                </>
              ) : (
                <>
                  <span>Extract Recipe</span>
                  <ArrowRight size={16} />
                </>
              )}
            </button>
          </div>

          {/* Quick Sample Chips */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              marginTop: '0.75rem',
              paddingTop: '0.5rem',
              borderTop: '1px solid var(--border-subtle)',
              flexWrap: 'wrap',
            }}
          >
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Try samples:</span>
            {sampleUrls.map((s, idx) => (
              <button
                key={idx}
                onClick={() => {
                  setUrl(s.url);
                  handleExtract(s.url);
                }}
                className="btn-ghost"
                style={{ padding: '0.2rem 0.5rem', fontSize: '0.72rem' }}
              >
                {s.label}
              </button>
            ))}
          </div>
        </div>

        {/* Live Loading Phase Deck */}
        {isLoading && (
          <div
            className="glass-panel"
            style={{
              maxWidth: '780px',
              margin: '0 auto 2rem',
              padding: '1.25rem',
              textAlign: 'center',
              border: '1px solid var(--border-active)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.65rem' }}>
              <Zap size={20} color="var(--accent-emerald)" className="animate-pulse-subtle" />
              <span style={{ fontWeight: 600, color: 'var(--accent-emerald)' }}>{loadingPhase}</span>
            </div>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '0.4rem' }}>
              Powered by Google Gemini 3.8 Flash • Sub-3s turnaround SLA
            </p>
          </div>
        )}

        {/* Error Alert */}
        {error && (
          <div
            className="glass-panel"
            style={{
              maxWidth: '780px',
              margin: '0 auto 2rem',
              padding: '1rem 1.25rem',
              border: '1px solid rgba(255, 65, 108, 0.4)',
              background: 'rgba(255, 65, 108, 0.1)',
              display: 'flex',
              alignItems: 'center',
              gap: '0.75rem',
            }}
          >
            <AlertCircle size={20} color="var(--accent-rose)" />
            <span style={{ fontSize: '0.875rem', color: '#FDA4AF' }}>{error}</span>
          </div>
        )}

        {/* Extraction Results: Dual Column Media & Structured Recipe View */}
        {result && (
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))',
              gap: '2rem',
              marginTop: '1.5rem',
            }}
          >
            {/* Left Column: Docked Media Player & Meta telemetry */}
            <div>
              <div className="glass-panel" style={{ padding: '1rem', overflow: 'hidden' }}>
                <h3
                  style={{
                    fontSize: '0.85rem',
                    color: 'var(--text-secondary)',
                    textTransform: 'uppercase',
                    letterSpacing: '0.05em',
                    marginBottom: '0.75rem',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                  }}
                >
                  <span>Single-Docked Media Player</span>
                  {result.cached && (
                    <span className="badge-pill badge-emerald">⚡ Instant Cache Hit</span>
                  )}
                </h3>

                {/* Video / Media Display */}
                {result.media_url ? (
                  <video
                    src={result.media_url}
                    controls
                    autoPlay
                    playsInline
                    style={{
                      width: '100%',
                      maxHeight: '440px',
                      borderRadius: 'var(--radius-sm)',
                      background: '#000',
                    }}
                  />
                ) : (
                  <div
                    style={{
                      height: '340px',
                      background: 'rgba(0, 0, 0, 0.4)',
                      borderRadius: 'var(--radius-sm)',
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                      justifyContent: 'center',
                      border: '1px dashed var(--border-subtle)',
                      gap: '0.5rem',
                    }}
                  >
                    <Play size={40} color="var(--accent-emerald)" opacity={0.6} />
                    <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                      Source Stream Ingested
                    </span>
                  </div>
                )}

                {/* Telemetry Metrics */}
                <div
                  style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(3, 1fr)',
                    gap: '0.5rem',
                    marginTop: '1rem',
                  }}
                >
                  <div className="glass-card" style={{ textAlign: 'center', padding: '0.65rem' }}>
                    <Clock size={16} color="var(--accent-emerald)" style={{ margin: '0 auto 0.25rem' }} />
                    <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>Cook Time</div>
                    <div style={{ fontSize: '0.85rem', fontWeight: 600 }}>
                      {result.cooking_time || result.prep_time || '15 mins'}
                    </div>
                  </div>

                  <div className="glass-card" style={{ textAlign: 'center', padding: '0.65rem' }}>
                    <Flame size={16} color="var(--accent-amber)" style={{ margin: '0 auto 0.25rem' }} />
                    <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>Dish Type</div>
                    <div style={{ fontSize: '0.85rem', fontWeight: 600 }}>
                      {result.dish_type || 'Main Course'}
                    </div>
                  </div>

                  <div className="glass-card" style={{ textAlign: 'center', padding: '0.65rem' }}>
                    <ShieldCheck size={16} color="#06B6D4" style={{ margin: '0 auto 0.25rem' }} />
                    <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>Verified</div>
                    <div style={{ fontSize: '0.85rem', fontWeight: 600, color: '#06B6D4' }}>
                      Gemini 3.8
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Right Column: Recipe Details & Serving Scaler */}
            <div>
              <div className="glass-panel" style={{ padding: '1.5rem' }}>
                <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '0.25rem' }}>
                  {result.recipe_title || result.title || 'Extracted Social Recipe'}
                </h2>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
                  Adjust serving yield to dynamically scale ingredients and cart links.
                </p>

                {/* Serving Scaler Component */}
                <ServingAdjuster
                  initialServings={result.servings || 2}
                  ingredients={result.ingredients || []}
                  recipeTitle={result.recipe_title || result.title || 'Recipe'}
                />

                {/* Step-by-Step Instructions */}
                <div style={{ marginTop: '1.5rem' }}>
                  <h3
                    style={{
                      fontSize: '1rem',
                      fontWeight: 600,
                      marginBottom: '0.75rem',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.5rem',
                    }}
                  >
                    <CheckCircle2 size={18} color="var(--accent-emerald)" />
                    <span>Preparation Method</span>
                  </h3>

                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
                    {result.instructions && result.instructions.length > 0 ? (
                      result.instructions.map((step, idx) => (
                        <div
                          key={idx}
                          style={{
                            display: 'flex',
                            alignItems: 'flex-start',
                            gap: '0.75rem',
                            padding: '0.65rem 0.85rem',
                            background: 'rgba(255, 255, 255, 0.02)',
                            borderRadius: '8px',
                            border: '1px solid rgba(255, 255, 255, 0.04)',
                          }}
                        >
                          <span
                            style={{
                              minWidth: '22px',
                              height: '22px',
                              borderRadius: '50%',
                              background: 'rgba(16, 185, 129, 0.2)',
                              color: 'var(--accent-emerald)',
                              fontSize: '0.75rem',
                              fontWeight: 700,
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'center',
                            }}
                          >
                            {idx + 1}
                          </span>
                          <p style={{ fontSize: '0.9rem', lineHeight: 1.4, color: 'var(--text-primary)' }}>
                            {step}
                          </p>
                        </div>
                      ))
                    ) : (
                      <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                        Follow the video clip for exact cooking steps.
                      </p>
                    )}
                  </div>
                </div>

                {/* Chef Tips if present */}
                {result.chef_tips && result.chef_tips.length > 0 && (
                  <div
                    style={{
                      marginTop: '1.25rem',
                      padding: '0.85rem 1rem',
                      background: 'rgba(245, 158, 11, 0.08)',
                      border: '1px solid rgba(245, 158, 11, 0.25)',
                      borderRadius: '8px',
                    }}
                  >
                    <span style={{ fontSize: '0.8rem', fontWeight: 600, color: '#FCD34D' }}>
                      💡 Chef Secret Tip:
                    </span>
                    <p style={{ fontSize: '0.85rem', color: 'var(--text-primary)', marginTop: '0.25rem' }}>
                      {result.chef_tips[0]}
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Slide-out Vault Library Drawer */}
      <VaultLibrary
        isOpen={isVaultOpen}
        onClose={() => setIsVaultOpen(false)}
        onSelectRecipe={(savedRecipe) => {
          setResult(savedRecipe);
        }}
      />
    </div>
  );
}

export default function HomePage() {
  return (
    <Suspense
      fallback={
        <div
          style={{
            minHeight: '100vh',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: '#0A0E1A',
            color: '#10B981',
          }}
        >
          Loading Universal Pro AI...
        </div>
      }
    >
      <RecipeDashboard />
    </Suspense>
  );
}
