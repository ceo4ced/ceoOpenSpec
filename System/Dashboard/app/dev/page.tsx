'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import ExperienceLauncher from '../../components/ExperienceLauncher';
import TestRunner from '../../components/TestRunner';
import './page.module.css';

export default function DevDashboard() {
    const router = useRouter();
    const [testResults, setTestResults] = useState<any>(null);

    return (
        <div className="dev-container">
            <div className="dev-grid">
                {/* Experience Launcher Section */}
                <section className="dev-section">
                    <h2 className="section-title">Experience Launcher</h2>
                    <p className="section-description">
                        Launch new user experiences with or without the onboarding flow
                    </p>
                    <ExperienceLauncher />
                </section>

                {/* Test Runner Section */}
                <section className="dev-section">
                    <h2 className="section-title">Test Runner</h2>
                    <p className="section-description">
                        Execute tests and view coverage metrics
                    </p>
                    <TestRunner onResultsChange={setTestResults} />
                </section>

                {/* Quick Links Section */}
                <section className="dev-section full-width">
                    <h2 className="section-title">Quick Navigation</h2>
                    <div className="quick-links-grid">
                        <a href="/onboarding" className="quick-link">
                            <span className="link-icon">🎯</span>
                            <span className="link-text">Onboarding</span>
                        </a>
                        <a href="/chairman" className="quick-link">
                            <span className="link-icon">👑</span>
                            <span className="link-text">Chairman</span>
                        </a>
                        <a href="/ceo" className="quick-link">
                            <span className="link-icon">🎯</span>
                            <span className="link-text">CEO</span>
                        </a>
                        <a href="/cfo" className="quick-link">
                            <span className="link-icon">💰</span>
                            <span className="link-text">CFO</span>
                        </a>
                        <a href="/cmo" className="quick-link">
                            <span className="link-icon">📣</span>
                            <span className="link-text">CMO</span>
                        </a>
                        <a href="/coo" className="quick-link">
                            <span className="link-icon">⚙️</span>
                            <span className="link-text">COO</span>
                        </a>
                        <a href="/cio" className="quick-link">
                            <span className="link-icon">🔐</span>
                            <span className="link-text">CIO</span>
                        </a>
                        <a href="/clo" className="quick-link">
                            <span className="link-icon">⚖️</span>
                            <span className="link-text">CLO</span>
                        </a>
                        <a href="/cpo" className="quick-link">
                            <span className="link-icon">📦</span>
                            <span className="link-text">CPO</span>
                        </a>
                        <a href="/cto" className="quick-link">
                            <span className="link-icon">💻</span>
                            <span className="link-text">CTO</span>
                        </a>
                        <a href="/cxa" className="quick-link">
                            <span className="link-icon">📋</span>
                            <span className="link-text">CXA</span>
                        </a>
                        <a href="/agents" className="quick-link">
                            <span className="link-icon">👥</span>
                            <span className="link-text">Agents</span>
                        </a>
                        <a href="/approvals" className="quick-link">
                            <span className="link-icon">✅</span>
                            <span className="link-text">Approvals</span>
                        </a>
                        <a href="/finance" className="quick-link">
                            <span className="link-icon">💵</span>
                            <span className="link-text">Finance</span>
                        </a>
                    </div>
                </section>
            </div>
        </div>
    );
}
