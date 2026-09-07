'use client';

import React, { useState, useEffect } from 'react';
import { Tag, Check, X, ShieldAlert, Save, ExternalLink } from 'lucide-react';

interface CreatorTagVaultProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function CreatorTagVault({ isOpen, onClose }: CreatorTagVaultProps) {
  const [amazonTag, setAmazonTag] = useState('');
  const [earnkaroId, setEarnkaroId] = useState('');
  const [loading, setLoading] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen) {
      fetch('/api/v1/auth/me')
        .then((r) => r.json())
        .then((data) => {
          if (data.user) {
            setAmazonTag(data.user.custom_amazon_tag || '');
            setEarnkaroId(data.user.custom_earnkaro_id || '');
          }
        })
        .catch(() => {});
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSaved(false);

    try {
      const res = await fetch('/api/v1/auth/profile', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          custom_amazon_tag: amazonTag.trim() || null,
          custom_earnkaro_id: earnkaroId.trim() || null
        })
      });
      const data = await res.json();
      if (data.status === 'success') {
        setSaved(true);
        setTimeout(() => setSaved(false), 3000);
      } else {
        setError(data.message || 'Failed to update creator tags');
      }
    } catch (err: any) {
      setError(err.message || 'Network error');
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
          maxWidth: '480px',
          backgroundColor: '#0F172A',
          border: '1px solid rgba(255, 255, 255, 0.12)',
          borderRadius: '20px',
          padding: '24px',
          color: '#F8FAFC',
          boxShadow: '0 20px 40px rgba(0, 0, 0, 0.5)',
          position: 'relative'
        }}
      >
        <button
          onClick={onClose}
          style={{
            position: 'absolute',
            top: '18px',
            right: '18px',
            background: 'none',
            border: 'none',
            color: '#94A3B8',
            cursor: 'pointer'
          }}
        >
          <X size={18} />
        </button>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
          <Tag size={20} color="#10B981" />
          <h3 style={{ fontSize: '18px', fontWeight: 700, margin: 0 }}>Creator Tag Vault</h3>
        </div>
        <p style={{ fontSize: '13px', color: '#94A3B8', margin: '0 0 16px 0', lineHeight: 1.4 }}>
          Inject your personal affiliate credentials into every extraction link you share. Keep 100% of outbound merchant commissions.
        </p>

        <form onSubmit={handleSave} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, color: '#CBD5E1', marginBottom: '6px' }}>
              Amazon Associates Tag
            </label>
            <input
              type="text"
              placeholder="e.g. yourbrand-21"
              value={amazonTag}
              onChange={(e) => setAmazonTag(e.target.value)}
              style={{
                width: '100%',
                padding: '10px 14px',
                borderRadius: '8px',
                border: '1px solid #334155',
                backgroundColor: '#1E293B',
                color: '#F8FAFC',
                fontSize: '14px',
                outline: 'none',
                boxSizing: 'border-box'
              }}
            />
            <span style={{ fontSize: '11px', color: '#64748B', marginTop: '4px', display: 'block' }}>
              Replaces default system tag on Amazon India ingredient cart links.
            </span>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, color: '#CBD5E1', marginBottom: '6px' }}>
              EarnKaro Affiliate ID
            </label>
            <input
              type="text"
              placeholder="e.g. 5608766"
              value={earnkaroId}
              onChange={(e) => setEarnkaroId(e.target.value)}
              style={{
                width: '100%',
                padding: '10px 14px',
                borderRadius: '8px',
                border: '1px solid #334155',
                backgroundColor: '#1E293B',
                color: '#F8FAFC',
                fontSize: '14px',
                outline: 'none',
                boxSizing: 'border-box'
              }}
            />
            <span style={{ fontSize: '11px', color: '#64748B', marginTop: '4px', display: 'block' }}>
              Used for Flipkart, Meesho, AJIO, and Nykaa merchant links.
            </span>
          </div>

          {error && <div style={{ color: '#EF4444', fontSize: '12px' }}>{error}</div>}
          {saved && (
            <div style={{ color: '#10B981', fontSize: '12px', display: 'flex', alignItems: 'center', gap: '4px' }}>
              <Check size={14} /> Creator tags successfully updated!
            </div>
          )}

          <div style={{ display: 'flex', gap: '10px', marginTop: '8px' }}>
            <button
              type="submit"
              disabled={loading}
              style={{
                flex: 1,
                padding: '10px 16px',
                borderRadius: '10px',
                border: 'none',
                backgroundColor: '#10B981',
                color: '#FFFFFF',
                fontSize: '14px',
                fontWeight: 600,
                cursor: loading ? 'not-allowed' : 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '6px'
              }}
            >
              <Save size={16} />
              {loading ? 'Saving...' : 'Save Creator Tags'}
            </button>
            <button
              type="button"
              onClick={onClose}
              style={{
                padding: '10px 16px',
                borderRadius: '10px',
                border: '1px solid #334155',
                backgroundColor: 'transparent',
                color: '#94A3B8',
                fontSize: '14px',
                fontWeight: 600,
                cursor: 'pointer'
              }}
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
