import React from 'react';

interface TokenPerformanceCardProps {
    role: string;
    roleName: string;
    todayTokens: string;
    weekTokens: string;
    monthTokens: string;
    weekBudget: string;
    monthPercent: string;
    successRate: number;
    responseQuality: number;
    avgResponseTime: string;
    contextEfficiency: number;
    recentTasks: Array<{
        task: string;
        time: string;
        tokens: string;
        status: 'complete' | 'active' | 'pending';
    }>;
}

// Mock data for each role
export const TOKEN_PERFORMANCE_DATA: Record<string, TokenPerformanceCardProps> = {
    cfo: {
        role: 'cfo',
        roleName: 'CFO',
        todayTokens: '18.2K',
        weekTokens: '98K',
        monthTokens: '420K',
        weekBudget: '150K',
        monthPercent: '84%',
        successRate: 96,
        responseQuality: 93,
        avgResponseTime: '1.8s',
        contextEfficiency: 82,
        recentTasks: [
            { task: 'Prepared monthly financial report', time: '5 min ago', tokens: '2,340', status: 'complete' },
            { task: 'Analyzing budget variances', time: 'In progress', tokens: '1,120', status: 'active' },
            { task: 'Reviewed vendor contracts', time: '1 hr ago', tokens: '1,890', status: 'complete' },
        ]
    },
    cmo: {
        role: 'cmo',
        roleName: 'CMO',
        todayTokens: '31.5K',
        weekTokens: '185K',
        monthTokens: '720K',
        weekBudget: '250K',
        monthPercent: '72%',
        successRate: 89,
        responseQuality: 91,
        avgResponseTime: '2.1s',
        contextEfficiency: 75,
        recentTasks: [
            { task: 'Approving TikTok campaign content', time: '3 min ago', tokens: '890', status: 'active' },
            { task: 'Generated Q1 marketing plan', time: '20 min ago', tokens: '3,450', status: 'complete' },
            { task: 'Analyzed competitor positioning', time: '45 min ago', tokens: '2,100', status: 'complete' },
        ]
    },
    coo: {
        role: 'coo',
        roleName: 'COO',
        todayTokens: '22.8K',
        weekTokens: '142K',
        monthTokens: '580K',
        weekBudget: '200K',
        monthPercent: '71%',
        successRate: 92,
        responseQuality: 88,
        avgResponseTime: '1.5s',
        contextEfficiency: 85,
        recentTasks: [
            { task: 'Monitoring support ticket queue', time: '1 min ago', tokens: '450', status: 'active' },
            { task: 'Optimized workflow processes', time: '30 min ago', tokens: '1,780', status: 'complete' },
            { task: 'Reviewed operational metrics', time: '2 hr ago', tokens: '2,340', status: 'complete' },
        ]
    },
    cio: {
        role: 'cio',
        roleName: 'CIO',
        todayTokens: '28.4K',
        weekTokens: '168K',
        monthTokens: '650K',
        weekBudget: '220K',
        monthPercent: '76%',
        successRate: 94,
        responseQuality: 92,
        avgResponseTime: '1.9s',
        contextEfficiency: 88,
        recentTasks: [
            { task: 'Running security audit scan', time: '2 min ago', tokens: '1,200', status: 'active' },
            { task: 'Evaluated cloud migration plan', time: '1 hr ago', tokens: '3,120', status: 'complete' },
            { task: 'Updated disaster recovery docs', time: '3 hr ago', tokens: '2,450', status: 'complete' },
        ]
    },
    clo: {
        role: 'clo',
        roleName: 'CLO',
        todayTokens: '15.6K',
        weekTokens: '82K',
        monthTokens: '340K',
        weekBudget: '120K',
        monthPercent: '68%',
        successRate: 97,
        responseQuality: 95,
        avgResponseTime: '2.4s',
        contextEfficiency: 90,
        recentTasks: [
            { task: 'Reviewing vendor contract terms', time: '8 min ago', tokens: '1,890', status: 'active' },
            { task: 'Drafted compliance policy update', time: '2 hr ago', tokens: '2,780', status: 'complete' },
            { task: 'Analyzed regulatory requirements', time: '4 hr ago', tokens: '1,560', status: 'complete' },
        ]
    },
    cpo: {
        role: 'cpo',
        roleName: 'CPO',
        todayTokens: '26.3K',
        weekTokens: '158K',
        monthTokens: '620K',
        weekBudget: '200K',
        monthPercent: '79%',
        successRate: 91,
        responseQuality: 89,
        avgResponseTime: '2.0s',
        contextEfficiency: 81,
        recentTasks: [
            { task: 'Finalizing Q2 roadmap PRD', time: '5 min ago', tokens: '2,890', status: 'active' },
            { task: 'Analyzed user feedback trends', time: '1 hr ago', tokens: '1,670', status: 'complete' },
            { task: 'Prioritized feature backlog', time: '3 hr ago', tokens: '2,120', status: 'complete' },
        ]
    },
    cto: {
        role: 'cto',
        roleName: 'CTO',
        todayTokens: '35.2K',
        weekTokens: '210K',
        monthTokens: '820K',
        weekBudget: '280K',
        monthPercent: '75%',
        successRate: 93,
        responseQuality: 94,
        avgResponseTime: '1.7s',
        contextEfficiency: 86,
        recentTasks: [
            { task: 'Code review for API v2.5', time: '3 min ago', tokens: '1,450', status: 'active' },
            { task: 'Evaluated new tech stack options', time: '45 min ago', tokens: '3,200', status: 'complete' },
            { task: 'Updated architecture docs', time: '2 hr ago', tokens: '2,890', status: 'complete' },
        ]
    },
    cxa: {
        role: 'cxa',
        roleName: 'CXA',
        todayTokens: '19.8K',
        weekTokens: '115K',
        monthTokens: '480K',
        weekBudget: '160K',
        monthPercent: '72%',
        successRate: 90,
        responseQuality: 87,
        avgResponseTime: '1.6s',
        contextEfficiency: 79,
        recentTasks: [
            { task: 'Processing incoming emails', time: '1 min ago', tokens: '680', status: 'active' },
            { task: 'Generated customer support report', time: '30 min ago', tokens: '1,890', status: 'complete' },
            { task: 'Analyzed CSAT feedback', time: '2 hr ago', tokens: '1,340', status: 'complete' },
        ]
    },
};

