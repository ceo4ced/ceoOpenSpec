'use client';

import React, { useState } from 'react';
import styles from './FunctionActivitySection.module.css';

export interface FunctionActivity {
    id: string;
    role: string;
    functionName: string;
    status: 'running' | 'success' | 'error' | 'pending';
    timestamp: Date;
    input?: Record<string, any>;
    output?: Record<string, any>;
    error?: string;
    progress?: number;
    estimatedRemaining?: number;
    duration?: number;
    tokens?: number;
    cost?: number;
}

// Mock function activities for demonstration
const MOCK_ACTIVITIES: FunctionActivity[] = [
    {
        id: '1',
        role: 'CEO',
        functionName: 'ceo.decide',
        status: 'running',
        timestamp: new Date(),
        input: { decision_type: 'strategic', options: 3 },
        progress: 67,
        estimatedRemaining: 12,
    },
    {
        id: '2',
        role: 'CEO',
        functionName: 'ceo.plan',
        status: 'success',
        timestamp: new Date(Date.now() - 2 * 60 * 1000),
        duration: 8.2,
        tokens: 1247,
        cost: 0.024,
    },
    {
        id: '3',
        role: 'CFO',
        functionName: 'cfo.analyze',
        status: 'success',
        timestamp: new Date(Date.now() - 5 * 60 * 1000),
        duration: 3.1,
        tokens: 892,
        cost: 0.018,
    },
    {
        id: '4',
        role: 'CMO',
        functionName: 'cmo.validate',
        status: 'success',
        timestamp: new Date(Date.now() - 12 * 60 * 1000),
        duration: 0.8,
        tokens: 156,
        cost: 0.003,
    },
    {
        id: '5',
        role: 'CTO',
        functionName: 'cto.status',
        status: 'error',
        timestamp: new Date(Date.now() - 18 * 60 * 1000),
        error: 'Gate is closed - awaiting CMO validation',
    },
];

interface FunctionActivitySectionProps {
    role?: string;
    activities?: FunctionActivity[];
}

