'use client';

import React, { useState } from 'react';
import styles from './ChairmanExecutiveSummary.module.css';

// All C-Suite plans
const ALL_PLANS = [
    { role: 'CEO', title: 'Business Plan', icon: '👔' },
    { role: 'CFO', title: 'Financial Plan', icon: '💰' },
    { role: 'CMO', title: 'Marketing Plan', icon: '📈' },
    { role: 'COO', title: 'Operations Plan', icon: '⚙️' },
    { role: 'CIO', title: 'Information Plan', icon: '🔐' },
    { role: 'CLO', title: 'Legal Plan', icon: '⚖️' },
    { role: 'CPO', title: 'Product Plan', icon: '📦' },
    { role: 'CTO', title: 'Technical Plan', icon: '🔧' },
    { role: 'CXA', title: 'Experience Plan', icon: '✨' },
];

type Period = 'weekly' | 'quarterly' | 'annual';

interface PlanSummary {
    narrative: string;
    keyMetrics: { label: string; value: string; trend: 'up' | 'down' | 'flat'; percent: number }[];
    status: 'on-track' | 'attention' | 'at-risk';
    chartData: number[]; // 7 data points for mini chart
}

// Plan summaries by role and period
const PLAN_SUMMARIES: Record<string, Record<Period, PlanSummary>> = {
    CEO: {
        weekly: {
            narrative: "Strategic alignment remains strong at 94%. Completed quarterly vision review and propagated updates to all C-Suite agents. Focus this week on validation gate progress with CMO.",
            keyMetrics: [
                { label: 'Alignment Score', value: '94%', trend: 'up', percent: 94 },
                { label: 'Decisions Made', value: '12', trend: 'up', percent: 80 },
                { label: 'Agent Syncs', value: '9/9', trend: 'flat', percent: 100 },
            ],
            status: 'on-track',
            chartData: [88, 90, 91, 89, 92, 93, 94],
        },
        quarterly: {
            narrative: "Q1 objectives 78% complete. Successfully onboarded all 9 C-Suite agents. Business plan iterations refined based on market feedback. Preparing for CTO activation pending CMO validation.",
            keyMetrics: [
                { label: 'Q1 Objectives', value: '78%', trend: 'up', percent: 78 },
                { label: 'Decisions Made', value: '156', trend: 'up', percent: 85 },
                { label: 'Strategic Pivots', value: '2', trend: 'flat', percent: 50 },
            ],
            status: 'on-track',
            chartData: [65, 68, 70, 72, 74, 76, 78],
        },
        annual: {
            narrative: "Year 1 focused on foundation building. All C-Suite agents operational. Validation framework established. Positioned for product development phase pending gate clearance.",
            keyMetrics: [
                { label: 'Annual Goals', value: '45%', trend: 'up', percent: 45 },
                { label: 'Major Milestones', value: '8/18', trend: 'up', percent: 44 },
                { label: 'Team Alignment', value: '91%', trend: 'up', percent: 91 },
            ],
            status: 'on-track',
            chartData: [20, 28, 32, 35, 38, 42, 45],
        },
    },
    CFO: {
        weekly: {
            narrative: "Token spend within budget at 64%. Daily monitoring shows efficient allocation across agents. CMO approaching budget ceiling - recommend review. Runway remains healthy at 383 days.",
            keyMetrics: [
                { label: 'Budget Used', value: '64%', trend: 'flat', percent: 64 },
                { label: 'Weekly Spend', value: '$47.80', trend: 'down', percent: 48 },
                { label: 'Runway', value: '383 days', trend: 'flat', percent: 95 },
            ],
            status: 'on-track',
            chartData: [52, 55, 58, 60, 61, 63, 64],
        },
        quarterly: {
            narrative: "Q1 financial health strong. Total spend of $612.40 against $750 quarterly budget. Token optimization strategies saved estimated $89. No overage alerts triggered.",
            keyMetrics: [
                { label: 'Q1 Budget', value: '82%', trend: 'up', percent: 82 },
                { label: 'Cost Savings', value: '$89', trend: 'up', percent: 70 },
                { label: 'Efficiency', value: '94%', trend: 'up', percent: 94 },
            ],
            status: 'on-track',
            chartData: [45, 52, 60, 68, 74, 78, 82],
        },
        annual: {
            narrative: "Seed capital of $5,000 carefully managed. Spent $2,247.80 YTD (45%). Conservative burn rate ensures 383-day runway. Revenue pipeline development underway.",
            keyMetrics: [
                { label: 'Capital Used', value: '45%', trend: 'flat', percent: 45 },
                { label: 'YTD Spend', value: '$2,247', trend: 'up', percent: 45 },
                { label: 'ROI Tracking', value: 'Pre-Rev', trend: 'flat', percent: 0 },
            ],
            status: 'on-track',
            chartData: [8, 15, 22, 28, 34, 40, 45],
        },
    },
    CMO: {
        weekly: {
            narrative: "Validation campaign in progress. TikTok content generating 3.2% engagement (above 2% threshold). 67 signups this week toward 100 target. Gate decision expected within 5 days.",
            keyMetrics: [
                { label: 'Signups', value: '67/100', trend: 'up', percent: 67 },
                { label: 'Engagement', value: '3.2%', trend: 'up', percent: 80 },
                { label: 'CPA', value: '$4.20', trend: 'down', percent: 84 },
            ],
            status: 'attention',
            chartData: [12, 24, 35, 42, 51, 59, 67],
        },
        quarterly: {
            narrative: "Marketing foundation established. Brand guidelines complete. 3 validation campaigns executed with iterative improvements. Current campaign tracking toward PROCEED decision.",
            keyMetrics: [
                { label: 'Campaigns', value: '3', trend: 'up', percent: 75 },
                { label: 'Total Signups', value: '234', trend: 'up', percent: 78 },
                { label: 'Brand Assets', value: '12', trend: 'up', percent: 100 },
            ],
            status: 'on-track',
            chartData: [15, 28, 45, 62, 78, 89, 95],
        },
        annual: {
            narrative: "Year 1 marketing focus: validation over scale. Successfully tested messaging across 3 campaigns. Building waitlist for product launch. Content library established.",
            keyMetrics: [
                { label: 'Waitlist', value: '456', trend: 'up', percent: 46 },
                { label: 'Content Pieces', value: '48', trend: 'up', percent: 80 },
                { label: 'Gate Status', value: 'Pending', trend: 'flat', percent: 67 },
            ],
            status: 'on-track',
            chartData: [5, 12, 22, 35, 48, 62, 75],
        },
    },
    COO: {
        weekly: {
            narrative: "All systems operational. 99.8% uptime maintained. Agent orchestration running smoothly. No incidents reported. Process documentation 85% complete.",
            keyMetrics: [
                { label: 'Uptime', value: '99.8%', trend: 'flat', percent: 99 },
                { label: 'Incidents', value: '0', trend: 'flat', percent: 100 },
                { label: 'Processes', value: '85%', trend: 'up', percent: 85 },
            ],
            status: 'on-track',
            chartData: [99, 99, 100, 99, 100, 100, 99],
        },
        quarterly: {
            narrative: "Operational excellence achieved. Agent coordination protocols refined. SLA compliance at 100%. Automated monitoring covering all critical paths.",
            keyMetrics: [
                { label: 'SLA Compliance', value: '100%', trend: 'flat', percent: 100 },
                { label: 'Automation', value: '78%', trend: 'up', percent: 78 },
                { label: 'Efficiency', value: '+12%', trend: 'up', percent: 85 },
            ],
            status: 'on-track',
            chartData: [92, 94, 95, 96, 97, 98, 99],
        },
        annual: {
            narrative: "Operations infrastructure built from ground up. All C-Suite agents integrated. Workflow automation at 78%. Prepared to scale with product launch.",
            keyMetrics: [
                { label: 'Infrastructure', value: '100%', trend: 'flat', percent: 100 },
                { label: 'Integration', value: '9/9', trend: 'flat', percent: 100 },
                { label: 'Scale Ready', value: 'Yes', trend: 'up', percent: 90 },
            ],
            status: 'on-track',
            chartData: [45, 58, 68, 78, 85, 92, 98],
        },
    },
    CIO: {
        weekly: {
            narrative: "12 MCP integrations active and healthy. OpenRouter latency averaging 45ms. Security audit passed. New Instagram API pending Chairman approval.",
            keyMetrics: [
                { label: 'MCPs Active', value: '12', trend: 'flat', percent: 80 },
                { label: 'API Health', value: '100%', trend: 'flat', percent: 100 },
                { label: 'Pending', value: '1', trend: 'up', percent: 50 },
            ],
            status: 'on-track',
            chartData: [10, 10, 11, 11, 12, 12, 12],
        },
        quarterly: {
            narrative: "Information infrastructure robust. All critical integrations operational. Data pipeline processing 100% of agent communications. Security posture strong.",
            keyMetrics: [
                { label: 'Integrations', value: '18', trend: 'up', percent: 90 },
                { label: 'Data Processed', value: '4.2M', trend: 'up', percent: 85 },
                { label: 'Security Score', value: 'A', trend: 'flat', percent: 95 },
            ],
            status: 'on-track',
            chartData: [8, 10, 12, 14, 15, 17, 18],
        },
        annual: {
            narrative: "Complete information architecture established. All agents connected via secure channels. BigQuery analytics operational. Ready for scale.",
            keyMetrics: [
                { label: 'Architecture', value: '100%', trend: 'flat', percent: 100 },
                { label: 'Uptime', value: '99.9%', trend: 'up', percent: 99 },
                { label: 'Compliance', value: '100%', trend: 'flat', percent: 100 },
            ],
            status: 'on-track',
            chartData: [40, 55, 68, 78, 85, 92, 98],
        },
    },
    CLO: {
        weekly: {
            narrative: "All operations compliant. Privacy policy current. Terms of service reviewed. No legal issues identified. GDPR readiness at 100% for EU expansion.",
            keyMetrics: [
                { label: 'Compliance', value: '100%', trend: 'flat', percent: 100 },
                { label: 'Reviews Done', value: '4', trend: 'up', percent: 100 },
                { label: 'Issues', value: '0', trend: 'flat', percent: 100 },
            ],
            status: 'on-track',
            chartData: [100, 100, 100, 100, 100, 100, 100],
        },
        quarterly: {
            narrative: "Legal framework complete. All required policies in place. Agent governance documentation finalized. IP protection strategy implemented.",
            keyMetrics: [
                { label: 'Policies', value: '12/12', trend: 'flat', percent: 100 },
                { label: 'Contracts', value: '8', trend: 'up', percent: 80 },
                { label: 'Risk Level', value: 'Low', trend: 'flat', percent: 95 },
            ],
            status: 'on-track',
            chartData: [85, 88, 92, 95, 98, 100, 100],
        },
        annual: {
            narrative: "Comprehensive legal protection established. All regulatory requirements met. Agent ethics framework operational. Ready for commercial operations.",
            keyMetrics: [
                { label: 'Legal Ready', value: '100%', trend: 'flat', percent: 100 },
                { label: 'Regulations', value: '8/8', trend: 'flat', percent: 100 },
                { label: 'Ethics', value: 'Active', trend: 'flat', percent: 100 },
            ],
            status: 'on-track',
            chartData: [65, 72, 80, 88, 94, 98, 100],
        },
    },
    CPO: {
        weekly: {
            narrative: "Product roadmap on track. 3 features in development. User research insights compiled. Awaiting CTO activation to begin build phase.",
            keyMetrics: [
                { label: 'Features', value: '3 WIP', trend: 'flat', percent: 60 },
                { label: 'Research', value: '12 interviews', trend: 'up', percent: 80 },
                { label: 'Roadmap', value: 'v1.2', trend: 'up', percent: 75 },
            ],
            status: 'on-track',
            chartData: [45, 50, 55, 58, 62, 65, 68],
        },
        quarterly: {
            narrative: "Product strategy defined. MVP scope locked. User personas validated through CMO research. Ready for development phase.",
            keyMetrics: [
                { label: 'MVP Scope', value: '100%', trend: 'flat', percent: 100 },
                { label: 'Personas', value: '4', trend: 'flat', percent: 100 },
                { label: 'Backlog', value: '48 items', trend: 'up', percent: 70 },
            ],
            status: 'on-track',
            chartData: [25, 40, 55, 68, 78, 88, 95],
        },
        annual: {
            narrative: "Product foundation complete. Clear vision, validated personas, prioritized roadmap. Positioned for rapid development once CTO gate clears.",
            keyMetrics: [
                { label: 'Vision', value: 'Locked', trend: 'flat', percent: 100 },
                { label: 'Validation', value: '85%', trend: 'up', percent: 85 },
                { label: 'Launch Ready', value: 'Pending', trend: 'flat', percent: 60 },
            ],
            status: 'on-track',
            chartData: [15, 28, 42, 55, 68, 78, 85],
        },
    },
    CTO: {
        weekly: {
            narrative: "Gate status: PENDING. Awaiting CMO validation PROCEED decision. Architecture documentation complete. Tech stack selected. Ready to begin on gate clearance.",
            keyMetrics: [
                { label: 'Gate Status', value: 'Pending', trend: 'flat', percent: 0 },
                { label: 'Architecture', value: '100%', trend: 'flat', percent: 100 },
                { label: 'Stack Ready', value: 'Yes', trend: 'flat', percent: 100 },
            ],
            status: 'attention',
            chartData: [0, 0, 0, 0, 0, 0, 0],
        },
        quarterly: {
            narrative: "Technical foundation prepared during gate hold. Architecture decisions finalized. Development environment configured. Team ready for sprint 1.",
            keyMetrics: [
                { label: 'Prep Work', value: '100%', trend: 'flat', percent: 100 },
                { label: 'Docs', value: '24 pages', trend: 'up', percent: 90 },
                { label: 'Blocked Days', value: '45', trend: 'up', percent: 50 },
            ],
            status: 'attention',
            chartData: [10, 25, 45, 65, 80, 92, 100],
        },
        annual: {
            narrative: "Year 1 in preparation mode. Gate structure ensures validated product before build. Technical debt: zero. Architecture: future-proof. Awaiting green light.",
            keyMetrics: [
                { label: 'Tech Debt', value: '$0', trend: 'flat', percent: 100 },
                { label: 'Readiness', value: '100%', trend: 'flat', percent: 100 },
                { label: 'Releases', value: '0', trend: 'flat', percent: 0 },
            ],
            status: 'attention',
            chartData: [0, 15, 35, 55, 75, 90, 100],
        },
    },
    CXA: {
        weekly: {
            narrative: "Customer experience framework active. Support response time averaging 2.1 hours. Satisfaction score 4.2/5. Journey mapping 80% complete.",
            keyMetrics: [
                { label: 'Satisfaction', value: '4.2/5', trend: 'up', percent: 84 },
                { label: 'Response Time', value: '2.1h', trend: 'down', percent: 79 },
                { label: 'Journey Maps', value: '80%', trend: 'up', percent: 80 },
            ],
            status: 'on-track',
            chartData: [3.8, 3.9, 4.0, 4.0, 4.1, 4.1, 4.2],
        },
        quarterly: {
            narrative: "Experience strategy aligned with brand. All touchpoints mapped. Feedback loops established. Voice of customer program active.",
            keyMetrics: [
                { label: 'NPS', value: '+42', trend: 'up', percent: 71 },
                { label: 'Touchpoints', value: '18', trend: 'up', percent: 90 },
                { label: 'Feedback', value: '156', trend: 'up', percent: 78 },
            ],
            status: 'on-track',
            chartData: [28, 32, 35, 38, 40, 41, 42],
        },
        annual: {
            narrative: "Customer-centric foundation built. Experience principles documented. Team trained on empathy-first approach. Ready to scale with product.",
            keyMetrics: [
                { label: 'CX Maturity', value: 'Level 3', trend: 'up', percent: 75 },
                { label: 'Principles', value: '8/8', trend: 'flat', percent: 100 },
                { label: 'Scale Ready', value: 'Yes', trend: 'up', percent: 85 },
            ],
            status: 'on-track',
            chartData: [35, 45, 52, 60, 68, 75, 82],
        },
    },
};

