import React, { useEffect, useRef } from 'react';
import { X } from 'lucide-react';

interface OverflowBottomSheetProps {
  isOpen: boolean;
  onClose: () => void;
  triggerRef?: React.RefObject<HTMLButtonElement | null>;
  children: React.ReactNode;
  title?: string;
}

export default function OverflowBottomSheet({
  isOpen,
  onClose,
  triggerRef,
  children,
  title = 'More Options'
}: OverflowBottomSheetProps) {
  const sheetRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isOpen) return;

    // 1. Save last active element to restore focus on close
    const previousFocusedElement = document.activeElement as HTMLElement;

    // 2. Focus first interactive element inside sheet
    const focusableElements = sheetRef.current?.querySelectorAll<HTMLElement>(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    if (focusableElements && focusableElements.length > 0) {
      focusableElements[0].focus();
    }

    // 3. Escape key listener to close sheet
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        e.preventDefault();
        onClose();
        return;
      }

      // 4. Focus Trap (Tab & Shift+Tab)
      if (e.key === 'Tab' && focusableElements && focusableElements.length > 0) {
        const first = focusableElements[0];
        const last = focusableElements[focusableElements.length - 1];

        if (e.shiftKey) {
          if (document.activeElement === first) {
            e.preventDefault();
            last.focus();
          }
        } else {
          if (document.activeElement === last) {
            e.preventDefault();
            first.focus();
          }
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);

    const targetTrigger = triggerRef?.current;

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      // Restore focus
      if (targetTrigger) {
        targetTrigger.focus();
      } else if (previousFocusedElement) {
        previousFocusedElement.focus();
      }
    };
  }, [isOpen, onClose, triggerRef]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-0 sm:p-4 bg-black/60 backdrop-blur-sm transition-opacity">
      <div
        ref={sheetRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="bottom-sheet-title"
        className="w-full sm:max-w-lg bg-[var(--bg-surface-solid)] border border-[var(--border-subtle)] rounded-t-2xl sm:rounded-2xl p-6 shadow-2xl animate-in slide-in-from-bottom duration-200"
      >
        <div className="flex items-center justify-between pb-4 mb-4 border-b border-[var(--border-subtle)]">
          <h3 id="bottom-sheet-title" className="text-lg font-bold text-[var(--text-primary)]">
            {title}
          </h3>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close options menu"
            className="p-2 rounded-full text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-subtle)] transition-colors min-h-[44px] min-w-[44px] flex items-center justify-center"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="space-y-3">
          {children}
        </div>
      </div>
    </div>
  );
}
