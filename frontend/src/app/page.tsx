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
  Globe,
  Layers,
  Dumbbell,
  Code2,
  ShoppingBag,
  MessageSquare,
  Cpu,
  Bookmark,
  Check,
  Copy,
  Download,
  FileText,
  Video,
  Send,
  Smartphone,
} from 'lucide-react';
import ServingAdjuster from '../components/ServingAdjuster';
import VaultLibrary from '../components/VaultLibrary';
import UpgradeModal from '../components/UpgradeModal';
import CreatorTagVault from '../components/CreatorTagVault';

interface ProductItem {
  name: string;
  price?: string;
  search_query?: string;
  links?: {
    amazon?: string;
    flipkart?: string;
    blinkit?: string;
    zepto?: string;
  };
}

interface ResourceItem {
  name: string;
  platform?: string;
  search_query?: string;
}

interface ExtractionResult {
  category?: string;
  title?: string;
  recipe_title?: string;
  summary?: string;
  dish_type?: string;
  workout_split?: string;
  difficulty?: string;
  prep_time?: string;
  cooking_time?: string;
  servings?: number;
  ingredients?: any[];
  instructions?: string[];
  equipment_needed?: string[];
  chef_tips?: string[];
  products?: ProductItem[];
  resources?: ResourceItem[];
  details?: string;
  source_url?: string;
  full_text?: string;
  media_url?: string;
  thumbnail_url?: string;
  cached?: boolean;
}

const DOMAIN_OPTIONS = [
  { id: 'auto', label: 'Auto-Detect (Universal AI)', icon: '⚡' },
  { id: 'recipe', label: '🍳 Cooking Recipe & Food', icon: '🍳' },
  { id: 'kitchen_product', label: '🛍️ Kitchen Finds & Home Gadgets', icon: '🛍️' },
  { id: 'fitness_workout', label: '🏋️ Fitness & Workout Routine', icon: '🏋️' },
  { id: 'tech_diy', label: '💻 Tech Tutorial & Code Guide', icon: '💻' },
  { id: 'unboxing', label: '📦 Product Unboxing & Amazon Finds', icon: '📦' },
  { id: 'diy', label: '💡 Life Hacks & Productivity', icon: '💡' },
];