export default function ChairmanExecutiveSummary() {
    const [selectedPeriod, setSelectedPeriod] = useState<Period>('weekly');
    const [selectedPlan, setSelectedPlan] = useState<string>('CEO');

    const summary = PLAN_SUMMARIES[selectedPlan]?.[selectedPeriod];
    const planInfo = ALL_PLANS.find(p => p.role === selectedPlan);

    const getStatusBadge = (status: PlanSummary['status']) => {
        switch (status) {
            case 'on-track': return { label: 'On Track', class: styles.statusOnTrack };
            case 'attention': return { label: 'Needs Attention', class: styles.statusAttention };
            case 'at-risk': return { label: 'At Risk', class: styles.statusAtRisk };
        }
    };

    const getTrendIcon = (trend: 'up' | 'down' | 'flat') => {
        switch (trend) {
            case 'up': return '↑';
            case 'down': return '↓';
            case 'flat': return '→';
        }
    };

    const getTrendClass = (trend: 'up' | 'down' | 'flat') => {
        switch (trend) {
            case 'up': return styles.trendUp;
            case 'down': return styles.trendDown;
            case 'flat': return styles.trendFlat;
        }
    };

    // Generate mini sparkline chart
    const renderMiniChart = (data: number[]) => {
        const max = Math.max(...data);
        const min = Math.min(...data);
        const range = max - min || 1;
        const height = 40;
        const width = 140;
        const stepX = width / (data.length - 1);

        const points = data.map((val, i) => {
            const x = i * stepX;
            const y = height - ((val - min) / range) * height;
            return `${x},${y}`;
        }).join(' ');

        return (
            <svg className={styles.miniChart} viewBox={`0 0 ${width} ${height}`}>
                <polyline
                    points={points}
                    fill="none"
                    stroke="#3b82f6"
                    strokeWidth="2"
                />
                {data.map((val, i) => (
                    <circle
                        key={i}
                        cx={i * stepX}
                        cy={height - ((val - min) / range) * height}
                        r="3"
                        fill={i === data.length - 1 ? '#3b82f6' : '#1e293b'}
                        stroke="#3b82f6"
                        strokeWidth="1"
                    />
                ))}
            </svg>
        );
    };

    const statusBadge = summary ? getStatusBadge(summary.status) : null;

    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <div className={styles.titleSection}>
                    <span className={styles.icon}>🏛️</span>
                    <span className={styles.title}>Executive Summary</span>
                </div>
                <div className={styles.periodTabs}>
                    <button
                        className={`${styles.periodTab} ${selectedPeriod === 'weekly' ? styles.active : ''}`}
                        onClick={() => setSelectedPeriod('weekly')}
                    >
                        Weekly
                    </button>
                    <button
                        className={`${styles.periodTab} ${selectedPeriod === 'quarterly' ? styles.active : ''}`}
                        onClick={() => setSelectedPeriod('quarterly')}
                    >
                        Quarterly
                    </button>
                    <button
                        className={`${styles.periodTab} ${selectedPeriod === 'annual' ? styles.active : ''}`}
                        onClick={() => setSelectedPeriod('annual')}
                    >
                        Annual
                    </button>
                </div>
            </div>

            <div className={styles.body}>
                {/* Left side: All Plans TOC */}
                <div className={styles.plansPanel}>
                    <div className={styles.panelHeader}>C-Suite Plans</div>
                    <div className={styles.plansList}>
                        {ALL_PLANS.map((plan) => {
                            const planSummary = PLAN_SUMMARIES[plan.role]?.[selectedPeriod];
                            const isSelected = selectedPlan === plan.role;
                            return (
                                <button
                                    key={plan.role}
                                    className={`${styles.planItem} ${isSelected ? styles.selected : ''}`}
                                    onClick={() => setSelectedPlan(plan.role)}
                                >
                                    <span className={styles.planIcon}>{plan.icon}</span>
                                    <div className={styles.planInfo}>
                                        <span className={styles.planRole}>{plan.role}</span>
                                        <span className={styles.planTitle}>{plan.title}</span>
                                    </div>
                                    {planSummary && (
                                        <span className={`${styles.planStatus} ${
                                            planSummary.status === 'on-track' ? styles.statusOnTrack :
                                            planSummary.status === 'attention' ? styles.statusAttention :
                                            styles.statusAtRisk
                                        }`}>●</span>
                                    )}
                                </button>
                            );
                        })}
                    </div>
                </div>

                {/* Right side: Selected Plan Summary */}
                <div className={styles.summaryPanel}>
                    {summary && planInfo && (
                        <>
                            <div className={styles.summaryHeader}>
                                <div className={styles.summaryTitle}>
                                    <span className={styles.summaryIcon}>{planInfo.icon}</span>
                                    <span>{planInfo.title}</span>
                                </div>
                                {statusBadge && (
                                    <span className={`${styles.statusBadge} ${statusBadge.class}`}>
                                        {statusBadge.label}
                                    </span>
                                )}
                            </div>

                            {/* Narrative */}
                            <div className={styles.narrative}>
                                {summary.narrative}
                            </div>

                            {/* Chart */}
                            <div className={styles.chartSection}>
                                <div className={styles.chartLabel}>
                                    {selectedPeriod === 'weekly' ? 'Last 7 Days' :
                                     selectedPeriod === 'quarterly' ? 'Last 7 Weeks' : 'Last 7 Months'}
                                </div>
                                {renderMiniChart(summary.chartData)}
                            </div>

                            {/* Key Metrics */}
                            <div className={styles.metricsSection}>
                                {summary.keyMetrics.map((metric, idx) => (
                                    <div key={idx} className={styles.metricItem}>
                                        <div className={styles.metricHeader}>
                                            <span className={styles.metricLabel}>{metric.label}</span>
                                            <span className={`${styles.metricTrend} ${getTrendClass(metric.trend)}`}>
                                                {getTrendIcon(metric.trend)}
                                            </span>
                                        </div>
                                        <div className={styles.metricValue}>{metric.value}</div>
                                        <div className={styles.metricBar}>
                                            <div
                                                className={styles.metricBarFill}
                                                style={{ width: `${metric.percent}%` }}
                                            />
                                        </div>
                                    </div>
                                ))}
                            </div>

                            {/* View Full Plan Link */}
                            <a
                                href={`/${planInfo.role.toLowerCase()}`}
                                className={styles.viewFullLink}
                            >
                                View Full {planInfo.title} →
                            </a>
                        </>
                    )}
                </div>
            </div>
        </div>
    );
}
