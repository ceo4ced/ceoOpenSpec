
import React from 'react';
import MetricCard from './MetricCard';
import AgentCard from './AgentCard';
import { METRICS, AGENT_STATUS, PENDING_APPROVALS, TABLE_DATA, RED_PHONE_ALERTS, AGENTS } from '@/lib/data';

interface DashboardProps {
    role?: string;
    onAgentClick?: (id: string) => void;
}

// Helper for metrics grid
export const MetricsGrid = ({ role }: { role: string }) => {
    const cards = METRICS[role]?.cards || [];
    return (
        <div className="metrics-grid">
            {cards.map((card: any, idx: number) => (
                <MetricCard key={idx} {...card} />
            ))}
        </div>
    );
};

// CHAIRMAN
export const ChairmanDashboard = ({ onAgentClick }: DashboardProps) => {
    const [expandedAlert, setExpandedAlert] = React.useState<number | null>(null);

    return (
        <div className="dashboard-grid">
            {RED_PHONE_ALERTS.length > 0 && (
                <div className="alerts-section" style={{ gridColumn: '1 / -1' }}>
                    <div className="alerts-header">
                        <span>🚨</span>
                        <span>RED PHONE ALERTS</span>
                        <a href="/red-phone" className="btn btn-secondary" style={{ marginLeft: 'auto' }}>
                            View All Details →
                        </a>
                    </div>
                    {RED_PHONE_ALERTS.map((alert: any, idx: number) => (
                        <div className="alert-item" key={idx} style={{ cursor: 'pointer' }} onClick={() => setExpandedAlert(expandedAlert === idx ? null : idx)}>
                            <div className="alert-priority"></div>
                            <div className="alert-content">
                                <div>{alert.message}</div>
                                {expandedAlert === idx && (
                                    <div style={{ marginTop: '1rem', padding: '1rem', background: 'var(--bg-tertiary)', borderRadius: '6px', fontSize: '0.875rem' }}>
                                        <p><strong>Severity:</strong> {alert.severity === 'critical' ? '🔴 Critical' : '⚠️ Warning'}</p>
                                        <p><strong>Impact:</strong> {alert.severity === 'critical' ? 'High - Service degradation' : 'Medium - Requires attention'}</p>
                                        <p><strong>Action:</strong> Click "View All Details" for full emergency controls</p>
                                    </div>
                                )}
                            </div>
                            <button className="btn btn-secondary" onClick={(e) => { e.stopPropagation(); }}>Acknowledge</button>
                        </div>
                    ))}
                </div>
            )}

            <div className="col-8">
                <div className="card">
                    <div className="card-header">
                        <h3 className="card-title">Agent Status Grid</h3>
                        <span className="badge badge-success">All Online</span>
                    </div>
                    <div className="card-body">
                        <div className="agent-grid">
                            {['ceo', 'cfo', 'cmo', 'coo', 'cio', 'clo', 'cpo', 'cto', 'cxa'].map(key => (
                                <div key={key} onClick={() => onAgentClick && onAgentClick(key)}>
                                    <AgentCard
                                        id={key}
                                        status={AGENT_STATUS[key].status}
                                        task={AGENT_STATUS[key].task}
                                        tokens={AGENT_STATUS[key].tokens}
                                    />
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
            <div className="col-4">
                <div className="card">
                    <div className="card-header">
                        <h3 className="card-title">Pending Approvals</h3>
                        <span className="badge badge-warning">{PENDING_APPROVALS.length}</span>
                    </div>
                    <div className="card-body">
                        <div className="approval-list">
                            {PENDING_APPROVALS.map((item: any, idx: number) => (
                                <div key={idx} className={`approval-item ${item.priority}`}>
                                    <div className="approval-content">
                                        <div className="approval-title">{item.title}</div>
                                        <div className="approval-meta">From {item.from} • {item.time}</div>
                                    </div>
                                    <div className="approval-actions">
                                        <button className="btn btn-icon btn-success">✓</button>
                                        <button className="btn btn-icon btn-danger">✗</button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

// CEO
export const CEODashboard = ({ onAgentClick }: DashboardProps) => {
    return (
        <div className="dashboard-grid">
            <div className="col-8">
                <div className="card">
                    <div className="card-header">
                        <h3 className="card-title">CEO Token Usage & Performance</h3>
                        <span className="badge badge-success">Healthy</span>
                    </div>
                    <div className="card-body">
                        {/* Token Usage Section */}
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1.5rem', marginBottom: '2rem' }}>
                            <div style={{ textAlign: 'center', padding: '1rem', background: 'var(--bg-tertiary)', borderRadius: '8px' }}>
                                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>Today's Tokens</div>
                                <div style={{ fontSize: '1.75rem', fontWeight: 700, color: 'var(--accent-blue)' }}>24.5K</div>
                                <div style={{ fontSize: '0.75rem', color: 'var(--success)' }}>↓ 12% vs avg</div>
                            </div>
                            <div style={{ textAlign: 'center', padding: '1rem', background: 'var(--bg-tertiary)', borderRadius: '8px' }}>
                                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>This Week</div>
                                <div style={{ fontSize: '1.75rem', fontWeight: 700, color: 'var(--accent-gold)' }}>142K</div>
                                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>of 200K budget</div>
                            </div>
                            <div style={{ textAlign: 'center', padding: '1rem', background: 'var(--bg-tertiary)', borderRadius: '8px' }}>
                                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>This Month</div>
                                <div style={{ fontSize: '1.75rem', fontWeight: 700 }}>580K</div>
                                <div style={{ fontSize: '0.75rem', color: 'var(--warning)' }}>72% of budget</div>
                            </div>
                        </div>

                        {/* Model Performance Section */}
                        <h4 style={{ fontSize: '0.875rem', marginBottom: '1rem', color: 'var(--text-muted)' }}>Model Performance</h4>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                            <div>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                    <span>Task Success Rate</span>
                                    <span style={{ fontWeight: 600, color: 'var(--success)' }}>94%</span>
                                </div>
                                <div className="progress-bar"><div className="progress-fill success" style={{ width: '94%' }}></div></div>
                            </div>
                            <div>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                    <span>Response Quality</span>
                                    <span style={{ fontWeight: 600, color: 'var(--success)' }}>91%</span>
                                </div>
                                <div className="progress-bar"><div className="progress-fill success" style={{ width: '91%' }}></div></div>
                            </div>
                            <div>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                    <span>Avg Response Time</span>
                                    <span style={{ fontWeight: 600 }}>2.3s</span>
                                </div>
                                <div className="progress-bar"><div className="progress-fill success" style={{ width: '85%' }}></div></div>
                            </div>
                            <div>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                    <span>Context Efficiency</span>
                                    <span style={{ fontWeight: 600, color: 'var(--warning)' }}>78%</span>
                                </div>
                                <div className="progress-bar"><div className="progress-fill warning" style={{ width: '78%' }}></div></div>
                            </div>
                        </div>

                        {/* Recent Activity */}
                        <h4 style={{ fontSize: '0.875rem', marginTop: '1.5rem', marginBottom: '1rem', color: 'var(--text-muted)' }}>Recent Tasks</h4>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                            <div style={{ padding: '0.75rem', background: 'var(--bg-tertiary)', borderRadius: '6px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <div>
                                    <div style={{ fontSize: '0.875rem' }}>Analyzed Q4 Financial Reports</div>
                                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>2 min ago • 1,240 tokens</div>
                                </div>
                                <span className="badge badge-success">Complete</span>
                            </div>
                            <div style={{ padding: '0.75rem', background: 'var(--bg-tertiary)', borderRadius: '6px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <div>
                                    <div style={{ fontSize: '0.875rem' }}>Prepared Executive Summary</div>
                                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>15 min ago • 2,100 tokens</div>
                                </div>
                                <span className="badge badge-success">Complete</span>
                            </div>
                            <div style={{ padding: '0.75rem', background: 'var(--bg-tertiary)', borderRadius: '6px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <div>
                                    <div style={{ fontSize: '0.875rem' }}>Reviewing Strategic Initiatives</div>
                                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>In progress • 890 tokens</div>
                                </div>
                                <span className="badge badge-warning">Active</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div className="col-4">
                <div className="card">
                    <div className="card-header">
                        <h3 className="card-title">Mission Alignment</h3>
                    </div>
                    <div className="card-body">
                        <div style={{ textAlign: 'center', marginBottom: '1rem' }}>
                            <div style={{ fontSize: '3rem', fontWeight: 700, color: 'var(--accent-gold)' }}>78%</div>
                            <div style={{ color: 'var(--text-muted)' }}>Overall Alignment Score</div>
                        </div>
                        <div className="progress-bar">
                            <div className="progress-fill success" style={{ width: '78%' }}></div>
                        </div>
                        <div style={{ marginTop: '1.5rem' }}>
                            <h4 style={{ fontSize: '0.875rem', marginBottom: '0.75rem' }}>By Objective</h4>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                                <div><span style={{ color: 'var(--text-muted)' }}>Revenue Growth</span> <span style={{ float: 'right' }}>85%</span></div>
                                <div className="progress-bar"><div className="progress-fill success" style={{ width: '85%' }}></div></div>
                                <div><span style={{ color: 'var(--text-muted)' }}>Customer Satisfaction</span> <span style={{ float: 'right' }}>72%</span></div>
                                <div className="progress-bar"><div className="progress-fill warning" style={{ width: '72%' }}></div></div>
                                <div><span style={{ color: 'var(--text-muted)' }}>Operational Excellence</span> <span style={{ float: 'right' }}>80%</span></div>
                                <div className="progress-bar"><div className="progress-fill success" style={{ width: '80%' }}></div></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

// CFO
export const CFODashboard = () => {
    return (
        <div className="dashboard-grid">
            <div className="col-6">
                <div className="card">
                    <div className="card-header">
                        <h3 className="card-title">Monthly Token Budget</h3>
                    </div>
                    <div className="card-body">
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
                            <div>
                                <div style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>Total Budget</div>
                                <div style={{ fontSize: '1.5rem', fontWeight: 700 }}>$5,000</div>
                            </div>
                            <div style={{ textAlign: 'right' }}>
                                <div style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>Used</div>
                                <div style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--accent-gold)' }}>$3,210 (64%)</div>
                            </div>
                        </div>
                        <div className="progress-bar" style={{ height: '12px' }}>
                            <div className="progress-fill warning" style={{ width: '64%' }}></div>
                        </div>
                        <div style={{ marginTop: '0.5rem', color: 'var(--text-muted)', fontSize: '0.875rem' }}>
                            Remaining: $1,790
                        </div>
                    </div>
                </div>
            </div>
            <div className="col-6">
                <div className="card">
                    <div className="card-header">
                        <h3 className="card-title">Expense Breakdown</h3>
                    </div>
                    <div className="card-body">
                        <div className="bar-chart">
                            <div className="bar-row">
                                <span className="bar-label">AI/LLM</span>
                                <div className="bar-track"><div className="bar-value" style={{ width: '59%', background: 'linear-gradient(90deg, #8b5cf6, #d946ef)' }}>59%</div></div>
                            </div>
                            <div className="bar-row">
                                <span className="bar-label">Infra</span>
                                <div className="bar-track"><div className="bar-value" style={{ width: '18%', background: 'linear-gradient(90deg, #3b82f6, #06b6d4)' }}>18%</div></div>
                            </div>
                            <div className="bar-row">
                                <span className="bar-label">Software</span>
                                <div className="bar-track"><div className="bar-value" style={{ width: '10%', background: 'linear-gradient(90deg, #10b981, #34d399)' }}>10%</div></div>
                            </div>
                            <div className="bar-row">
                                <span className="bar-label">Marketing</span>
                                <div className="bar-track"><div className="bar-value" style={{ width: '8%', background: '#ec4899' }}>8%</div></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div className="col-12">
                <div className="card">
                    <div className="card-header">
                        <h3 className="card-title">Financial Controls</h3>
                    </div>
                    <div className="card-body" style={{ display: 'flex', gap: '1rem' }}>
                        <button className="btn btn-danger">🚨 Emergency Pause</button>
                        <button className="btn btn-secondary">📊 Adjust Budgets</button>
                        <button className="btn btn-secondary">💰 Cost Mode</button>
                    </div>
                </div>
            </div>
        </div>
    );
};

// CMO with Tabs
export const CMODashboard = () => {
    const [activeTab, setActiveTab] = React.useState('acquisition');

    return (
        <>
            <div className="tab-nav">
                <button
                    className={`tab-btn ${activeTab === 'acquisition' ? 'active' : ''}`}
                    onClick={() => setActiveTab('acquisition')}
                >
                    Acquisition
                </button>
                <button
                    className={`tab-btn ${activeTab === 'engagement' ? 'active' : ''}`}
                    onClick={() => setActiveTab('engagement')}
                >
                    Engagement & Brand
                </button>
            </div>

            <div className="dashboard-grid">
                {activeTab === 'acquisition' ? (
                    <>
                        <div className="col-6">
                            <div className="card">
                                <div className="card-header">
                                    <h3 className="card-title">ROAS by Channel</h3>
                                </div>
                                <div className="card-body">
                                    <div className="bar-chart">
                                        {TABLE_DATA.cmo_roas.map((row: any, idx: number) => (
                                            <div className="bar-row" key={idx}>
                                                <span className="bar-label">{row.channel}</span>
                                                <div className="bar-track">
                                                    <div className="bar-value" style={{ width: `${(parseFloat(row.roas) / 7) * 100}%`, background: 'linear-gradient(90deg, #8b5cf6, #d946ef)' }}>{row.roas}</div>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="col-6">
                            <div className="card">
                                <div className="card-header">
                                    <h3 className="card-title">Marketing Funnel</h3>
                                </div>
                                <div className="card-body">
                                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                                        <div className="funnel-step" style={{ width: '100%', background: 'var(--accent-pink)', padding: '0.75rem', borderRadius: '0.5rem', textAlign: 'center' }}>
                                            <div style={{ fontWeight: 600 }}>Impressions</div>
                                            <div style={{ fontSize: '1.25rem' }}>1.2M</div>
                                        </div>
                                        <div style={{ textAlign: 'center', color: 'var(--text-muted)' }}>↓ 2.4%</div>
                                        <div className="funnel-step" style={{ width: '80%', margin: '0 auto', background: 'var(--accent-purple)', padding: '0.75rem', borderRadius: '0.5rem', textAlign: 'center' }}>
                                            <div style={{ fontWeight: 600 }}>Clicks</div>
                                            <div style={{ fontSize: '1.25rem' }}>28.8K</div>
                                        </div>
                                        <div style={{ textAlign: 'center', color: 'var(--text-muted)' }}>↓ 30%</div>
                                        <div className="funnel-step" style={{ width: '60%', margin: '0 auto', background: 'var(--accent-blue)', padding: '0.75rem', borderRadius: '0.5rem', textAlign: 'center' }}>
                                            <div style={{ fontWeight: 600 }}>Add to Cart</div>
                                            <div style={{ fontSize: '1.25rem' }}>8,640</div>
                                        </div>
                                        <div style={{ textAlign: 'center', color: 'var(--text-muted)' }}>↓ 50%</div>
                                        <div className="funnel-step" style={{ width: '40%', margin: '0 auto', background: 'var(--accent-green)', padding: '0.75rem', borderRadius: '0.5rem', textAlign: 'center' }}>
                                            <div style={{ fontWeight: 600 }}>Purchase</div>
                                            <div style={{ fontSize: '1.25rem' }}>3,456</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </>
                ) : (
                    <>
                        <div className="col-8">
                            <div className="card">
                                <div className="card-header">
                                    <h3 className="card-title">Social Media Sentiment</h3>
                                    <span className="badge badge-success">Positive Trend</span>
                                </div>
                                <div className="card-body">
                                    <div style={{ display: 'flex', alignItems: 'flex-end', height: '200px', gap: '1rem', paddingBottom: '1rem', borderBottom: '1px solid var(--border-color)' }}>
                                        {[45, 60, 55, 75, 80, 85, 82].map((h, i) => (
                                            <div key={i} style={{ flex: 1, background: 'linear-gradient(180deg, #8b5cf6 0%, rgba(139, 92, 246, 0.2) 100%)', height: `${h}%`, borderRadius: '4px 4px 0 0', opacity: 0.8 }}></div>
                                        ))}
                                    </div>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '1rem' }}>
                                        <div>
                                            <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>Brand Mentions</div>
                                            <div style={{ fontSize: '1.5rem', fontWeight: 600 }}>12.4K</div>
                                        </div>
                                        <div>
                                            <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>Positive</div>
                                            <div style={{ fontSize: '1.5rem', fontWeight: 600, color: 'var(--accent-green)' }}>84%</div>
                                        </div>
                                        <div>
                                            <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>Negative</div>
                                            <div style={{ fontSize: '1.5rem', fontWeight: 600, color: 'var(--accent-pink)' }}>4%</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="col-4">
                            <div className="card">
                                <div className="card-header">
                                    <h3 className="card-title">Recent Posts</h3>
                                </div>
                                <div className="card-body">
                                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                                        <div style={{ padding: '0.75rem', background: 'var(--bg-tertiary)', borderRadius: '0.5rem' }}>
                                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                                <span style={{ fontWeight: 600 }}>Twitter / X</span>
                                                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>2h ago</span>
                                            </div>
                                            <div style={{ fontSize: '0.9rem', marginBottom: '0.5rem' }}>Announcing our new AI features... 🚀</div>
                                            <div style={{ fontSize: '0.8rem', color: 'var(--accent-blue)' }}>❤️ 1.2K  🔁 450</div>
                                        </div>
                                        <div style={{ padding: '0.75rem', background: 'var(--bg-tertiary)', borderRadius: '0.5rem' }}>
                                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                                <span style={{ fontWeight: 600 }}>LinkedIn</span>
                                                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>5h ago</span>
                                            </div>
                                            <div style={{ fontSize: '0.9rem', marginBottom: '0.5rem' }}>We are hiring! Join the team...</div>
                                            <div style={{ fontSize: '0.8rem', color: 'var(--accent-blue)' }}>👍 856  💬 42</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </>
                )}
            </div>
        </>
    );
};

export const COODashboard = () => {
    return (
        <div className="dashboard-grid">
            <div className="col-8">
                <div className="card">
                    <div className="card-header">
                        <h3 className="card-title">Ticket Queue</h3>
                        <span className="badge badge-warning">23 Open</span>
                    </div>
                    <div className="card-body" style={{ padding: 0 }}>
                        <table className="data-table">
                            <thead>
                                <tr>
                                    <th>Priority</th>
                                    <th>Ticket</th>
                                    <th>Subject</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {TABLE_DATA.coo_tickets.map((t: any, idx: number) => (
                                    <tr key={idx}>
                                        <td><span className={`badge badge-${t.priority === 'critical' ? 'danger' : t.priority === 'high' ? 'warning' : 'info'}`}>{t.priority}</span></td>
                                        <td>{t.id}</td>
                                        <td>{t.subject}</td>
                                        <td>{t.status}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            <div className="col-4">
                <div className="card">
                    <div className="card-header"><h3 className="card-title">Call Center</h3></div>
                    <div className="card-body">
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                            <div style={{ textAlign: 'center', padding: '1rem', background: 'var(--bg-tertiary)', borderRadius: '0.5rem' }}>
                                <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--accent-gold)' }}>47</div>
                                <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>Calls Today</div>
                            </div>
                            <div style={{ textAlign: 'center', padding: '1rem', background: 'var(--bg-tertiary)', borderRadius: '0.5rem' }}>
                                <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--accent-green)' }}>4.2m</div>
                                <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>Avg Duration</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export const CIODashboard = () => {
    return (
        <div className="dashboard-grid">
            <div className="col-8">
                <div className="card">
                    <div className="card-header">
                        <h3 className="card-title">MCP Server Status</h3>
                        <span className="badge badge-success">12/12 Online</span>
                    </div>
                    <div className="card-body" style={{ padding: 0 }}>
                        <table className="data-table">
                            <thead>
                                <tr>
                                    <th>Service</th>
                                    <th>Status</th>
                                    <th>Latency</th>
                                    <th>Calls/hr</th>
                                </tr>
                            </thead>
                            <tbody>
                                {TABLE_DATA.cio_servers.map((s: any, idx: number) => (
                                    <tr key={idx}>
                                        <td>{s.service}</td>
                                        <td><span className="badge badge-success">● {s.status}</span></td>
                                        <td>{s.latency}</td>
                                        <td>{s.calls}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            <div className="col-4">
                <div className="card">
                    <div className="card-header">
                        <h3 className="card-title">Security Status</h3>
                    </div>
                    <div className="card-body">
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.75rem', background: 'var(--bg-tertiary)', borderRadius: '0.5rem' }}>
                                <span>Active Incidents</span>
                                <span style={{ color: 'var(--accent-green)', fontWeight: 600 }}>0</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export const CLODashboard = () => {
    return (
        <div className="dashboard-grid">
            <div className="col-6">
                <div className="card">
                    <div className="card-header">
                        <h3 className="card-title">Jurisdictional Compliance</h3>
                    </div>
                    <div className="card-body" style={{ padding: 0 }}>
                        <table className="data-table">
                            <thead><tr><th>Jurisdiction</th><th>Status</th></tr></thead>
                            <tbody>
                                <tr><td>US Federal</td><td><span className="badge badge-success">Compliant</span></td></tr>
                                <tr><td>California</td><td><span className="badge badge-success">Compliant</span></td></tr>
                                <tr><td>EU GDPR</td><td><span className="badge badge-success">Compliant</span></td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            <div className="col-6">
                <div className="card">
                    <div className="card-header">
                        <h3 className="card-title">Active Contracts</h3>
                    </div>
                    <div className="card-body" style={{ padding: 0 }}>
                        <table className="data-table">
                            <thead><tr><th>Contract</th><th>Status</th></tr></thead>
                            <tbody>
                                <tr><td>SaaS Agreement</td><td><span className="badge badge-success">Active</span></td></tr>
                                <tr><td>AWS MSA</td><td><span className="badge badge-warning">Renew Soon</span></td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    );
};

export const CPODashboard = () => {
    return (
        <div className="dashboard-grid">
            <div className="col-8">
                <div className="card">
                    <div className="card-header">
                        <h3 className="card-title">Q1 2026 Roadmap</h3>
                        <span className="badge badge-info">60% Complete</span>
                    </div>
                    <div className="card-body">
                        <div className="progress-bar" style={{ height: '12px', marginBottom: '1.5rem' }}>
                            <div className="progress-fill success" style={{ width: '60%' }}></div>
                        </div>
                        <h4 style={{ fontSize: '0.875rem', color: 'var(--accent-green)', marginBottom: '0.5rem' }}>✓ Shipped</h4>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', marginBottom: '1rem' }}>
                            <div style={{ padding: '0.5rem', background: 'rgba(16, 185, 129, 0.1)', borderRadius: '0.25rem' }}>User Onboarding v2</div>
                        </div>
                        <h4 style={{ fontSize: '0.875rem', color: 'var(--accent-blue)', marginBottom: '0.5rem' }}>🔄 In Progress</h4>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                            <div style={{ padding: '0.5rem', background: 'rgba(59, 130, 246, 0.1)', borderRadius: '0.25rem', display: 'flex', justifyContent: 'space-between' }}>
                                <span>Mobile App MVP</span>
                                <span>70%</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div className="col-4">
                <div className="card">
                    <div className="card-header">
                        <h3 className="card-title">Feedback</h3>
                    </div>
                    <div className="card-body">
                        <div style={{ padding: '0.5rem', background: 'var(--bg-tertiary)', borderRadius: '0.25rem' }}>
                            <span style={{ color: 'var(--accent-gold)' }}>256</span> API Docs Requests
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export const CTODashboard = () => {
    return (
        <div className="dashboard-grid">
            <div className="col-8">
                <div className="card">
                    <div className="card-header">
                        <h3 className="card-title">SpecKit Status</h3>
                    </div>
                    <div className="card-body" style={{ padding: 0 }}>
                        <table className="data-table">
                            <thead>
                                <tr>
                                    <th>Component</th>
                                    <th>Tests</th>
                                    <th>Coverage</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {TABLE_DATA.cto_deploys.map((row: any, idx: number) => (
                                    <tr key={idx}>
                                        <td>{row.component}</td>
                                        <td>{row.tests}</td>
                                        <td>{row.coverage}</td>
                                        <td><span className={`badge badge-${row.status === 'Passing' ? 'success' : 'warning'}`}>{row.status}</span></td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            <div className="col-4">
                <div className="card">
                    <div className="card-header"><h3 className="card-title">Backups</h3></div>
                    <div className="card-body">
                        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                            <span>Database</span>
                            <span style={{ color: 'var(--accent-green)' }}>✓ 1h ago</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export const CXADashboard = () => {
    return (
        <div className="dashboard-grid">
            <div className="col-8">
                <div className="card">
                    <div className="card-header">
                        <h3 className="card-title">Email Inbox</h3>
                        <span className="badge badge-info">47 Today</span>
                    </div>
                    <div className="card-body" style={{ padding: 0 }}>
                        <table className="data-table">
                            <thead>
                                <tr>
                                    <th>Status</th>
                                    <th>Subject</th>
                                    <th>From</th>
                                    <th>Routed To</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr><td><span className="badge badge-danger">Urgent</span></td><td>Q4 Report Review</td><td>John Smith (CFO)</td><td>CEO</td></tr>
                                <tr><td><span className="badge badge-warning">Normal</span></td><td>Project Update</td><td>Sarah Davis</td><td>COO</td></tr>
                                <tr><td><span className="badge badge-info">Low</span></td><td>Newsletter</td><td>Team</td><td>Archive</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            <div className="col-4">
                <div className="card">
                    <div className="card-header">
                        <h3 className="card-title">Human Calendar</h3>
                    </div>
                    <div className="card-body">
                        <h4 style={{ fontSize: '0.875rem', marginBottom: '0.75rem' }}>Today</h4>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                            <div style={{ padding: '0.5rem', background: 'var(--bg-tertiary)', borderLeft: '3px solid var(--accent-blue)', borderRadius: '0.25rem' }}>
                                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>09:30 AM</div>
                                <div>Strategy Sync</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

// Placeholders for others (if any needed, but coverage seems complete above)
