'use client';

import { useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Loader2, Share2 } from 'lucide-react';

function ShareTargetHandler() {
  const router = useRouter();
  const searchParams = useSearchParams();

  useEffect(() => {
    const rawUrl = searchParams.get('url');
    const rawText = searchParams.get('text') || '';
    const rawTitle = searchParams.get('title') || '';

    // Find any URL within text or explicit url parameter
    let targetUrl = rawUrl || '';
    if (!targetUrl && rawText) {
      const urlRegex = /(https?:\/\/[^\s]+)/g;
      const match = rawText.match(urlRegex);
      if (match && match.length > 0) {
        targetUrl = match[0];
      }
    }

    if (targetUrl) {
      // Forward to main dashboard with autostart=1
      router.replace(`/?url=${encodeURIComponent(targetUrl)}&autostart=1`);
    } else {
      // If no valid URL found, route to root dashboard
      router.replace('/');
    }
  }, [router, searchParams]);

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        background: 'var(--bg-base)',
        color: 'var(--text-primary)',
        padding: '2rem',
        textAlign: 'center',
      }}
    >
      <div
        className="glass-panel"
        style={{
          padding: '2.5rem',
          maxWidth: '420px',
          width: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '1rem',
        }}
      >
        <div
          style={{
            width: '56px',
            height: '56px',
            borderRadius: '50%',
            background: 'rgba(16, 185, 129, 0.15)',
            border: '1px solid rgba(16, 185, 129, 0.3)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <Share2 size={28} color="var(--accent-emerald)" />
        </div>
        <h2 style={{ fontSize: '1.25rem', fontWeight: 700 }}>Ingesting Shared Reel...</h2>
        <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
          Universal Pro AI is preparing the multimodal extraction pipeline.
        </p>
        <Loader2 size={24} color="var(--accent-emerald)" className="animate-pulse-subtle" />
      </div>
    </div>
  );
}

export default function ShareTargetPage() {
  return (
    <Suspense
      fallback={
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            minHeight: '100vh',
            background: 'var(--bg-base)',
          }}
        >
          <Loader2 size={32} color="#10B981" />
        </div>
      }
    >
      <ShareTargetHandler />
    </Suspense>
  );
}
