'use client';

import React, { useState } from 'react';
import {
  HelpCircle,
  ChevronDown,
  ChevronUp,
  Search,
  Sparkles,
  Play,
  ShoppingCart,
  MessageSquare,
  BookOpen,
  Zap,
  CheckCircle2,
  ExternalLink,
  ShieldCheck,
  Smartphone,
  Flame,
  PackageCheck
} from 'lucide-react';

interface FaqItem {
  id: string;
  category: 'getting_started' | 'features' | 'platforms' | 'troubleshooting';
  question: string;
  answer: React.ReactNode;
  tags: string[];
}

const FAQ_DATA: FaqItem[] = [
  {
    id: 'how-to-extract',
    category: 'getting_started',
    question: 'How do I extract a recipe, workout, or product list from a video URL?',
    answer: (
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
        <p>Follow these 4 simple steps to extract structured intelligence from any public video or link:</p>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem', marginTop: '0.25rem' }}>
          <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.65rem' }}>
            <span style={{ background: 'rgba(16, 185, 129, 0.15)', color: '#34D399', width: '24px', height: '24px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.75rem', fontWeight: 700, flexShrink: 0 }}>1</span>
            <div>
              <strong style={{ color: 'var(--text-primary)' }}>Copy Video URL:</strong> Open YouTube (Shorts or Videos), Instagram (Reels or Posts), TikTok, or Facebook Reels, and copy the link.
            </div>
          </div>
          <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.65rem' }}>
            <span style={{ background: 'rgba(16, 185, 129, 0.15)', color: '#34D399', width: '24px', height: '24px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.75rem', fontWeight: 700, flexShrink: 0 }}>2</span>
            <div>
              <strong style={{ color: 'var(--text-primary)' }}>Paste into Extractor:</strong> Paste the link into the search bar at the top of Universal Pro AI.
            </div>
          </div>
          <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.65rem' }}>
            <span style={{ background: 'rgba(16, 185, 129, 0.15)', color: '#34D399', width: '24px', height: '24px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.75rem', fontWeight: 700, flexShrink: 0 }}>3</span>
            <div>
              <strong style={{ color: 'var(--text-primary)' }}>Select Category (Optional):</strong> Keep set to <em>"Auto-Detect"</em> or pick a specific domain like 🍳 Cooking Recipe, 🛍️ Kitchen Finds, or 🏋️ Workout Routine.
            </div>
          </div>
          <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.65rem' }}>
            <span style={{ background: 'rgba(16, 185, 129, 0.15)', color: '#34D399', width: '24px', height: '24px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.75rem', fontWeight: 700, flexShrink: 0 }}>4</span>
            <div>
              <strong style={{ color: 'var(--text-primary)' }}>Click "Extract Anything":</strong> Universal Pro AI processes video keyframes & audio transcripts in sub-3s to produce interactive recipe cards, ingredient lists, or product find links!
            </div>
          </div>
        </div>
      </div>
    ),
    tags: ['steps', 'how to use', 'extract', 'youtube', 'instagram', 'tiktok', 'recipe']
  },
  {
    id: 'supported-platforms',
    category: 'platforms',
    question: 'Which social media platforms and URL formats are supported?',
    answer: (
      <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        <p>Universal Pro AI supports major short-form and long-form video platforms including:</p>
        <ul style={{ paddingLeft: '1.25rem', lineHeight: '1.6' }}>
          <li><strong style={{ color: '#FF6B6B' }}>YouTube & YouTube Shorts:</strong> <code>https://youtube.com/shorts/...</code> or <code>https://youtu.be/...</code></li>
          <li><strong style={{ color: '#E1306C' }}>Instagram Reels & Posts:</strong> <code>https://instagram.com/reel/...</code> or <code>https://instagram.com/p/...</code></li>
          <li><strong style={{ color: '#00F2FE' }}>TikTok Videos:</strong> <code>https://tiktok.com/@user/video/...</code></li>
          <li><strong style={{ color: '#1877F2' }}>Facebook Reels:</strong> <code>https://facebook.com/reel/...</code></li>
          <li><strong style={{ color: '#10B981' }}>Web Articles & Recipe Blogs:</strong> Direct article or recipe blog post links.</li>
        </ul>
      </div>
    ),
    tags: ['platforms', 'urls', 'youtube shorts', 'instagram reel', 'tiktok', 'facebook']
  },
  {
    id: 'one-click-buying',
    category: 'features',
    question: 'How does 1-Click E-Commerce & 10-Minute Quick Commerce delivery work?',
    answer: (
      <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        <p>When Universal Pro AI extracts ingredients, cookware, or product recommendations, it automatically generates direct shoppable links:</p>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '0.5rem', marginTop: '0.4rem' }}>
          <div style={{ padding: '0.5rem 0.75rem', background: 'rgba(255, 153, 0, 0.1)', border: '1px solid rgba(255, 153, 0, 0.25)', borderRadius: '8px' }}>
            <strong style={{ color: '#FF9900' }}>🛒 E-Commerce Stores</strong>
            <div style={{ fontSize: '0.8rem', marginTop: '0.2rem' }}>Amazon India, Flipkart, Myntra, Meesho, AJIO</div>
          </div>
          <div style={{ padding: '0.5rem 0.75rem', background: 'rgba(234, 179, 8, 0.1)', border: '1px solid rgba(234, 179, 8, 0.25)', borderRadius: '8px' }}>
            <strong style={{ color: '#FACC15' }}>⚡ 10-Minute Delivery</strong>
            <div style={{ fontSize: '0.8rem', marginTop: '0.2rem' }}>Blinkit, Zepto, Swiggy Instamart, BigBasket</div>
          </div>
        </div>
        <p style={{ marginTop: '0.25rem', fontSize: '0.85rem', fontStyle: 'italic', color: 'var(--text-muted)' }}>
          Clicking any store badge opens the exact pre-filled search query so you can add ingredients or products straight to your cart in seconds!
        </p>
      </div>
    ),
    tags: ['shopping', 'amazon', 'blinkit', 'zepto', 'instamart', 'quick commerce', 'ingredients']
  },
  {
    id: 'serving-adjuster',
    category: 'features',
    question: 'How do I adjust ingredient measurements for different serving sizes?',
    answer: (
      <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        <p>
          Every extracted cooking recipe includes an interactive <strong style={{ color: '#34D399' }}>Serving Adjuster</strong> card.
        </p>
        <p>
          Click the <strong>+</strong> or <strong>-</strong> buttons to increase or decrease the portion size. The AI dynamically recalculates ingredient quantities (grams, cups, tablespoons, teaspoons, pieces) in real-time without losing formatting!
        </p>
      </div>
    ),
    tags: ['servings', 'ingredients', 'portion', 'recipe adjuster', 'scaling']
  },
  {
    id: 'whatsapp-export',
    category: 'features',
    question: 'Can I export extractions to WhatsApp or download plain text notes?',
    answer: (
      <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        <p>Yes! Universal Pro AI offers multiple export options for your extracted cards:</p>
        <ul style={{ paddingLeft: '1.25rem', lineHeight: '1.6' }}>
          <li><strong style={{ color: '#25D366' }}>Send via WhatsApp:</strong> Click the WhatsApp icon on any result card, enter your phone number, and send formatted summary notes, ingredients, and purchase links directly to your phone.</li>
          <li><strong style={{ color: '#38BDF8' }}>Download TXT File:</strong> Click "Download TXT" to save a clean text report offline.</li>
          <li><strong style={{ color: '#F472B6' }}>Copy Markdown Notes:</strong> Click "Copy Notes" to paste formatted Markdown into Notion, Evernote, or Apple Notes.</li>
        </ul>
      </div>
    ),
    tags: ['whatsapp', 'export', 'download', 'txt', 'copy notes', 'notion']
  },
  {
    id: 'vault-library',
    category: 'features',
    question: 'Where are my saved extractions stored?',
    answer: (
      <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        <p>
          All your extractions are saved in your local browser's <strong style={{ color: '#34D399' }}>Intelligence Vault Library</strong>.
        </p>
        <p>
          Click the <strong style={{ color: 'var(--accent-emerald)' }}>Intelligence Vault</strong> button in the top navigation bar at any time to browse, search, or reload past recipe cards and product extractions—even without internet connection!
        </p>
      </div>
    ),
    tags: ['vault', 'saved', 'library', 'history', 'offline', 'storage']
  },
  {
    id: 'troubleshooting-bot-check',
    category: 'troubleshooting',
    question: 'What should I do if a YouTube Short or Instagram Reel fails to load?',
    answer: (
      <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        <p>
          Universal Pro AI includes an automated <strong>Resilient Dual-Fallback Engine</strong>:
        </p>
        <ol style={{ paddingLeft: '1.25rem', lineHeight: '1.6' }}>
          <li>If YouTube or Instagram temporarily restricts cloud datacenter IP downloads with a bot sign-in prompt, our fallback engine automatically detects the restriction within milliseconds.</li>
          <li>It instantly switches to pulling high-resolution keyframe snapshots and oEmbed metadata.</li>
          <li>The AI model processes visual frames and description context to generate complete extraction cards without failing.</li>
        </ol>
        <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
          If a URL fails twice, ensure the video is <strong>Public</strong> (not Private or Unlisted) and try re-submitting.
        </p>
      </div>
    ),
    tags: ['error', 'bot check', 'youtube shorts error', 'instagram reel fail', 'fallback']
  },
  {
    id: 'mobile-chat-bots',
    category: 'features',
    question: 'How do I extract recipes directly inside Telegram or WhatsApp?',
    answer: (
      <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        <p>
          You can use our official mobile chat bots without installing any extra app:
        </p>
        <ul style={{ paddingLeft: '1.25rem', lineHeight: '1.6' }}>
          <li>
            <strong style={{ color: '#0088CC' }}>Telegram Bot:</strong> Send any reel or short link to <code>@UniversalProRecipeBot</code> (or click the 💬 Telegram Bot button in top nav) to receive structured ingredient cards and one-click feedback buttons instantly.
          </li>
          <li>
            <strong style={{ color: '#25D366' }}>WhatsApp Bot:</strong> Message our WhatsApp Assistant (or click 🟢 WhatsApp Bot in top nav) to forward links or type recipe names. Receive cleanly formatted markdown recipes with 10-minute delivery links for Blinkit & Zepto!
          </li>
        </ul>
      </div>
    ),
    tags: ['telegram', 'whatsapp', 'bot', 'chat', 'mobile', 'blinkit', 'zepto']
  },
  {
    id: 'how-to-use-telegram-bot',
    category: 'getting_started',
    question: 'How do I use the Telegram Bot (@universalProRecipeBot)?',
    answer: (
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
        <p>Using our official Telegram Bot is fast, free, and works directly inside Telegram without extra app installs:</p>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem', marginTop: '0.25rem' }}>
          <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.65rem' }}>
            <span style={{ background: 'rgba(0, 136, 204, 0.15)', color: '#0088CC', width: '24px', height: '24px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.75rem', fontWeight: 700, flexShrink: 0 }}>1</span>
            <div>
              <strong style={{ color: 'var(--text-primary)' }}>Open Chat:</strong> Search for <code style={{ color: '#0088CC', background: 'rgba(0,136,204,0.1)', padding: '0.1rem 0.35rem', borderRadius: '4px' }}>@universalProRecipeBot</code> in Telegram or click the 💬 <strong>Telegram Bot</strong> button in the top navigation bar.
            </div>
          </div>
          <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.65rem' }}>
            <span style={{ background: 'rgba(0, 136, 204, 0.15)', color: '#0088CC', width: '24px', height: '24px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.75rem', fontWeight: 700, flexShrink: 0 }}>2</span>
            <div>
              <strong style={{ color: 'var(--text-primary)' }}>Send /start:</strong> Tap <strong>Start</strong> or type <code>/start</code> to initialize the bot.
            </div>
          </div>
          <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.65rem' }}>
            <span style={{ background: 'rgba(0, 136, 204, 0.15)', color: '#0088CC', width: '24px', height: '24px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.75rem', fontWeight: 700, flexShrink: 0 }}>3</span>
            <div>
              <strong style={{ color: 'var(--text-primary)' }}>Paste Video Link:</strong> Share or paste any public link from Instagram Reels, YouTube Shorts, or TikTok.
            </div>
          </div>
          <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.65rem' }}>
            <span style={{ background: 'rgba(0, 136, 204, 0.15)', color: '#0088CC', width: '24px', height: '24px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.75rem', fontWeight: 700, flexShrink: 0 }}>4</span>
            <div>
              <strong style={{ color: 'var(--text-primary)' }}>Receive Extraction & Buy Links:</strong> Get formatted recipe ingredients, preparation steps, interactive accuracy buttons, and 10-minute Blinkit/Zepto delivery links in seconds!
            </div>
          </div>
        </div>
      </div>
    ),
    tags: ['telegram', 'bot', 'how to use', 'mobile', 'universalProRecipeBot', 'blinkit', 'zepto', 'reels']
  },
];

