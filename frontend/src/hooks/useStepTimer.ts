import { useState, useEffect, useCallback, useRef } from 'react';

/**
 * Mobile Timer Delta Math & Web Audio Pre-Unlock (SAFE-1103)
 * =========================================================
 * Calculates remaining step duration using target epoch timestamp deltas
 * (targetEndTime - Date.now()) to prevent background tab throttling drift.
 * Pre-unlocks Web Audio API AudioContext on user interaction and triggers
 * completion chime + navigator.vibrate().
 */

export interface UseStepTimerOptions {
  durationSeconds: number;
  onComplete?: () => void;
}

export interface UseStepTimerReturn {
  remainingSeconds: number;
  isRunning: boolean;
  isCompleted: boolean;
  progressPercent: number;
  start: () => void;
  pause: () => void;
  reset: () => void;
  unlockAudio: () => void;
}

export function useStepTimer({ durationSeconds, onComplete }: UseStepTimerOptions): UseStepTimerReturn {
  const [remainingSeconds, setRemainingSeconds] = useState<number>(durationSeconds);
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [isCompleted, setIsCompleted] = useState<boolean>(false);

  const targetEndTimeRef = useRef<number | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const timerIntervalRef = useRef<any>(null);

  // Pre-unlock Web Audio API on initial user interaction (taps/clicks)
  const unlockAudio = useCallback(() => {
    if (typeof window === 'undefined') return;
    try {
      if (!audioContextRef.current) {
        const AudioCtx = window.AudioContext || (window as any).webkitAudioContext;
        if (AudioCtx) {
          audioContextRef.current = new AudioCtx();
        }
      }
      if (audioContextRef.current && audioContextRef.current.state === 'suspended') {
        audioContextRef.current.resume();
      }
    } catch (e) {
      // Graceful fallback for webviews without AudioContext support
    }
  }, []);

  const playCompletionChime = useCallback(() => {
    try {
      if (audioContextRef.current) {
        const ctx = audioContextRef.current;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(880, ctx.currentTime); // A5 tone
        gain.gain.setValueAtTime(0.1, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.5);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.5);
      }
    } catch (e) {
      // Audio playback fallback
    }

    if (typeof navigator !== 'undefined' && 'vibrate' in navigator) {
      try {
        navigator.vibrate([200, 100, 200]);
      } catch (e) {}
    }
  }, []);

  const start = useCallback(() => {
    unlockAudio();
    if (isCompleted) {
      setRemainingSeconds(durationSeconds);
      setIsCompleted(false);
    }
    targetEndTimeRef.current = Date.now() + remainingSeconds * 1000;
    setIsRunning(true);
  }, [durationSeconds, isCompleted, remainingSeconds, unlockAudio]);

  const pause = useCallback(() => {
    setIsRunning(false);
    if (targetEndTimeRef.current) {
      const remaining = Math.max(0, Math.ceil((targetEndTimeRef.current - Date.now()) / 1000));
      setRemainingSeconds(remaining);
      targetEndTimeRef.current = null;
    }
  }, []);

  const reset = useCallback(() => {
    setIsRunning(false);
    setIsCompleted(false);
    setRemainingSeconds(durationSeconds);
    targetEndTimeRef.current = null;
  }, [durationSeconds]);

  useEffect(() => {
    if (!isRunning) {
      if (timerIntervalRef.current) clearInterval(timerIntervalRef.current);
      return;
    }

    timerIntervalRef.current = setInterval(() => {
      if (!targetEndTimeRef.current) return;
      const now = Date.now();
      const diff = Math.ceil((targetEndTimeRef.current - now) / 1000);

      if (diff <= 0) {
        setRemainingSeconds(0);
        setIsRunning(false);
        setIsCompleted(true);
        clearInterval(timerIntervalRef.current);
        playCompletionChime();
        if (onComplete) onComplete();
      } else {
        setRemainingSeconds(diff);
      }
    }, 250);

    return () => {
      if (timerIntervalRef.current) clearInterval(timerIntervalRef.current);
    };
  }, [isRunning, onComplete, playCompletionChime]);

  const progressPercent = Math.min(100, Math.max(0, ((durationSeconds - remainingSeconds) / durationSeconds) * 100));

  return { remainingSeconds, isRunning, isCompleted, progressPercent, start, pause, reset, unlockAudio };
}
