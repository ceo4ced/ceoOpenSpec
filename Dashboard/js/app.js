// C-Suite Dashboard Application

class Dashboard {
    constructor() {
        this.currentPage = 'chairman';
        this.init();
    }

    init() {
        this.bindEvents();
        this.updateTimestamp();
        this.loadPage('chairman');

        // Update timestamp every minute
        setInterval(() => this.updateTimestamp(), 60000);
    }

    bindEvents() {
        // Navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const page = item.dataset.page;
                this.navigateTo(page);
            });
        });

        // Profile sidebar close
        document.getElementById('closeProfile').addEventListener('click', () => {
            this.closeProfile();
        });

        // Red Phone button
        document.getElementById('redPhoneBtn').addEventListener('click', () => {
            this.openRedPhoneModal();
        });

        // Modal close buttons
        document.querySelectorAll('.close-modal').forEach(btn => {
            btn.addEventListener('click', () => {
                this.closeAllModals();
            });
        });

        // Send red phone alert
        document.getElementById('sendRedPhone').addEventListener('click', () => {
            this.sendRedPhoneAlert();
        });

        // Refresh button
        document.getElementById('refreshBtn').addEventListener('click', () => {
            this.refresh();
        });

        // Click outside modal to close
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.closeAllModals();
                }
            });
        });
    }

    navigateTo(page) {
        // Update nav active state
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
            if (item.dataset.page === page) {
                item.classList.add('active');
            }
        });

        this.currentPage = page;
        this.loadPage(page);
    }

    loadPage(page) {
        const agent = AGENTS[page];
        const metrics = METRICS[page];

        // Update page title
        document.getElementById('pageTitle').textContent = `${agent.name} Dashboard`;

        // Generate page content
        let content = '';

        // Metrics cards
        content += this.generateMetricsCards(metrics.cards);

        // Page-specific content
        content += this.generatePageContent(page);

        document.getElementById('dashboardContent').innerHTML = content;

        // Bind dynamic events
        this.bindDynamicEvents();
    }

    generateMetricsCards(cards) {
        let html = '<div class="metrics-grid">';

        cards.forEach(card => {
            const trendClass = card.trend === 'up' ? 'up' : card.trend === 'down' ? 'down' : 'neutral';
            const trendIcon = card.trend === 'up' ? '▲' : card.trend === 'down' ? '▼' : '•';

            html += `
                <div class="metric-card">
                    <div class="metric-header">
                        <span class="metric-label">${card.label}</span>
                        <span class="metric-icon">${card.icon}</span>
                    </div>
                    <div class="metric-value">${card.value}</div>
                    <div class="metric-change ${trendClass}">
                        <span>${trendIcon}</span>
                        <span>${card.change}</span>
                    </div>
                </div>
            `;
        });

        html += '</div>';
        return html;
    }

    generatePageContent(page) {
        switch (page) {
            case 'chairman':
                return this.generateChairmanContent();
            case 'ceo':
                return this.generateCEOContent();
            case 'cfo':
                return this.generateCFOContent();
            case 'cmo':
                return this.generateCMOContent();
            case 'coo':
                return this.generateCOOContent();
            case 'cio':
                return this.generateCIOContent();
            case 'clo':
                return this.generateCLOContent();
            case 'cpo':
                return this.generateCPOContent();
            case 'cto':
                return this.generateCTOContent();
            case 'cxa':
                return this.generateCXAContent();
            default:
                return '';
        }
    }

    generateChairmanContent() {
        let html = '';

        // Red Phone Alerts
        if (RED_PHONE_ALERTS.length > 0) {
            html += `
                <div class="alerts-section">
                    <div class="alerts-header">
                        <span>🚨</span>
                        <span>RED PHONE ALERTS</span>
                    </div>
                    ${RED_PHONE_ALERTS.map(alert => `
                        <div class="alert-item">
                            <div class="alert-priority"></div>
                            <div class="alert-content">${alert.message}</div>
                            <button class="btn btn-secondary">Acknowledge</button>
                        </div>
                    `).join('')}
                </div>
            `;
        }

        html += '<div class="dashboard-grid">';

        // Agent Status Grid
        html += `
            <div class="col-8">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Agent Status Grid</h3>
                        <span class="badge badge-success">All Online</span>
                    </div>
                    <div class="card-body">
                        <div class="agent-grid">
                            ${this.generateAgentCards()}
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Pending Approvals
        html += `
            <div class="col-4">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Pending Approvals</h3>
                        <span class="badge badge-warning">${PENDING_APPROVALS.length}</span>
                    </div>
                    <div class="card-body">
                        <div class="approval-list">
                            ${PENDING_APPROVALS.map(item => `
                                <div class="approval-item ${item.priority}">
                                    <div class="approval-content">
                                        <div class="approval-title">${item.title}</div>
                                        <div class="approval-meta">From ${item.from} • ${item.time}</div>
                                    </div>
                                    <div class="approval-actions">
                                        <button class="btn btn-success">✓</button>
                                        <button class="btn btn-danger">✗</button>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
        `;

        html += '</div>';
        return html;
    }

    generateAgentCards() {
        const agents = ['ceo', 'cfo', 'cmo', 'coo', 'cio', 'clo', 'cpo', 'cto', 'cxa'];

        return agents.map(key => {
            const agent = AGENTS[key];
            const status = AGENT_STATUS[key];

            return `
                <div class="agent-card" data-agent="${key}">
                    <div class="agent-avatar">
                        <div class="placeholder">${agent.icon}</div>
                        <div class="agent-status-indicator ${status.status}"></div>
                    </div>
                    <div class="agent-info">
                        <div class="agent-name">${agent.name}</div>
                        <div class="agent-role">${agent.role}</div>
                        <div class="agent-task">${status.task}</div>
                    </div>
                    <div class="agent-meta">
                        <div class="agent-tokens">${status.tokens} tokens</div>
                    </div>
                </div>
            `;
        }).join('');
    }

    generateCEOContent() {
        let html = '<div class="dashboard-grid">';

        // Agent Overview
        html += `
            <div class="col-8">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">C-Suite Status</h3>
                    </div>
                    <div class="card-body">
                        <div class="agent-grid">
                            ${this.generateAgentCards()}
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Mission Alignment
        html += `
            <div class="col-4">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Mission Alignment</h3>
                    </div>
                    <div class="card-body">
                        <div style="text-align: center; margin-bottom: 1rem;">
                            <div style="font-size: 3rem; font-weight: 700; color: var(--accent-gold);">78%</div>
                            <div style="color: var(--text-muted);">Overall Alignment Score</div>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill success" style="width: 78%;"></div>
                        </div>
                        <div style="margin-top: 1.5rem;">
                            <h4 style="font-size: 0.875rem; margin-bottom: 0.75rem;">By Objective</h4>
                            <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                                <div><span style="color: var(--text-muted);">Revenue Growth</span> <span style="float: right">85%</span></div>
                                <div class="progress-bar"><div class="progress-fill success" style="width: 85%;"></div></div>
                                <div><span style="color: var(--text-muted);">Customer Satisfaction</span> <span style="float: right">72%</span></div>
                                <div class="progress-bar"><div class="progress-fill warning" style="width: 72%;"></div></div>
                                <div><span style="color: var(--text-muted);">Operational Excellence</span> <span style="float: right">80%</span></div>
                                <div class="progress-bar"><div class="progress-fill success" style="width: 80%;"></div></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        html += '</div>';
        return html;
    }

    generateCFOContent() {
        let html = '<div class="dashboard-grid">';

        // Token Budget
        html += `
            <div class="col-6">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Monthly Token Budget</h3>
                    </div>
                    <div class="card-body">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                            <div>
                                <div style="color: var(--text-muted); font-size: 0.875rem;">Total Budget</div>
                                <div style="font-size: 1.5rem; font-weight: 700;">$5,000</div>
                            </div>
                            <div style="text-align: right;">
                                <div style="color: var(--text-muted); font-size: 0.875rem;">Used</div>
                                <div style="font-size: 1.5rem; font-weight: 700; color: var(--accent-gold);">$3,210 (64%)</div>
                            </div>
                        </div>
                        <div class="progress-bar" style="height: 12px;">
                            <div class="progress-fill warning" style="width: 64%;"></div>
                        </div>
                        <div style="margin-top: 0.5rem; color: var(--text-muted); font-size: 0.875rem;">
                            Remaining: $1,790
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Expense Breakdown
        html += `
            <div class="col-6">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Expense Breakdown</h3>
                    </div>
                    <div class="card-body">
                        <div class="bar-chart">
                            <div class="bar-row">
                                <span class="bar-label">AI/LLM</span>
                                <div class="bar-track">
                                    <div class="bar-value" style="width: 59%; background: var(--gradient-purple);">59%</div>
                                </div>
                            </div>
                            <div class="bar-row">
                                <span class="bar-label">Infrastructure</span>
                                <div class="bar-track">
                                    <div class="bar-value" style="width: 18%; background: var(--gradient-blue);">18%</div>
                                </div>
                            </div>
                            <div class="bar-row">
                                <span class="bar-label">Software</span>
                                <div class="bar-track">
                                    <div class="bar-value" style="width: 10%; background: var(--gradient-green);">10%</div>
                                </div>
                            </div>
                            <div class="bar-row">
                                <span class="bar-label">Marketing</span>
                                <div class="bar-track">
                                    <div class="bar-value" style="width: 8%; background: var(--accent-pink);">8%</div>
                                </div>
                            </div>
                            <div class="bar-row">
                                <span class="bar-label">Other</span>
                                <div class="bar-track">
                                    <div class="bar-value" style="width: 5%; background: var(--text-muted);">5%</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Controls
        html += `
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Financial Controls</h3>
                    </div>
                    <div class="card-body" style="display: flex; gap: 1rem;">
                        <button class="btn btn-danger">🚨 Emergency Pause All Spending</button>
                        <button class="btn btn-secondary">📊 Adjust Budgets</button>
                        <button class="btn btn-secondary">💰 Switch to Cost Mode</button>
                    </div>
                </div>
            </div>
        `;

        html += '</div>';
        return html;
    }

    generateCMOContent() {
        let html = '';

        // Tabs
        html += `
            <div class="tab-nav">
                <button class="tab-btn active" data-tab="acquisition">Acquisition</button>
                <button class="tab-btn" data-tab="engagement">Engagement & Brand</button>
            </div>
        `;

        html += '<div class="dashboard-grid">';

        // ROAS by Channel
        html += `
            <div class="col-6">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">ROAS by Channel</h3>
                    </div>
                    <div class="card-body">
                        <div class="bar-chart">
                            ${TABLE_DATA.cmo_roas.map(row => `
                                <div class="bar-row">
                                    <span class="bar-label">${row.channel}</span>
                                    <div class="bar-track">
                                        <div class="bar-value" style="width: ${(parseFloat(row.roas) / 7) * 100}%; background: var(--gradient-purple);">${row.roas}</div>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Marketing Funnel
        html += `
            <div class="col-6">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Marketing Funnel</h3>
                    </div>
                    <div class="card-body">
                        <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                            <div style="display: flex; align-items: center; gap: 1rem;">
                                <div style="width: 100%; background: var(--accent-pink); padding: 0.75rem; border-radius: 0.5rem; text-align: center;">
                                    <div style="font-weight: 600;">Impressions</div>
                                    <div style="font-size: 1.25rem;">1.2M</div>
                                </div>
                            </div>
                            <div style="text-align: center; color: var(--text-muted);">↓ 2.4%</div>
                            <div style="display: flex; align-items: center; gap: 1rem;">
                                <div style="width: 80%; margin: 0 auto; background: var(--accent-purple); padding: 0.75rem; border-radius: 0.5rem; text-align: center;">
                                    <div style="font-weight: 600;">Clicks</div>
                                    <div style="font-size: 1.25rem;">28.8K</div>
                                </div>
                            </div>
                            <div style="text-align: center; color: var(--text-muted);">↓ 30%</div>
                            <div style="display: flex; align-items: center; gap: 1rem;">
                                <div style="width: 60%; margin: 0 auto; background: var(--accent-blue); padding: 0.75rem; border-radius: 0.5rem; text-align: center;">
                                    <div style="font-weight: 600;">Add to Cart</div>
                                    <div style="font-size: 1.25rem;">8,640</div>
                                </div>
                            </div>
                            <div style="text-align: center; color: var(--text-muted);">↓ 50%</div>
                            <div style="display: flex; align-items: center; gap: 1rem;">
                                <div style="width: 40%; margin: 0 auto; background: var(--accent-green); padding: 0.75rem; border-radius: 0.5rem; text-align: center;">
                                    <div style="font-weight: 600;">Purchase</div>
                                    <div style="font-size: 1.25rem;">3,456</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Ad Performance Table
        html += `
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Ad Performance</h3>
                    </div>
                    <div class="card-body" style="padding: 0;">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Channel</th>
                                    <th>Spend</th>
                                    <th>Conversions</th>
                                    <th>ROAS</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${TABLE_DATA.cmo_roas.map(row => `
                                    <tr>
                                        <td>${row.channel}</td>
                                        <td>${row.spend}</td>
                                        <td>${row.conversions.toLocaleString()}</td>
                                        <td><span class="badge badge-success">${row.roas}</span></td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        `;

        html += '</div>';
        return html;
    }

    generateCOOContent() {
        let html = '<div class="dashboard-grid">';

        // Ticket Queue
        html += `
            <div class="col-8">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Ticket Queue</h3>
                        <span class="badge badge-warning">23 Open</span>
                    </div>
                    <div class="card-body" style="padding: 0;">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Priority</th>
                                    <th>Ticket</th>
                                    <th>Subject</th>
                                    <th>Age</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${TABLE_DATA.coo_tickets.map(ticket => `
                                    <tr>
                                        <td><span class="badge badge-${ticket.priority === 'critical' ? 'danger' : ticket.priority === 'high' ? 'warning' : 'info'}">${ticket.priority}</span></td>
                                        <td>${ticket.id}</td>
                                        <td>${ticket.subject}</td>
                                        <td>${ticket.age}</td>
                                        <td>${ticket.status}</td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        `;

        // Call Center
        html += `
            <div class="col-4">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Call Center Status</h3>
                    </div>
                    <div class="card-body">
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                            <div style="text-align: center; padding: 1rem; background: var(--bg-tertiary); border-radius: 0.5rem;">
                                <div style="font-size: 2rem; font-weight: 700; color: var(--accent-gold);">47</div>
                                <div style="color: var(--text-muted); font-size: 0.8rem;">Calls Today</div>
                            </div>
                            <div style="text-align: center; padding: 1rem; background: var(--bg-tertiary); border-radius: 0.5rem;">
                                <div style="font-size: 2rem; font-weight: 700; color: var(--accent-green);">4.2m</div>
                                <div style="color: var(--text-muted); font-size: 0.8rem;">Avg Duration</div>
                            </div>
                            <div style="text-align: center; padding: 1rem; background: var(--bg-tertiary); border-radius: 0.5rem;">
                                <div style="font-size: 2rem; font-weight: 700; color: var(--accent-green);">0.5m</div>
                                <div style="color: var(--text-muted); font-size: 0.8rem;">Wait Time</div>
                            </div>
                            <div style="text-align: center; padding: 1rem; background: var(--bg-tertiary); border-radius: 0.5rem;">
                                <div style="font-size: 2rem; font-weight: 700;">0</div>
                                <div style="color: var(--text-muted); font-size: 0.8rem;">In Queue</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        html += '</div>';
        return html;
    }

    generateCIOContent() {
        let html = '<div class="dashboard-grid">';

        // MCP Server Status
        html += `
            <div class="col-8">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">MCP Server Status</h3>
                        <span class="badge badge-success">12/12 Online</span>
                    </div>
                    <div class="card-body" style="padding: 0;">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Service</th>
                                    <th>Status</th>
                                    <th>Latency</th>
                                    <th>Calls/hr</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${TABLE_DATA.cio_servers.map(server => `
                                    <tr>
                                        <td>${server.service}</td>
                                        <td><span class="badge badge-success">● ${server.status}</span></td>
                                        <td>${server.latency}</td>
                                        <td>${server.calls}</td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        `;

        // Security & Redundancy
        html += `
            <div class="col-4">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Security Status</h3>
                    </div>
                    <div class="card-body">
                        <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                            <div style="display: flex; justify-content: space-between; padding: 0.75rem; background: var(--bg-tertiary); border-radius: 0.5rem;">
                                <span>Active Incidents</span>
                                <span style="color: var(--accent-green); font-weight: 600;">0</span>
                            </div>
                            <div style="display: flex; justify-content: space-between; padding: 0.75rem; background: var(--bg-tertiary); border-radius: 0.5rem;">
                                <span>Vulnerabilities</span>
                                <span style="color: var(--accent-green); font-weight: 600;">0</span>
                            </div>
                            <div style="display: flex; justify-content: space-between; padding: 0.75rem; background: var(--bg-tertiary); border-radius: 0.5rem;">
                                <span>Access Reviews</span>
                                <span style="color: var(--accent-green); font-weight: 600;">Current</span>
                            </div>
                            <div style="display: flex; justify-content: space-between; padding: 0.75rem; background: var(--bg-tertiary); border-radius: 0.5rem;">
                                <span>Last Pen Test</span>
                                <span>Jan 15, 2026</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="card" style="margin-top: 1.5rem;">
                    <div class="card-header">
                        <h3 class="card-title">Redundancy Status</h3>
                    </div>
                    <div class="card-body">
                        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                            <div style="display: flex; align-items: center; gap: 0.5rem;">
                                <span style="color: var(--accent-green);">✓</span>
                                <span>LLM Failover Chain</span>
                            </div>
                            <div style="display: flex; align-items: center; gap: 0.5rem;">
                                <span style="color: var(--accent-green);">✓</span>
                                <span>Database Replica</span>
                            </div>
                            <div style="display: flex; align-items: center; gap: 0.5rem;">
                                <span style="color: var(--accent-green);">✓</span>
                                <span>Auth Fallback</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        html += '</div>';
        return html;
    }

    generateCLOContent() {
        let html = '<div class="dashboard-grid">';

        // Compliance
        html += `
            <div class="col-6">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Jurisdictional Compliance</h3>
                    </div>
                    <div class="card-body" style="padding: 0;">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Jurisdiction</th>
                                    <th>Applicability</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr><td>US Federal</td><td>High</td><td><span class="badge badge-success">Compliant</span></td></tr>
                                <tr><td>California</td><td>High</td><td><span class="badge badge-success">Compliant</span></td></tr>
                                <tr><td>New York</td><td>Medium</td><td><span class="badge badge-success">Compliant</span></td></tr>
                                <tr><td>Texas</td><td>Medium</td><td><span class="badge badge-success">Compliant</span></td></tr>
                                <tr><td>EU GDPR</td><td>High</td><td><span class="badge badge-success">Compliant</span></td></tr>
                                <tr><td>UK</td><td>Medium</td><td><span class="badge badge-success">Compliant</span></td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        `;

        // Contracts
        html += `
            <div class="col-6">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Active Contracts</h3>
                        <span class="badge badge-info">12 Active</span>
                    </div>
                    <div class="card-body" style="padding: 0;">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Contract</th>
                                    <th>Expires</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr><td>SaaS Agreement</td><td>Dec 31, 2026</td><td><span class="badge badge-success">Active</span></td></tr>
                                <tr><td>AWS MSA</td><td>Nov 15, 2026</td><td><span class="badge badge-warning">Renew Soon</span></td></tr>
                                <tr><td>GCP MSA</td><td>Mar 1, 2027</td><td><span class="badge badge-success">Active</span></td></tr>
                                <tr><td>Vendor NDA</td><td>Oct 30, 2026</td><td><span class="badge badge-warning">Expiring</span></td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        `;

        html += '</div>';
        return html;
    }

    generateCPOContent() {
        let html = '<div class="dashboard-grid">';

        // Roadmap
        html += `
            <div class="col-8">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Q1 2026 Roadmap</h3>
                        <span class="badge badge-info">60% Complete</span>
                    </div>
                    <div class="card-body">
                        <div class="progress-bar" style="height: 12px; margin-bottom: 1.5rem;">
                            <div class="progress-fill success" style="width: 60%;"></div>
                        </div>
                        
                        <h4 style="font-size: 0.875rem; color: var(--accent-green); margin-bottom: 0.5rem;">✓ Shipped</h4>
                        <div style="display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 1rem;">
                            <div style="padding: 0.5rem; background: rgba(16, 185, 129, 0.1); border-radius: 0.25rem;">User Onboarding v2</div>
                            <div style="padding: 0.5rem; background: rgba(16, 185, 129, 0.1); border-radius: 0.25rem;">Payment Integration</div>
                        </div>
                        
                        <h4 style="font-size: 0.875rem; color: var(--accent-blue); margin-bottom: 0.5rem;">🔄 In Progress</h4>
                        <div style="display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 1rem;">
                            <div style="padding: 0.5rem; background: rgba(59, 130, 246, 0.1); border-radius: 0.25rem; display: flex; justify-content: space-between;">
                                <span>Mobile App MVP</span>
                                <span>70%</span>
                            </div>
                            <div style="padding: 0.5rem; background: rgba(59, 130, 246, 0.1); border-radius: 0.25rem; display: flex; justify-content: space-between;">
                                <span>Analytics Dashboard</span>
                                <span>40%</span>
                            </div>
                        </div>
                        
                        <h4 style="font-size: 0.875rem; color: var(--text-muted); margin-bottom: 0.5rem;">📅 Upcoming</h4>
                        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                            <div style="padding: 0.5rem; background: var(--bg-tertiary); border-radius: 0.25rem;">API v2</div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Customer Feedback
        html += `
            <div class="col-4">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Top Feature Requests</h3>
                    </div>
                    <div class="card-body">
                        <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                            <div style="display: flex; justify-content: space-between; padding: 0.75rem; background: var(--bg-tertiary); border-radius: 0.5rem;">
                                <span>Enhanced API Docs</span>
                                <span style="color: var(--accent-gold);">256</span>
                            </div>
                            <div style="display: flex; justify-content: space-between; padding: 0.75rem; background: var(--bg-tertiary); border-radius: 0.5rem;">
                                <span>Custom Dashboards</span>
                                <span style="color: var(--accent-gold);">198</span>
                            </div>
                            <div style="display: flex; justify-content: space-between; padding: 0.75rem; background: var(--bg-tertiary); border-radius: 0.5rem;">
                                <span>Slack Integration</span>
                                <span style="color: var(--accent-gold);">145</span>
                            </div>
                            <div style="display: flex; justify-content: space-between; padding: 0.75rem; background: var(--bg-tertiary); border-radius: 0.5rem;">
                                <span>Advanced Reporting</span>
                                <span style="color: var(--accent-gold);">112</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        html += '</div>';
        return html;
    }

    generateCTOContent() {
        let html = '<div class="dashboard-grid">';

        // SpecKit Status
        html += `
            <div class="col-8">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">SpecKit Status</h3>
                    </div>
                    <div class="card-body" style="padding: 0;">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Component</th>
                                    <th>Tests</th>
                                    <th>Coverage</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${TABLE_DATA.cto_deploys.map(row => `
                                    <tr>
                                        <td>${row.component}</td>
                                        <td>${row.tests}</td>
                                        <td>${row.coverage}</td>
                                        <td><span class="badge badge-${row.status === 'Passing' ? 'success' : 'warning'}">${row.status}</span></td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        `;

        // Backup & Deploy Status
        html += `
            <div class="col-4">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Deployment Status</h3>
                    </div>
                    <div class="card-body">
                        <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                            <div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.75rem; background: var(--bg-tertiary); border-radius: 0.5rem;">
                                <span style="color: var(--accent-green);">●</span>
                                <div>
                                    <div style="font-weight: 500;">Production v2.4.1</div>
                                    <div style="font-size: 0.8rem; color: var(--text-muted);">Deployed Oct 25, 22:15 UTC</div>
                                </div>
                            </div>
                            <div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.75rem; background: var(--bg-tertiary); border-radius: 0.5rem;">
                                <span style="color: var(--accent-gold);">●</span>
                                <div>
                                    <div style="font-weight: 500;">Staging v2.5.0</div>
                                    <div style="font-size: 0.8rem; color: var(--text-muted);">Ready for deployment</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="card" style="margin-top: 1.5rem;">
                    <div class="card-header">
                        <h3 class="card-title">Backup Status</h3>
                    </div>
                    <div class="card-body">
                        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                            <div style="display: flex; justify-content: space-between;">
                                <span>Database</span>
                                <span style="color: var(--accent-green);">✓ 1h ago</span>
                            </div>
                            <div style="display: flex; justify-content: space-between;">
                                <span>BigQuery</span>
                                <span style="color: var(--accent-green);">✓ 30m ago</span>
                            </div>
                            <div style="display: flex; justify-content: space-between;">
                                <span>Files</span>
                                <span style="color: var(--accent-green);">✓ 2h ago</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        html += '</div>';
        return html;
    }

    generateCXAContent() {
        let html = '<div class="dashboard-grid">';

        // Email Inbox
        html += `
            <div class="col-8">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Email Inbox</h3>
                        <span class="badge badge-info">47 Today</span>
                    </div>
                    <div class="card-body" style="padding: 0;">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Status</th>
                                    <th>Subject</th>
                                    <th>From</th>
                                    <th>Routed To</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><span class="badge badge-danger">Urgent</span></td>
                                    <td>Q4 Report Review</td>
                                    <td>John Smith (CFO)</td>
                                    <td>CEO</td>
                                </tr>
                                <tr>
                                    <td><span class="badge badge-warning">Normal</span></td>
                                    <td>Project Update Meeting</td>
                                    <td>Sarah Davis (COO)</td>
                                    <td>COO</td>
                                </tr>
                                <tr>
                                    <td><span class="badge badge-info">Low</span></td>
                                    <td>Newsletter Options</td>
                                    <td>Team Updates</td>
                                    <td>Auto-archive</td>
                                </tr>
                                <tr>
                                    <td><span class="badge badge-danger">Urgent</span></td>
                                    <td>Client Proposal Feedback</td>
                                    <td>Michael Lee (CFO)</td>
                                    <td>CFO</td>
                                </tr>
                                <tr>
                                    <td><span class="badge badge-warning">Normal</span></td>
                                    <td>HR Policy Questions</td>
                                    <td>Emily Chen (HR)</td>
                                    <td>Human Direct</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        `;

        // Calendar & Routing
        html += `
            <div class="col-4">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Human Calendar</h3>
                    </div>
                    <div class="card-body">
                        <h4 style="font-size: 0.875rem; margin-bottom: 0.75rem;">Today (Jan 31)</h4>
                        <div style="display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 1rem;">
                            <div style="padding: 0.5rem; background: var(--bg-tertiary); border-radius: 0.25rem; border-left: 3px solid var(--accent-blue);">
                                <div style="font-size: 0.8rem; color: var(--text-muted);">09:30 - 10:30 AM</div>
                                <div>Strategy Sync (Zoom)</div>
                            </div>
                            <div style="padding: 0.5rem; background: rgba(16, 185, 129, 0.1); border-radius: 0.25rem; border-left: 3px solid var(--accent-green);">
                                <div style="font-size: 0.8rem; color: var(--accent-green);">11:00 - 11:45 AM</div>
                                <div>Available for scheduling</div>
                            </div>
                            <div style="padding: 0.5rem; background: var(--bg-tertiary); border-radius: 0.25rem; border-left: 3px solid var(--accent-blue);">
                                <div style="font-size: 0.8rem; color: var(--text-muted);">01:30 - 02:15 PM</div>
                                <div>Client Call</div>
                            </div>
                        </div>
                        
                        <h4 style="font-size: 0.875rem; margin-bottom: 0.75rem;">Pending Requests</h4>
                        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                            <div style="padding: 0.5rem; background: var(--bg-tertiary); border-radius: 0.25rem;">
                                <span style="color: var(--accent-gold);">●</span> Request from Anna B. - 30 min
                            </div>
                            <div style="padding: 0.5rem; background: var(--bg-tertiary); border-radius: 0.25rem;">
                                <span style="color: var(--accent-gold);">●</span> Request from Mark T. - 15 min
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        html += '</div>';
        return html;
    }

    bindDynamicEvents() {
        // Agent cards click to open profile
        document.querySelectorAll('.agent-card').forEach(card => {
            card.addEventListener('click', () => {
                const agentKey = card.dataset.agent;
                this.openProfile(agentKey);
            });
        });

        // Tab navigation
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            });
        });
    }

    openProfile(agentKey) {
        const agent = AGENTS[agentKey];
        const status = AGENT_STATUS[agentKey] || { status: 'online', task: 'Idle', tokens: '0' };

        // Update profile content
        document.getElementById('profileName').textContent = agent.fullName;
        document.getElementById('profileRole').textContent = agent.name + ' - ' + agent.role;
        document.getElementById('profileEnneagram').textContent = agent.personality.enneagram;
        document.getElementById('profileMbti').textContent = agent.personality.mbti;
        document.getElementById('profileWestern').textContent = agent.personality.western;
        document.getElementById('profileChinese').textContent = agent.personality.chinese;
        document.getElementById('profileCommStyle').textContent = agent.commStyle;
        document.getElementById('profileSampleVoice').textContent = agent.sampleVoice;
        document.getElementById('profileCurrentTask').textContent = status.task;
        document.getElementById('profileTokens').textContent = status.tokens;
        document.getElementById('profileLastAction').textContent = 'Just now';

        // Set image or placeholder
        const imgEl = document.getElementById('profileImage');
        imgEl.onerror = function () {
            this.style.display = 'none';
            this.parentElement.innerHTML = `<div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: var(--gradient-gold); border-radius: 50%; font-size: 3rem;">${agent.icon}</div>`;
        };
        imgEl.src = agent.imagePath;

        // Open sidebar
        document.getElementById('profileSidebar').classList.add('open');
    }

    closeProfile() {
        document.getElementById('profileSidebar').classList.remove('open');
    }

    openRedPhoneModal() {
        document.getElementById('redPhoneModal').classList.add('open');
    }

    closeAllModals() {
        document.querySelectorAll('.modal').forEach(modal => {
            modal.classList.remove('open');
        });
    }

    sendRedPhoneAlert() {
        const message = document.getElementById('redPhoneMessage').value;
        if (message.trim()) {
            alert('🚨 RED PHONE ALERT SENT TO CHAIRMAN\n\n' + message);
            document.getElementById('redPhoneMessage').value = '';
            this.closeAllModals();
        }
    }

    refresh() {
        this.updateTimestamp();
        this.loadPage(this.currentPage);
    }

    updateTimestamp() {
        const now = new Date();
        const options = {
            month: 'short',
            day: 'numeric',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            timeZoneName: 'short'
        };
        document.getElementById('lastUpdated').textContent =
            'Last Updated: ' + now.toLocaleDateString('en-US', options);
    }
}

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new Dashboard();
});
