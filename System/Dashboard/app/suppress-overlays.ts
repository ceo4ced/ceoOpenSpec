// Disable Next.js error overlay in development
if (typeof window !== 'undefined' && process.env.NODE_ENV === 'development') {
    // Hide the error overlay indicator
    const style = document.createElement('style');
    style.innerHTML = `
        nextjs-portal { display: none !important; }
        #nextjs__container_errors_label { display: none !important; }
        #nextjs__container_build_error_label { display: none !important; }
        #nextjs__container_errors { display: none !important; }
        [data-nextjs-toast] { display: none !important; }
        [data-nextjs-dialog-overlay] { display: none !important; }
    `;
    document.head.appendChild(style);

    // Override console.error to suppress hydration warnings
    const originalError = console.error;
    console.error = function (...args) {
        if (
            args[0]?.includes?.('Hydration') ||
            args[0]?.includes?.('hydration') ||
            args[0]?.includes?.('did not match')
        ) {
            return; // Suppress hydration errors
        }
        originalError.apply(console, args);
    };
}

export { };
