
'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { SYSTEM_STATUS } from '@/lib/data';

export default function Sidebar() {
    const pathname = usePathname();
    const status = SYSTEM_STATUS;

    // Check if path starts with /<role>
    const isActive = (role: string) => {
        if (role === 'chairman') {
            return pathname === '/' || pathname === '/chairman' ? 'active' : '';
        }
        return pathname === `/${role}` ? 'active' : '';
    };

    return (
        <nav className="sidebar">
            <div className="sidebar-header">
                <div className="logo">
                    <div className="logo-icon">🍌</div>
                    <div className="logo-text">C-Suite</div>
                </div>
            </div>

            <div className="nav-section">
                <div className="nav-section-title">NAVIGATION</div>
                <a href="#" className="nav-item">
                    <span className="nav-icon">👥</span>
                    <span>Agent Profiles</span>
                </a>
                <Link href="/corporate" className={`nav-item ${isActive('corporate')}`}>
                    <span className="nav-icon">🏢</span>
                    <span>Corporate</span>
                </Link>
            </div>

            <div className="nav-section">
                <div className="nav-section-title">COMMAND CENTER</div>
                <Link href="/" className={`nav-item ${isActive('chairman')}`}>
                    <span className="nav-icon">👑</span>
                    <span>Chairman</span>
                </Link>
            </div>

            <div className="nav-section">
                <div className="nav-section-title">C-SUITE</div>
                <Link href="/ceo" className={`nav-item ${isActive('ceo')}`}>
                    <span className="nav-icon">🎯</span>
                    <span>CEO</span>
                </Link>
                <Link href="/cfo" className={`nav-item ${isActive('cfo')}`}>
                    <span className="nav-icon">💰</span>
                    <span>CFO</span>
                </Link>
                <Link href="/cmo" className={`nav-item ${isActive('cmo')}`}>
                    <span className="nav-icon">📣</span>
                    <span>CMO</span>
                </Link>
                <Link href="/coo" className={`nav-item ${isActive('coo')}`}>
                    <span className="nav-icon">⚙️</span>
                    <span>COO</span>
                </Link>
                <Link href="/cio" className={`nav-item ${isActive('cio')}`}>
                    <span className="nav-icon">🔐</span>
                    <span>CIO</span>
                </Link>
                <Link href="/clo" className={`nav-item ${isActive('clo')}`}>
                    <span className="nav-icon">⚖️</span>
                    <span>CLO</span>
                </Link>
                <Link href="/cpo" className={`nav-item ${isActive('cpo')}`}>
                    <span className="nav-icon">📦</span>
                    <span>CPO</span>
                </Link>
                <Link href="/cto" className={`nav-item ${isActive('cto')}`}>
                    <span className="nav-icon">💻</span>
                    <span>CTO</span>
                </Link>
                <Link href="/cxa" className={`nav-item ${isActive('cxa')}`}>
                    <span className="nav-icon">📋</span>
                    <span>CXA</span>
                </Link>
            </div>

            <div className="sidebar-footer">
                <Link href="/logs" className="system-status" style={{ cursor: 'pointer', textDecoration: 'none' }}>
                    <span className="status-dot" style={{ backgroundColor: status.color }}></span>
                    <div>
                        <span>{status.statusText}</span>
                        {status.issueCount > 0 && (
                            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                                {status.issueCount} issue{status.issueCount > 1 ? 's' : ''}
                            </div>
                        )}
                    </div>
                </Link>
                {process.env.NODE_ENV === 'development' && (
                    <Link href="/dev" className="dev-link">
                        <span className="nav-icon">⚙️</span>
                        <span>Dev Dashboard</span>
                    </Link>
                )}
            </div>
        </nav>
    );
}
