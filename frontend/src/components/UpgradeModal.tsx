'use client';

import React, { useState } from 'react';
import { Sparkles, Check, X, ShieldCheck, Zap, Globe, CreditCard } from 'lucide-react';

interface UpgradeModalProps {
  isOpen: boolean;
  onClose: () => void;
  reason?: string;
}

export default function UpgradeModal({ isOpen, onClose, reason }: UpgradeModalProps) {
  const [currency, setCurrency] = useState<'INR' | 'USD'>('INR');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleCheckout = async () => {
    setLoading(true);
    setError(null);
    try {
      const provider = currency === 'INR' ? 'razorpay' : 'stripe';
      const res = await fetch('/api/v1/billing/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ provider })
      });
      const data = await res.json();
      if (data.status === 'success' && data.checkout_session) {
        const session = data.checkout_session;
        if (session.checkout_url) {
          window.location.href = session.checkout_url;
        } else {
          // Razorpay simulated / live modal checkout
          alert(`Razorpay checkout initialized for ${session.plan_id} (₹299/mo). Subscription ID: ${session.subscription_id}`);
          onClose();
        }
      } else {
        setError('Failed to initiate checkout. Please try again.');
      }
    } catch (err: any) {
      setError(err.message || 'Payment service unreachable');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        zIndex: 9999,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: 'rgba(5, 8, 16, 0.85)',
        backdropFilter: 'blur(8px)',
        padding: '16px'
      }}
    >
      <div
        style={{
          width: '100%',
          maxWidth: '520px',
          backgroundColor: '#0F172A',
          border: '1px solid rgba(255, 255, 255, 0.12)',
          borderRadius: '24px',
          padding: '28px',
          boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.6), 0 0 30px rgba(16, 185, 129, 0.15)',
          color: '#F8FAFC',
          position: 'relative'
        }}
      >
        {/* Close button */}
        <button
          onClick={onClose}
          style={{
            position: 'absolute',
            top: '20px',
            right: '20px',
            background: 'rgba(255, 255, 255, 0.06)',
            border: 'none',
            borderRadius: '50%',
            width: '36px',
            height: '36px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#94A3B8',
            cursor: 'pointer',
            transition: 'all 0.2s'
          }}
        >
          <X size={18} />
        </button>

        {/* Badge */}
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
            <Sparkles size={14} /> Universal Pro Plan
          </span>
          {reason && (
            <span style={{ fontSize: '12px', color: '#F59E0B', fontWeight: 500 }}>
              {reason}
            </span>
          )}
        </div>

        <h2 style={{ fontSize: '24px', fontWeight: 700, margin: '0 0 8px 0', letterSpacing: '-0.02em' }}>
          Unlock Unlimited AI Extractions
        </h2>
        <p style={{ fontSize: '14px', color: '#94A3B8', margin: '0 0 20px 0', lineHeight: 1.5 }}>
          Extract recipes, workouts, tutorials, and gadgets with zero daily limits, prioritized AI inference, and custom creator monetization.
        </p>

        {/* Currency Switcher */}
        <div
          style={{
            display: 'flex',
            backgroundColor: '#1E293B',
            padding: '4px',
            borderRadius: '12px',
            marginBottom: '20px'
          }}
        >
          <button
            onClick={() => setCurrency('INR')}
            style={{
              flex: 1,
              padding: '8px 14px',
              borderRadius: '8px',
              border: 'none',
              fontSize: '13px',
              fontWeight: 600,
              cursor: 'pointer',
              backgroundColor: currency === 'INR' ? '#10B981' : 'transparent',
              color: currency === 'INR' ? '#FFFFFF' : '#94A3B8',
              transition: 'all 0.2s'
            }}
          >
            🇮🇳 India (₹299/mo UPI AutoPay)
          </button>
          <button
            onClick={() => setCurrency('USD')}
            style={{
              flex: 1,
              padding: '8px 14px',
              borderRadius: '8px',
              border: 'none',
              fontSize: '13px',
              fontWeight: 600,
              cursor: 'pointer',
              backgroundColor: currency === 'USD' ? '#10B981' : 'transparent',
              color: currency === 'USD' ? '#FFFFFF' : '#94A3B8',
              transition: 'all 0.2s'
            }}
          >
            🌐 Global ($4.99/mo Stripe)
          </button>
        </div>

        {/* Price Card */}
        <div
          style={{
            backgroundColor: 'rgba(255, 255, 255, 0.03)',
            border: '1px solid rgba(16, 185, 129, 0.25)',
            borderRadius: '16px',
            padding: '16px 20px',
            marginBottom: '20px',
            display: 'flex',
            alignItems: 'baseline',
            justifyContent: 'space-between'
          }}
        >
          <div>
            <div style={{ fontSize: '12px', color: '#94A3B8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Billed Monthly • Cancel Anytime
            </div>
            <div style={{ fontSize: '32px', fontWeight: 800, color: '#F8FAFC', marginTop: '4px' }}>
              {currency === 'INR' ? '₹299' : '$4.99'}
              <span style={{ fontSize: '14px', fontWeight: 500, color: '#64748B' }}> / month</span>
            </div>
          </div>
          <span style={{ fontSize: '12px', color: '#10B981', fontWeight: 600 }}>
            {currency === 'INR' ? 'Instant UPI AutoPay' : 'Card / Apple Pay'}
          </span>
        </div>

        {/* Feature List */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '24px' }}>
          {[
            'Unlimited Daily Reel & Short Extractions',
            'Sub-3s Gemini 3.8 Flash Multimodal Synthesis',
            'Creator Tag Vault (Keep 100% of your Amazon & EarnKaro affiliate earnings)',
            'Dynamic 1-12 Portion Serving Adjuster & 1-Click Quick Commerce (Zepto/Blinkit)',
            'Unlimited Personal Vault Storage & Markdown/JSON Exports',
            'Telegram & WhatsApp Bot Instant Ingestion Sync'
          ].map((item, idx) => (
            <div key={idx} style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '13px', color: '#CBD5E1' }}>
              <div
                style={{
                  width: '18px',
                  height: '18px',
                  borderRadius: '50%',
                  backgroundColor: 'rgba(16, 185, 129, 0.2)',
                  color: '#10B981',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  flexShrink: 0
                }}
              >
                <Check size={12} strokeWidth={3} />
              </div>
              <span>{item}</span>
            </div>
          ))}
        </div>

        {error && (
          <div style={{ color: '#EF4444', fontSize: '13px', marginBottom: '14px', textAlign: 'center' }}>
            {error}
          </div>
        )}

        {/* Action Button */}
        <button
          onClick={handleCheckout}
          disabled={loading}
          style={{
            width: '100%',
            padding: '14px',
            borderRadius: '12px',
            border: 'none',
            fontSize: '15px',
            fontWeight: 700,
            cursor: loading ? 'not-allowed' : 'pointer',
            backgroundColor: '#10B981',
            color: '#FFFFFF',
            boxShadow: '0 4px 14px rgba(16, 185, 129, 0.4)',
            transition: 'all 0.2s',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '8px'
          }}
        >
          {loading ? (
            'Initiating Secure Checkout...'
          ) : (
            <>
              <Zap size={18} />
              Upgrade to Pro — {currency === 'INR' ? '₹299/mo' : '$4.99/mo'}
            </>
          )}
        </button>

        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px', marginTop: '12px', color: '#64748B', fontSize: '11px' }}>
          <ShieldCheck size={14} /> 256-Bit Encrypted Secure Checkout via {currency === 'INR' ? 'Razorpay' : 'Stripe'}
        </div>
      </div>
    </div>
  );
}
