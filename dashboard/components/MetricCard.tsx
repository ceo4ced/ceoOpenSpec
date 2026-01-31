
import React from 'react';

interface MetricCardProps {
    label: string;
    value: string;
    change: string;
    trend: 'up' | 'down' | 'neutral';
    icon: string;
}

export default function MetricCard({ label, value, change, trend, icon }: MetricCardProps) {
    return (
        <div className="metric-card">
            <div className="metric-header">
                <span className="metric-label">{label}</span>
                <span className="metric-icon">{icon}</span>
            </div>
            <div className={`metric-value ${trend === 'up' ? 'positive' : trend === 'down' ? 'negative' : ''}`}>
                {value}
            </div>
            <div className={`metric-change ${trend}`}>
                <span>{trend === 'up' ? '↑' : trend === 'down' ? '↓' : '•'}</span>
                <span>{change}</span>
            </div>
        </div>
    );
}
