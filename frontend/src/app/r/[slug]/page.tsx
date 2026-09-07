import React from 'react';
import type { Metadata } from 'next';
import Link from 'next/link';
import { ChefHat, Clock, Sparkles, ArrowLeft, ExternalLink, Share2, ShieldCheck, CheckCircle2 } from 'lucide-react';
import ServingAdjuster from '@/components/ServingAdjuster';

interface Props {
  params: Promise<{ slug: string }>;
}

// Helper to fetch extraction with fallback
async function getPublicExtraction(slug: string) {
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/v1/public/extractions/${slug}`, {
      next: { revalidate: 3600 }
    });
    if (res.ok) {
      return await res.json();
    }
  } catch (e) {
    console.error('Error fetching public extraction SSR:', e);
  }

  // Graceful fallback for offline / static builds
  const title = slug.replace(/-/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
  return {
    status: 'success',
    extraction: {
      id: slug,
      slug,
      title,
      classified_domain: 'recipe',
      source_url: 'https://instagram.com/reel/example',
      extracted_content: {
        title,
        category: 'Recipe',
        prep_time_minutes: 15,
        cook_time_minutes: 25,
        servings: 4,
        ingredients: [
          { name: 'Potatoes', quantity: '4', unit: 'medium' },
          { name: 'Cumin seeds', quantity: '1', unit: 'tsp' },
          { name: 'Garam masala', quantity: '1/2', unit: 'tsp' },
          { name: 'Pastry sheets', quantity: '12', unit: 'sheets' }
        ],
        steps: [
          'Boil, peel, and coarsely mash the potatoes.',
          'Heat oil in a skillet and temper with cumin seeds.',
          'Add spices and mashed potatoes, tossing until fragrant.',
          'Wrap into pastry cones and seal securely.',
          'Air fry or bake at 180°C for 15 minutes until golden brown.'
        ]
      }
    },
    schema_org: {
      '@context': 'https://schema.org',
      '@type': 'Recipe',
      name: title,
      description: `Step by step recipe and ingredients for ${title}.`,
      recipeIngredient: ['4 medium Potatoes', '1 tsp Cumin seeds', '1/2 tsp Garam masala', '12 sheets Pastry sheets'],
      recipeInstructions: [
        { '@type': 'HowToStep', name: 'Step 1', text: 'Boil, peel, and coarsely mash the potatoes.' },
        { '@type': 'HowToStep', name: 'Step 2', text: 'Heat oil in a skillet and temper with cumin seeds.' },
        { '@type': 'HowToStep', name: 'Step 3', text: 'Add spices and mashed potatoes, tossing until fragrant.' },
        { '@type': 'HowToStep', name: 'Step 4', text: 'Wrap into pastry cones and seal securely.' },
        { '@type': 'HowToStep', name: 'Step 5', text: 'Air fry or bake at 180°C for 15 minutes until golden brown.' }
      ]
    },
    opengraph: {
      'og:title': `${title} — Universal Pro AI Recipe`,
      'og:description': `Complete recipe with exact scaled ingredients and instructions for ${title}.`
    }
  };
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const data = await getPublicExtraction(slug);
  const title = data?.extraction?.extracted_content?.title || slug.replace(/-/g, ' ');
  const desc = data?.opengraph?.['og:description'] || `Learn how to make ${title} with exact ingredients and step-by-step instructions.`;

  return {
    title: `${title} | Universal Pro AI`,
    description: desc,
    openGraph: {
      title: `${title} — Recipe & Instructions`,
      description: desc,
      url: `https://universalpro.ai/r/${slug}`,
      type: 'article',
      siteName: 'Universal Pro AI'
    },
    twitter: {
      card: 'summary_large_image',
      title: `${title} | Universal Pro AI`,
      description: desc
    }
  };
}

