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
  HelpCircle,
  Sun,
  Moon,
} from 'lucide-react';
import ServingAdjuster from '../components/ServingAdjuster';
import VaultLibrary from '../components/VaultLibrary';
import UpgradeModal from '../components/UpgradeModal';
import FaqSection from '../components/FaqSection';
import ParticleBackground from '../components/ParticleBackground';
import CookingModeDrawer from '../components/CookingModeDrawer';
import { ProductItem, ResourceItem, ExtractionResult } from '../types/recipe';


const DOMAIN_OPTIONS = [
  { id: 'auto', label: 'Auto-Detect (Universal AI)', icon: '⚡' },
  { id: 'recipe', label: '🍳 Cooking Recipe & Food', icon: '🍳' },
  { id: 'kitchen_product', label: '🛍️ Kitchen Finds & Home Gadgets', icon: '🛍️' },
  { id: 'fitness_workout', label: '🏋️ Fitness & Workout Routine', icon: '🏋️' },
  { id: 'interior_design', label: '🏠 Interior & Home Decor', icon: '🏠' },
  { id: 'gaming', label: '🎮 Gaming & Tech Setup', icon: '🎮' },
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
  const [isFaqModalOpen, setIsFaqModalOpen] = useState<boolean>(false);
  const [isSavedInVault, setIsSavedInVault] = useState<boolean>(false);
  const [langMode, setLangMode] = useState<'english' | 'native'>('english');
  const [isUpgradeModalOpen, setIsUpgradeModalOpen] = useState<boolean>(false);
  const [upgradeReason, setUpgradeReason] = useState<string>('');
  const [isCreatorVaultOpen, setIsCreatorVaultOpen] = useState<boolean>(false);
  const [quotaRemaining, setQuotaRemaining] = useState<number>(10);
  const [copiedLink, setCopiedLink] = useState<boolean>(false);
  const [copiedNotes, setCopiedNotes] = useState<boolean>(false);
  const [downloadedTxt, setDownloadedTxt] = useState<boolean>(false);
  const [waCountryCode, setWaCountryCode] = useState<string>('+91');
  const [waPhoneNumber, setWaPhoneNumber] = useState<string>('');
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  const [isCookingDrawerOpen, setIsCookingDrawerOpen] = useState<boolean>(false);
  const [faqCategory, setFaqCategory] = useState<string>('all');

  const toggleSaveToVault = () => {
    if (!result) return;
    try {
      const rawLocal = localStorage.getItem('upa_vault_items');
      let currentItems: any[] = [];
      if (rawLocal) {
        currentItems = JSON.parse(rawLocal);
        if (!Array.isArray(currentItems)) currentItems = [];
      }
      const currentUrl = result.source_url || url;
      if (isSavedInVault) {
        const updated = currentItems.filter((i: any) => (i.source_url || i.url) !== currentUrl);
        localStorage.setItem('upa_vault_items', JSON.stringify(updated));
        setIsSavedInVault(false);
      } else {
        const newVaultItem = {
          ...result,
          source_url: currentUrl,
          created_at: new Date().toISOString()
        };
        const filtered = currentItems.filter((i: any) => (i.source_url || i.url) !== currentUrl);
        filtered.unshift(newVaultItem);
        localStorage.setItem('upa_vault_items', JSON.stringify(filtered.slice(0, 50)));
        setIsSavedInVault(true);
      }
    } catch (e) {
      console.error(e);
    }
  };

  // Synchronize initial theme from localStorage (default: light mode)
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') as 'light' | 'dark' | null;
    const initialTheme = savedTheme || 'light';
    setTheme(initialTheme);
    if (initialTheme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, []);

  const toggleTheme = () => {
    const nextTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(nextTheme);
    localStorage.setItem('theme', nextTheme);
    if (nextTheme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  };

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
    if (c.includes('INTERIOR')) return 'Interior Styling & Design Recommendations';
    if (c.includes('GAMING') || c.includes('GAME')) return 'Game Settings, Keybinds & Gear Setup';
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
    const mode = searchParams.get('mode');

    if (initialUrl) {
      setUrl(initialUrl);
      if (autostart === '1') {
        handleExtract(initialUrl);
      }
    }

    if (mode === 'cook') {
      setIsCookingDrawerOpen(true);
      setTimeout(() => {
        const cookEl = document.getElementById('cooking-mode-section');
        if (cookEl) {
          cookEl.scrollIntoView({ behavior: 'smooth' });
        }
      }, 500);
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
    }
  }, [isLoading, Math.floor(loadingProgress / 10)]);

  // ==========================================================================
  // Cameron Breen's Scroll Animation Principles & Multi-Plane Parallax (UPA-806)
  // ==========================================================================
  useEffect(() => {
    let ticking = false;
    const handleScroll = () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          document.documentElement.style.setProperty('--scroll-y', `${window.scrollY}`);
          ticking = false;
        });
        ticking = true;
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();

    // IntersectionObserver for scroll-driven reveals (.sc-reveal -> .sc-visible)
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('sc-visible');
          }
        });
      },
      { threshold: 0.1, rootMargin: '0px 0px -50px 0px' }
    );

    const revealElements = document.querySelectorAll('.sc-reveal');
    revealElements.forEach((el) => observer.observe(el));

    return () => {
      window.removeEventListener('scroll', handleScroll);
      observer.disconnect();
    };
  }, []);

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

  const formatCleanTitle = (rawTitle?: string): string => {
    if (!rawTitle) return '';
    let clean = rawTitle.trim();
    clean = clean.replace(/^(this_video_is_a_recipe_tutorial_for_|this_video_shows_|this_video_is_a_|video_of_|video_)/i, '');
    clean = clean.replace(/_/g, ' ');
    clean = clean.replace(/\s+/g, ' ').trim();
    if (clean && (clean === clean.toLowerCase() || clean.includes(' '))) {
      clean = clean
        .split(' ')
        .map((w) => (w.length > 0 ? w[0].toUpperCase() + w.slice(1).toLowerCase() : ''))
        .join(' ');
    }
    return clean;
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
      setIsSavedInVault(true);
      try {
        const rawLocal = localStorage.getItem('upa_vault_items');
        let currentItems: any[] = [];
        if (rawLocal) {
          currentItems = JSON.parse(rawLocal);
          if (!Array.isArray(currentItems)) currentItems = [];
        }
        const newVaultItem = {
          ...finalData,
          source_url: finalUrl,
          created_at: new Date().toISOString()
        };
        const filtered = currentItems.filter((i: any) => (i.source_url || i.url) !== finalUrl);
        filtered.unshift(newVaultItem);
        localStorage.setItem('upa_vault_items', JSON.stringify(filtered.slice(0, 50)));
      } catch (saveErr) {
        console.warn('Vault auto-save error:', saveErr);
      }
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
    { label: '🍳 Steamed Egg Curry Reel', url: 'https://www.instagram.com/reel/DdGvPs9zhVu/', domain: 'recipe' },
    { label: '💻 Quick Python Tips Short', url: 'https://www.youtube.com/shorts/KrFDs2M_FSE', domain: 'tech_diy' },
    { label: '🛍️ Keyboard & Gadget Short', url: 'https://www.youtube.com/shorts/c2gT6kCnLmc?si=Vo9bLGzNsdIY38rt', domain: 'unboxing' },
    { label: '⚡ Viral Meme Short', url: 'https://www.youtube.com/shorts/fC7oUOUEEi4', domain: 'auto' },
  ];

  const parseRecipeSections = (meta: any, detailsTextStr: string) => {
    let equipment: string[] = meta?.equipment || [];
    let ingredients: any[] = meta?.ingredients || [];
    let instructions: string[] = meta?.instructions || [];

    const textToParse = detailsTextStr || meta?.details || meta?.notes_english || meta?.full_text || '';
    if (textToParse && (equipment.length === 0 || ingredients.length === 0 || instructions.length === 0)) {
      let currSec = '';
      const eqAcc: string[] = [];
      const ingAcc: any[] = [];
      const instAcc: string[] = [];

      textToParse.split('\n').forEach((line) => {
        const trimmed = line.trim();
        if (!trimmed) return;
        const upper = trimmed.toUpperCase();

        if (upper.includes('EQUIPMENT NEEDED') || upper.includes('EQUIPMENT:') || upper.includes('UTENSILS NEEDED') || upper.includes('COOKWARE NEEDED')) {
          currSec = 'EQUIPMENT';
          return;
        } else if (upper.includes('II. INGREDIENTS') || upper.includes('INGREDIENTS:') || upper.includes('INGREDIENTS WITH EXACT')) {
          currSec = 'INGREDIENTS';
          return;
        } else if (upper.includes('III. STEP-BY-STEP') || upper.includes('STEP-BY-STEP INSTRUCTIONS') || upper.includes('COOKING INSTRUCTIONS') || upper.includes('COOKING METHOD')) {
          currSec = 'INSTRUCTIONS';
          return;
        } else if (upper.includes('CHEF TIPS') || upper.includes('VARIATIONS') || upper.includes('NUTRITION')) {
          currSec = 'OTHER';
          return;
        }

        const clean = trimmed.replace(/^[I|V|X\d\.\-\*\•\+a-zA-Z]\s*/, '').replace(/^\*\*\s*/, '').replace(/\s*\*\*$/, '').trim();
        if (!clean) return;

        if (currSec === 'EQUIPMENT') {
          eqAcc.push(clean);
        } else if (currSec === 'INGREDIENTS') {
          const parts = clean.split(/\s*[\(\-\:]\s*/);
          if (parts.length >= 2 && !clean.startsWith('(')) {
            ingAcc.push({ name: parts[0].trim(), quantity: parts.slice(1).join(' ').replace(/[\(\)]/g, '').trim() });
          } else {
            ingAcc.push({ name: clean, quantity: '' });
          }
        } else if (currSec === 'INSTRUCTIONS') {
          instAcc.push(clean);
        }
      });

      if (equipment.length === 0 && eqAcc.length > 0) equipment = eqAcc;
      if (ingredients.length === 0 && ingAcc.length > 0) ingredients = ingAcc;
      if (instructions.length === 0 && instAcc.length > 0) instructions = instAcc;
    }

    return { equipment, ingredients, instructions };
  };

  const parseTravelItinerary = (meta: any, detailsTextStr: string) => {
    if (meta?.travel_itinerary && Array.isArray(meta.travel_itinerary) && meta.travel_itinerary.length > 0) {
      return meta.travel_itinerary;
    }

    const textToParse = detailsTextStr || meta?.details || meta?.notes_english || meta?.full_text || '';
    const itinerary: Array<{ day: string; activities: Array<{ description: string; location_name?: string; maps_url?: string }> }> = [];

    if (!textToParse && (!meta?.instructions || meta.instructions.length === 0)) {
      return itinerary;
    }

    let currentDay = 'Day 1';
    let currentActivities: Array<{ description: string; location_name?: string; maps_url?: string }> = [];

    const lines = meta?.instructions && meta.instructions.length > 0 ? meta.instructions : textToParse.split('\n');

    lines.forEach((line: string) => {
      const trimmed = line.trim();
      if (!trimmed) return;

      const dayMatch = trimmed.match(/^(?:\*\*)?(Day\s*\d+|Day\s*[IVXLCDM]+|Day\s*\d+[:\-]?)(?:\*\*)?/i);
      if (dayMatch && (trimmed.toLowerCase().startsWith('day') || trimmed.startsWith('**Day'))) {
        if (currentActivities.length > 0) {
          itinerary.push({ day: currentDay, activities: [...currentActivities] });
          currentActivities = [];
        }
        let rawDay = dayMatch[1].replace(/[:\-]$/, '').trim();
        if (!rawDay.toLowerCase().startsWith('day')) rawDay = `Day ${rawDay}`;
        currentDay = rawDay;
        return;
      }

      let cleanAct = trimmed
        .replace(/^(?:Activity\s*\d+[:\-]?|[\-\*•\d\.]+\s*)/i, '')
        .replace(/^\*\*\s*/, '')
        .replace(/\s*\*\*$/, '')
        .trim();

      if (!cleanAct) return;

      let location_name = '';
      let maps_url = '';

      const locMatch = cleanAct.match(/\|?\s*LOCATION:\s*([^\|]+)(?:\|\s*SEARCH:\s*([^\|]+))?/i);
      if (locMatch) {
        location_name = locMatch[1].trim();
        const searchQ = (locMatch[2] || location_name).trim();
        cleanAct = cleanAct.replace(/\|?\s*LOCATION:[^\|]+(?:\|\s*SEARCH:[^\|]+)?/i, '').trim();
        maps_url = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(searchQ)}`;
      } else if (meta?.google_maps_locations && Array.isArray(meta.google_maps_locations)) {
        for (const loc of meta.google_maps_locations) {
          if (loc.name && cleanAct.toLowerCase().includes(loc.name.toLowerCase())) {
            location_name = loc.name;
            maps_url = loc.maps_url;
            break;
          }
        }
      }

      if (!maps_url && cleanAct) {
        maps_url = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(cleanAct.slice(0, 60))}`;
      }

      currentActivities.push({
        description: cleanAct,
        location_name,
        maps_url,
      });
    });

    if (currentActivities.length > 0) {
      itinerary.push({ day: currentDay, activities: [...currentActivities] });
    }

    return itinerary;
  };

  const generateStructuredText = (meta: any, isWhatsApp = false): string => {
    if (!meta) return '';
    const title = formatCleanTitle(meta.title || meta.recipe_title) || 'Universal AI Extraction';
    const category = (meta.category || meta.category_name || 'INTELLIGENCE').toUpperCase();
    const isRecipe = category.includes('RECIPE') || category.includes('COOK');
    const isTravel = category.includes('TRAVEL') || (meta.travel_itinerary && meta.travel_itinerary.length > 0);

    // Category emoji
    let emoji = '⚡';
    if (isRecipe) emoji = '🍳';
    else if (category.includes('PRODUCT') || category.includes('UNBOX') || category.includes('GADGET')) emoji = '🛍️';
    else if (category.includes('TUTORIAL') || category.includes('TECH') || category.includes('CODE')) emoji = '💻';
    else if (category.includes('FITNESS') || category.includes('WORKOUT')) emoji = '🏋️';
    else if (category.includes('BEAUTY') || category.includes('SKINCARE')) emoji = '✨';
    else if (isTravel) emoji = '✈️';
    else if (category.includes('INTERIOR')) emoji = '🏠';
    else if (category.includes('GAMING') || category.includes('GAME')) emoji = '🎮';

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

    if (isRecipe) {
      const { equipment, ingredients, instructions } = parseRecipeSections(meta, meta.details || meta.notes_english || '');

      // I. Equipment Needed
      if (equipment && equipment.length > 0) {
        lines.push(isWhatsApp ? `🍳 *I. Equipment Needed:*` : `==================================================\n🍳 I. Equipment Needed:\n==================================================`);
        equipment.forEach((eq: string, idx: number) => {
          const letter = String.fromCharCode(97 + idx); // a, b, c...
          lines.push(`   ${letter}. ${eq}`);
        });
        lines.push('');
      }

      // II. Ingredients
      if (ingredients && ingredients.length > 0) {
        lines.push(isWhatsApp ? `🥗 *II. Ingredients (with quantity):*` : `==================================================\n🥗 II. Ingredients (with quantity):\n==================================================`);
        ingredients.forEach((ing: any, idx: number) => {
          const qty = ing.quantity ? ` - ${ing.quantity}` : '';
          const unit = ing.unit ? ` ${ing.unit}` : '';
          const name = ing.name || ing;
          lines.push(`   ${idx + 1}. ${name}${qty}${unit}`);
        });
        lines.push('');
      }

      // III. Step-by-Step Instructions
      if (instructions && instructions.length > 0) {
        lines.push(isWhatsApp ? `📝 *III. Step-by-Step Instructions:*` : `==================================================\n📝 III. Step-by-Step Instructions:\n==================================================`);
        instructions.forEach((step: string, idx: number) => {
          const cleanStep = isWhatsApp ? step.replace(/\*\*/g, '*') : step.replace(/\*\*/g, '');
          lines.push(`   ${idx + 1}. ${cleanStep}`);
        });
        lines.push('');
      } else if (meta.details) {
        lines.push(isWhatsApp ? `📝 *III. Step-by-Step Instructions:*\n${meta.details}\n` : `==================================================\n📝 III. Step-by-Step Instructions:\n==================================================\n\n${meta.details}\n`);
      }

      // Products split into Equipment Links and Purchase Ingredients
      if (meta.products && meta.products.length > 0) {
        const equipProds: any[] = [];
        const ingProds: any[] = [];
        meta.products.forEach((p: any) => {
          const pNameLower = (p.name || '').toLowerCase();
          const isEquipKw = /\b(pan|skillet|knife|blender|cooker|oven|air fryer|bowl|board|apron|spatula|pot|kettle|kadai|tawa|wok|grinder|chopper|tray|sheet)\b/i.test(pNameLower);
          if (isEquipKw) equipProds.push(p);
          else ingProds.push(p);
        });

        if (equipProds.length > 0) {
          lines.push(isWhatsApp ? `🛒 *1. Equipment Links:*` : `==================================================\n🛒 1. Equipment Links (Buy on Amazon / Flipkart):\n==================================================`);
          equipProds.forEach((p: any, idx: number) => {
            lines.push(`   ${idx + 1}. ${p.name}`);
            if (p.amazon_url) lines.push(`      • Amazon: ${p.amazon_url}`);
            if (p.flipkart_url) lines.push(`      • Flipkart: ${p.flipkart_url}`);
          });
          lines.push('');
        }

        if (ingProds.length > 0) {
          lines.push(isWhatsApp ? `🥦 *2. Purchase Ingredients:*` : `==================================================\n🥦 2. Purchase Ingredients (Blinkit, Zepto, Swiggy Instamart, BigBasket, Amazon Fresh):\n==================================================`);
          ingProds.forEach((p: any, idx: number) => {
            lines.push(`   ${idx + 1}. ${p.name}`);
            if (p.blinkit_url) lines.push(`      • Blinkit (10-Min): ${p.blinkit_url}`);
            if (p.zepto_url) lines.push(`      • Zepto (10-Min): ${p.zepto_url}`);
            if (p.instamart_url) lines.push(`      • Swiggy Instamart: ${p.instamart_url}`);
            if (p.bigbasket_url) lines.push(`      • BigBasket: ${p.bigbasket_url}`);
            if (p.amazon_url) lines.push(`      • Amazon Fresh: ${p.amazon_url}`);
          });
          lines.push('');
        }
      }
    } else if (isTravel) {
      const travelData = parseTravelItinerary(meta, meta.details || meta.notes_english || '');
      if (travelData && travelData.length > 0) {
        travelData.forEach((dayGroup: any) => {
          lines.push(isWhatsApp ? `✈️ *${dayGroup.day}:*` : `==================================================\n✈️ ${dayGroup.day}:\n==================================================`);
          dayGroup.activities.forEach((act: any, idx: number) => {
            const cleanDesc = isWhatsApp ? act.description.replace(/\*\*/g, '*') : act.description.replace(/\*\*/g, '');
            lines.push(`   Activity ${idx + 1} : ${cleanDesc}`);
            if (act.maps_url) {
              lines.push(`      📍 Google Maps: ${act.maps_url}`);
            }
          });
          lines.push('');
        });
      }
    } else {
      // General/Non-Recipe text output
      if (meta.ingredients && meta.ingredients.length > 0) {
        lines.push(isWhatsApp ? `🥗 *Ingredients:*` : `==================================================\n🥗 Ingredients:\n==================================================`);
        meta.ingredients.forEach((ing: any) => {
          const qty = ing.quantity ? ` - ${ing.quantity}` : '';
          const unit = ing.unit ? ` ${ing.unit}` : '';
          lines.push(`• ${ing.name}${qty}${unit}`);
        });
        lines.push('');
      }

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

      if (meta.products && meta.products.length > 0) {
        lines.push(isWhatsApp ? `*🛍️ Featured Products & Buy Links:*` : `==================================================\n🛍️ Featured Products & Buy Links:\n==================================================`);
        meta.products.forEach((p: any, idx: number) => {
          const priceStr = p.price ? ` (${p.price})` : '';
          lines.push(`${idx + 1}. ${p.name}${priceStr}`);
          if (p.amazon_url) lines.push(`   🛒 Amazon: ${p.amazon_url}`);
          if (p.flipkart_url) lines.push(`   ⚡ Flipkart: ${p.flipkart_url}`);
        });
        lines.push('');
      }
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
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', position: 'relative', overflow: 'hidden' }}>
      {/* Interactive Constellation Particle Canvas & Ambient Aura Layers */}
      <ParticleBackground theme={theme} />
      {theme === 'dark' ? (
        <>
          <div className="bg-hero-texture" />
          <div className="bg-ambient-layer" />
          <div className="bg-glass-artwork" />
        </>
      ) : (
        <div className="bg-light-aura" />
      )}

      {/* Top Navigation Bar */}
      <header
        style={{
          borderBottom: '1px solid var(--border-subtle)',
          background: 'var(--bg-surface)',
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
            {/* Theme Toggle Button (Light / Dark Mode) */}
            <button
              onClick={toggleTheme}
              className="btn-ghost"
              style={{ padding: '0.45rem 0.85rem' }}
              title={`Switch to ${theme === 'light' ? 'Dark' : 'Light'} Mode`}
            >
              {theme === 'light' ? (
                <>
                  <Moon size={16} color="#06B6D4" />
                  <span>Dark Mode</span>
                </>
              ) : (
                <>
                  <Sun size={16} color="#F59E0B" />
                  <span>Light Mode</span>
                </>
              )}
            </button>

            {/* FAQ & How It Works Guide Button */}
            <button
              onClick={() => {
                setFaqCategory('all');
                setIsFaqModalOpen(true);
              }}
              className="btn-ghost"
              style={{ padding: '0.45rem 0.85rem' }}
            >
              <HelpCircle size={16} color="#34D399" />
              <span>FAQ & Guide</span>
            </button>

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
      <main style={{ flex: 1, maxWidth: '1280px', margin: '0 auto', width: '100%', padding: '2rem 1.5rem', position: 'relative', zIndex: 1 }}>
          <h1
            style={{
              fontSize: '2.65rem',
              fontWeight: 800,
              lineHeight: 1.15,
              marginBottom: '0.75rem',
              letterSpacing: '-0.03em',
            }}
          >
            Universal Reel & Shorts <br />
            <span className="gradient-text-animated">AI Intelligence Extractor</span>
          </h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '1.05rem', maxWidth: '640px', margin: '0 auto 1.25rem', lineHeight: '1.5' }}>
            Instant AI extraction for recipes, tutorials, travel guides, gadgets & shorts.
          </p>

        {/* Input Bar Card - Undisputed Streamlined Focal Point */}
        <div
          className="glass-panel plane-mid sc-reveal sc-visible accent-border-t glass-panel-glow"
          style={{
            maxWidth: '860px',
            margin: '0 auto 1.5rem',
            padding: '0.85rem 1rem',
          }}
        >
          <div className="main-search-input-container" style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', flexWrap: 'nowrap' }}>
            {platformInfo && (
              <span
                style={{
                  fontSize: '0.75rem',
                  fontWeight: 700,
                  padding: '0.4rem 0.65rem',
                  borderRadius: '8px',
                  background: 'rgba(16, 185, 129, 0.14)',
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
                fontWeight: 500,
                outline: 'none',
                padding: '0.5rem 0.5rem',
              }}
            />
            {/* Inline Compact Domain Selector */}
            <select
              value={selectedDomain}
              onChange={(e) => setSelectedDomain(e.target.value)}
              className="chip-tactile"
              title="Content Domain Classifier"
              style={{
                background: 'var(--bg-surface-elevated)',
                border: '1px solid var(--border-subtle)',
                borderRadius: '8px',
                color: 'var(--text-primary)',
                padding: '0.45rem 0.65rem',
                fontSize: '0.78rem',
                fontWeight: 600,
                outline: 'none',
                cursor: 'pointer',
                maxWidth: '145px',
                whiteSpace: 'nowrap',
              }}
            >
              {DOMAIN_OPTIONS.map((d) => (
                <option key={d.id} value={d.id} style={{ background: 'var(--bg-base)', color: 'var(--text-primary)' }}>
                  {d.label}
                </option>
              ))}
            </select>

            <button
              onClick={() => handleExtract()}
              disabled={isLoading || !url}
              className="btn-emerald btn-tactile"
              style={{ padding: '0.75rem 1.4rem', fontWeight: 700, whiteSpace: 'nowrap' }}
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
                className="btn-ghost chip-tactile"
                style={{ padding: '0.25rem 0.6rem', fontSize: '0.72rem' }}
              >
                {s.label}
              </button>
            ))}
          </div>
        </div>

        {/* Dynamic Technical Progress Bar & Intelligence Deck */}
        {isLoading && (
          <div
            className="shimmer-card accent-border-t glass-panel-glow"
            style={{
              maxWidth: '820px',
              margin: '0 auto 2rem',
              padding: '1.35rem 1.5rem',
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
                className="tabular-num"
                style={{
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

            {/* Skeleton Shimmer Sweep Lines */}
            <div style={{ marginTop: '1.15rem', display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
              <div className="shimmer-block" style={{ width: '65%', height: '14px' }} />
              <div className="shimmer-block" style={{ width: '90%', height: '10px' }} />
              <div className="shimmer-block" style={{ width: '45%', height: '10px' }} />
            </div>

            {/* Technical Subtext */}
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                marginTop: '0.85rem',
              }}
            >
              <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                {loadingSubtext || 'Real-Time Multimodal Intelligence Pipeline Active'}
              </span>
              <span
                className="tabular-num"
                style={{
                  fontSize: '0.68rem',
                  color: 'var(--accent-emerald)',
                  fontWeight: 600,
                }}
              >
                ⚡ ~2.4s Benchmark Target
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



        {/* Extraction Results: Multi-Genre Responsive View */}
        {result && (() => {
          const detailsText = langMode === 'native' && result.notes_original_language ? result.notes_original_language : (result.details || result.full_text || '');
          return (
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
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '0.5rem', marginBottom: '0.5rem', flexWrap: 'wrap' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
                    <span className="badge-pill badge-emerald" style={{ fontSize: '0.7rem' }}>
                      {result.category || 'UNIVERSAL INTELLIGENCE'}
                    </span>
                    {result.audio_song && (
                      <span className="badge-pill badge-purple" style={{ fontSize: '0.7rem', display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                        🎵 Song: {result.audio_song}
                      </span>
                    )}
                    {result.reel_language && (
                      <span className="badge-pill" style={{ fontSize: '0.7rem', background: 'rgba(56, 189, 248, 0.14)', color: '#38BDF8', border: '1px solid rgba(56, 189, 248, 0.3)' }}>
                        🌐 {result.reel_language}
                      </span>
                    )}
                  </div>

                  {/* UPA-1009: Save to Vault Action Button */}
                  <button
                    onClick={toggleSaveToVault}
                    className="btn-tactile"
                    style={{
                      background: isSavedInVault ? 'rgba(16, 185, 129, 0.18)' : 'rgba(255, 255, 255, 0.08)',
                      border: isSavedInVault ? '1px solid rgba(16, 185, 129, 0.4)' : '1px solid var(--border-subtle)',
                      color: isSavedInVault ? '#34D399' : 'var(--text-primary)',
                      padding: '0.35rem 0.75rem',
                      borderRadius: '8px',
                      fontSize: '0.78rem',
                      fontWeight: 700,
                      cursor: 'pointer',
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: '5px'
                    }}
                  >
                    <Bookmark size={14} color={isSavedInVault ? '#34D399' : 'var(--text-secondary)'} />
                    <span>{isSavedInVault ? 'Saved in Vault' : 'Save to Vault'}</span>
                  </button>
                </div>

                <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '0.4rem' }}>
                  {formatCleanTitle(result.title || result.recipe_title) || 'Extracted Social Intelligence'}
                </h2>

                {result.summary && (
                  <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.5, marginBottom: '1.25rem' }}>
                    {result.summary}
                  </p>
                )}

                {/* Travel Google Maps Location Card (Item 7) */}
                {result.google_maps_locations && result.google_maps_locations.length > 0 && (
                  <div
                    style={{
                      marginBottom: '1.25rem',
                      padding: '0.85rem 1rem',
                      background: 'rgba(56, 189, 248, 0.08)',
                      border: '1px solid rgba(56, 189, 248, 0.25)',
                      borderRadius: '10px'
                    }}
                  >
                    <span style={{ fontSize: '0.82rem', fontWeight: 700, color: '#38BDF8', display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '0.5rem' }}>
                      <Globe size={15} />
                      <span>📍 Featured Travel Locations & Google Maps Directions</span>
                    </span>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
                      {result.google_maps_locations.map((loc, idx) => (
                        <div key={idx} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.82rem', color: 'var(--text-primary)' }}>
                          <span>• {loc.name}</span>
                          <a
                            href={loc.maps_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            style={{
                              color: '#38BDF8',
                              fontWeight: 700,
                              textDecoration: 'none',
                              fontSize: '0.74rem',
                              background: 'rgba(56, 189, 248, 0.15)',
                              padding: '2px 8px',
                              borderRadius: '6px',
                              border: '1px solid rgba(56, 189, 248, 0.3)',
                              display: 'inline-flex',
                              alignItems: 'center',
                              gap: '3px'
                            }}
                          >
                            <span>Open Map</span>
                            <ExternalLink size={10} />
                          </a>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Non-English Reel Dual Language Toggle (Item 6) */}
                {result.notes_original_language && result.reel_language && result.reel_language.toLowerCase() !== 'english' && (
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Notes Language:</span>
                    <button
                      onClick={() => setLangMode('english')}
                      style={{
                        padding: '0.25rem 0.6rem',
                        fontSize: '0.74rem',
                        fontWeight: 700,
                        borderRadius: '6px',
                        border: langMode === 'english' ? '1px solid #10B981' : '1px solid var(--border-subtle)',
                        background: langMode === 'english' ? '#10B981' : 'transparent',
                        color: langMode === 'english' ? '#FFFFFF' : 'var(--text-secondary)',
                        cursor: 'pointer'
                      }}
                    >
                      English (Default)
                    </button>
                    <button
                      onClick={() => setLangMode('native')}
                      style={{
                        padding: '0.25rem 0.6rem',
                        fontSize: '0.74rem',
                        fontWeight: 700,
                        borderRadius: '6px',
                        border: langMode === 'native' ? '1px solid #10B981' : '1px solid var(--border-subtle)',
                        background: langMode === 'native' ? '#10B981' : 'transparent',
                        color: langMode === 'native' ? '#FFFFFF' : 'var(--text-secondary)',
                        cursor: 'pointer'
                      }}
                    >
                      {result.reel_language} (Original)
                    </button>
                  </div>
                )}

                {/* Recipe-Specific: Serving Scaler if Ingredients exist */}
                {result.ingredients && result.ingredients.length > 0 && (
                  <div style={{ marginBottom: '1.5rem' }}>
                    <ServingAdjuster
                      initialServings={result.servings || 2}
                      ingredients={result.ingredients}
                      recipeTitle={formatCleanTitle(result.title || result.recipe_title) || 'Recipe'}
                    />
                  </div>
                )}

                {/* Recipe Extraction 3-Section Rendering & General Content Fallback */}
                {(() => {
                  const isRecipeDomain = (result.category || '').toUpperCase().includes('RECIPE') || (result.category_name || '').toUpperCase().includes('RECIPE');
                  const recipeData = isRecipeDomain ? parseRecipeSections(result, detailsText) : null;

                  if (isRecipeDomain && recipeData) {
                    const { equipment, ingredients, instructions } = recipeData;
                    const equipProds: any[] = [];
                    const ingProds: any[] = [];
                    (result.products || []).forEach((p: any) => {
                      const pNameLower = (p.name || '').toLowerCase();
                      const isEquipKw = /\b(pan|skillet|knife|blender|cooker|oven|air fryer|bowl|board|apron|spatula|pot|kettle|kadai|tawa|wok|grinder|chopper|tray|sheet)\b/i.test(pNameLower);
                      if (isEquipKw) equipProds.push(p);
                      else ingProds.push(p);
                    });

                    return (
                      <div style={{ marginTop: '1rem', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
                        {/* Section I. Equipment Needed */}
                        {equipment && equipment.length > 0 && (
                          <div style={{ background: 'rgba(255, 255, 255, 0.02)', border: '1px solid rgba(255, 255, 255, 0.06)', borderRadius: '12px', padding: '1rem' }}>
                            <h3 style={{ fontSize: '0.98rem', fontWeight: 700, color: '#38BDF8', display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '0.75rem' }}>
                              <Flame size={16} color="#38BDF8" />
                              <span>I. Equipment Needed</span>
                            </h3>
                            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                              {equipment.map((item, idx) => {
                                const letter = String.fromCharCode(97 + idx); // a, b, c...
                                return (
                                  <div key={idx} style={{ padding: '0.45rem 0.75rem', background: 'rgba(56, 189, 248, 0.08)', border: '1px solid rgba(56, 189, 248, 0.2)', borderRadius: '8px', fontSize: '0.85rem', color: 'var(--text-primary)', display: 'inline-flex', alignItems: 'center', gap: '6px' }}>
                                    <span style={{ fontWeight: 800, color: '#38BDF8' }}>{letter}.</span>
                                    <span>{item}</span>
                                  </div>
                                );
                              })}
                            </div>
                          </div>
                        )}

                        {/* Section II. Ingredients */}
                        {ingredients && ingredients.length > 0 && (
                          <div style={{ background: 'rgba(255, 255, 255, 0.02)', border: '1px solid rgba(255, 255, 255, 0.06)', borderRadius: '12px', padding: '1rem' }}>
                            <h3 style={{ fontSize: '0.98rem', fontWeight: 700, color: '#34D399', display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '0.75rem' }}>
                              <ChefHat size={16} color="#34D399" />
                              <span>II. Ingredients (with quantity)</span>
                            </h3>
                            <ServingAdjuster
                              initialServings={result.servings || 2}
                              ingredients={ingredients}
                              recipeTitle={formatCleanTitle(result.title || result.recipe_title) || 'Recipe'}
                            />
                          </div>
                        )}

                        {/* Section III. Step-by-Step Instructions */}
                        <div id="cooking-mode-section" style={{ background: 'rgba(255, 255, 255, 0.02)', border: '1px solid rgba(255, 255, 255, 0.06)', borderRadius: '12px', padding: '1rem' }}>
                          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem', flexWrap: 'wrap', gap: '0.5rem' }}>
                            <h3 style={{ fontSize: '0.98rem', fontWeight: 700, color: 'var(--accent-emerald)', display: 'flex', alignItems: 'center', gap: '8px', margin: 0 }}>
                              <CheckCircle2 size={16} color="var(--accent-emerald)" />
                              <span>III. Step-by-Step Instructions</span>
                            </h3>

                            <button
                              onClick={() => setIsCookingDrawerOpen(true)}
                              className="btn-emerald btn-tactile"
                              style={{ padding: '0.45rem 0.85rem', fontSize: '0.78rem', fontWeight: 700, borderRadius: '8px' }}
                            >
                              <span>🧑‍🍳 Start Cooking Mode</span>
                            </button>
                          </div>
                          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
                            {instructions && instructions.length > 0 ? (
                              instructions.map((step, idx) => (
                                <div key={idx} style={{ display: 'flex', alignItems: 'flex-start', gap: '0.75rem', padding: '0.65rem 0.85rem', background: 'rgba(0, 0, 0, 0.2)', borderRadius: '8px', border: '1px solid rgba(255, 255, 255, 0.04)' }}>
                                  <span style={{ minWidth: '22px', height: '22px', borderRadius: '50%', background: 'rgba(16, 185, 129, 0.2)', color: 'var(--accent-emerald)', fontSize: '0.75rem', fontWeight: 700, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                    {idx + 1}
                                  </span>
                                  <p style={{ fontSize: '0.88rem', lineHeight: 1.45, color: 'var(--text-primary)', margin: 0 }}>{step}</p>
                                </div>
                              ))
                            ) : (
                              <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Follow the video clip for step-by-step guidance.</p>
                            )}
                          </div>
                        </div>

                        {/* Buy Links Divided into 1. Equipment Links & 2. Purchase Ingredients */}
                        {(equipProds.length > 0 || ingProds.length > 0) && (
                          <div style={{ marginTop: '0.5rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                            {equipProds.length > 0 && (
                              <div>
                                <h4 style={{ fontSize: '0.9rem', fontWeight: 700, color: '#FF9900', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '6px' }}>
                                  <ShoppingCart size={15} color="#FF9900" />
                                  <span>1. Equipment Links (Buy on Amazon / Flipkart)</span>
                                </h4>
                                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '0.65rem' }}>
                                  {equipProds.map((p, idx) => (
                                    <div key={idx} style={{ padding: '0.65rem', background: 'rgba(255, 255, 255, 0.02)', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
                                      <span style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-primary)' }}>{p.name}</span>
                                      <div style={{ display: 'flex', gap: '0.4rem', marginTop: '0.45rem' }}>
                                        {p.amazon_url && <a href={p.amazon_url} target="_blank" rel="noopener noreferrer" style={{ flex: 1, textAlign: 'center', padding: '0.28rem', background: 'rgba(255, 153, 0, 0.15)', color: '#FF9900', border: '1px solid rgba(255, 153, 0, 0.3)', borderRadius: '6px', fontSize: '0.72rem', fontWeight: 700, textDecoration: 'none' }}>Amazon</a>}
                                        {p.flipkart_url && <a href={p.flipkart_url} target="_blank" rel="noopener noreferrer" style={{ flex: 1, textAlign: 'center', padding: '0.28rem', background: 'rgba(40, 116, 240, 0.15)', color: '#60A5FA', border: '1px solid rgba(40, 116, 240, 0.3)', borderRadius: '6px', fontSize: '0.72rem', fontWeight: 700, textDecoration: 'none' }}>Flipkart</a>}
                                      </div>
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}

                            {ingProds.length > 0 && (
                              <div>
                                <h4 style={{ fontSize: '0.9rem', fontWeight: 700, color: '#34D399', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '6px' }}>
                                  <ShoppingBag size={15} color="#34D399" />
                                  <span>2. Purchase Ingredients (Blinkit, Zepto, Swiggy Instamart, BigBasket, Amazon Fresh)</span>
                                </h4>
                                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '0.65rem' }}>
                                  {ingProds.map((p, idx) => (
                                    <div key={idx} style={{ padding: '0.65rem', background: 'rgba(255, 255, 255, 0.02)', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
                                      <span style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-primary)' }}>{p.name}</span>
                                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35rem', marginTop: '0.45rem' }}>
                                        {p.blinkit_url && <a href={p.blinkit_url} target="_blank" rel="noopener noreferrer" style={{ padding: '0.25rem 0.45rem', background: 'rgba(244, 196, 48, 0.15)', color: '#F4C430', border: '1px solid rgba(244, 196, 48, 0.3)', borderRadius: '6px', fontSize: '0.7rem', fontWeight: 700, textDecoration: 'none' }}>Blinkit</a>}
                                        {p.zepto_url && <a href={p.zepto_url} target="_blank" rel="noopener noreferrer" style={{ padding: '0.25rem 0.45rem', background: 'rgba(167, 139, 250, 0.15)', color: '#A78BFA', border: '1px solid rgba(167, 139, 250, 0.3)', borderRadius: '6px', fontSize: '0.7rem', fontWeight: 700, textDecoration: 'none' }}>Zepto</a>}
                                        {p.instamart_url && <a href={p.instamart_url} target="_blank" rel="noopener noreferrer" style={{ padding: '0.25rem 0.45rem', background: 'rgba(252, 128, 25, 0.15)', color: '#FC8019', border: '1px solid rgba(252, 128, 25, 0.3)', borderRadius: '6px', fontSize: '0.7rem', fontWeight: 700, textDecoration: 'none' }}>Instamart</a>}
                                        {p.bigbasket_url && <a href={p.bigbasket_url} target="_blank" rel="noopener noreferrer" style={{ padding: '0.25rem 0.45rem', background: 'rgba(132, 204, 22, 0.15)', color: '#84CC16', border: '1px solid rgba(132, 204, 22, 0.3)', borderRadius: '6px', fontSize: '0.7rem', fontWeight: 700, textDecoration: 'none' }}>BigBasket</a>}
                                        {p.amazon_url && <a href={p.amazon_url} target="_blank" rel="noopener noreferrer" style={{ padding: '0.25rem 0.45rem', background: 'rgba(16, 185, 129, 0.15)', color: '#34D399', border: '1px solid rgba(16, 185, 129, 0.3)', borderRadius: '6px', fontSize: '0.7rem', fontWeight: 700, textDecoration: 'none' }}>Amazon Fresh</a>}
                                      </div>
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    );
                  }

                  const isTravelDomain = (result.category || '').toUpperCase().includes('TRAVEL') || (result.category_name || '').toUpperCase().includes('TRAVEL') || (result.travel_itinerary && result.travel_itinerary.length > 0);

                  if (isTravelDomain) {
                    const travelData = parseTravelItinerary(result, detailsText);
                    return (
                      <div style={{ marginTop: '1.25rem', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
                        <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#38BDF8', display: 'flex', alignItems: 'center', gap: '8px', margin: 0 }}>
                          <Globe size={18} color="#38BDF8" />
                          <span>Day-by-Day Travel Itinerary</span>
                        </h3>

                        {travelData && travelData.length > 0 ? (
                          travelData.map((dayGroup: any, dayIdx: number) => (
                            <div key={dayIdx} style={{ background: 'rgba(255, 255, 255, 0.02)', border: '1px solid rgba(56, 189, 248, 0.22)', borderRadius: '12px', padding: '1.1rem' }}>
                              <h4 style={{ fontSize: '0.95rem', fontWeight: 800, color: '#38BDF8', marginBottom: '0.85rem', display: 'flex', alignItems: 'center', gap: '6px' }}>
                                <span>📍 {dayGroup.day}</span>
                              </h4>
                              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                                {dayGroup.activities && dayGroup.activities.map((act: any, actIdx: number) => (
                                  <div key={actIdx} style={{ display: 'flex', flexDirection: 'column', gap: '0.45rem', padding: '0.75rem 0.9rem', background: 'rgba(0, 0, 0, 0.25)', borderRadius: '8px', border: '1px solid rgba(255, 255, 255, 0.05)' }}>
                                    <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '0.5rem' }}>
                                      <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.65rem', flex: 1 }}>
                                        <span style={{ fontSize: '0.74rem', fontWeight: 800, color: '#38BDF8', background: 'rgba(56, 189, 248, 0.15)', border: '1px solid rgba(56, 189, 248, 0.3)', padding: '2px 8px', borderRadius: '6px', whiteSpace: 'nowrap' }}>
                                          Activity {actIdx + 1}
                                        </span>
                                        <p style={{ fontSize: '0.88rem', lineHeight: 1.45, color: 'var(--text-primary)', margin: 0, fontWeight: 500 }}>
                                          {act.description}
                                        </p>
                                      </div>
                                    </div>

                                    {act.maps_url && (
                                      <div style={{ marginTop: '0.2rem', display: 'flex', justifyContent: 'flex-end' }}>
                                        <a
                                          href={act.maps_url}
                                          target="_blank"
                                          rel="noopener noreferrer"
                                          style={{
                                            fontSize: '0.74rem',
                                            fontWeight: 700,
                                            color: '#38BDF8',
                                            background: 'rgba(56, 189, 248, 0.12)',
                                            border: '1px solid rgba(56, 189, 248, 0.3)',
                                            borderRadius: '6px',
                                            padding: '3px 10px',
                                            textDecoration: 'none',
                                            display: 'inline-flex',
                                            alignItems: 'center',
                                            gap: '4px',
                                            transition: 'all 0.2s ease',
                                          }}
                                        >
                                          <span>📍 Open in Google Maps</span>
                                          <ExternalLink size={11} />
                                        </a>
                                      </div>
                                    )}
                                  </div>
                                ))}
                              </div>
                            </div>
                          ))
                        ) : (
                          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>No detailed itinerary steps found.</p>
                        )}
                      </div>
                    );
                  }

                  // Non-Recipe Standard UI Fallback
                  return (
                    <div style={{ marginTop: '1.25rem' }}>
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                        <h3 style={{ fontSize: '1rem', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.5rem', margin: 0 }}>
                          <CheckCircle2 size={18} color="var(--accent-emerald)" />
                          <span>{getSectionTitle(result.category)}</span>
                        </h3>
                      </div>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
                        {result.instructions && result.instructions.length > 0 ? (
                          result.instructions.map((step, idx) => (
                            <div key={idx} style={{ display: 'flex', alignItems: 'flex-start', gap: '0.75rem', padding: '0.65rem 0.85rem', background: 'rgba(255, 255, 255, 0.02)', borderRadius: '8px', border: '1px solid rgba(255, 255, 255, 0.04)' }}>
                              <span style={{ minWidth: '22px', height: '22px', borderRadius: '50%', background: 'rgba(16, 185, 129, 0.2)', color: 'var(--accent-emerald)', fontSize: '0.75rem', fontWeight: 700, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                {idx + 1}
                              </span>
                              <p style={{ fontSize: '0.88rem', lineHeight: 1.45, color: 'var(--text-primary)', margin: 0 }}>{step}</p>
                            </div>
                          ))
                        ) : (
                          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Follow the video clip for exact step-by-step guidance.</p>
                        )}
                      </div>
                    </div>
                  );
                })()}

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
          );
        })()}

        {/* Interactive FAQ & User Guide Modal Drawer */}
        <FaqSection isOpen={isFaqModalOpen} onClose={() => setIsFaqModalOpen(false)} initialCategory={faqCategory} />
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

      {/* Fullscreen Interactive Cooking Mode Drawer */}
      <CookingModeDrawer
        isOpen={isCookingDrawerOpen}
        onClose={() => setIsCookingDrawerOpen(false)}
        recipe={result}
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
