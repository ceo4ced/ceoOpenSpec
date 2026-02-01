'use client';

import React, { useState } from 'react';
import styles from './ChairmanTabs.module.css';

type TabId = 'finances' | 'agents' | 'mcps' | 'tokens' | 'models' | 'logs';

interface Tab {
    id: TabId;
    label: string;
    icon: string;
}

const TABS: Tab[] = [
    { id: 'finances', label: 'Finances', icon: '💰' },
    { id: 'agents', label: 'Agents', icon: '🤖' },
    { id: 'mcps', label: 'MCPs', icon: '🔌' },
    { id: 'tokens', label: 'Tokens', icon: '🪙' },
    { id: 'models', label: 'Models', icon: '🧠' },
    { id: 'logs', label: 'Logs', icon: '📋' },
];

// Mock data for demonstration
const MOCK_DATA = {
    finances: {
        seedCapital: 5000,
        spent: 247.80,
        remaining: 4752.20,
        runway: 383,
        dailyBudget: 50,
        dailySpent: 12.40,
        monthlyBudget: 500,
        monthlySpent: 247.80,
    },
    agents: [
        { id: 'ceo', name: 'CEO', status: 'active', task: 'Processing vision update', tokens: 2340, cost: 0.07 },
        { id: 'cfo', name: 'CFO', status: 'idle', task: 'Awaiting commands', tokens: 0, cost: 0 },
        { id: 'cmo', name: 'CMO', status: 'working', task: 'Generating TikTok content', tokens: 8920, cost: 0.27 },
        { id: 'coo', name: 'COO', status: 'idle', task: 'Monitoring operations', tokens: 0, cost: 0 },
        { id: 'cio', name: 'CIO', status: 'idle', task: 'MCP health check', tokens: 0, cost: 0 },
        { id: 'clo', name: 'CLO', status: 'idle', task: 'Compliance monitoring', tokens: 0, cost: 0 },
        { id: 'cpo', name: 'CPO', status: 'idle', task: 'Roadmap planning', tokens: 0, cost: 0 },
        { id: 'cto', name: 'CTO', status: 'gated', task: 'Awaiting validation gate', tokens: 0, cost: 0 },
        { id: 'cxa', name: 'CXA', status: 'idle', task: 'Journey mapping', tokens: 0, cost: 0 },
    ],
    mcps: [
        { name: 'OpenRouter', status: 'online', calls: 234, cost: 8.20, hasCost: true },
        { name: 'GitKraken', status: 'online', calls: 45, cost: 0, hasCost: false },
        { name: 'Nano Banana', status: 'online', calls: 8, cost: 2.40, hasCost: true },
        { name: 'TikTok', status: 'online', calls: 2, cost: 0, hasCost: false },
        { name: 'BigQuery', status: 'online', calls: 12, cost: 0.80, hasCost: true },
        { name: 'Telegram', status: 'online', calls: 18, cost: 0, hasCost: false },
    ],
    tokens: {
        total: 4234567,
        input: 3102456,
        output: 1132111,
        cost: 189.40,
        byAgent: [
            { agent: 'CEO', input: 892340, output: 412230, total: 1304570, cost: 52.40, budgetPercent: 35 },
            { agent: 'CMO', input: 1456780, output: 523450, total: 1980230, cost: 89.40, budgetPercent: 90 },
            { agent: 'CFO', input: 342120, output: 98340, total: 440460, cost: 15.20, budgetPercent: 30 },
            { agent: 'COO', input: 201340, output: 52120, total: 253460, cost: 8.40, budgetPercent: 17 },
            { agent: 'CIO', input: 123450, output: 34560, total: 158010, cost: 5.80, budgetPercent: 12 },
            { agent: 'CLO', input: 56780, output: 8900, total: 65680, cost: 12.00, budgetPercent: 24 },
            { agent: 'CPO', input: 29646, output: 2511, total: 32157, cost: 6.20, budgetPercent: 25 },
        ],
    },
    models: [
        { name: 'claude-3.5-sonnet', provider: 'Anthropic', inputCost: 3.00, outputCost: 15.00, quality: 4 },
        { name: 'claude-3-opus', provider: 'Anthropic', inputCost: 15.00, outputCost: 75.00, quality: 5 },
        { name: 'claude-3-haiku', provider: 'Anthropic', inputCost: 0.25, outputCost: 1.25, quality: 3 },
        { name: 'gpt-4o', provider: 'OpenAI', inputCost: 2.50, outputCost: 10.00, quality: 4 },
        { name: 'gpt-4o-mini', provider: 'OpenAI', inputCost: 0.15, outputCost: 0.60, quality: 3 },
        { name: 'gemini-2.0-flash', provider: 'Google', inputCost: 0.10, outputCost: 0.40, quality: 3 },
    ],
    logs: [
        { time: '09:15:23', agent: 'CMO', type: 'thinking', message: 'Analyzing TikTok performance data...', model: 'claude-3.5-sonnet' },
        { time: '09:10:45', agent: 'CEO', type: 'command', message: 'ceo.vision - Vision update from human', tokens: 2340, cost: 0.07 },
        { time: '09:05:12', agent: 'HUMAN', type: 'approval', message: 'Content approved for 3pm publish' },
        { time: '09:00:00', agent: 'CFO', type: 'budget', message: 'Daily budget reset to $50.00' },
        { time: '08:45:30', agent: 'CIO', type: 'mcp', message: 'OpenRouter health check - Status: Healthy, Latency: 45ms' },
    ],
};

