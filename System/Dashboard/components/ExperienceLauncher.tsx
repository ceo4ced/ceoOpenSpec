'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import './ExperienceLauncher.css';

export default function ExperienceLauncher() {
    const router = useRouter();

    const handleLaunchWithOnboarding = () => {
        // Open onboarding in a new window
        if (typeof window !== 'undefined') {
            window.open('/onboarding', '_blank');
        }
    };

    const handleLaunchWithoutOnboarding = () => {
        // Open chairman dashboard in a new window
        if (typeof window !== 'undefined') {
            window.open('/chairman', '_blank');
        }
    };

    const handleClearSession = () => {
        if (typeof window !== 'undefined') {
            sessionStorage.clear();
            localStorage.clear();
            alert('Session and local storage cleared successfully!');
        }
    };

    return (
        <div className="experience-launcher">
            <div className="launcher-actions">
                <button
                    className="launch-btn primary"
                    onClick={handleLaunchWithOnboarding}
                >
                    <span className="btn-icon">🚀</span>
                    <div className="btn-content">
                        <div className="btn-title">Launch with Onboarding</div>
                        <div className="btn-description">Start from the beginning</div>
                    </div>
                </button>

                <button
                    className="launch-btn secondary"
                    onClick={handleLaunchWithoutOnboarding}
                >
                    <span className="btn-icon">⚡</span>
                    <div className="btn-content">
                        <div className="btn-title">Skip to Dashboard</div>
                        <div className="btn-description">Bypass onboarding flow</div>
                    </div>
                </button>

                <button
                    className="launch-btn danger"
                    onClick={handleClearSession}
                >
                    <span className="btn-icon">🗑️</span>
                    <div className="btn-content">
                        <div className="btn-title">Clear Session</div>
                        <div className="btn-description">Reset all stored data</div>
                    </div>
                </button>
            </div>

            <div className="launcher-info">
                <div className="info-item">
                    <span className="info-label">Onboarding Flow:</span>
                    <span className="info-value">Opens /onboarding in new window</span>
                </div>
                <div className="info-item">
                    <span className="info-label">Dashboard Bypass:</span>
                    <span className="info-value">Opens /chairman in new window</span>
                </div>
            </div>
        </div>
    );
}
