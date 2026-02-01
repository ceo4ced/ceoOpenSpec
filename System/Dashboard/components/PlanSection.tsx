'use client';

import React, { useState, useEffect } from 'react';
import styles from './PlanSection.module.css';

// Role to plan mapping
const ROLE_PLAN_MAPPING: Record<string, { path: string; title: string }> = {
    ceo: { path: 'C-Suites/CEO/README.md', title: 'Business Plan' },
    cfo: { path: 'C-Suites/CFO/README.md', title: 'Financial Plan' },
    cmo: { path: 'C-Suites/CMO/README.md', title: 'Marketing Plan' },
    coo: { path: 'C-Suites/COO/README.md', title: 'Operations Plan' },
    cio: { path: 'C-Suites/CIO/README.md', title: 'Information Plan' },
    clo: { path: 'C-Suites/CLO/README.md', title: 'Legal Plan' },
    cpo: { path: 'C-Suites/CPO/README.md', title: 'Product Plan' },
    cto: { path: 'C-Suites/CTO/README.md', title: 'Technical Plan' },
    cxa: { path: 'C-Suites/CXA/README.md', title: 'Experience Plan' },
};

interface TableOfContentsItem {
    id: string;
    title: string;
    level: number;
}

interface PlanSectionProps {
    role: string;
}

export default function PlanSection({ role }: PlanSectionProps) {
    const [isExpanded, setIsExpanded] = useState(false);
    const [activeSection, setActiveSection] = useState<string | null>(null);
    const [tocItems, setTocItems] = useState<TableOfContentsItem[]>([]);

    const planInfo = ROLE_PLAN_MAPPING[role.toLowerCase()] || {
        path: `C-Suites/${role.toUpperCase()}/README.md`,
        title: `${role.toUpperCase()} Plan`
    };

    // Mock TOC items based on the plan documents we created
    useEffect(() => {
        const mockTocItems = getTocItemsForRole(role);
        setTocItems(mockTocItems);
        if (mockTocItems.length > 0) {
            setActiveSection(mockTocItems[0].id);
        }
    }, [role]);

    const handleSectionClick = (sectionId: string) => {
        setActiveSection(sectionId);
    };

    const toggleExpand = () => {
        setIsExpanded(!isExpanded);
    };

    return (
        <div className={`${styles.planSection} ${isExpanded ? styles.expanded : ''}`}>
            <div className={styles.header}>
                <div className={styles.title}>
                    <span className={styles.icon}>📋</span>
                    <span>{planInfo.title}</span>
                </div>
                <div className={styles.actions}>
                    <button
                        className={styles.actionButton}
                        onClick={toggleExpand}
                        title={isExpanded ? 'Collapse' : 'Expand'}
                    >
                        {isExpanded ? '↙' : '↗'}
                    </button>
                    <button className={styles.actionButton} title="Edit Plan">
                        ✎
                    </button>
                </div>
            </div>

            <div className={styles.body}>
                <div className={styles.toc}>
                    <div className={styles.tocHeader}>Table of Contents</div>
                    <div className={styles.tocList}>
                        {tocItems.map((item) => (
                            <button
                                key={item.id}
                                className={`${styles.tocItem} ${activeSection === item.id ? styles.active : ''}`}
                                style={{ paddingLeft: `${(item.level - 1) * 12 + 8}px` }}
                                onClick={() => handleSectionClick(item.id)}
                            >
                                <span className={styles.tocBullet}>
                                    {activeSection === item.id ? '●' : '○'}
                                </span>
                                <span className={styles.tocText}>{item.title}</span>
                            </button>
                        ))}
                    </div>
                    <div className={styles.tocMeta}>
                        <div className={styles.metaItem}>
                            <span className={styles.metaLabel}>Last Updated:</span>
                            <span className={styles.metaValue}>{new Date().toLocaleDateString()}</span>
                        </div>
                        <div className={styles.metaItem}>
                            <span className={styles.metaLabel}>Review Cycle:</span>
                            <span className={styles.metaValue}>Quarterly</span>
                        </div>
                    </div>
                    <div className={styles.statusIndicators}>
                        <span className={`${styles.statusBadge} ${styles.compliant}`}>● Compliant</span>
                        <span className={`${styles.statusBadge} ${styles.review}`}>○ Review</span>
                    </div>
                </div>

                <div className={styles.content}>
                    <div className={styles.contentHeader}>
                        <h2>{activeSection ? tocItems.find(t => t.id === activeSection)?.title : planInfo.title}</h2>
                    </div>
                    <div className={styles.contentBody}>
                        {renderContentPreview(role, activeSection)}
                    </div>
                    <div className={styles.progressSection}>
                        <div className={styles.progressItem}>
                            <span className={styles.progressLabel}>Complete</span>
                            <div className={styles.progressBar}>
                                <div className={styles.progressFill} style={{ width: '80%' }}></div>
                            </div>
                            <span className={styles.progressValue}>80%</span>
                        </div>
                        <div className={styles.progressItem}>
                            <span className={styles.progressLabel}>In Review</span>
                            <div className={styles.progressBar}>
                                <div className={`${styles.progressFill} ${styles.warning}`} style={{ width: '20%' }}></div>
                            </div>
                            <span className={styles.progressValue}>20%</span>
                        </div>
                    </div>
                </div>
            </div>

            {isExpanded && (
                <div className={styles.expandedOverlay} onClick={toggleExpand}></div>
            )}
        </div>
    );
}

