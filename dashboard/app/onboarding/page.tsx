
'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import '../onboarding.css'; // Global import for this page

export default function Onboarding() {
    const router = useRouter();
    const [step, setStep] = useState(1);
    const [formData, setFormData] = useState({
        creatorName: '',
        creatorRole: 'Founder',
        securityKey: '',
        bizName: '',
        bizMission: '',
        bizValues: '',
        opMode: 'balanced',
        initCapital: 5000
    });

    const totalSteps = 4;

    const handleNext = () => {
        if (!validateStep(step)) return;

        if (step < totalSteps) {
            setStep(step + 1);
        } else {
            // Launch
            handleLaunch();
        }
    };

    const handlePrev = () => {
        if (step > 1) setStep(step - 1);
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
        setFormData({ ...formData, [e.target.id]: e.target.value });
    };

    const validateStep = (currentStep: number) => {
        let valid = true;
        if (currentStep === 1) {
            if (!formData.creatorName) {
                shakeField('creatorName');
                valid = false;
            }
        }
        if (currentStep === 2) {
            if (!formData.bizName) {
                shakeField('bizName');
                valid = false;
            }
        }
        return valid;
    };

    const shakeField = (id: string) => {
        const el = document.getElementById(id);
        if (el) {
            el.classList.add('shake');
            el.style.borderColor = '#f87171';
            setTimeout(() => {
                el.classList.remove('shake');
                el.style.borderColor = '#30363d';
            }, 500);
        }
    };

    const handleLaunch = () => {
        const btn = document.getElementById('nextBtn');
        if (btn) btn.innerHTML = "Initializing...";

        setTimeout(() => {
            router.push('/');
        }, 2000);
    };

    const progressPercentage = ((step - 1) / (totalSteps - 1)) * 100;

    return (
        <div className="onboarding-container">
            {/* Left Side: Visual */}
            <div className="visual-panel">
                <div className="visual-content">
                    <div className="logo-large">
                        <span className="logo-icon">🍌</span>
                        <span className="logo-text">The Factory</span>
                    </div>
                    <div className="visual-art">
                        <div className="neural-network">
                            <div className="node n1"></div>
                            <div className="node n2"></div>
                            <div className="node n3"></div>
                            <div className="node n4"></div>
                            <div className="connection c1"></div>
                            <div className="connection c2"></div>
                            <div className="connection c3"></div>
                        </div>
                    </div>
                    <div className="visual-footer">
                        <p>Intelligent C-Suite Systems</p>
                        <p className="sub-text">Powered by Neural Core Technology</p>
                    </div>
                </div>
            </div>

            {/* Right Side: Form Wizard */}
            <div className="form-panel">
                <div className="form-header">
                    <h1>Initialize C-Suite</h1>
                    <div className="progress-bar-container">
                        <div className="progress-steps">
                            {[1, 2, 3, 4].map(num => (
                                <div key={num} className={`step ${num <= step ? 'active' : ''}`}>
                                    <div className="step-circle">{num}</div>
                                    <span className="step-label">
                                        {num === 1 && 'Identity'}
                                        {num === 2 && 'Vision'}
                                        {num === 3 && 'Config'}
                                        {num === 4 && 'Launch'}
                                    </span>
                                </div>
                            ))}
                        </div>
                        <div className="progress-line">
                            <div className="progress-fill" style={{ width: `${progressPercentage}%` }}></div>
                        </div>
                    </div>
                </div>

                <div className="form-content">
                    {/* Step 1: Identity */}
                    <div className={`form-step ${step === 1 ? 'active' : ''}`} id="step1">
                        <h2>Creator Identity</h2>
                        <p className="step-desc">Establish the primary human authority for the system.</p>
                        <div className="input-group">
                            <label>Full Name</label>
                            <input type="text" id="creatorName" value={formData.creatorName} onChange={handleChange} placeholder="e.g. Jane Doe" />
                        </div>
                        <div className="input-group">
                            <label>Role / Title</label>
                            <input type="text" id="creatorRole" value={formData.creatorRole} onChange={handleChange} placeholder="e.g. Founder" />
                        </div>
                        <div className="input-group">
                            <label>Security Key</label>
                            <input type="password" id="securityKey" value={formData.securityKey} onChange={handleChange} placeholder="Create a master password" />
                        </div>
                    </div>

                    {/* Step 2: Vision */}
                    <div className={`form-step ${step === 2 ? 'active' : ''}`} id="step2">
                        <h2>Company Vision</h2>
                        <p className="step-desc">Define the core purpose for the CEO agent to propagate.</p>
                        <div className="input-group">
                            <label>Business Name</label>
                            <input type="text" id="bizName" value={formData.bizName} onChange={handleChange} placeholder="e.g. Acme Corp" />
                        </div>
                        <div className="input-group">
                            <label>Mission Statement</label>
                            <textarea id="bizMission" value={formData.bizMission} onChange={handleChange} placeholder="What problem are you solving? (Max 300 chars)" rows={3}></textarea>
                        </div>
                        <div className="input-group">
                            <label>Core Values</label>
                            <input type="text" id="bizValues" value={formData.bizValues} onChange={handleChange} placeholder="e.g. Innovation, Integrity, Speed" />
                        </div>
                    </div>

                    {/* Step 3: Configuration */}
                    <div className={`form-step ${step === 3 ? 'active' : ''}`} id="step3">
                        <h2>System Configuration</h2>
                        <p className="step-desc">Set operational parameters for the C-Suite agents.</p>
                        <div className="input-group">
                            <label>Operating Mode</label>
                            <select id="opMode" value={formData.opMode} onChange={handleChange}>
                                <option value="aggressive">Aggressive Growth (High Risk)</option>
                                <option value="balanced">Balanced (Standard)</option>
                                <option value="conservative">Conservative (Low Risk)</option>
                            </select>
                        </div>
                        <div className="input-group">
                            <label>Initial Capital (Tokens)</label>
                            <input type="number" id="initCapital" value={formData.initCapital} onChange={handleChange} />
                        </div>
                    </div>

                    {/* Step 4: Launch */}
                    <div className={`form-step ${step === 4 ? 'active' : ''}`} id="step4">
                        <h2>Ready to Launch</h2>
                        <p className="step-desc">Review your configuration and initialize the C-Suite.</p>
                        <div className="summary-card">
                            <div className="summary-row">
                                <span>Creator</span>
                                <span>{formData.creatorName || '--'}</span>
                            </div>
                            <div className="summary-row">
                                <span>Business</span>
                                <span>{formData.bizName || '--'}</span>
                            </div>
                            <div className="summary-row">
                                <span>Mode</span>
                                <span>{formData.opMode}</span>
                            </div>
                        </div>
                        <div className="checklist">
                            <div className="check-item"><span className="check-icon">✓</span> CEO Agent Ready</div>
                            <div className="check-item"><span className="check-icon">✓</span> Data Uplink Secure</div>
                            <div className="check-item"><span className="check-icon">✓</span> Governance Protocols Active</div>
                        </div>
                    </div>
                </div>

                <div className="form-footer">
                    <button className="btn btn-secondary" onClick={handlePrev} disabled={step === 1}>Back</button>
                    <button className="btn btn-primary" id="nextBtn" onClick={handleNext}>
                        {step === totalSteps ? 'Initialize System' : 'Continue'}
                    </button>
                </div>
            </div>
        </div>
    );
}