function UniversalDashboard() {
  const searchParams = useSearchParams();
  const [url, setUrl] = useState<string>('');
  const [selectedDomain, setSelectedDomain] = useState<string>('auto');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [loadingPhase, setLoadingPhase] = useState<string>('Ready');
  const [loadingProgress, setLoadingProgress] = useState<number>(0);
  const [loadingSubtext, setLoadingSubtext] = useState<string>('');
  const [result, setResult] = useState<ExtractionResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isVaultOpen, setIsVaultOpen] = useState<boolean>(false);
  const [isUpgradeModalOpen, setIsUpgradeModalOpen] = useState<boolean>(false);
  const [upgradeReason, setUpgradeReason] = useState<string>('');
  const [isCreatorVaultOpen, setIsCreatorVaultOpen] = useState<boolean>(false);
  const [quotaRemaining, setQuotaRemaining] = useState<number>(10);
  const [copiedLink, setCopiedLink] = useState<boolean>(false);
  const [copiedNotes, setCopiedNotes] = useState<boolean>(false);
  const [downloadedTxt, setDownloadedTxt] = useState<boolean>(false);
  const [waCountryCode, setWaCountryCode] = useState<string>('+91');
  const [waPhoneNumber, setWaPhoneNumber] = useState<string>('');

  // Detect platform from URL
  const detectPlatform = (inputUrl: string) => {
    if (!inputUrl) return null;
    if (inputUrl.includes('instagram.com')) return { name: 'Instagram Reel', color: '#E1306C' };
    if (inputUrl.includes('tiktok.com')) return { name: 'TikTok', color: '#00F2FE' };
    if (inputUrl.includes('youtube.com') || inputUrl.includes('youtu.be'))
      return { name: 'YouTube Short', color: '#FF0000' };
    if (inputUrl.includes('facebook.com')) return { name: 'Facebook Reel', color: '#1877F2' };
    return { name: 'Social Stream', color: '#10B981' };
  };

  const platformInfo = detectPlatform(url);

  // Resolve media preview: Direct video, Instagram Reel iframe embed, or YouTube Short iframe embed
  const resolveMediaPreview = () => {
    const target = result?.source_url || (result as any)?.media_url || url;
    if (!target) return null;

    // 1. Direct video link (mp4, webm, etc.)
    if (result?.media_url && (result.media_url.endsWith('.mp4') || result.media_url.endsWith('.webm') || result.media_url.includes('/video/'))) {
      return {
        type: 'video' as const,
        src: result.media_url,
      };
    }

    // 2. Instagram Reel or Post: /reel/{id} or /p/{id}
    const igMatch = target.match(/instagram\.com\/(?:reel|p|tv)\/([A-Za-z0-9_-]+)/i);
    if (igMatch && igMatch[1]) {
      return {
        type: 'instagram' as const,
        streamSrc: `/api/v1/extract/stream-video?url=${encodeURIComponent(target)}`,
        embedSrc: `https://www.instagram.com/reel/${igMatch[1]}/embed/`,
        externalUrl: `https://www.instagram.com/reel/${igMatch[1]}/`,
        id: igMatch[1],
      };
    }

    // 3. YouTube Shorts or standard YouTube video
    const ytMatch = target.match(/(?:youtube\.com\/(?:shorts\/|watch\?v=)|youtu\.be\/)([A-Za-z0-9_-]{11})/i);
    if (ytMatch && ytMatch[1]) {
      return {
        type: 'youtube' as const,
        src: `https://www.youtube-nocookie.com/embed/${ytMatch[1]}?autoplay=0&rel=0&modestbranding=1`,
        externalUrl: `https://www.youtube.com/shorts/${ytMatch[1]}`,
        id: ytMatch[1],
      };
    }

    // 4. TikTok Video
    const ttMatch = target.match(/tiktok\.com\/(?:@[^/]+\/video\/|v\/)(\d+)/i);
    if (ttMatch && ttMatch[1]) {
      return {
        type: 'tiktok' as const,
        src: `https://www.tiktok.com/embed/v2/${ttMatch[1]}`,
        externalUrl: target,
        id: ttMatch[1],
      };
    }

    return null;
  };

  // Helper to extract clean details if not explicitly present in cached payload
  const getResolvedDetails = (): string => {
    if (result?.details && result.details.trim()) {
      return result.details.trim();
    }
    if ((result as any)?.full_text) {
      const match = (result as any).full_text.match(/(?:Detailed Steps & Notes:|\[DETAILS\]:)\s*={0,50}\s*([\s\S]+)/i);
      if (match && match[1]) {
        return match[1].trim();
      }
    }
    return '';
  };

  const getSectionTitle = (cat?: string) => {
    const c = (cat || '').toUpperCase();
    if (c.includes('FITNESS') || c.includes('WORKOUT')) return 'Workout Routine & Form Steps';
    if (c.includes('TUTORIAL') || c.includes('TECH') || c.includes('CODE')) return 'Step-by-Step Tutorial Guide & Commands';
    if (c.includes('PRODUCT') || c.includes('UNBOXING') || c.includes('GADGET') || c.includes('KITCHEN_FIND')) return 'Key Features, Specifications & Review Notes';
    if (c.includes('RECIPE') || c.includes('COOK')) return 'Cooking Method & Instructions';
    if (c.includes('EDUCATIONAL') || c.includes('EXPLAINER')) return 'Core Concepts & Key Takeaways';
    if (c.includes('FINANCE') || c.includes('BUSINESS')) return 'Strategy, Metrics & Action Steps';
    if (c.includes('BEAUTY') || c.includes('FASHION')) return 'Styling Routine & Application Steps';
    if (c.includes('LIFE_HACK') || c.includes('HACK')) return 'Productivity Hacks & Actionable Tips';
    return 'Detailed Steps & Intelligence Notes';
  };

  const handleCopyNotes = (notes: string) => {
    navigator.clipboard.writeText(notes);
    setCopiedNotes(true);
    setTimeout(() => setCopiedNotes(false), 2000);
  };

  const mediaPreview = resolveMediaPreview();
  const detailsText = getResolvedDetails();

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

  // Dynamic progress bar progression timer & technical stage updater
  useEffect(() => {
    if (!isLoading) {
      return;
    }

    const interval = setInterval(() => {
      setLoadingProgress((prev) => {
        if (prev < 25) return prev + 3.2;
        if (prev < 50) return prev + 2.0;
        if (prev < 75) return prev + 1.2;
        if (prev < 90) return prev + 0.6;
        if (prev < 96) return prev + 0.15;
        return prev;
      });
    }, 150);

    return () => clearInterval(interval);
  }, [isLoading]);

  // Synchronize high-tech stage narrative with progress milestones
  useEffect(() => {
    if (!isLoading) return;
    if (loadingProgress < 25) {
      setLoadingPhase('Ingesting Video Stream & Resolving Media Buffers...');
      setLoadingSubtext('Demuxing container stream and validating media headers');
    } else if (loadingProgress < 50) {
      setLoadingPhase('Sampling Visual Frames & Computing Audio Spectrogram...');
      setLoadingSubtext('Acoustic waveform analysis and frame extraction at 30fps');
    } else if (loadingProgress < 75) {
      setLoadingPhase('Executing Neural Multimodal Vision & Audio Reasoning...');
      setLoadingSubtext('Cross-referencing audio narration with visual action sequences');
    } else if (loadingProgress < 92) {
      setLoadingPhase('Synthesizing Structured Entities & Action Steps...');
      setLoadingSubtext('Structuring chronological steps, ingredient vectors, and equipment');
    } else if (loadingProgress < 99) {
      setLoadingPhase('Validating Output Schema & Shoppable Links...');
      setLoadingSubtext('Resolving verified quick-commerce product tags and parameters');
    }
  }, [isLoading, Math.floor(loadingProgress / 10)]);

  // Polling helper for background jobs (HTTP 202)
  const pollExtractionStatus = async (pollUrl: string, maxAttempts = 60) => {
    for (let i = 0; i < maxAttempts; i++) {
      await new Promise((resolve) => setTimeout(resolve, 1500));
      try {
        const statusRes = await fetch(pollUrl);
        if (statusRes.ok) {
          const statusData = await statusRes.json();
          if (statusData.stage) {
            if (statusData.stage === 'downloading_media') {
              setLoadingPhase('Ingesting Video Stream & Resolving Media Buffers...');
              setLoadingSubtext('Demuxing container stream and validating media headers');
              setLoadingProgress((prev) => Math.max(prev, 25));
            } else if (statusData.stage === 'multimodal_ai_inference') {
              setLoadingPhase('Executing Neural Multimodal Vision & Audio Reasoning...');
              setLoadingSubtext('Cross-referencing audio narration with visual action sequences');
              setLoadingProgress((prev) => Math.max(prev, 60));
            } else if (statusData.stage === 'completed') {
              setLoadingPhase('Extraction Finalized Successfully');
              setLoadingSubtext('Rendering structured intelligence output');
              setLoadingProgress(100);
            }
          }
          if (statusData.progress_percent) {
            setLoadingProgress((prev) => Math.max(prev, statusData.progress_percent));
          }
          if (statusData.status === 'completed' && statusData.data) {
            return statusData.data;
          }
          if (statusData.status === 'failed') {
            throw new Error(statusData.error || 'Extraction processing failed.');
          }
        }
      } catch (pollErr: any) {
        if (pollErr.message && !pollErr.message.includes('fetch')) {
          throw pollErr;
        }
      }
    }
    throw new Error('Extraction timed out. The server is still processing; check the Vault shortly.');
  };

  const handleExtract = async (targetUrl?: any) => {
    const rawUrl = typeof targetUrl === 'string' ? targetUrl : url;
    const finalUrl = typeof rawUrl === 'string' ? rawUrl.trim() : '';

    if (!finalUrl) {
      setError('Please paste a valid video URL from Instagram, TikTok, or YouTube.');
      return;
    }

    setUrl(finalUrl);
    setError(null);
    setIsLoading(true);
    setLoadingProgress(8);
    setLoadingPhase('Ingesting Video Stream & Resolving Media Buffers...');
    setLoadingSubtext('Demuxing container stream and validating media headers');

    try {
      const response = await fetch('/api/v1/extract', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          video_url: finalUrl,
          url: finalUrl,
          domain_hint: selectedDomain,
        }),
      });

      if (!response.ok) {
        if (response.status === 429) {
          setUpgradeReason('Daily free quota limit reached. Upgrade for unlimited extractions!');
          setIsUpgradeModalOpen(true);
          throw new Error('Daily extraction quota reached. Upgrade to Pro for unlimited access.');
        }
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.detail || 'Extraction failed. Please check the URL.');
      }

      const initialData = await response.json();
      let finalData: any = null;

      // Handle async polling if job was enqueued (HTTP 202)
      if (initialData.poll_url && initialData.status === 'queued') {
        finalData = await pollExtractionStatus(initialData.poll_url);
      } else {
        finalData = initialData.data || initialData;
      }

      setLoadingProgress(100);
      setLoadingPhase('Extraction Finalized Successfully');
      setLoadingSubtext('Structured intelligence ready');
      await new Promise((resolve) => setTimeout(resolve, 300));

      setResult(finalData);
      setQuotaRemaining((prev) => Math.max(0, prev - 1));
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'Unable to complete intelligence extraction.');
    } finally {
      setIsLoading(false);
      setLoadingProgress(0);
      setLoadingPhase('Ready');
      setLoadingSubtext('');
    }
  };

  const sampleUrls = [
    { label: '🍳 Butter Chicken Reel', url: 'https://www.instagram.com/reel/C8ButterChickenSample/', domain: 'recipe' },
    { label: '🏋️ 6 Core Bodyweight Workout', url: 'https://www.youtube.com/shorts/65QnIrbBBWs', domain: 'fitness_workout' },
    { label: '💻 Quick Python Tips Short', url: 'https://www.youtube.com/shorts/KrFDs2M_FSE', domain: 'tech_diy' },
    { label: '🛍️ Viral Kitchen Slicer Find', url: 'https://www.instagram.com/reel/C7KitchenSlicerSample/', domain: 'kitchen_product' },
  ];

  const generateStructuredText = (meta: any, isWhatsApp = false): string => {
    if (!meta) return '';
    const title = meta.title || meta.recipe_title || 'Universal AI Extraction';
    const category = (meta.category || meta.category_name || 'INTELLIGENCE').toUpperCase();

    // Category emoji
    let emoji = '⚡';
    if (category.includes('RECIPE') || category.includes('COOK')) emoji = '🍳';
    else if (category.includes('PRODUCT') || category.includes('UNBOX') || category.includes('GADGET')) emoji = '🛍️';
    else if (category.includes('TUTORIAL') || category.includes('TECH') || category.includes('CODE')) emoji = '💻';
    else if (category.includes('FITNESS') || category.includes('WORKOUT')) emoji = '🏋️';
    else if (category.includes('BEAUTY') || category.includes('SKINCARE')) emoji = '✨';
    else if (category.includes('TRAVEL')) emoji = '✈️';

    const lines: string[] = [];

    if (isWhatsApp) {
      lines.push(`${emoji} *${title}*`);
      lines.push(`_${meta.category || 'Universal AI'}_ • Extracted via Universal Pro AI\n`);
    } else {
      lines.push('==================================================');
      lines.push(`${emoji} ${title} (${meta.category || 'Universal Intelligence'})`);
      lines.push('==================================================\n');
    }

    // Summary
    if (meta.summary) {
      lines.push(isWhatsApp ? `📋 *Summary:*\n${meta.summary}\n` : `📋 Summary:\n${meta.summary}\n`);
    }

    // Ingredients (if available)
    if (meta.ingredients && meta.ingredients.length > 0) {
      lines.push(isWhatsApp ? `🥗 *Ingredients:*` : `==================================================\n🥗 Ingredients:\n==================================================`);
      meta.ingredients.forEach((ing: any) => {
        const qty = ing.quantity ? ` - ${ing.quantity}` : '';
        const unit = ing.unit ? ` ${ing.unit}` : '';
        lines.push(`• ${ing.name}${qty}${unit}`);
      });
      lines.push('');
    }

    // Instructions / Steps / Specifications
    const secTitle = getSectionTitle(meta.category);
    if (meta.instructions && meta.instructions.length > 0) {
      lines.push(isWhatsApp ? `📝 *${secTitle}:*` : `==================================================\n📝 ${secTitle}:\n==================================================`);
      meta.instructions.forEach((step: string, idx: number) => {
        const cleanStep = isWhatsApp ? step.replace(/\*\*/g, '*') : step.replace(/\*\*/g, '');
        lines.push(`${idx + 1}. ${cleanStep}`);
      });
      lines.push('');
    } else if (meta.details || detailsText) {
      const d = meta.details || detailsText;
      lines.push(isWhatsApp ? `📝 *${secTitle}:*\n${d}\n` : `==================================================\n📝 ${secTitle}:\n==================================================\n\n${d}\n`);
    }

    // Products & E-Commerce / Quick Commerce Links
    if (meta.products && meta.products.length > 0) {
      const isRecipe = category.includes('RECIPE') || category.includes('COOK');
      const prodHeader = isRecipe ? '🛒 Ingredients & 1-Click Buy Links:' : '🛍️ Featured Products & 1-Click Buy Links:';
      lines.push(isWhatsApp ? `*${prodHeader}*` : `==================================================\n${prodHeader}\n==================================================`);
      meta.products.forEach((p: any, idx: number) => {
        const priceStr = p.price ? ` (${p.price})` : '';
        lines.push(`${idx + 1}. ${p.name}${priceStr}`);
        if (p.blinkit_url) lines.push(`   🟡 Blinkit (10-Min): ${p.blinkit_url}`);
        if (p.zepto_url) lines.push(`   ⚡ Zepto (10-Min): ${p.zepto_url}`);
        if (p.instamart_url) lines.push(`   🛵 Swiggy Instamart: ${p.instamart_url}`);
        if (p.amazon_url) lines.push(`   🛒 Amazon: ${p.amazon_url}`);
        if (p.flipkart_url) lines.push(`   ⚡ Flipkart: ${p.flipkart_url}`);
      });
      lines.push('');
    }

    // Tutorial Resources
    if (meta.resources && meta.resources.length > 0) {
      lines.push(isWhatsApp ? `🎓 *Tutorial & Learning Links:*` : `==================================================\n🎓 Tutorial & Learning Links:\n==================================================`);
      meta.resources.forEach((r: any, idx: number) => {
        lines.push(`${idx + 1}. ${r.name}`);
        if (r.youtube_url) lines.push(`   ▶️ YouTube: ${r.youtube_url}`);
        if (r.github_url) lines.push(`   🐙 GitHub: ${r.github_url}`);
      });
      lines.push('');
    }

    if (isWhatsApp) {
      lines.push(`💡 _Full notes & file downloads at: https://universal-pro-ai.vercel.app_`);
    } else {
      lines.push('==================================================');
      lines.push('Extracted via Universal Pro AI — Sub-3s Multimodal Video Intelligence');
      lines.push('https://universal-pro-ai.vercel.app');
      lines.push('==================================================');
    }

    return lines.join('\n');
  };

  const handleShareWhatsApp = (customPhone?: string) => {
    if (!result) return;
    const fullText = generateStructuredText(result, true);

    let phoneParam = '';
    const phoneToUse = customPhone !== undefined ? customPhone : waPhoneNumber;
    if (phoneToUse && phoneToUse.trim()) {
      const cleanDigits = phoneToUse.replace(/[^\d]/g, '');
      const ccDigits = waCountryCode.replace(/[^\d]/g, '') || '91';
      const fullDigits = cleanDigits.startsWith(ccDigits) ? cleanDigits : `${ccDigits}${cleanDigits}`;
      phoneParam = `phone=${fullDigits}&`;
    }

    let encodedText = encodeURIComponent(fullText);
    // WhatsApp URL length guardrail (~3800 chars)
    if (encodedText.length > 3800) {
      const compactText = generateStructuredText(result, true).slice(0, 2600) + '\n\n... (Full notes & buy links in downloaded .txt)\n\n🔗 https://universal-pro-ai.vercel.app';
      encodedText = encodeURIComponent(compactText);
    }

    window.open(`https://api.whatsapp.com/send?${phoneParam}text=${encodedText}`, '_blank');
  };

  const handleDownloadTxt = () => {
    if (!result) return;
    const txtContent = generateStructuredText(result, false);
    const title = result.title || result.recipe_title || 'Universal_Intelligence';
    const cleanFileName = `${title.replace(/[^a-zA-Z0-9_\-]/g, '_').slice(0, 45)}_Notes.txt`;

    const blob = new Blob([txtContent], { type: 'text/plain;charset=utf-8' });
    const blobUrl = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = blobUrl;
    link.download = cleanFileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(blobUrl);
  };

  const handleDownloadVideo = () => {
    if (!result) return;
    const videoSrc = (result as any).media_url || (result as any).video_source || url;
    if (videoSrc) {
      if (videoSrc.endsWith('.mp4')) {
        const link = document.createElement('a');
        link.href = videoSrc;
        link.download = `${(result.title || 'video').replace(/[^a-zA-Z0-9_\-]/g, '_')}.mp4`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } else {
        window.open(videoSrc, '_blank');
      }
    }
  };

  const handleCopyLink = () => {
    navigator.clipboard.writeText(window.location.href);
    setCopiedLink(true);
    setTimeout(() => setCopiedLink(false), 2000);
  };

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
            flexWrap: 'wrap',
            gap: '0.75rem',
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
              <Zap size={20} color="#FFFFFF" />
            </div>
            <div>
              <span style={{ fontSize: '1.15rem', fontWeight: 800, letterSpacing: '-0.02em' }}>
                UNIVERSAL <span className="gradient-text">PRO AI</span>
              </span>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
            {/* Intelligence Vault Library Button */}
            <button
              onClick={() => setIsVaultOpen(true)}
              className="btn-ghost"
              style={{ padding: '0.45rem 0.85rem' }}
            >
              <BookOpen size={16} color="var(--accent-emerald)" />
              <span>Intelligence Vault</span>
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
              Sub-3s Universal AI • Multi-Genre Multimodal Engine
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
            Universal Reel & Shorts <br />
            <span className="gradient-text">AI Intelligence Extractor</span>
          </h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '1rem', maxWidth: '680px', margin: '0 auto' }}>
            Turn any Instagram Reel or YouTube Short into structured step-by-step recipes, workout
            routines, code tutorials, and monetized shoppable product links — in under 3 seconds.
          </p>
        </div>

        {/* Input Bar Card with Domain Selector */}
        <div
          className="glass-panel"
          style={{
            maxWidth: '820px',
            margin: '0 auto 1.5rem',
            padding: '1rem',
            boxShadow: '0 10px 40px rgba(0, 0, 0, 0.4)',
          }}
        >
          {/* Domain Selector Bar */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              marginBottom: '0.75rem',
              paddingBottom: '0.65rem',
              borderBottom: '1px solid var(--border-subtle)',
              flexWrap: 'wrap',
              gap: '0.5rem',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--text-secondary)' }}>
                🎯 Content Domain:
              </span>
              <select
                value={selectedDomain}
                onChange={(e) => setSelectedDomain(e.target.value)}
                style={{
                  background: 'rgba(255, 255, 255, 0.06)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '8px',
                  color: 'var(--text-primary)',
                  padding: '0.35rem 0.75rem',
                  fontSize: '0.8rem',
                  fontWeight: 600,
                  outline: 'none',
                  cursor: 'pointer',
                }}
              >
                {DOMAIN_OPTIONS.map((d) => (
                  <option key={d.id} value={d.id} style={{ background: '#0F172A', color: '#F8FAFC' }}>
                    {d.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

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
              placeholder="Paste Instagram Reel, TikTok, or YouTube Short link (e.g. https://...)"
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
                  <span>Extract Intelligence</span>
                  <ArrowRight size={16} />
                </>
              )}
            </button>
          </div>

          {/* Quick Sample Chips across multiple domains */}
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
                  setSelectedDomain(s.domain);
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

        {/* Dynamic Technical Progress Bar & Intelligence Deck */}
        {isLoading && (
          <div
            className="glass-panel"
            style={{
              maxWidth: '820px',
              margin: '0 auto 2rem',
              padding: '1.35rem 1.5rem',
              border: '1px solid var(--border-active)',
              position: 'relative',
              overflow: 'hidden',
              boxShadow: '0 8px 32px rgba(0, 0, 0, 0.35)',
            }}
          >
            {/* Header: Status Icon, Technical Phase, and Percentage */}
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                marginBottom: '0.75rem',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
                <Zap size={18} color="var(--accent-emerald)" className="animate-pulse-subtle" />
                <span
                  style={{
                    fontWeight: 600,
                    fontSize: '0.92rem',
                    color: 'var(--accent-emerald)',
                    letterSpacing: '-0.01em',
                  }}
                >
                  {loadingPhase}
                </span>
              </div>
              <span
                style={{
                  fontFamily: 'monospace',
                  fontSize: '0.85rem',
                  fontWeight: 700,
                  color: 'var(--text-secondary)',
                  letterSpacing: '0.02em',
                }}
              >
                {Math.round(loadingProgress)}%
              </span>
            </div>

            {/* Glowing Dynamic Progress Track */}
            <div
              style={{
                width: '100%',
                height: '6px',
                background: 'rgba(255, 255, 255, 0.08)',
                borderRadius: '9999px',
                overflow: 'hidden',
                position: 'relative',
              }}
            >
              <div
                style={{
                  height: '100%',
                  width: `${Math.min(100, Math.max(0, loadingProgress))}%`,
                  background: 'linear-gradient(90deg, #10B981 0%, #06B6D4 50%, #3B82F6 100%)',
                  borderRadius: '9999px',
                  transition: 'width 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
                  boxShadow: '0 0 14px rgba(16, 185, 129, 0.5)',
                }}
              />
            </div>

            {/* Technical Subtext (Without Model Names or Specifics) */}
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                marginTop: '0.65rem',
              }}
            >
              <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                {loadingSubtext || 'Real-Time Multimodal Intelligence Pipeline Active'}
              </span>
              <span
                style={{
                  fontSize: '0.68rem',
                  color: 'var(--accent-emerald)',
                  fontFamily: 'monospace',
                  letterSpacing: '0.05em',
                }}
              >
                PIPELINE_STATUS: ACTIVE
              </span>
            </div>
          </div>
        )}

        {/* Error Alert */}
        {error && (
          <div
            className="glass-panel"
            style={{
              maxWidth: '820px',
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

        {/* Platform Superpowers Showcase (Displayed when no active extraction) */}
        {!result && !isLoading && (
          <div style={{ maxWidth: '980px', margin: '2.5rem auto 0' }}>
            <h2
              style={{
                fontSize: '1rem',
                fontWeight: 700,
                textTransform: 'uppercase',
                letterSpacing: '0.08em',
                color: 'var(--text-secondary)',
                textAlign: 'center',
                marginBottom: '1.25rem',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '0.5rem',
              }}
            >
              <Sparkles size={16} color="var(--accent-emerald)" />
              <span>Platform Superpowers</span>
            </h2>

            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
                gap: '1rem',
              }}
            >
              <div className="glass-panel" style={{ padding: '1.25rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.5rem' }}>
                  <Globe size={20} color="#38BDF8" />
                  <h3 style={{ fontSize: '0.92rem', fontWeight: 700 }}>Universal Stream Parsing</h3>
                </div>
                <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', lineHeight: 1.45 }}>
                  Seamless ingestion of Instagram Reels, YouTube Shorts, and TikTok with high-res auto-resolution.
                </p>
              </div>

              <div className="glass-panel" style={{ padding: '1.25rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.5rem' }}>
                  <Cpu size={20} color="#A78BFA" />
                  <h3 style={{ fontSize: '0.92rem', fontWeight: 700 }}>Multimodal Neural Vision</h3>
                </div>
                <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', lineHeight: 1.45 }}>
                  Simultaneously analyzes video frames, on-screen text, audio transcripts & voiceovers.
                </p>
              </div>

              <div className="glass-panel" style={{ padding: '1.25rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.5rem' }}>
                  <ShoppingBag size={20} color="#F472B6" />
                  <h3 style={{ fontSize: '0.92rem', fontWeight: 700 }}>Shoppable Product Links</h3>
                </div>
                <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', lineHeight: 1.45 }}>
                  Identifies cookware, fitness gear, gadgets & ingredients with instant 1-click buy tags.
                </p>
              </div>

              <div className="glass-panel" style={{ padding: '1.25rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.5rem' }}>
                  <MessageSquare size={20} color="#34D399" />
                  <h3 style={{ fontSize: '0.92rem', fontWeight: 700 }}>Instant WhatsApp Sync</h3>
                </div>
                <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', lineHeight: 1.45 }}>
                  Direct delivery of clean, formatted intelligence notes straight to your phone.
                </p>
              </div>
            </div>

            {/* Bottom Telemetry Badges */}
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '1rem',
                marginTop: '1.75rem',
                flexWrap: 'wrap',
              }}
            >
              <span className="badge-pill" style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid var(--border-subtle)' }}>
                ⚡ ~2.4s AI Turnaround
              </span>
              <span className="badge-pill" style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid var(--border-subtle)' }}>
                🛒 Amazon and Flipkart link
              </span>
              <span className="badge-pill" style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid var(--border-subtle)' }}>
                📲 1-Click WhatsApp Share
              </span>
            </div>
          </div>
        )}

        {/* Extraction Results: Multi-Genre Responsive View */}
        {result && (
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))',
              gap: '2rem',
              marginTop: '1.5rem',
            }}
          >
            {/* Left Column: Docked Media Player & Domain Telemetry */}
            <div>
              <div className="glass-panel" style={{ padding: '1rem', overflow: 'hidden' }}>
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    marginBottom: '0.75rem',
                  }}
                >
                  <span
                    style={{
                      fontSize: '0.75rem',
                      fontWeight: 700,
                      textTransform: 'uppercase',
                      letterSpacing: '0.05em',
                      color: 'var(--text-secondary)',
                    }}
                  >
                    Single-Docked Media Player
                  </span>
                  {result.cached && (
                    <span className="badge-pill badge-emerald">⚡ Instant Cache Hit</span>
                  )}
                </div>

                {/* Video / Media Display */}
                {mediaPreview?.type === 'instagram' ? (
                  <div style={{ position: 'relative', width: '100%', borderRadius: 'var(--radius-sm)', overflow: 'hidden', background: '#05070D' }}>
                    <video
                      src={mediaPreview.streamSrc}
                      controls
                      playsInline
                      preload="metadata"
                      style={{
                        width: '100%',
                        maxHeight: '460px',
                        borderRadius: 'var(--radius-sm)',
                        background: '#05070D',
                        objectFit: 'contain',
                        display: 'block',
                      }}
                      onError={(e) => {
                        const target = e.currentTarget;
                        target.style.display = 'none';
                        const fallbackIframe = document.getElementById('ig-fallback-iframe');
                        if (fallbackIframe) fallbackIframe.style.display = 'block';
                      }}
                    />
                    <iframe
                      id="ig-fallback-iframe"
                      src={mediaPreview.embedSrc}
                      title="Instagram Reel Preview"
                      style={{
                        display: 'none',
                        width: '100%',
                        height: '460px',
                        border: 'none',
                        background: '#05070D',
                        borderRadius: 'var(--radius-sm)',
                      }}
                      allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share"
                      allowFullScreen
                    />
                    <div style={{ marginTop: '0.45rem', display: 'flex', justifyContent: 'center' }}>
                      <a
                        href={mediaPreview.externalUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{
                          fontSize: '0.78rem',
                          color: '#E1306C',
                          textDecoration: 'none',
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '4px',
                          fontWeight: 600,
                        }}
                      >
                        <span>▶ Open Reel in Instagram App</span>
                        <ExternalLink size={12} />
                      </a>
                    </div>
                  </div>
                ) : mediaPreview?.type === 'youtube' ? (
                  <div style={{ position: 'relative', width: '100%', borderRadius: 'var(--radius-sm)', overflow: 'hidden' }}>
                    <iframe
                      src={mediaPreview.src}
                      title="YouTube Short Preview"
                      style={{
                        width: '100%',
                        height: '460px',
                        border: 'none',
                        background: '#05070D',
                        borderRadius: 'var(--radius-sm)',
                      }}
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                      allowFullScreen
                    />
                    <div style={{ marginTop: '0.45rem', display: 'flex', justifyContent: 'center' }}>
                      <a
                        href={mediaPreview.externalUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{
                          fontSize: '0.78rem',
                          color: '#FF0000',
                          textDecoration: 'none',
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '4px',
                          fontWeight: 600,
                        }}
                      >
                        <span>▶ Watch on YouTube Shorts</span>
                        <ExternalLink size={12} />
                      </a>
                    </div>
                  </div>
                ) : mediaPreview?.type === 'video' ? (
                  <video
                    src={mediaPreview.src}
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
                      height: '320px',
                      background: 'rgba(0, 0, 0, 0.4)',
                      borderRadius: 'var(--radius-sm)',
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                      justifyContent: 'center',
                      border: '1px dashed var(--border-subtle)',
                      gap: '0.5rem',
                      padding: '1rem',
                      textAlign: 'center',
                    }}
                  >
                    <Play size={40} color="var(--accent-emerald)" opacity={0.6} />
                    <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                      Source Stream Ingested
                    </span>
                    {(result.source_url || url) && (
                      <a
                        href={result.source_url || url}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{
                          marginTop: '0.4rem',
                          fontSize: '0.78rem',
                          color: 'var(--accent-emerald)',
                          textDecoration: 'none',
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '4px',
                          background: 'rgba(16, 185, 129, 0.1)',
                          padding: '4px 10px',
                          borderRadius: '6px',
                          border: '1px solid rgba(16, 185, 129, 0.25)',
                        }}
                      >
                        <span>View Source Reel</span>
                        <ExternalLink size={12} />
                      </a>
                    )}
                  </div>
                )}

                {/* Telemetry Metrics */}
                <div
                  style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(2, 1fr)',
                    gap: '0.5rem',
                    marginTop: '1rem',
                  }}
                >
                  <div className="glass-card" style={{ textAlign: 'center', padding: '0.65rem' }}>
                    <Clock size={16} color="var(--accent-emerald)" style={{ margin: '0 auto 0.25rem' }} />
                    <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>Duration</div>
                    <div style={{ fontSize: '0.85rem', fontWeight: 600 }}>
                      {result.cooking_time || result.prep_time || 'Short Form'}
                    </div>
                  </div>

                  <div className="glass-card" style={{ textAlign: 'center', padding: '0.65rem' }}>
                    <Flame size={16} color="var(--accent-amber)" style={{ margin: '0 auto 0.25rem' }} />
                    <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>Domain</div>
                    <div style={{ fontSize: '0.85rem', fontWeight: 600 }}>
                      {result.category || result.dish_type || 'Intelligence'}
                    </div>
                  </div>
                </div>

                {/* Forward, Export & Download Hub */}
                <div style={{ marginTop: '1rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  {/* Row 1: WhatsApp Full Intelligence & Download .txt */}
                  <div style={{ display: 'flex', gap: '0.5rem' }}>
                    <button
                      onClick={() => handleShareWhatsApp()}
                      style={{
                        flex: 1.15,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '0.45rem',
                        background: 'linear-gradient(135deg, #25D366, #128C7E)',
                        color: '#FFFFFF',
                        border: 'none',
                        borderRadius: '8px',
                        padding: '0.55rem 0.65rem',
                        fontSize: '0.78rem',
                        fontWeight: 700,
                        cursor: 'pointer',
                        boxShadow: '0 3px 12px rgba(37, 211, 102, 0.35)',
                      }}
                      title="Share complete recipe and buy links via WhatsApp"
                    >
                      <MessageSquare size={14} />
                      <span>WhatsApp Notes</span>
                    </button>

                    <button
                      onClick={() => {
                        handleDownloadTxt();
                        setDownloadedTxt(true);
                        setTimeout(() => setDownloadedTxt(false), 2500);
                      }}
                      style={{
                        flex: 1,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '0.45rem',
                        background: 'linear-gradient(135deg, #0284C7, #0369A1)',
                        color: '#FFFFFF',
                        border: 'none',
                        borderRadius: '8px',
                        padding: '0.55rem 0.65rem',
                        fontSize: '0.78rem',
                        fontWeight: 700,
                        cursor: 'pointer',
                        boxShadow: '0 3px 12px rgba(2, 132, 199, 0.35)',
                      }}
                      title="Download complete structured intelligence as a clean .txt file"
                    >
                      {downloadedTxt ? <Check size={14} color="#34D399" /> : <Download size={14} />}
                      <span>{downloadedTxt ? 'Downloaded!' : 'Download .txt'}</span>
                    </button>
                  </div>

                  {/* Row 2: Source Video / Download & Copy Link */}
                  <div style={{ display: 'flex', gap: '0.5rem' }}>
                    <button
                      onClick={handleDownloadVideo}
                      style={{
                        flex: 1,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '0.4rem',
                        background: 'rgba(255, 255, 255, 0.06)',
                        color: 'var(--text-primary)',
                        border: '1px solid var(--border-subtle)',
                        borderRadius: '8px',
                        padding: '0.48rem',
                        fontSize: '0.74rem',
                        fontWeight: 600,
                        cursor: 'pointer',
                      }}
                      title="Open source stream or download video"
                    >
                      <Video size={13} color="#38BDF8" />
                      <span>Video Stream</span>
                    </button>

                    <button
                      onClick={handleCopyLink}
                      style={{
                        flex: 1,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '0.4rem',
                        background: 'rgba(255, 255, 255, 0.06)',
                        color: 'var(--text-primary)',
                        border: '1px solid var(--border-subtle)',
                        borderRadius: '8px',
                        padding: '0.48rem',
                        fontSize: '0.74rem',
                        fontWeight: 600,
                        cursor: 'pointer',
                      }}
                    >
                      {copiedLink ? <Check size={13} color="#34D399" /> : <Share2 size={13} />}
                      <span>{copiedLink ? 'Link Copied!' : 'Copy Link'}</span>
                    </button>
                  </div>

                  {/* Direct WhatsApp Forward Drawer */}
                  <div
                    style={{
                      marginTop: '0.25rem',
                      padding: '0.55rem 0.65rem',
                      background: 'rgba(15, 23, 42, 0.65)',
                      border: '1px solid rgba(56, 189, 248, 0.22)',
                      borderRadius: '8px',
                    }}
                  >
                    <div style={{ marginBottom: '0.35rem' }}>
                      <span style={{ fontSize: '0.7rem', fontWeight: 600, color: '#38BDF8', display: 'flex', alignItems: 'center', gap: '4px' }}>
                        <Smartphone size={11} />
                        <span>Send directly to WhatsApp Number:</span>
                      </span>
                    </div>

                    <div style={{ display: 'flex', gap: '0.35rem' }}>
                      <input
                        type="text"
                        value={waCountryCode}
                        onChange={(e) => setWaCountryCode(e.target.value)}
                        placeholder="+91"
                        style={{
                          width: '46px',
                          padding: '0.32rem 0.4rem',
                          background: 'rgba(0,0,0,0.3)',
                          border: '1px solid var(--border-subtle)',
                          borderRadius: '6px',
                          color: '#FFFFFF',
                          fontSize: '0.72rem',
                          textAlign: 'center',
                        }}
                      />
                      <input
                        type="tel"
                        value={waPhoneNumber}
                        onChange={(e) => setWaPhoneNumber(e.target.value)}
                        placeholder="Mobile (e.g. 9876543210)"
                        style={{
                          flex: 1,
                          padding: '0.32rem 0.5rem',
                          background: 'rgba(0,0,0,0.3)',
                          border: '1px solid var(--border-subtle)',
                          borderRadius: '6px',
                          color: '#FFFFFF',
                          fontSize: '0.72rem',
                        }}
                      />
                      <button
                        onClick={() => handleShareWhatsApp(waPhoneNumber)}
                        style={{
                          background: '#10B981',
                          color: '#FFFFFF',
                          border: 'none',
                          borderRadius: '6px',
                          padding: '0.32rem 0.65rem',
                          fontSize: '0.72rem',
                          fontWeight: 700,
                          cursor: 'pointer',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '3px',
                        }}
                      >
                        <Send size={11} />
                        <span>Send</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Right Column: Structured Intelligence Guide & Products */}
            <div>
              <div className="glass-panel" style={{ padding: '1.5rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                  <span className="badge-pill badge-emerald" style={{ fontSize: '0.7rem' }}>
                    {result.category || 'UNIVERSAL INTELLIGENCE'}
                  </span>
                </div>

                <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '0.4rem' }}>
                  {result.title || result.recipe_title || 'Extracted Social Intelligence'}
                </h2>

                {result.summary && (
                  <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.5, marginBottom: '1.25rem' }}>
                    {result.summary}
                  </p>
                )}

                {/* Recipe-Specific: Serving Scaler if Ingredients exist */}
                {result.ingredients && result.ingredients.length > 0 && (
                  <div style={{ marginBottom: '1.5rem' }}>
                    <ServingAdjuster
                      initialServings={result.servings || 2}
                      ingredients={result.ingredients}
                      recipeTitle={result.title || result.recipe_title || 'Recipe'}
                    />
                  </div>
                )}

                {/* Step-by-Step Instructions / Workout Routines / Features & Specs */}
                <div style={{ marginTop: '1.25rem' }}>
                  <div
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      marginBottom: '0.75rem',
                    }}
                  >
                    <h3
                      style={{
                        fontSize: '1rem',
                        fontWeight: 600,
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.5rem',
                        margin: 0,
                      }}
                    >
                      <CheckCircle2 size={18} color="var(--accent-emerald)" />
                      <span>{getSectionTitle(result.category)}</span>
                    </h3>

                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <button
                        onClick={() => {
                          handleDownloadTxt();
                          setDownloadedTxt(true);
                          setTimeout(() => setDownloadedTxt(false), 2500);
                        }}
                        style={{
                          background: 'rgba(2, 132, 199, 0.15)',
                          border: '1px solid rgba(56, 189, 248, 0.3)',
                          borderRadius: '6px',
                          color: '#38BDF8',
                          padding: '4px 9px',
                          fontSize: '0.74rem',
                          fontWeight: 600,
                          cursor: 'pointer',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '4px',
                        }}
                        title="Download complete structured intelligence as a .txt file"
                      >
                        {downloadedTxt ? <Check size={12} color="#34D399" /> : <Download size={12} />}
                        <span>{downloadedTxt ? 'Downloaded!' : '.txt Notes'}</span>
                      </button>

                      <button
                        onClick={() => handleShareWhatsApp()}
                        style={{
                          background: 'rgba(37, 211, 102, 0.15)',
                          border: '1px solid rgba(37, 211, 102, 0.3)',
                          borderRadius: '6px',
                          color: '#25D366',
                          padding: '4px 9px',
                          fontSize: '0.74rem',
                          fontWeight: 600,
                          cursor: 'pointer',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '4px',
                        }}
                        title="Share complete recipe and notes via WhatsApp"
                      >
                        <MessageSquare size={12} />
                        <span>WhatsApp</span>
                      </button>

                      {detailsText && (
                        <button
                          onClick={() => handleCopyNotes(detailsText)}
                          style={{
                            background: 'rgba(255, 255, 255, 0.05)',
                            border: '1px solid var(--border-subtle)',
                            borderRadius: '6px',
                            color: 'var(--text-secondary)',
                            padding: '4px 9px',
                            fontSize: '0.74rem',
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '4px',
                          }}
                        >
                          {copiedNotes ? <Check size={12} color="#34D399" /> : <Copy size={12} />}
                          <span>{copiedNotes ? 'Copied!' : 'Copy Notes'}</span>
                        </button>
                      )}
                    </div>
                  </div>

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
                          <p style={{ fontSize: '0.88rem', lineHeight: 1.45, color: 'var(--text-primary)', margin: 0 }}>
                            {step}
                          </p>
                        </div>
                      ))
                    ) : detailsText ? (
                      <div
                        style={{
                          display: 'flex',
                          flexDirection: 'column',
                          gap: '0.5rem',
                        }}
                      >
                        {detailsText.split('\n').map((line, idx) => {
                          const trimmed = line.trim();
                          if (!trimmed) return null;

                          if (trimmed.startsWith('**') && (trimmed.endsWith('**') || trimmed.endsWith(':**') || trimmed.endsWith('**:') || trimmed.endsWith(':'))) {
                            const cleanHeader = trimmed.replace(/\*\*/g, '').replace(/:$/, '');
                            return (
                              <div
                                key={idx}
                                style={{
                                  fontSize: '0.88rem',
                                  fontWeight: 700,
                                  color: 'var(--accent-emerald)',
                                  marginTop: idx > 0 ? '0.5rem' : 0,
                                  display: 'flex',
                                  alignItems: 'center',
                                  gap: '0.35rem',
                                }}
                              >
                                <span>⚡</span>
                                <span>{cleanHeader}</span>
                              </div>
                            );
                          }

                          if (trimmed.startsWith('- ') || trimmed.startsWith('* ') || trimmed.startsWith('• ')) {
                            const withoutBullet = trimmed.replace(/^[-*•]\s*/, '');
                            const boldMatch = withoutBullet.match(/^\*\*([^*]+)\*\*:\s*(.+)$/);
                            if (boldMatch) {
                              return (
                                <div
                                  key={idx}
                                  style={{
                                    display: 'flex',
                                    alignItems: 'flex-start',
                                    gap: '0.6rem',
                                    padding: '0.55rem 0.75rem',
                                    background: 'rgba(255, 255, 255, 0.02)',
                                    borderRadius: '8px',
                                    border: '1px solid rgba(255, 255, 255, 0.04)',
                                    fontSize: '0.88rem',
                                    lineHeight: 1.5,
                                  }}
                                >
                                  <span style={{ color: 'var(--accent-emerald)', fontWeight: 700, minWidth: '6px' }}>•</span>
                                  <div>
                                    <strong style={{ color: '#38BDF8', fontWeight: 600 }}>{boldMatch[1]}: </strong>
                                    <span style={{ color: 'var(--text-primary)' }}>{boldMatch[2]}</span>
                                  </div>
                                </div>
                              );
                            }
                            return (
                              <div
                                key={idx}
                                style={{
                                  display: 'flex',
                                  alignItems: 'flex-start',
                                  gap: '0.6rem',
                                  padding: '0.55rem 0.75rem',
                                  background: 'rgba(255, 255, 255, 0.02)',
                                  borderRadius: '8px',
                                  border: '1px solid rgba(255, 255, 255, 0.04)',
                                  fontSize: '0.88rem',
                                  lineHeight: 1.5,
                                  color: 'var(--text-primary)',
                                }}
                              >
                                <span style={{ color: 'var(--accent-emerald)', fontWeight: 700 }}>•</span>
                                <span>{withoutBullet}</span>
                              </div>
                            );
                          }

                          return (
                            <p key={idx} style={{ fontSize: '0.88rem', color: 'var(--text-primary)', margin: '0.2rem 0', lineHeight: 1.5 }}>
                              {trimmed}
                            </p>
                          );
                        })}
                      </div>
                    ) : (
                      <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                        Follow the video clip for exact step-by-step guidance.
                      </p>
                    )}
                  </div>
                </div>

                {/* Shoppable Products & Gadgets Section */}
                {result.products && result.products.length > 0 && (
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
                      <ShoppingCart size={18} color="#F472B6" />
                      <span>Featured Products & 1-Click Buy Links</span>
                    </h3>

                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '0.75rem' }}>
                      {result.products.map((p, idx) => (
                        <div
                          key={idx}
                          style={{
                            padding: '0.75rem',
                            background: 'rgba(255, 255, 255, 0.02)',
                            borderRadius: '8px',
                            border: '1px solid var(--border-subtle)',
                            display: 'flex',
                            flexDirection: 'column',
                            justifyContent: 'space-between',
                          }}
                        >
                          <div>
                            <span style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                              {p.name}
                            </span>
                            {p.price && (
                              <div style={{ fontSize: '0.75rem', color: '#34D399', marginTop: '0.2rem' }}>
                                {p.price}
                              </div>
                            )}
                          </div>
                          <div style={{ display: 'flex', gap: '0.4rem', marginTop: '0.65rem' }}>
                            <a
                              href={
                                p.links?.amazon ||
                                `https://www.amazon.in/s?k=${encodeURIComponent(p.search_query || p.name)}&tag=manasdas11155-21`
                              }
                              target="_blank"
                              rel="noopener noreferrer"
                              style={{
                                flex: 1,
                                textAlign: 'center',
                                padding: '0.3rem 0.5rem',
                                background: 'rgba(255, 153, 0, 0.15)',
                                color: '#FF9900',
                                border: '1px solid rgba(255, 153, 0, 0.3)',
                                borderRadius: '6px',
                                fontSize: '0.72rem',
                                fontWeight: 700,
                                textDecoration: 'none',
                              }}
                            >
                              Amazon
                            </a>
                            <a
                              href={
                                p.links?.flipkart ||
                                `https://www.flipkart.com/search?q=${encodeURIComponent(p.search_query || p.name)}`
                              }
                              target="_blank"
                              rel="noopener noreferrer"
                              style={{
                                flex: 1,
                                textAlign: 'center',
                                padding: '0.3rem 0.5rem',
                                background: 'rgba(40, 116, 240, 0.15)',
                                color: '#60A5FA',
                                border: '1px solid rgba(40, 116, 240, 0.3)',
                                borderRadius: '6px',
                                fontSize: '0.72rem',
                                fontWeight: 700,
                                textDecoration: 'none',
                              }}
                            >
                              Flipkart
                            </a>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Educational / Tutorial Resources if present */}
                {result.resources && result.resources.length > 0 && (
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
                      <BookOpen size={18} color="#38BDF8" />
                      <span>Recommended Learning Resources</span>
                    </h3>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                      {result.resources.map((resItem, idx) => (
                        <div
                          key={idx}
                          style={{
                            padding: '0.65rem 0.85rem',
                            background: 'rgba(56, 189, 248, 0.05)',
                            border: '1px solid rgba(56, 189, 248, 0.2)',
                            borderRadius: '8px',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'space-between',
                          }}
                        >
                          <div>
                            <span style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-primary)' }}>
                              {resItem.name}
                            </span>
                            {resItem.platform && (
                              <span style={{ fontSize: '0.72rem', color: '#38BDF8', marginLeft: '0.5rem' }}>
                                ({resItem.platform})
                              </span>
                            )}
                          </div>
                          <a
                            href={`https://www.youtube.com/results?search_query=${encodeURIComponent(resItem.search_query || resItem.name)}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            style={{
                              padding: '0.25rem 0.55rem',
                              background: 'rgba(255, 0, 0, 0.15)',
                              color: '#FF6B6B',
                              border: '1px solid rgba(255, 0, 0, 0.3)',
                              borderRadius: '6px',
                              fontSize: '0.72rem',
                              fontWeight: 600,
                              textDecoration: 'none',
                            }}
                          >
                            Watch
                          </a>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Secret Tip / Expert Advice */}
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
                      💡 Expert Secret Tip:
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

      {/* Slide-out Intelligence Vault Library Drawer */}
      <VaultLibrary
        isOpen={isVaultOpen}
        onClose={() => setIsVaultOpen(false)}
        onSelectRecipe={(savedRecipe) => {
          setResult(savedRecipe);
        }}
      />

      {/* Pro Upgrade Checkout Modal */}
      <UpgradeModal
        isOpen={isUpgradeModalOpen}
        onClose={() => setIsUpgradeModalOpen(false)}
        reason={upgradeReason}
      />

      {/* Creator Tag Vault Drawer */}
      <CreatorTagVault
        isOpen={isCreatorVaultOpen}
        onClose={() => setIsCreatorVaultOpen(false)}
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
      <UniversalDashboard />
    </Suspense>
  );
}