export default function ChairmanTabs() {
    const [activeTab, setActiveTab] = useState<TabId>('finances');

    const formatNumber = (num: number) => {
        if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
        if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
        return num.toLocaleString();
    };

    const renderFinances = () => (
        <div className={styles.tabContent}>
            <div className={styles.section}>
                <h3 className={styles.sectionTitle}>Seed Capital</h3>
                <div className={styles.capitalGrid}>
                    <div className={styles.capitalItem}>
                        <span className={styles.capitalLabel}>Initial</span>
                        <span className={styles.capitalValue}>${MOCK_DATA.finances.seedCapital.toLocaleString()}</span>
                    </div>
                    <div className={styles.capitalItem}>
                        <span className={styles.capitalLabel}>Spent</span>
                        <span className={styles.capitalValue} style={{ color: '#f59e0b' }}>${MOCK_DATA.finances.spent.toFixed(2)}</span>
                    </div>
                    <div className={styles.capitalItem}>
                        <span className={styles.capitalLabel}>Remaining</span>
                        <span className={styles.capitalValue} style={{ color: '#10b981' }}>${MOCK_DATA.finances.remaining.toFixed(2)}</span>
                    </div>
                    <div className={styles.capitalItem}>
                        <span className={styles.capitalLabel}>Runway</span>
                        <span className={styles.capitalValue}>{MOCK_DATA.finances.runway} days</span>
                    </div>
                </div>
                <div className={styles.progressBar}>
                    <div className={styles.progressFill} style={{ width: `${(MOCK_DATA.finances.remaining / MOCK_DATA.finances.seedCapital) * 100}%` }} />
                </div>
                <div className={styles.progressLabel}>{((MOCK_DATA.finances.remaining / MOCK_DATA.finances.seedCapital) * 100).toFixed(1)}% remaining</div>
            </div>

            <div className={styles.section}>
                <h3 className={styles.sectionTitle}>Budget Status</h3>
                <div className={styles.budgetGrid}>
                    <div className={styles.budgetCard}>
                        <div className={styles.budgetLabel}>Today</div>
                        <div className={styles.budgetValue}>${MOCK_DATA.finances.dailySpent.toFixed(2)} / ${MOCK_DATA.finances.dailyBudget}</div>
                        <div className={styles.progressBar}>
                            <div className={styles.progressFill} style={{ width: `${(MOCK_DATA.finances.dailySpent / MOCK_DATA.finances.dailyBudget) * 100}%` }} />
                        </div>
                    </div>
                    <div className={styles.budgetCard}>
                        <div className={styles.budgetLabel}>This Month</div>
                        <div className={styles.budgetValue}>${MOCK_DATA.finances.monthlySpent.toFixed(2)} / ${MOCK_DATA.finances.monthlyBudget}</div>
                        <div className={styles.progressBar}>
                            <div className={styles.progressFill} style={{ width: `${(MOCK_DATA.finances.monthlySpent / MOCK_DATA.finances.monthlyBudget) * 100}%` }} />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );

    const renderAgents = () => (
        <div className={styles.tabContent}>
            <div className={styles.agentGrid}>
                {MOCK_DATA.agents.map(agent => (
                    <div key={agent.id} className={`${styles.agentCard} ${styles[agent.status]}`}>
                        <div className={styles.agentHeader}>
                            <span className={styles.agentName}>{agent.name}</span>
                            <span className={`${styles.agentStatus} ${styles[agent.status]}`}>
                                {agent.status === 'active' ? '🟢' : agent.status === 'working' ? '🟡' : agent.status === 'gated' ? '⬜' : '🟢'}
                                {agent.status.charAt(0).toUpperCase() + agent.status.slice(1)}
                            </span>
                        </div>
                        <div className={styles.agentTask}>{agent.task}</div>
                        {agent.tokens > 0 && (
                            <div className={styles.agentStats}>
                                Session: {formatNumber(agent.tokens)} tokens | ${agent.cost.toFixed(2)}
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );

    const renderMCPs = () => (
        <div className={styles.tabContent}>
            <div className={styles.mcpGrid}>
                {MOCK_DATA.mcps.map(mcp => (
                    <div key={mcp.name} className={styles.mcpCard}>
                        <div className={styles.mcpHeader}>
                            <span className={`${styles.mcpStatus} ${mcp.status === 'online' ? styles.online : styles.offline}`}>●</span>
                            <span className={styles.mcpName}>{mcp.name}</span>
                            {mcp.hasCost && <span className={styles.mcpCostBadge}>Has Cost</span>}
                        </div>
                        <div className={styles.mcpStats}>
                            <span>Today: {mcp.calls} calls</span>
                            {mcp.hasCost && <span>Cost: ${mcp.cost.toFixed(2)}</span>}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );

    const renderTokens = () => (
        <div className={styles.tabContent}>
            <div className={styles.section}>
                <h3 className={styles.sectionTitle}>Summary (This Month)</h3>
                <div className={styles.tokenSummary}>
                    <div className={styles.tokenStat}>
                        <span className={styles.tokenLabel}>Total Tokens</span>
                        <span className={styles.tokenValue}>{formatNumber(MOCK_DATA.tokens.total)}</span>
                    </div>
                    <div className={styles.tokenStat}>
                        <span className={styles.tokenLabel}>Input</span>
                        <span className={styles.tokenValue}>{formatNumber(MOCK_DATA.tokens.input)} (73%)</span>
                    </div>
                    <div className={styles.tokenStat}>
                        <span className={styles.tokenLabel}>Output</span>
                        <span className={styles.tokenValue}>{formatNumber(MOCK_DATA.tokens.output)} (27%)</span>
                    </div>
                    <div className={styles.tokenStat}>
                        <span className={styles.tokenLabel}>Total Cost</span>
                        <span className={styles.tokenValue}>${MOCK_DATA.tokens.cost.toFixed(2)}</span>
                    </div>
                </div>
            </div>

            <div className={styles.section}>
                <h3 className={styles.sectionTitle}>By Agent</h3>
                <table className={styles.tokenTable}>
                    <thead>
                        <tr>
                            <th>Agent</th>
                            <th>Input</th>
                            <th>Output</th>
                            <th>Total</th>
                            <th>Cost</th>
                            <th>% Budget</th>
                        </tr>
                    </thead>
                    <tbody>
                        {MOCK_DATA.tokens.byAgent.map(row => (
                            <tr key={row.agent}>
                                <td>{row.agent}</td>
                                <td>{formatNumber(row.input)}</td>
                                <td>{formatNumber(row.output)}</td>
                                <td>{formatNumber(row.total)}</td>
                                <td>${row.cost.toFixed(2)}</td>
                                <td>
                                    <span className={row.budgetPercent > 80 ? styles.warning : styles.ok}>
                                        {row.budgetPercent}%
                                    </span>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );

    const renderModels = () => (
        <div className={styles.tabContent}>
            <div className={styles.section}>
                <h3 className={styles.sectionTitle}>Available Models (via OpenRouter)</h3>
                <table className={styles.modelTable}>
                    <thead>
                        <tr>
                            <th>Model</th>
                            <th>Provider</th>
                            <th>Input Cost/1M</th>
                            <th>Output Cost/1M</th>
                            <th>Quality</th>
                        </tr>
                    </thead>
                    <tbody>
                        {MOCK_DATA.models.map(model => (
                            <tr key={model.name}>
                                <td className={styles.modelName}>{model.name}</td>
                                <td>{model.provider}</td>
                                <td>${model.inputCost.toFixed(2)}</td>
                                <td>${model.outputCost.toFixed(2)}</td>
                                <td>{'⭐'.repeat(model.quality)}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );

    const renderLogs = () => (
        <div className={styles.tabContent}>
            <div className={styles.logList}>
                {MOCK_DATA.logs.map((log, idx) => (
                    <div key={idx} className={`${styles.logEntry} ${styles[log.type]}`}>
                        <span className={styles.logIcon}>
                            {log.type === 'thinking' ? '🧠' :
                             log.type === 'command' ? '⚙️' :
                             log.type === 'approval' ? '✅' :
                             log.type === 'budget' ? '💰' : '🔌'}
                        </span>
                        <span className={styles.logTime}>{log.time}</span>
                        <span className={styles.logAgent}>{log.agent}</span>
                        <span className={styles.logMessage}>{log.message}</span>
                        {log.tokens && (
                            <span className={styles.logTokens}>{formatNumber(log.tokens)} tokens | ${log.cost?.toFixed(2)}</span>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );

    const renderTabContent = () => {
        switch (activeTab) {
            case 'finances': return renderFinances();
            case 'agents': return renderAgents();
            case 'mcps': return renderMCPs();
            case 'tokens': return renderTokens();
            case 'models': return renderModels();
            case 'logs': return renderLogs();
        }
    };

    return (
        <div className={styles.container}>
            <div className={styles.tabBar}>
                {TABS.map(tab => (
                    <button
                        key={tab.id}
                        className={`${styles.tab} ${activeTab === tab.id ? styles.active : ''}`}
                        onClick={() => setActiveTab(tab.id)}
                    >
                        <span className={styles.tabIcon}>{tab.icon}</span>
                        <span className={styles.tabLabel}>{tab.label}</span>
                    </button>
                ))}
            </div>
            {renderTabContent()}
        </div>
    );
}
