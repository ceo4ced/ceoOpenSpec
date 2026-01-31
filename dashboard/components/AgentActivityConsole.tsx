'use client';

import React from 'react';
import { AGENT_ACTIVITIES } from '@/lib/agent-activity';
import type { AgentActivity } from '@/lib/agent-activity';
import styles from './AgentActivityConsole.module.css';

export default function AgentActivityConsole() {
    const formatTimestamp = (timestamp: string) => {
        const date = new Date(timestamp);
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

    const getStatusIcon = (status: AgentActivity['status']) => {
        switch (status) {
            case 'active': return '●';
            case 'idle': return '○';
            case 'error': return '✕';
            default: return '•';
        }
    };

    // Sort by timestamp, most recent first
    const sortedActivities = [...AGENT_ACTIVITIES].sort((a, b) =>
        new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
    );

    return (
        <div className={styles.console}>
            <div className={styles.consoleHeader}>
                <div className={styles.consoleTitle}>
                    <span className={styles.terminalIcon}>⚡</span>
                    <span>Agent Activity Console</span>
                </div>
                <div className={styles.consoleMeta}>
                    <span className={styles.liveIndicator}>● LIVE</span>
                </div>
            </div>

            <div className={styles.consoleBody}>
                {sortedActivities.map((activity) => (
                    <div
                        key={activity.id}
                        className={styles.activityLine}
                        data-status={activity.status}
                    >
                        <span className={styles.activityTimestamp}>
                            {formatTimestamp(activity.timestamp)}
                        </span>
                        <span className={styles.activityStatus}>
                            {getStatusIcon(activity.status)}
                        </span>
                        <span className={styles.activityAgent}>
                            [{activity.agentName}]
                        </span>
                        <span className={styles.activityText}>
                            {activity.activity}
                        </span>
                        {activity.duration && (
                            <span className={styles.activityDuration}>
                                ({activity.duration})
                            </span>
                        )}
                    </div>
                ))}
            </div>

            <div className={styles.consoleFooter}>
                <span className={styles.footerText}>
                    {sortedActivities.length} activities • Updated {formatTimestamp(sortedActivities[0]?.timestamp || new Date().toISOString())}
                </span>
            </div>
        </div>
    );
}
