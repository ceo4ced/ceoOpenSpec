export default function DevLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="dev-layout">
            <div className="dev-header">
                <div className="dev-logo">
                    <span className="dev-icon">⚙️</span>
                    <span className="dev-title">Developer Dashboard</span>
                </div>
                <a href="/chairman" className="back-to-app">
                    ← Back to Main App
                </a>
            </div>
            {children}
        </div>
    );
}
