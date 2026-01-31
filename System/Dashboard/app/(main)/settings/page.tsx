'use client';

import React, { useState } from 'react';
import './page.module.css';

export default function SettingsPage() {
    const [formData, setFormData] = useState({
        name: 'Cedric Williams',
        email: 'cedric@factory.ai',
        phone: '+1 (555) 123-4567',
        notifyAlerts: true,
        notifyApprovals: true,
        notifyReports: false,
        theme: 'dark',
        compactMode: false,
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        const { name, value, type } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value
        }));
    };

    const handleSave = (e: React.FormEvent) => {
        e.preventDefault();
        // TODO: Implement save logic
        alert('Settings saved successfully!');
    };

    return (
        <div className="dashboard-content">
            <div className="content-header">
                <div>
                    <h1>Settings</h1>
                    <p className="subtitle">Manage your account and preferences</p>
                </div>
            </div>

            <form onSubmit={handleSave}>
                <div className="dashboard-grid">
                    <div className="col-8">
                        <div className="card">
                            <div className="card-header">
                                <h3 className="card-title">Personal Information</h3>
                            </div>
                            <div className="card-body">
                                <div className="settings-form">
                                    <div className="form-group">
                                        <label htmlFor="name">Full Name</label>
                                        <input
                                            type="text"
                                            id="name"
                                            name="name"
                                            value={formData.name}
                                            onChange={handleChange}
                                            className="form-input"
                                        />
                                    </div>
                                    <div className="form-group">
                                        <label htmlFor="email">Email Address</label>
                                        <input
                                            type="email"
                                            id="email"
                                            name="email"
                                            value={formData.email}
                                            onChange={handleChange}
                                            className="form-input"
                                        />
                                    </div>
                                    <div className="form-group">
                                        <label htmlFor="phone">Phone Number</label>
                                        <input
                                            type="tel"
                                            id="phone"
                                            name="phone"
                                            value={formData.phone}
                                            onChange={handleChange}
                                            className="form-input"
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="card">
                            <div className="card-header">
                                <h3 className="card-title">Notification Preferences</h3>
                            </div>
                            <div className="card-body">
                                <div className="settings-form">
                                    <div className="form-toggle">
                                        <div>
                                            <div className="toggle-label">Red Phone Alerts</div>
                                            <div className="toggle-description">Receive notifications for critical system alerts</div>
                                        </div>
                                        <label className="toggle-switch">
                                            <input
                                                type="checkbox"
                                                name="notifyAlerts"
                                                checked={formData.notifyAlerts}
                                                onChange={handleChange}
                                            />
                                            <span className="toggle-slider"></span>
                                        </label>
                                    </div>
                                    <div className="form-toggle">
                                        <div>
                                            <div className="toggle-label">Approval Requests</div>
                                            <div className="toggle-description">Get notified when agents request approvals</div>
                                        </div>
                                        <label className="toggle-switch">
                                            <input
                                                type="checkbox"
                                                name="notifyApprovals"
                                                checked={formData.notifyApprovals}
                                                onChange={handleChange}
                                            />
                                            <span className="toggle-slider"></span>
                                        </label>
                                    </div>
                                    <div className="form-toggle">
                                        <div>
                                            <div className="toggle-label">Daily Reports</div>
                                            <div className="toggle-description">Receive end-of-day summary reports</div>
                                        </div>
                                        <label className="toggle-switch">
                                            <input
                                                type="checkbox"
                                                name="notifyReports"
                                                checked={formData.notifyReports}
                                                onChange={handleChange}
                                            />
                                            <span className="toggle-slider"></span>
                                        </label>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="card">
                            <div className="card-header">
                                <h3 className="card-title">Dashboard Preferences</h3>
                            </div>
                            <div className="card-body">
                                <div className="settings-form">
                                    <div className="form-group">
                                        <label htmlFor="theme">Theme</label>
                                        <select
                                            id="theme"
                                            name="theme"
                                            value={formData.theme}
                                            onChange={handleChange}
                                            className="form-input"
                                        >
                                            <option value="dark">Dark Mode</option>
                                            <option value="light">Light Mode</option>
                                            <option value="auto">Auto (System)</option>
                                        </select>
                                    </div>
                                    <div className="form-toggle">
                                        <div>
                                            <div className="toggle-label">Compact Mode</div>
                                            <div className="toggle-description">Reduce spacing for more information density</div>
                                        </div>
                                        <label className="toggle-switch">
                                            <input
                                                type="checkbox"
                                                name="compactMode"
                                                checked={formData.compactMode}
                                                onChange={handleChange}
                                            />
                                            <span className="toggle-slider"></span>
                                        </label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="col-4">
                        <div className="card">
                            <div className="card-header">
                                <h3 className="card-title">Account Status</h3>
                            </div>
                            <div className="card-body">
                                <div className="account-status">
                                    <div className="status-item">
                                        <span className="status-label">Role</span>
                                        <span className="status-value">Chairman</span>
                                    </div>
                                    <div className="status-item">
                                        <span className="status-label">Access Level</span>
                                        <span className="status-value badge badge-success">Full Access</span>
                                    </div>
                                    <div className="status-item">
                                        <span className="status-label">Member Since</span>
                                        <span className="status-value">January 2026</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="card">
                            <div className="card-header">
                                <h3 className="card-title">API Access</h3>
                            </div>
                            <div className="card-body">
                                <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginBottom: '1rem' }}>
                                    API keys are managed by the CIO. Contact them for access.
                                </p>
                                <button type="button" className="btn btn-secondary btn-full">
                                    View API Documentation
                                </button>
                            </div>
                        </div>

                        <div className="save-section">
                            <button type="submit" className="btn btn-primary btn-full">
                                Save Changes
                            </button>
                            <button type="button" className="btn btn-secondary btn-full">
                                Reset to Defaults
                            </button>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    );
}