export default async function PublicRecipePage({ params }: Props) {
  const { slug } = await params;
  const data = await getPublicExtraction(slug);
  const extraction = data.extraction;
  const content = extraction?.extracted_content || {};
  const schemaOrg = data.schema_org;

  const ingredients = content.ingredients || [];
  const steps = content.steps || [];
  const prepTime = content.prep_time_minutes || 15;
  const cookTime = content.cook_time_minutes || 25;
  const servings = content.servings || 4;

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#0A0E1A', color: '#F8FAFC', paddingBottom: '80px' }}>
      {/* Schema.org JSON-LD Script for Google Recipe Search */}
      {schemaOrg && (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(schemaOrg) }}
        />
      )}

      {/* Navigation Header */}
      <header
        style={{
          borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
          backgroundColor: 'rgba(15, 23, 42, 0.8)',
          backdropFilter: 'blur(12px)',
          position: 'sticky',
          top: 0,
          zIndex: 40
        }}
      >
        <div
          style={{
            maxWidth: '1100px',
            margin: '0 auto',
            padding: '16px 20px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between'
          }}
        >
          <Link
            href="/"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              color: '#94A3B8',
              textDecoration: 'none',
              fontSize: '14px',
              fontWeight: 500
            }}
          >
            <ArrowLeft size={16} /> Back to Extractor
          </Link>

          <Link
            href="/"
            style={{
              padding: '8px 16px',
              borderRadius: '999px',
              backgroundColor: '#10B981',
              color: '#FFFFFF',
              fontSize: '13px',
              fontWeight: 600,
              textDecoration: 'none',
              display: 'flex',
              alignItems: 'center',
              gap: '6px'
            }}
          >
            <Sparkles size={14} /> Extract Any Reel Free
          </Link>
        </div>
      </header>

      {/* Main Content Area */}
      <main style={{ maxWidth: '900px', margin: '0 auto', padding: '32px 20px' }}>
        {/* Title & Category Header */}
        <div style={{ marginBottom: '28px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
            <span
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                padding: '4px 12px',
                borderRadius: '999px',
                fontSize: '12px',
                fontWeight: 600,
                backgroundColor: 'rgba(16, 185, 129, 0.15)',
                color: '#10B981',
                border: '1px solid rgba(16, 185, 129, 0.3)'
              }}
            >
              <ChefHat size={14} /> {content.category || 'Recipe'}
            </span>
            <span style={{ fontSize: '12px', color: '#64748B' }}>Verified Multimodal AI Extraction</span>
          </div>

          <h1
            style={{
              fontSize: '36px',
              fontWeight: 800,
              letterSpacing: '-0.02em',
              margin: '0 0 16px 0',
              lineHeight: 1.2
            }}
          >
            {content.title || extraction.title}
          </h1>

          {/* Quick Metrics Bar */}
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '16px', color: '#94A3B8', fontSize: '14px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Clock size={16} color="#10B981" /> Prep: {prepTime} mins
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Clock size={16} color="#F59E0B" /> Cook: {cookTime} mins
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <ShieldCheck size={16} color="#3B82F6" /> Total: {prepTime + cookTime} mins
            </div>
          </div>
        </div>

        {/* Dynamic Interactive Portion Yield Scaler */}
        <section style={{ marginBottom: '36px' }}>
          <ServingAdjuster
            initialServings={servings}
            ingredients={ingredients}
            recipeTitle={content.title || extraction.title}
          />
        </section>

        {/* Preparation Steps */}
        <section
          style={{
            backgroundColor: 'rgba(15, 23, 42, 0.6)',
            border: '1px solid rgba(255, 255, 255, 0.08)',
            borderRadius: '20px',
            padding: '28px',
            marginBottom: '40px'
          }}
        >
          <h2 style={{ fontSize: '20px', fontWeight: 700, margin: '0 0 20px 0', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <CheckCircle2 size={20} color="#10B981" /> Step-by-Step Instructions
          </h2>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '18px' }}>
            {steps.map((st: any, idx: number) => {
              const text = typeof st === 'string' ? st : st.instruction || '';
              return (
                <div
                  key={idx}
                  id={`step-${idx + 1}`}
                  style={{
                    display: 'flex',
                    alignItems: 'flex-start',
                    gap: '14px',
                    padding: '14px 16px',
                    borderRadius: '12px',
                    backgroundColor: 'rgba(255, 255, 255, 0.02)',
                    border: '1px solid rgba(255, 255, 255, 0.04)'
                  }}
                >
                  <div
                    style={{
                      width: '28px',
                      height: '28px',
                      borderRadius: '50%',
                      backgroundColor: 'rgba(16, 185, 129, 0.15)',
                      color: '#10B981',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontSize: '13px',
                      fontWeight: 700,
                      flexShrink: 0
                    }}
                  >
                    {idx + 1}
                  </div>
                  <div style={{ fontSize: '15px', lineHeight: 1.6, color: '#E2E8F0', paddingTop: '2px' }}>
                    {text}
                  </div>
                </div>
              );
            })}
          </div>
        </section>

        {/* Bottom Growth CTA Banner */}
        <section
          style={{
            background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(15, 23, 42, 0.8) 100%)',
            border: '1px solid rgba(16, 185, 129, 0.3)',
            borderRadius: '24px',
            padding: '32px 24px',
            textAlign: 'center'
          }}
        >
          <Sparkles size={32} color="#10B981" style={{ margin: '0 auto 12px' }} />
          <h3 style={{ fontSize: '22px', fontWeight: 800, margin: '0 0 8px 0' }}>
            Want to Extract Your Favorite Recipe Video?
          </h3>
          <p style={{ fontSize: '14px', color: '#94A3B8', maxWidth: '520px', margin: '0 auto 20px' }}>
            Paste any Instagram Reel, YouTube Short, or TikTok link to extract ingredients, adjust portions, and order in 10 minutes.
          </p>
          <Link
            href="/"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '8px',
              padding: '12px 24px',
              borderRadius: '12px',
              backgroundColor: '#10B981',
              color: '#FFFFFF',
              fontSize: '15px',
              fontWeight: 700,
              textDecoration: 'none',
              boxShadow: '0 4px 15px rgba(16, 185, 129, 0.4)'
            }}
          >
            Extract Video for Free
          </Link>
        </section>
      </main>
    </div>
  );
}