function getTocItemsForRole(role: string): TableOfContentsItem[] {
    const tocByRole: Record<string, TableOfContentsItem[]> = {
        ceo: [
            { id: 'vision', title: '1. Vision Plan', level: 1 },
            { id: 'strategic', title: '2. Strategic Plan', level: 1 },
            { id: 'business-model', title: '3. Business Model', level: 1 },
            { id: 'succession', title: '4. Succession Plan', level: 1 },
            { id: 'stakeholder', title: '5. Stakeholder Plan', level: 1 },
            { id: 'risk', title: '6. Risk Management', level: 1 },
        ],
        cfo: [
            { id: 'budget', title: '1. Budget Plan', level: 1 },
            { id: 'funding', title: '2. Funding Plan', level: 1 },
            { id: 'token-cost', title: '3. Token & Cost Plan', level: 1 },
            { id: 'tax', title: '4. Tax Plan', level: 1 },
            { id: 'audit', title: '5. Audit Plan', level: 1 },
            { id: 'forecast', title: '6. Forecast Plan', level: 1 },
        ],
        cmo: [
            { id: 'brand', title: '1. Brand Plan', level: 1 },
            { id: 'gtm', title: '2. Go-to-Market Plan', level: 1 },
            { id: 'validation', title: '3. Validation Plan', level: 1 },
            { id: 'content', title: '4. Content Plan', level: 1 },
            { id: 'campaign', title: '5. Campaign Plan', level: 1 },
            { id: 'channel', title: '6. Channel Plan', level: 1 },
        ],
        coo: [
            { id: 'workforce', title: '1. Workforce Plan', level: 1 },
            { id: 'process', title: '2. Process Plan', level: 1 },
            { id: 'logistics', title: '3. Logistics Plan', level: 1 },
            { id: 'quality', title: '4. Quality Plan', level: 1 },
            { id: 'contingency', title: '5. Contingency Plan', level: 1 },
            { id: 'facilities', title: '6. Facilities Plan', level: 1 },
        ],
        cio: [
            { id: 'data', title: '1. Data Plan', level: 1 },
            { id: 'security', title: '2. Security Plan', level: 1 },
            { id: 'privacy', title: '3. Privacy Plan', level: 1 },
            { id: 'infrastructure', title: '4. Infrastructure Plan', level: 1 },
            { id: 'redundancy', title: '5. Redundancy Plan', level: 1 },
            { id: 'integration', title: '6. Integration Plan', level: 1 },
        ],
        clo: [
            { id: 'compliance', title: '1. Compliance Plan', level: 1 },
            { id: 'ip', title: '2. IP Plan', level: 1 },
            { id: 'contract', title: '3. Contract Plan', level: 1 },
            { id: 'risk', title: '4. Risk Plan', level: 1 },
            { id: 'jurisdiction', title: '5. Jurisdiction Plan', level: 1 },
            { id: 'litigation', title: '6. Litigation Plan', level: 1 },
        ],
        cpo: [
            { id: 'strategy', title: '1. Product Strategy', level: 1 },
            { id: 'roadmap', title: '2. Roadmap Plan', level: 1 },
            { id: 'mvp', title: '3. MVP Plan', level: 1 },
            { id: 'metrics', title: '4. Metrics Plan', level: 1 },
            { id: 'research', title: '5. Research Plan', level: 1 },
            { id: 'deprecation', title: '6. Deprecation Plan', level: 1 },
        ],
        cto: [
            { id: 'tech-strategy', title: '1. Technical Strategy', level: 1 },
            { id: 'implementation', title: '2. Implementation Plan', level: 1 },
            { id: 'devops', title: '3. DevOps Plan', level: 1 },
            { id: 'scaling', title: '4. Scaling Plan', level: 1 },
            { id: 'tech-debt', title: '5. Tech Debt Plan', level: 1 },
            { id: 'security-impl', title: '6. Security Implementation', level: 1 },
        ],
        cxa: [
            { id: 'communication', title: '1. Communication Plan', level: 1 },
            { id: 'engagement', title: '2. Engagement Plan', level: 1 },
            { id: 'support', title: '3. Support Plan', level: 1 },
            { id: 'onboarding', title: '4. Onboarding Plan', level: 1 },
            { id: 'feedback', title: '5. Feedback Plan', level: 1 },
            { id: 'crisis', title: '6. Crisis Communication', level: 1 },
        ],
    };

    return tocByRole[role.toLowerCase()] || [];
}

function renderContentPreview(role: string, sectionId: string | null): React.ReactNode {
    // Return a placeholder content preview
    if (!sectionId) {
        return <p className={styles.placeholder}>Select a section to view content.</p>;
    }

    return (
        <div className={styles.previewContent}>
            <p className={styles.previewText}>
                This section contains the detailed plan for the selected area.
                Content is loaded from the respective plan document.
            </p>
            <div className={styles.previewTable}>
                <table>
                    <thead>
                        <tr>
                            <th>Item</th>
                            <th>Status</th>
                            <th>Owner</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Section content</td>
                            <td><span className={styles.statusComplete}>Complete</span></td>
                            <td>{role.toUpperCase()}</td>
                        </tr>
                        <tr>
                            <td>Review items</td>
                            <td><span className={styles.statusReview}>In Review</span></td>
                            <td>{role.toUpperCase()}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    );
}
