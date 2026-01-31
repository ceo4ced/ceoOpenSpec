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


            </div>
        </div>
    );
}
