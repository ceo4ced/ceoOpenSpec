'use client';

import React from 'react';
import Link from 'next/link';
import { RED_PHONE_ALERTS } from '@/lib/data';
import './page.module.css';

export default function RedPhonePage() {
    const handleAcknowledge = (index: number) => {
        // TODO: Implement acknowledgement logic
        console.log(`Acknowledged alert ${index}`);
    };

    const handleResolve = (index: number) => {
        // TODO: Implement resolution logic
        console.log(`Resolved alert ${index}`);
    };

    return (
        <div className="dashboard-content">
            <div className="content-header">
                <div>
                    <h1>🚨 RED PHONE - Emergency Control Center</h1>
                    <p className="subtitle">Critical alerts and emergency controls</p>
                </div>
                <Link href="/" className="btn btn-secondary">
                    ← Back to Dashboard
                </Link>
            </div>

            {RED_PHONE_ALERTS.length === 0 ? (
                <div className="card">
                    <div className="card-body" style={{ textAlign: 'center', padding: '3rem' }}>
                        <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>✅</div>
                        <h2>All Clear</h2>
                        <p style={{ color: 'var(--text-muted)' }}>No active red phone alerts</p>
                    </div>
                </div>
            ) : (
                <>
                    <div className="dashboard-grid">
                        <div className="col-12">
                            <div className="card red-phone-card">
                                <div className="card-header">
                                    <h3 className="card-title">Active Alerts</h3>
                                    <span className="badge badge-danger">{RED_PHONE_ALERTS.length} Critical</span>
                                </div>
                                <div className="card-body">
                                    <div className="red-phone-alerts">
                                        {RED_PHONE_ALERTS.map((alert, index) => (
                                            <div key={index} className={`red-phone-alert-item severity-${alert.severity}`}>
                                                <div className="alert-indicator"></div>
                                                <div className="alert-main">
                                                    <div className="alert-header">
                                                        <span className={`severity-badge severity-${alert.severity}`}>
                                                            {alert.severity === 'critical' ? '🔴 CRITICAL' : '⚠️ WARNING'}
                                                        </span>
                                                        <span className="alert-time">2 hours ago</span>
                                                    </div>
                                                    <h4 className="alert-title">{alert.message}</h4>
                                                    <div className="alert-details">
                                                        <p><strong>Affected Systems:</strong> {alert.severity === 'critical' ? 'US-East Region, API Gateway' : 'Global Network'}</p>
                                                        <p><strong>Impact:</strong> {alert.severity === 'critical' ? 'High - Service degradation affecting 15% of users' : 'Medium - Monitoring for escalation'}</p>
                                                        <p><strong>Recommended Action:</strong> {alert.severity === 'critical' ? 'Immediate failover to US-West backup servers' : 'Review IP range and adjust firewall rules'}</p>
                                                    </div>
                                                    <div className="alert-actions">
                                                        <button
                                                            className="btn btn-secondary"
                                                            onClick={() => handleAcknowledge(index)}
                                                        >
                                                            Acknowledge
                                                        </button>
                                                        <button
                                                            className="btn btn-success"
                                                            onClick={() => handleResolve(index)}
                                                        >
                                                            Mark Resolved
                                                        </button>
                                                        <button className="btn btn-danger">
                                                            Escalate to All C-Suite
                                                        </button>
                                                    </div>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="col-12">
                            <div className="card">
                                <div className="card-header">
                                    <h3 className="card-title">Emergency Controls</h3>
                                </div>
                                <div className="card-body emergency-controls">
                                    <div className="emergency-control-group">
                                        <h4>Agent Controls</h4>
                                        <div className="control-buttons">
                                            <button className="btn btn-danger">🛑 Emergency Pause All Agents</button>
                                            <button className="btn btn-warning">⏸️ Pause Non-Essential Agents</button>
                                            <button className="btn btn-secondary">🔄 Restart All Systems</button>
                                        </div>
                                    </div>
                                    <div className="emergency-control-group">
                                        <h4>Financial Controls</h4>
                                        <div className="control-buttons">
                                            <button className="btn btn-danger">💳 Freeze All Spending</button>
                                            <button className="btn btn-warning">💰 Enter Cost-Saving Mode</button>
                                        </div>
                                    </div>
                                    <div className="emergency-control-group">
                                        <h4>Communication</h4>
                                        <div className="control-buttons">
                                            <button className="btn btn-primary">📞 Call Chairman</button>
                                            <button className="btn btn-primary">📧 Alert All C-Suite</button>
                                            <button className="btn btn-secondary">📢 Send Status Update</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </>
            )}
        </div>
    );
}
