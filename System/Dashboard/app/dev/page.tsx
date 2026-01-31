'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import ExperienceLauncher from '../../components/ExperienceLauncher';
import TestRunner from '../../components/TestRunner';
import styles from './page.module.css';

export default function DevDashboard() {
    const router = useRouter();
    const [testResults, setTestResults] = useState<any>(null);

    return (
        <div className={styles['dev-container']}>
            <div className={styles['dev-grid']}>
                {/* Experience Launcher Section */}
                <section className={styles['dev-section']}>
                    <h2 className={styles['section-title']}>&gt;&gt; EXPERIENCE_LAUNCHER</h2>
                    <p className={styles['section-description']}>
                        [SYSTEM]: Initialize user scenarios. Select boot mode.
                    </p>
                    <ExperienceLauncher />
                </section>

                {/* Test Runner Section */}
                <section className={styles['dev-section']}>
                    <h2 className={styles['section-title']}>&gt;&gt; SYSTEM_DIAGNOSTICS</h2>
                    <p className={styles['section-description']}>
                        [SYSTEM]: Execute unit test protocols. Analyze coverage.
                    </p>
                    <TestRunner onResultsChange={setTestResults} />
                </section>

                {/* Quick Links Section */}
                <section className={`${styles['dev-section']} ${styles['full-width']}`}>
                    <h2 className={styles['section-title']}>&gt;&gt; FAST_TRAVEL_PROTOCOLS</h2>
                    <div className={styles['quick-links-grid']}>
                        <a href="/onboarding" className={styles['quick-link']}>
                            <span className={styles['link-icon']}>🎯</span>
                            <span className={styles['link-text']}>Onboarding</span>
                        </a>
                        <a href="/chairman" className={styles['quick-link']}>
                            <span className={styles['link-icon']}>👑</span>
                            <span className={styles['link-text']}>Chairman</span>
                        </a>
                        <a href="/ceo" className={styles['quick-link']}>
                            <span className={styles['link-icon']}>🎯</span>
                            <span className={styles['link-text']}>CEO</span>
                        </a>
                        <a href="/cfo" className={styles['quick-link']}>
                            <span className={styles['link-icon']}>💰</span>
                            <span className={styles['link-text']}>CFO</span>
                        </a>
                        <a href="/cmo" className={styles['quick-link']}>
                            <span className={styles['link-icon']}>📣</span>
                            <span className={styles['link-text']}>CMO</span>
                        </a>
                        <a href="/coo" className={styles['quick-link']}>
                            <span className={styles['link-icon']}>⚙️</span>
                            <span className={styles['link-text']}>COO</span>
                        </a>
                        <a href="/cio" className={styles['quick-link']}>
                            <span className={styles['link-icon']}>🔐</span>
                            <span className={styles['link-text']}>CIO</span>
                        </a>
                        <a href="/clo" className={styles['quick-link']}>
                            <span className={styles['link-icon']}>⚖️</span>
                            <span className={styles['link-text']}>CLO</span>
                        </a>
                        <a href="/cpo" className={styles['quick-link']}>
                            <span className={styles['link-icon']}>📦</span>
                            <span className={styles['link-text']}>CPO</span>
                        </a>
                        <a href="/cto" className={styles['quick-link']}>
                            <span className={styles['link-icon']}>💻</span>
                            <span className={styles['link-text']}>CTO</span>
                        </a>
                        <a href="/cxa" className={styles['quick-link']}>
                            <span className={styles['link-icon']}>📋</span>
                            <span className={styles['link-text']}>CXA</span>
                        </a>
                        <a href="/agents" className={styles['quick-link']}>
                            <span className={styles['link-icon']}>👥</span>
                            <span className={styles['link-text']}>Agents</span>
                        </a>
                        <a href="/approvals" className={styles['quick-link']}>
                            <span className={styles['link-icon']}>✅</span>
                            <span className={styles['link-text']}>Approvals</span>
                        </a>
                        <a href="/finance" className={styles['quick-link']}>
                            <span className={styles['link-icon']}>💵</span>
                            <span className={styles['link-text']}>Finance</span>
                        </a>
                    </div>
                </section>
            </div>
        </div>
    );
}
