'use client';

import { useEffect } from 'react';

export default function OverlaySuppressor() {
    useEffect(() => {
        if (process.env.NODE_ENV === 'development') {
            // Hide Next.js error overlay and all indicators
            const style = document.createElement('style');
            style.id = 'overlay-suppressor';
            style.innerHTML = `
                nextjs-portal,
                nextjs-portal * { display: none !important; }
                #nextjs__container_errors_label,
                #nextjs__container_build_error_label,
                #nextjs__container_errors,
                #__next-build-watcher,
                #__next-build-watcher *,
                [data-nextjs-toast],
                [data-nextjs-dialog-overlay],
                [data-nextjs-scroll-lock],
                [id*="nextjs"],
                [class*="nextjs"],
                [data-nextjs-root-layout-error-boundary] { 
                    display: none !important;
                    opacity: 0 !important;
                    pointer-events: none !important;
                    visibility: hidden !important;
                }
            `;
            document.head.appendChild(style);

            // Also hide via DOM manipulation
            const interval = setInterval(() => {
                const indicators = document.querySelectorAll('[id*="nextjs"], nextjs-portal, #__next-build-watcher');
                indicators.forEach(el => {
                    if (el && el.parentNode) {
                        el.parentNode.removeChild(el);
                    }
                });
            }, 500);

            // Suppress hydration warnings
            const originalError = console.error;
            console.error = function (...args) {
                const msg = args[0]?.toString() || '';
                if (
                    msg.includes('Hydration') ||
                    msg.includes('hydration') ||
                    msg.includes('did not match') ||
                    msg.includes('server rendered HTML')
                ) {
                    return;
                }
                originalError.apply(console, args);
            };

            return () => clearInterval(interval);
        }
    }, []);

    return null;
}
