'use client';

import React from 'react';
import './page.module.css';

export default function CorporatePage() {
    return (
        <div className="dashboard-content">
            <div className="content-header">
                <div>
                    <h1>Corporate Information</h1>
                    <p className="subtitle">Company mission, values, and identity</p>
                </div>
            </div>

            <div className="dashboard-grid">
                <div className="col-8">
                    <div className="card">
                        <div className="card-header">
                            <h3 className="card-title">Company Branding</h3>
                        </div>
                        <div className="card-body">
                            <div className="branding-section">
                                <div className="logo-display">
                                    <div className="logo-placeholder">
                                        <span className="logo-icon">🏭</span>
                                        <div className="logo-text">The Factory</div>
                                    </div>
                                </div>
                                <div className="brand-colors">
                                    <h4>Brand Colors</h4>
                                    <div className="color-palette">
                                        <div className="color-swatch">
                                            <div className="swatch" style={{ background: '#fbbf24' }}></div>
                                            <span>Gold</span>
                                            <code>#fbbf24</code>
                                        </div>
                                        <div className="color-swatch">
                                            <div className="swatch" style={{ background: '#3b82f6' }}></div>
                                            <span>Blue</span>
                                            <code>#3b82f6</code>
                                        </div>
                                        <div className="color-swatch">
                                            <div className="swatch" style={{ background: '#8b5cf6' }}></div>
                                            <span>Purple</span>
                                            <code>#8b5cf6</code>
                                        </div>
                                        <div className="color-swatch">
                                            <div className="swatch" style={{ background: '#10b981' }}></div>
                                            <span>Green</span>
                                            <code>#10b981</code>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="card">
                        <div className="card-header">
                            <h3 className="card-title">Mission Statement</h3>
                        </div>
                        <div className="card-body corporate-text">
                            <p className="mission-statement">
                                To democratize AI-driven business creation through transparent, ethical,
                                and autonomous C-suite agents, empowering entrepreneurs to build and scale
                                businesses with confidence.
                            </p>
                        </div>
                    </div>

                    <div className="card">
                        <div className="card-header">
                            <h3 className="card-title">Core Values</h3>
                        </div>
                        <div className="card-body corporate-text">
                            <div className="values-list">
                                <div className="value-item">
                                    <div className="value-icon">🎯</div>
                                    <div className="value-content">
                                        <h4>Transparency</h4>
                                        <p>Full visibility into all agent actions and decisions. Every action is logged and auditable.</p>
                                    </div>
                                </div>
                                <div className="value-item">
                                    <div className="value-icon">⚖️</div>
                                    <div className="value-content">
                                        <h4>Ethics First</h4>
                                        <p>Human authority over AI. Governance frameworks that cannot be modified by agents.</p>
                                    </div>
                                </div>
                                <div className="value-item">
                                    <div className="value-icon">📊</div>
                                    <div className="value-content">
                                        <h4>Evidence-Based</h4>
                                        <p>All decisions grounded in empirical evidence and published research with citations.</p>
                                    </div>
                                </div>
                                <div className="value-item">
                                    <div className="value-icon">🤝</div>
                                    <div className="value-content">
                                        <h4>Compliance</h4>
                                        <p>Full adherence to US, EU, and international regulations across all jurisdictions.</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="col-4">
                    <div className="card">
                        <div className="card-header">
                            <h3 className="card-title">Elevator Pitch</h3>
                        </div>
                        <div className="card-body corporate-text">
                            <p className="elevator-pitch">
                                We're building the template factory for AI-driven businesses. Fork our repo,
                                configure your mission, and deploy a full C-suite of autonomous agents that
                                work together to build and operate your business—with you maintaining full control.
                            </p>
                        </div>
                    </div>

                    <div className="card">
                        <div className="card-header">
                            <h3 className="card-title">Company Metadata</h3>
                        </div>
                        <div className="card-body">
                            <div className="metadata-list">
                                <div className="metadata-item">
                                    <span className="metadata-label">Legal Name</span>
                                    <span className="metadata-value">The Factory AI Inc.</span>
                                </div>
                                <div className="metadata-item">
                                    <span className="metadata-label">Founded</span>
                                    <span className="metadata-value">January 2026</span>
                                </div>
                                <div className="metadata-item">
                                    <span className="metadata-label">Jurisdiction</span>
                                    <span className="metadata-value">Delaware, USA</span>
                                </div>
                                <div className="metadata-item">
                                    <span className="metadata-label">Industry</span>
                                    <span className="metadata-value">AI/SaaS</span>
                                </div>
                                <div className="metadata-item">
                                    <span className="metadata-label">Business Model</span>
                                    <span className="metadata-value">B2B Platform</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="card">
                        <div className="card-header">
                            <h3 className="card-title">Quick Stats</h3>
                        </div>
                        <div className="card-body">
                            <div className="stats-grid">
                                <div className="stat-box">
                                    <div className="stat-value">9</div>
                                    <div className="stat-label">AI Agents</div>
                                </div>
                                <div className="stat-box">
                                    <div className="stat-value">100%</div>
                                    <div className="stat-label">Uptime</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
