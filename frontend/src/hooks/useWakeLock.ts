import { useState, useEffect, useCallback, useRef } from 'react';

/**
 * Screen Wake-Lock Defensive Hook & Auto-Reacquire (SAFE-1102)
 * ==========================================================
 * Manages navigator.wakeLock.request('screen') safely across mobile webviews,
 * low-power modes, and iOS WKWebView. Auto-reacquires lock upon document
 * visibility restoration.
 */

export interface UseWakeLockReturn {
  isSupported: boolean;
  isLocked: boolean;
  request: () => Promise<boolean>;
  release: () => Promise<boolean>;
}

export function useWakeLock(): UseWakeLockReturn {
  const [isSupported, setIsSupported] = useState<boolean>(false);
  const [isLocked, setIsLocked] = useState<boolean>(false);
  const wakeLockSentinelRef = useRef<any>(null);

  useEffect(() => {
    setIsSupported(typeof navigator !== 'undefined' && 'wakeLock' in navigator);
  }, []);

  const request = useCallback(async (): Promise<boolean> => {
    if (typeof navigator === 'undefined' || !('wakeLock' in navigator)) {
      return false;
    }
    try {
      const sentinel = await (navigator as any).wakeLock.request('screen');
      wakeLockSentinelRef.current = sentinel;
      setIsLocked(true);

      sentinel.addEventListener('release', () => {
        setIsLocked(false);
        wakeLockSentinelRef.current = null;
      });
      return true;
    } catch (err: any) {
      // Gracefully catches NotAllowedError, low-power mode blocks, or webview restrictions
      setIsLocked(false);
      return false;
    }
  }, []);

  const release = useCallback(async (): Promise<boolean> => {
    if (wakeLockSentinelRef.current) {
      try {
        await wakeLockSentinelRef.current.release();
        wakeLockSentinelRef.current = null;
        setIsLocked(false);
        return true;
      } catch (err) {
        return false;
      }
    }
    return false;
  }, []);

  useEffect(() => {
    const handleVisibilityChange = async () => {
      if (document.visibilityState === 'visible' && isLocked) {
        await request();
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
      if (wakeLockSentinelRef.current) {
        wakeLockSentinelRef.current.release().catch(() => {});
      }
    };
  }, [isLocked, request]);

  return { isSupported, isLocked, request, release };
}