export default function TokenPerformanceCard({ role }: { role: string }) {
    const data = TOKEN_PERFORMANCE_DATA[role];
    if (!data) return null;

    const getStatusBadge = (status: string) => {
        switch (status) {
            case 'complete': return <span className="badge badge-success">Complete</span>;
            case 'active': return <span className="badge badge-warning">Active</span>;
            default: return <span className="badge badge-secondary">Pending</span>;
        }
    };

    const getProgressColor = (value: number) => value >= 85 ? 'success' : value >= 70 ? 'warning' : 'error';

    return (
        <div className="dashboard-grid" style={{ marginBottom: '1.5rem' }}>
            <div className="col-12">
                <div className="card">
                    <div className="card-header">
                        <h3 className="card-title">{data.roleName} Token Usage & Performance</h3>
                        <span className="badge badge-success">Healthy</span>
                    </div>
                    <div className="card-body">
                        {/* Token Usage Section */}
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1.5rem', marginBottom: '2rem' }}>
                            <div style={{ textAlign: 'center', padding: '1rem', background: 'var(--bg-tertiary)', borderRadius: '8px' }}>
                                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>Today's Tokens</div>
                                <div style={{ fontSize: '1.75rem', fontWeight: 700, color: 'var(--accent-blue)' }}>{data.todayTokens}</div>
                                <div style={{ fontSize: '0.75rem', color: 'var(--success)' }}>↓ 8% vs avg</div>
                            </div>
                            <div style={{ textAlign: 'center', padding: '1rem', background: 'var(--bg-tertiary)', borderRadius: '8px' }}>
                                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>This Week</div>
                                <div style={{ fontSize: '1.75rem', fontWeight: 700, color: 'var(--accent-gold)' }}>{data.weekTokens}</div>
                                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>of {data.weekBudget} budget</div>
                            </div>
                            <div style={{ textAlign: 'center', padding: '1rem', background: 'var(--bg-tertiary)', borderRadius: '8px' }}>
                                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>This Month</div>
                                <div style={{ fontSize: '1.75rem', fontWeight: 700 }}>{data.monthTokens}</div>
                                <div style={{ fontSize: '0.75rem', color: 'var(--warning)' }}>{data.monthPercent} of budget</div>
                            </div>
                        </div>

                        {/* Model Performance Section */}
                        <h4 style={{ fontSize: '0.875rem', marginBottom: '1rem', color: 'var(--text-muted)' }}>Model Performance</h4>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr', gap: '1rem', marginBottom: '1.5rem' }}>
                            <div>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                    <span style={{ fontSize: '0.875rem' }}>Task Success Rate</span>
                                    <span style={{ fontWeight: 600, color: `var(--${getProgressColor(data.successRate)})` }}>{data.successRate}%</span>
                                </div>
                                <div className="progress-bar"><div className={`progress-fill ${getProgressColor(data.successRate)}`} style={{ width: `${data.successRate}%` }}></div></div>
                            </div>
                            <div>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                    <span style={{ fontSize: '0.875rem' }}>Response Quality</span>
                                    <span style={{ fontWeight: 600, color: `var(--${getProgressColor(data.responseQuality)})` }}>{data.responseQuality}%</span>
                                </div>
                                <div className="progress-bar"><div className={`progress-fill ${getProgressColor(data.responseQuality)}`} style={{ width: `${data.responseQuality}%` }}></div></div>
                            </div>
                            <div>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                    <span style={{ fontSize: '0.875rem' }}>Avg Response Time</span>
                                    <span style={{ fontWeight: 600 }}>{data.avgResponseTime}</span>
                                </div>
                                <div className="progress-bar"><div className="progress-fill success" style={{ width: '85%' }}></div></div>
                            </div>
                            <div>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                    <span style={{ fontSize: '0.875rem' }}>Context Efficiency</span>
                                    <span style={{ fontWeight: 600, color: `var(--${getProgressColor(data.contextEfficiency)})` }}>{data.contextEfficiency}%</span>
                                </div>
                                <div className="progress-bar"><div className={`progress-fill ${getProgressColor(data.contextEfficiency)}`} style={{ width: `${data.contextEfficiency}%` }}></div></div>
                            </div>
                        </div>

                        {/* Recent Tasks */}
                        <h4 style={{ fontSize: '0.875rem', marginBottom: '1rem', color: 'var(--text-muted)' }}>Recent Tasks</h4>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                            {data.recentTasks.map((task, idx) => (
                                <div key={idx} style={{ padding: '0.75rem', background: 'var(--bg-tertiary)', borderRadius: '6px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                    <div>
                                        <div style={{ fontSize: '0.875rem' }}>{task.task}</div>
                                        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{task.time} • {task.tokens} tokens</div>
                                    </div>
                                    {getStatusBadge(task.status)}
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