export default function FaqSection() {
  const [isSectionExpanded, setIsSectionExpanded] = useState<boolean>(false); // Collapsed by default
  const [activeCategory, setActiveCategory] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [openId, setOpenId] = useState<string | null>(null); // Accordions collapsed by default

  const toggleAccordion = (id: string) => {
    setOpenId((prev) => (prev === id ? null : id));
  };

  const filteredFaqs = FAQ_DATA.filter((faq) => {
    const matchesCategory = activeCategory === 'all' || faq.category === activeCategory;
    const matchesSearch =
      searchQuery.trim() === '' ||
      faq.question.toLowerCase().includes(searchQuery.toLowerCase()) ||
      faq.tags.some((t) => t.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesCategory && matchesSearch;
  });

  return (
    <section
      id="faq-section"
      style={{
        marginTop: '4rem',
        marginBottom: '4rem',
        padding: '2.5rem 1.5rem',
        background: 'var(--bg-surface)',
        backdropFilter: 'blur(16px)',
        WebkitBackdropFilter: 'blur(16px)',
        border: '1px solid var(--border-subtle)',
        borderRadius: 'var(--radius-lg)',
        boxShadow: '0 20px 40px -15px rgba(0, 0, 0, 0.5)'
      }}
      className="sc-reveal"
    >
      {/* Header Badge & Title */}
      <div style={{ textAlign: 'center', marginBottom: isSectionExpanded ? '2.5rem' : '1rem' }}>
        <div
          className="badge-pill badge-emerald"
          style={{ marginBottom: '0.75rem', padding: '0.35rem 0.85rem', fontSize: '0.75rem', cursor: 'pointer', display: 'inline-flex' }}
          onClick={() => setIsSectionExpanded((prev) => !prev)}
        >
          <HelpCircle size={14} color="#34D399" />
          <span>User Guide & Knowledge Base</span>
        </div>

        <h2
          style={{
            fontSize: '2rem',
            fontWeight: 800,
            letterSpacing: '-0.02em',
            color: 'var(--text-primary)',
            marginBottom: '0.75rem',
            cursor: 'pointer'
          }}
          onClick={() => setIsSectionExpanded((prev) => !prev)}
        >
          How to Use <span className="gradient-text">Universal Pro AI & Telegram Bot</span>
        </h2>

        <p style={{ color: 'var(--text-secondary)', fontSize: '1rem', maxWidth: '640px', margin: '0 auto 1.25rem' }}>
          Everything you need to know about extracting cooking recipes, workout plans, Telegram bot setup, and quick-commerce shopping links.
        </p>

        {/* Collapsible Header Button */}
        <button
          onClick={() => setIsSectionExpanded((prev) => !prev)}
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.5rem',
            padding: '0.65rem 1.5rem',
            borderRadius: 'var(--radius-full)',
            fontSize: '0.9rem',
            fontWeight: 700,
            background: isSectionExpanded ? 'var(--bg-surface-elevated)' : '#10B981',
            color: isSectionExpanded ? 'var(--text-primary)' : '#FFFFFF',
            border: isSectionExpanded ? '1px solid var(--border-subtle)' : 'none',
            boxShadow: isSectionExpanded ? 'none' : '0 4px 16px rgba(16, 185, 129, 0.4)',
            cursor: 'pointer',
            transition: 'all 0.2s ease-in-out'
          }}
        >
          {isSectionExpanded ? (
            <>
              <span>Collapse FAQ Section</span>
              <ChevronUp size={18} />
            </>
          ) : (
            <>
              <HelpCircle size={18} />
              <span>Expand FAQ & Telegram Bot Guide (9 Articles)</span>
              <ChevronDown size={18} />
            </>
          )}
        </button>
      </div>

      {isSectionExpanded && (
        <>
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
          gap: '1rem',
          marginBottom: '3rem'
        }}
      >
        <div
          style={{
            padding: '1.25rem',
            background: 'var(--bg-card)',
            border: '1px solid var(--border-subtle)',
            borderRadius: 'var(--radius-md)',
            display: 'flex',
            flexDirection: 'column',
            gap: '0.75rem'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div
              style={{
                width: '40px',
                height: '40px',
                borderRadius: '10px',
                background: 'rgba(16, 185, 129, 0.15)',
                color: '#059669',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontWeight: 800,
                fontSize: '1.1rem'
              }}
            >
              01
            </div>
            <Play size={20} color="#059669" />
          </div>
          <div>
            <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.25rem' }}>
              Copy Video Link
            </h3>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: '1.4' }}>
              Copy any URL from YouTube Shorts, Instagram Reels, TikTok, or Facebook Reels.
            </p>
          </div>
        </div>

        <div
          style={{
            padding: '1.25rem',
            background: 'var(--bg-card)',
            border: '1px solid var(--border-subtle)',
            borderRadius: 'var(--radius-md)',
            display: 'flex',
            flexDirection: 'column',
            gap: '0.75rem'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div
              style={{
                width: '40px',
                height: '40px',
                borderRadius: '10px',
                background: 'rgba(2, 132, 199, 0.15)',
                color: '#0284C7',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontWeight: 800,
                fontSize: '1.1rem'
              }}
            >
              02
            </div>
            <Zap size={20} color="#0284C7" />
          </div>
          <div>
            <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.25rem' }}>
              Sub-3s AI Analysis
            </h3>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: '1.4' }}>
              Our multimodal neural engine samples video frames and transcribes audio narration.
            </p>
          </div>
        </div>

        <div
          style={{
            padding: '1.25rem',
            background: 'var(--bg-card)',
            border: '1px solid var(--border-subtle)',
            borderRadius: 'var(--radius-md)',
            display: 'flex',
            flexDirection: 'column',
            gap: '0.75rem'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div
              style={{
                width: '40px',
                height: '40px',
                borderRadius: '10px',
                background: 'rgba(217, 119, 6, 0.15)',
                color: '#D97706',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontWeight: 800,
                fontSize: '1.1rem'
              }}
            >
              03
            </div>
            <ShoppingCart size={20} color="#D97706" />
          </div>
          <div>
            <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.25rem' }}>
              1-Click Buy & Store Search
            </h3>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: '1.4' }}>
              Get direct 1-click buy links for Amazon, Blinkit, Zepto, Swiggy Instamart, and Flipkart.
            </p>
          </div>
        </div>

        <div
          style={{
            padding: '1.25rem',
            background: 'var(--bg-card)',
            border: '1px solid var(--border-subtle)',
            borderRadius: 'var(--radius-md)',
            display: 'flex',
            flexDirection: 'column',
            gap: '0.75rem'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div
              style={{
                width: '40px',
                height: '40px',
                borderRadius: '10px',
                background: 'rgba(192, 38, 211, 0.15)',
                color: '#C026D3',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontWeight: 800,
                fontSize: '1.1rem'
              }}
            >
              04
            </div>
            <Smartphone size={20} color="#C026D3" />
          </div>
          <div>
            <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.25rem' }}>
              Export to WhatsApp & Vault
            </h3>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: '1.4' }}>
              Send formatted notes straight to WhatsApp or save extractions offline in your Vault.
            </p>
          </div>
        </div>
      </div>

      {/* Filter Tabs & Search Bar */}
      <div
        style={{
          display: 'flex',
          flexDirection: 'row',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '1rem',
          marginBottom: '1.5rem'
        }}
      >
        {/* Category Pills */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
          {[
            { id: 'all', label: 'All Questions' },
            { id: 'getting_started', label: '🚀 Getting Started' },
            { id: 'features', label: '✨ Features & Shopping' },
            { id: 'platforms', label: '📱 Platforms' },
            { id: 'troubleshooting', label: '🛠️ Troubleshooting' }
          ].map((cat) => (
            <button
              key={cat.id}
              onClick={() => setActiveCategory(cat.id)}
              style={{
                padding: '0.45rem 0.85rem',
                borderRadius: 'var(--radius-full)',
                fontSize: '0.825rem',
                fontWeight: 700,
                border: activeCategory === cat.id ? '1px solid #059669' : '1px solid var(--border-subtle)',
                background: activeCategory === cat.id ? '#10B981' : 'var(--bg-surface-elevated)',
                color: activeCategory === cat.id ? '#FFFFFF' : 'var(--text-secondary)',
                boxShadow: activeCategory === cat.id ? '0 4px 12px rgba(16, 185, 129, 0.35)' : 'none',
                cursor: 'pointer',
                transition: 'all 0.2s ease'
              }}
            >
              {cat.label}
            </button>
          ))}
        </div>

        {/* FAQ Search Bar */}
        <div style={{ position: 'relative', width: '100%', maxWidth: '280px' }}>
          <Search
            size={16}
            color="var(--text-muted)"
            style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)' }}
          />
          <input
            type="text"
            placeholder="Search FAQs..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{
              width: '100%',
              padding: '0.45rem 0.75rem 0.45rem 2.2rem',
              background: 'var(--bg-card)',
              border: '1px solid var(--border-subtle)',
              borderRadius: 'var(--radius-sm)',
              color: 'var(--text-primary)',
              fontSize: '0.85rem',
              outline: 'none'
            }}
          />
        </div>
      </div>

      {/* Accordion FAQ Items List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
        {filteredFaqs.length > 0 ? (
          filteredFaqs.map((faq) => {
            const isOpen = openId === faq.id;
            return (
              <div
                key={faq.id}
                style={{
                  background: 'var(--bg-card)',
                  border: isOpen ? '1px solid rgba(16, 185, 129, 0.35)' : '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-sm)',
                  overflow: 'hidden',
                  transition: 'all 0.2s ease-in-out'
                }}
              >
                <button
                  onClick={() => toggleAccordion(faq.id)}
                  style={{
                    width: '100%',
                    padding: '1.1rem 1.25rem',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    gap: '1rem',
                    background: 'transparent',
                    border: 'none',
                    color: 'var(--text-primary)',
                    fontSize: '0.975rem',
                    fontWeight: 600,
                    textAlign: 'left',
                    cursor: 'pointer'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                    <HelpCircle size={18} color={isOpen ? '#34D399' : 'var(--text-muted)'} style={{ flexShrink: 0 }} />
                    <span>{faq.question}</span>
                  </div>
                  {isOpen ? (
                    <ChevronUp size={18} color="#34D399" style={{ flexShrink: 0 }} />
                  ) : (
                    <ChevronDown size={18} color="var(--text-muted)" style={{ flexShrink: 0 }} />
                  )}
                </button>

                {isOpen && (
                  <div
                    style={{
                      padding: '0 1.25rem 1.25rem 3rem',
                      borderTop: '1px solid rgba(255, 255, 255, 0.05)',
                      marginTop: '0.25rem',
                      paddingTop: '1rem'
                    }}
                  >
                    {faq.answer}
                  </div>
                )}
              </div>
            );
          })
        ) : (
          <div
            style={{
              padding: '2rem',
              textAlign: 'center',
              color: 'var(--text-muted)',
              fontSize: '0.9rem'
            }}
          >
            No FAQs matching "{searchQuery}". Try searching for terms like "recipe", "YouTube", "Blinkit", or "servings".
          </div>
        )}
      </div>
        </>
      )}
    </section>
  );
}