export default function FunctionActivitySection({ role, activities = MOCK_ACTIVITIES }: FunctionActivitySectionProps) {
    const [expandedIds, setExpandedIds] = useState<Set<string>>(new Set(['1'])); // Auto-expand running
    const [filter, setFilter] = useState<string>('all');

    const toggleExpand = (id: string) => {
        const newExpanded = new Set(expandedIds);
        if (newExpanded.has(id)) {
            newExpanded.delete(id);
        } else {
            newExpanded.add(id);
        }
        setExpandedIds(newExpanded);
    };

    const formatTimestamp = (date: Date) => {
        const now = new Date();
        const diff = now.getTime() - date.getTime();
        const minutes = Math.floor(diff / (1000 * 60));

        if (minutes < 1) return 'just now';
        if (minutes === 1) return '1m ago';
        if (minutes < 60) return `${minutes}m ago`;

        const hours = Math.floor(minutes / 60);
        if (hours === 1) return '1h ago';
        return `${hours}h ago`;
    };

    const getStatusIcon = (status: FunctionActivity['status']) => {
        switch (status) {
            case 'running': return '●';
            case 'success': return '✓';
            case 'error': return '✕';
            case 'pending': return '○';
            default: return '•';
        }
    };

    const getStatusBadge = (status: FunctionActivity['status']) => {
        switch (status) {
            case 'running': return 'RUN';
            case 'success': return 'OK';
            case 'error': return 'ERR';
            case 'pending': return 'WAIT';
            default: return '...';
        }
    };

    // Filter activities
    let filteredActivities = [...activities];
    if (filter === 'running') {
        filteredActivities = filteredActivities.filter(a => a.status === 'running');
    } else if (filter === 'error') {
        filteredActivities = filteredActivities.filter(a => a.status === 'error');
    } else if (filter === 'role' && role) {
        filteredActivities = filteredActivities.filter(a => a.role.toLowerCase() === role.toLowerCase());
    }

    // Sort by timestamp (newest first)
    filteredActivities.sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime());

    const clearActivities = () => {
        // In a real implementation, this would clear the activity log
        console.log('Clear activities');
    };

    return (
        <div className={styles.functionActivity}>
            <div className={styles.header}>
                <div className={styles.title}>
                    <span className={styles.icon}>⚡</span>
                    <span>Function Activity</span>
                </div>
                <div className={styles.actions}>
                    <select
                        className={styles.filterSelect}
                        value={filter}
                        onChange={(e) => setFilter(e.target.value)}
                    >
                        <option value="all">All</option>
                        <option value="running">Running</option>
                        <option value="error">Errors</option>
                        {role && <option value="role">This Role Only</option>}
                    </select>
                    <button className={styles.actionButton} onClick={clearActivities} title="Clear">
                        ×
                    </button>
                </div>
            </div>

            <div className={styles.body}>
                {filteredActivities.length === 0 ? (
                    <div className={styles.emptyState}>
                        <span>No function activities to display</span>
                    </div>
                ) : (
                    filteredActivities.map((activity) => {
                        const isExpanded = expandedIds.has(activity.id);

                        return (
                            <div
                                key={activity.id}
                                className={`${styles.entry} ${styles[activity.status]} ${isExpanded ? styles.expanded : ''}`}
                            >
                                <div
                                    className={styles.entryHeader}
                                    onClick={() => toggleExpand(activity.id)}
                                >
                                    <div className={styles.entryLeft}>
                                        <span className={styles.expandIcon}>
                                            {isExpanded ? '▼' : '▶'}
                                        </span>
                                        <span className={styles.functionName}>
                                            {activity.functionName}()
                                        </span>
                                    </div>
                                    <div className={styles.entryRight}>
                                        <span className={styles.timestamp}>
                                            {formatTimestamp(activity.timestamp)}
                                        </span>
                                        <span className={`${styles.statusIcon} ${styles[activity.status]}`}>
                                            {getStatusIcon(activity.status)}
                                        </span>
                                        <span className={`${styles.statusBadge} ${styles[activity.status]}`}>
                                            {getStatusBadge(activity.status)}
                                        </span>
                                    </div>
                                </div>

                                {isExpanded && (
                                    <div className={styles.entryDetails}>
                                        {activity.input && (
                                            <div className={styles.detailRow}>
                                                <span className={styles.detailLabel}>├─ Input:</span>
                                                <span className={styles.detailValue}>
                                                    {JSON.stringify(activity.input)}
                                                </span>
                                            </div>
                                        )}

                                        {activity.status === 'running' && (
                                            <>
                                                <div className={styles.detailRow}>
                                                    <span className={styles.detailLabel}>├─ Processing:</span>
                                                    <span className={styles.detailValue}>
                                                        Evaluating options...
                                                    </span>
                                                </div>
                                                <div className={styles.detailRow}>
                                                    <span className={styles.detailLabel}>└─ Status:</span>
                                                    <div className={styles.progressContainer}>
                                                        <div className={styles.progressBar}>
                                                            <div
                                                                className={styles.progressFill}
                                                                style={{ width: `${activity.progress || 0}%` }}
                                                            ></div>
                                                        </div>
                                                        <span className={styles.progressText}>
                                                            {activity.progress}% | Est: {activity.estimatedRemaining}s remaining
                                                        </span>
                                                    </div>
                                                </div>
                                            </>
                                        )}

                                        {activity.status === 'success' && (
                                            <div className={styles.detailRow}>
                                                <span className={styles.detailLabel}>└─</span>
                                                <span className={styles.detailValue}>
                                                    Completed in {activity.duration}s | Tokens: {activity.tokens?.toLocaleString()} | Cost: ${activity.cost?.toFixed(3)}
                                                </span>
                                            </div>
                                        )}

                                        {activity.status === 'error' && activity.error && (
                                            <div className={styles.detailRow}>
                                                <span className={styles.detailLabel}>└─ Error:</span>
                                                <span className={`${styles.detailValue} ${styles.errorText}`}>
                                                    {activity.error}
                                                </span>
                                            </div>
                                        )}
                                    </div>
                                )}

                                {!isExpanded && activity.status === 'success' && (
                                    <div className={styles.entrySummary}>
                                        Completed in {activity.duration}s | Tokens: {activity.tokens?.toLocaleString()} | Cost: ${activity.cost?.toFixed(3)}
                                    </div>
                                )}

                                {!isExpanded && activity.status === 'error' && activity.error && (
                                    <div className={`${styles.entrySummary} ${styles.errorText}`}>
                                        {activity.error}
                                    </div>
                                )}
                            </div>
                        );
                    })
                )}
            </div>
        </div>
    );
}
