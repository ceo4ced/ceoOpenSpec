'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';

import ExperienceLauncher from '../../components/ExperienceLauncher';
import TestRunner from '../../components/TestRunner';
import FactoryManager from '../../components/FactoryManager';
import styles from './page.module.css';

export default function DevDashboard() {
    const router = useRouter();
    const [testResults, setTestResults] = useState<any>(null);

    return (
        <div className={styles['dev-container']}>
            <div className={styles['dev-grid']}>
                {/* Factory Replication System */}
                <FactoryManager />

                {/* Experience Launcher Section */}
                <section className={styles['dev-section']}>
                    <h2 className={styles['section-title']}>Experience Launcher</h2>
                    <p className={styles['section-description']}>
                        Initialize user scenarios and select boot mode for testing.
                    </p>
                    <ExperienceLauncher />
                </section>

                {/* Test Runner Section */}
                <section className={styles['dev-section']}>
                    <h2 className={styles['section-title']}>System Diagnostics</h2>
                    <p className={styles['section-description']}>
                        Execute unit test protocols and analyze system coverage.
                    </p>
                    <TestRunner onResultsChange={setTestResults} />
                </section>


            </div>
        </div>
    );
}
