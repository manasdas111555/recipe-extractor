'use client';

import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  X,
  ChevronLeft,
  ChevronRight,
  Play,
  Pause,
  RotateCcw,
  Volume2,
  VolumeX,
  Mic,
  MicOff,
  Sun,
  Flame,
  CheckCircle2,
  Clock,
  ChefHat,
  ListFilter,
  Maximize2,
  Minimize2,
  Sparkles,
} from 'lucide-react';
import { useWakeLock } from '../hooks/useWakeLock';
import { useStepTimer } from '../hooks/useStepTimer';
import { parseInstructionDurations } from '../utils/durationParser';
import { useRecipe } from '../context/RecipeContext';
import { ExtractionResult } from '../types/recipe';

export interface CookingModeDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  recipe: ExtractionResult | null;
  initialStep?: number;
}

export default function CookingModeDrawer({
  isOpen,
  onClose,
  recipe,
  initialStep = 0,
}: CookingModeDrawerProps) {
  const [currentStepIndex, setCurrentStepIndex] = useState<number>(initialStep);
  const [isVoiceActive, setIsVoiceActive] = useState<boolean>(false);
  const [voiceTranscript, setVoiceTranscript] = useState<string>('');
  const [showIngredientList, setShowIngredientList] = useState<boolean>(false);
  const [isFullscreen, setIsFullscreen] = useState<boolean>(false);
  const [touchStartX, setTouchStartX] = useState<number | null>(null);

  // Screen Wake Lock hook integration
  const { isSupported: isWakeLockSupported, isLocked: isWakeLockActive, request: requestWakeLock, release: releaseWakeLock } = useWakeLock();

  // Recipe context state
  const { servingsMultiplier, setServingsMultiplier, checkedIngredientIds, toggleIngredientCheck } = useRecipe();

  // Instructions array extraction
  const instructions: string[] = recipe?.instructions || recipe?.steps || [];
  const totalSteps = instructions.length;
  const currentStepText = instructions[currentStepIndex] || 'No instructions available.';

  // Parse durations for active step
  const parsedDurations = parseInstructionDurations(currentStepText);
  const activeDurationSeconds = parsedDurations.length > 0 ? parsedDurations[0].totalSeconds : 0;

  // Active step timer hook
  const {
    remainingSeconds,
    isRunning: isTimerRunning,
    start: startTimer,
    pause: pauseTimer,
    reset: resetTimer,
  } = useStepTimer({
    durationSeconds: activeDurationSeconds,
    onComplete: () => {
      // Step timer completed feedback
    },
  });

  // Automatically trigger WakeLock when Cooking Mode opens
  useEffect(() => {
    if (isOpen) {
      requestWakeLock();
    } else {
      releaseWakeLock();
      setIsVoiceActive(false);
    }
  }, [isOpen, requestWakeLock, releaseWakeLock]);

  // Synchronize initial step when opened
  useEffect(() => {
    if (isOpen) {
      setCurrentStepIndex(initialStep);
    }
  }, [isOpen, initialStep]);

  // Keyboard Navigation: ArrowRight / Space -> Next, ArrowLeft -> Prev, Escape -> Close
  useEffect(() => {
    if (!isOpen) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight' || e.key === 'Space') {
        if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;
        e.preventDefault();
        handleNextStep();
      } else if (e.key === 'ArrowLeft') {
        if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;
        e.preventDefault();
        handlePrevStep();
      } else if (e.key === 'Escape') {
        e.preventDefault();
        onClose();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, currentStepIndex, totalSteps]);

  // Touch Swipe Gesture Handlers
  const handleTouchStart = (e: React.TouchEvent) => {
    setTouchStartX(e.touches[0].clientX);
  };

  const handleTouchEnd = (e: React.TouchEvent) => {
    if (touchStartX === null) return;
    const touchEndX = e.changedTouches[0].clientX;
    const deltaX = touchEndX - touchStartX;

    if (deltaX < -50) {
      // Swipe left -> Next step
      handleNextStep();
    } else if (deltaX > 50) {
      // Swipe right -> Previous step
      handlePrevStep();
    }
    setTouchStartX(null);
  };

  const handleNextStep = () => {
    if (currentStepIndex < totalSteps - 1) {
      setCurrentStepIndex((prev) => prev + 1);
      resetTimer();
    }
  };

  const handlePrevStep = () => {
    if (currentStepIndex > 0) {
      setCurrentStepIndex((prev) => prev - 1);
      resetTimer();
    }
  };

  // Fullscreen API toggle
  const toggleFullscreenMode = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
      setIsFullscreen(true);
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen().catch(() => {});
        setIsFullscreen(false);
      }
    }
  };

  // Web Speech API Voice Recognition Bridge (Defensive Fallback)
  const toggleVoiceNavigation = useCallback(() => {
    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert('Voice navigation is not supported in this browser. Please use Chrome, Safari, or Edge.');
      return;
    }

    if (isVoiceActive) {
      setIsVoiceActive(false);
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = false;
      recognition.lang = 'en-US';

      recognition.onstart = () => {
        setIsVoiceActive(true);
      };

      recognition.onresult = (event: any) => {
        const lastIndex = event.results.length - 1;
        const transcript = event.results[lastIndex][0].transcript.trim().toLowerCase();
        setVoiceTranscript(transcript);

        if (transcript.includes('next') || transcript.includes('forward')) {
          handleNextStep();
        } else if (transcript.includes('back') || transcript.includes('previous')) {
          handlePrevStep();
        } else if (transcript.includes('start') || transcript.includes('timer')) {
          startTimer();
        } else if (transcript.includes('stop') || transcript.includes('pause')) {
          pauseTimer();
        } else if (transcript.includes('reset')) {
          resetTimer();
        }
      };

      recognition.onerror = () => {
        setIsVoiceActive(false);
      };

      recognition.onend = () => {
        setIsVoiceActive(false);
      };

      recognition.start();
    } catch (e) {
      console.warn('SpeechRecognition initialization error:', e);
      setIsVoiceActive(false);
    }
  }, [isVoiceActive, currentStepIndex, totalSteps]);

  if (!isOpen || !recipe) return null;

  const progressPercent = totalSteps > 0 ? ((currentStepIndex + 1) / totalSteps) * 100 : 0;
  const ingredients = recipe.ingredients || [];

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        zIndex: 9999,
        background: 'rgba(5, 7, 13, 0.96)',
        backdropFilter: 'blur(24px)',
        display: 'flex',
        flexDirection: 'column',
        color: '#FFFFFF',
        overflow: 'hidden',
      }}
      onTouchStart={handleTouchStart}
      onTouchEnd={handleTouchEnd}
    >
      {/* Top Header Bar */}
      <header
        style={{
          padding: '1rem 1.5rem',
          borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          background: 'rgba(15, 23, 42, 0.8)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div
            style={{
              width: '38px',
              height: '38px',
              borderRadius: '10px',
              background: 'linear-gradient(135deg, #10B981, #059669)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <ChefHat size={22} color="#FFFFFF" />
          </div>
          <div>
            <h2 style={{ fontSize: '1.1rem', fontWeight: 800, margin: 0, letterSpacing: '-0.02em' }}>
              {recipe.title || recipe.recipe_title || 'Cooking Mode'}
            </h2>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '0.15rem' }}>
              <span style={{ fontSize: '0.75rem', color: '#94A3B8' }}>
                Step {currentStepIndex + 1} of {totalSteps}
              </span>
              {isWakeLockActive && (
                <span
                  style={{
                    fontSize: '0.68rem',
                    fontWeight: 700,
                    padding: '0.15rem 0.45rem',
                    borderRadius: '9999px',
                    background: 'rgba(16, 185, 129, 0.2)',
                    color: '#34D399',
                    border: '1px solid rgba(16, 185, 129, 0.4)',
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '4px',
                  }}
                >
                  <Sun size={11} /> Screen Awake
                </span>
              )}
            </div>
          </div>
        </div>

        {/* Top Control Buttons */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          {/* Toggle Voice Navigation */}
          <button
            onClick={toggleVoiceNavigation}
            style={{
              padding: '0.45rem 0.75rem',
              borderRadius: '8px',
              background: isVoiceActive ? 'rgba(239, 68, 68, 0.2)' : 'rgba(255, 255, 255, 0.08)',
              border: isVoiceActive ? '1px solid #EF4444' : '1px solid rgba(255, 255, 255, 0.15)',
              color: isVoiceActive ? '#FCA5A5' : '#FFFFFF',
              fontSize: '0.78rem',
              fontWeight: 700,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
            }}
            title="Voice Navigation (Next, Back, Timer)"
          >
            {isVoiceActive ? <Mic size={15} color="#EF4444" className="animate-pulse" /> : <MicOff size={15} />}
            <span>{isVoiceActive ? 'Voice Active' : 'Voice Mode'}</span>
          </button>

          {/* Toggle Ingredients Drawer */}
          <button
            onClick={() => setShowIngredientList((prev) => !prev)}
            style={{
              padding: '0.45rem 0.75rem',
              borderRadius: '8px',
              background: showIngredientList ? 'rgba(16, 185, 129, 0.2)' : 'rgba(255, 255, 255, 0.08)',
              border: showIngredientList ? '1px solid #10B981' : '1px solid rgba(255, 255, 255, 0.15)',
              color: showIngredientList ? '#34D399' : '#FFFFFF',
              fontSize: '0.78rem',
              fontWeight: 700,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
            }}
          >
            <ListFilter size={15} />
            <span>Ingredients ({ingredients.length})</span>
          </button>

          {/* Toggle Fullscreen */}
          <button
            onClick={toggleFullscreenMode}
            style={{
              padding: '0.45rem',
              borderRadius: '8px',
              background: 'rgba(255, 255, 255, 0.08)',
              border: '1px solid rgba(255, 255, 255, 0.15)',
              color: '#FFFFFF',
              cursor: 'pointer',
            }}
            title="Toggle Fullscreen Mode"
          >
            {isFullscreen ? <Minimize2 size={16} /> : <Maximize2 size={16} />}
          </button>

          {/* Close Cooking Mode */}
          <button
            onClick={onClose}
            style={{
              padding: '0.45rem',
              borderRadius: '8px',
              background: 'rgba(255, 255, 255, 0.08)',
              border: '1px solid rgba(255, 255, 255, 0.15)',
              color: '#FFFFFF',
              cursor: 'pointer',
            }}
            title="Exit Cooking Mode (Esc)"
          >
            <X size={18} />
          </button>
        </div>
      </header>

      {/* Progress Bar Track */}
      <div style={{ width: '100%', height: '4px', background: 'rgba(255, 255, 255, 0.08)' }}>
        <div
          style={{
            height: '100%',
            width: `${progressPercent}%`,
            background: 'linear-gradient(90deg, #10B981 0%, #3B82F6 100%)',
            transition: 'width 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            boxShadow: '0 0 10px rgba(16, 185, 129, 0.6)',
          }}
        />
      </div>

      {/* Main Active Step Canvas */}
      <div
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '2rem 1.5rem',
          maxWidth: '900px',
          margin: '0 auto',
          width: '100%',
          position: 'relative',
          overflowY: 'auto',
        }}
      >
        {/* Step Badge */}
        <div
          style={{
            padding: '0.4rem 1rem',
            borderRadius: '9999px',
            background: 'rgba(16, 185, 129, 0.15)',
            border: '1px solid rgba(16, 185, 129, 0.3)',
            color: '#34D399',
            fontSize: '0.85rem',
            fontWeight: 800,
            marginBottom: '1.5rem',
            letterSpacing: '0.05em',
            textTransform: 'uppercase',
          }}
        >
          Step {currentStepIndex + 1}
        </div>

        {/* Large High-Contrast Instruction Display */}
        <div
          style={{
            fontSize: '1.85rem',
            fontWeight: 700,
            lineHeight: 1.45,
            textAlign: 'center',
            color: '#FFFFFF',
            marginBottom: '2rem',
            letterSpacing: '-0.02em',
            textShadow: '0 2px 10px rgba(0,0,0,0.5)',
          }}
        >
          {currentStepText}
        </div>

        {/* Interactive Step Timer Component */}
        {activeDurationSeconds > 0 && (
          <div
            style={{
              padding: '1.25rem 2rem',
              borderRadius: '16px',
              background: 'rgba(15, 23, 42, 0.9)',
              border: '1px solid rgba(56, 189, 248, 0.3)',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: '0.75rem',
              boxShadow: '0 8px 32px rgba(0, 0, 0, 0.4)',
              marginBottom: '1.5rem',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#38BDF8' }}>
              <Clock size={20} />
              <span style={{ fontSize: '0.88rem', fontWeight: 700 }}>Step Timer Detected</span>
            </div>

            <div
              className="tabular-num"
              style={{
                fontSize: '2.5rem',
                fontWeight: 900,
                color: isTimerRunning ? '#34D399' : '#FFFFFF',
                letterSpacing: '0.05em',
              }}
            >
              {Math.floor(remainingSeconds / 60)}:{(remainingSeconds % 60).toString().padStart(2, '0')}
            </div>

            <div style={{ display: 'flex', gap: '0.75rem' }}>
              {!isTimerRunning ? (
                <button
                  onClick={startTimer}
                  style={{
                    padding: '0.5rem 1.25rem',
                    borderRadius: '8px',
                    background: '#10B981',
                    color: '#FFFFFF',
                    border: 'none',
                    fontWeight: 700,
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px',
                  }}
                >
                  <Play size={16} /> Start Timer
                </button>
              ) : (
                <button
                  onClick={pauseTimer}
                  style={{
                    padding: '0.5rem 1.25rem',
                    borderRadius: '8px',
                    background: '#F59E0B',
                    color: '#FFFFFF',
                    border: 'none',
                    fontWeight: 700,
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px',
                  }}
                >
                  <Pause size={16} /> Pause
                </button>
              )}

              <button
                onClick={resetTimer}
                style={{
                  padding: '0.5rem 0.85rem',
                  borderRadius: '8px',
                  background: 'rgba(255, 255, 255, 0.1)',
                  color: '#FFFFFF',
                  border: '1px solid rgba(255, 255, 255, 0.2)',
                  fontWeight: 600,
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px',
                }}
              >
                <RotateCcw size={14} /> Reset
              </button>
            </div>
          </div>
        )}

        {/* Voice Command Feedback Indicator */}
        {isVoiceActive && voiceTranscript && (
          <div
            style={{
              fontSize: '0.8rem',
              color: '#94A3B8',
              background: 'rgba(0, 0, 0, 0.4)',
              padding: '0.35rem 0.85rem',
              borderRadius: '9999px',
              border: '1px solid rgba(255, 255, 255, 0.1)',
            }}
          >
            🎙️ Voice Heard: <span style={{ color: '#38BDF8', fontWeight: 600 }}>"{voiceTranscript}"</span>
          </div>
        )}
      </div>

      {/* Side Slide-Over Ingredients List Drawer */}
      {showIngredientList && (
        <div
          style={{
            position: 'absolute',
            top: '72px',
            right: 0,
            bottom: '90px',
            width: '320px',
            background: 'rgba(15, 23, 42, 0.98)',
            borderLeft: '1px solid rgba(255, 255, 255, 0.15)',
            padding: '1.25rem',
            overflowY: 'auto',
            zIndex: 10,
            backdropFilter: 'blur(16px)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
            <h3 style={{ fontSize: '1rem', fontWeight: 800, margin: 0, color: '#34D399', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <ChefHat size={18} /> Ingredients List
            </h3>
            <button
              onClick={() => setShowIngredientList(false)}
              style={{ background: 'none', border: 'none', color: '#94A3B8', cursor: 'pointer' }}
            >
              <X size={16} />
            </button>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.55rem' }}>
            {ingredients.map((ing: any, idx: number) => {
              const ingId = `ing-${idx}`;
              const isChecked = checkedIngredientIds.includes(ingId);
              const name = typeof ing === 'object' ? ing.name || ing.item : String(ing);
              const qty = typeof ing === 'object' ? ing.quantity || ing.amount : '';

              return (
                <div
                  key={idx}
                  onClick={() => toggleIngredientCheck(ingId)}
                  style={{
                    padding: '0.6rem 0.75rem',
                    borderRadius: '8px',
                    background: isChecked ? 'rgba(16, 185, 129, 0.12)' : 'rgba(255, 255, 255, 0.04)',
                    border: isChecked ? '1px solid rgba(16, 185, 129, 0.3)' : '1px solid rgba(255, 255, 255, 0.08)',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.65rem',
                    textDecoration: isChecked ? 'line-through' : 'none',
                    opacity: isChecked ? 0.6 : 1,
                  }}
                >
                  <div
                    style={{
                      width: '18px',
                      height: '18px',
                      borderRadius: '4px',
                      border: isChecked ? 'none' : '2px solid #64748B',
                      background: isChecked ? '#10B981' : 'transparent',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                    }}
                  >
                    {isChecked && <CheckCircle2 size={14} color="#FFFFFF" />}
                  </div>
                  <span style={{ fontSize: '0.85rem', color: '#FFFFFF', flex: 1 }}>{name}</span>
                  {qty && <span style={{ fontSize: '0.75rem', color: '#94A3B8', fontWeight: 600 }}>{qty}</span>}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Bottom Sticky Navigation Dock */}
      <footer
        style={{
          padding: '1rem 1.5rem',
          borderTop: '1px solid rgba(255, 255, 255, 0.1)',
          background: 'rgba(15, 23, 42, 0.9)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '1rem',
        }}
      >
        <button
          onClick={handlePrevStep}
          disabled={currentStepIndex === 0}
          style={{
            padding: '0.75rem 1.5rem',
            borderRadius: '12px',
            background: currentStepIndex === 0 ? 'rgba(255, 255, 255, 0.05)' : 'rgba(255, 255, 255, 0.12)',
            color: currentStepIndex === 0 ? '#475569' : '#FFFFFF',
            border: '1px solid rgba(255, 255, 255, 0.15)',
            fontSize: '0.95rem',
            fontWeight: 700,
            cursor: currentStepIndex === 0 ? 'not-allowed' : 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
          }}
        >
          <ChevronLeft size={20} /> Previous
        </button>

        <span style={{ fontSize: '0.82rem', color: '#94A3B8', fontWeight: 600 }}>
          Swipe or press <kbd style={{ background: 'rgba(255,255,255,0.1)', padding: '2px 6px', borderRadius: '4px' }}>→</kbd> for next step
        </span>

        <button
          onClick={handleNextStep}
          disabled={currentStepIndex >= totalSteps - 1}
          style={{
            padding: '0.75rem 1.5rem',
            borderRadius: '12px',
            background: currentStepIndex >= totalSteps - 1 ? 'rgba(255, 255, 255, 0.05)' : 'linear-gradient(135deg, #10B981, #059669)',
            color: currentStepIndex >= totalSteps - 1 ? '#475569' : '#FFFFFF',
            border: 'none',
            fontSize: '0.95rem',
            fontWeight: 700,
            cursor: currentStepIndex >= totalSteps - 1 ? 'not-allowed' : 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            boxShadow: currentStepIndex >= totalSteps - 1 ? 'none' : '0 4px 16px rgba(16, 185, 129, 0.4)',
          }}
        >
          Next <ChevronRight size={20} />
        </button>
      </footer>
    </div>
  );
}
