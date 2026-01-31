
import React from 'react';
import Image from 'next/image';
import { AGENTS } from '@/lib/data';

interface ProfileSidebarProps {
    agentId: string | null;
    isOpen: boolean;
    onClose: () => void;
}

export default function ProfileSidebar({ agentId, isOpen, onClose }: ProfileSidebarProps) {
    const agent = agentId ? AGENTS[agentId] : null;

    if (!agent) return null;

    return (
        <aside className={`profile-sidebar ${isOpen ? 'open' : ''}`}>
            <div className="profile-content-wrapper">
                <div className="profile-header">
                    <button className="close-profile" onClick={onClose}>×</button>
                    <div className="profile-image-container">
                        <div className="profile-image-wrapper">
                            {agent.imagePath ? (
                                <Image
                                    src={agent.imagePath}
                                    alt={agent.name}
                                    fill
                                    className="profile-image"
                                />
                            ) : (
                                <div className="profile-image placeholder">{agent.icon}</div>
                            )}
                        </div>
                        <div className="profile-status online"></div>
                    </div>
                    <h2 className="profile-name">{agent.fullName}</h2>
                    <p className="profile-role">{agent.role}</p>
                </div>

                <div className="profile-content">
                    <div className="profile-section">
                        <h3>Personality Profile</h3>
                        <div className="personality-grid">
                            <div className="personality-item">
                                <span className="label">Enneagram</span>
                                <span className="value">{agent.personality.enneagram}</span>
                            </div>
                            <div className="personality-item">
                                <span className="label">MBTI</span>
                                <span className="value">{agent.personality.mbti}</span>
                            </div>
                            <div className="personality-item">
                                <span className="label">Western</span>
                                <span className="value">{agent.personality.western}</span>
                            </div>
                            <div className="personality-item">
                                <span className="label">Chinese</span>
                                <span className="value">{agent.personality.chinese}</span>
                            </div>
                        </div>
                    </div>

                    <div className="profile-section">
                        <h3>Communication Style</h3>
                        <p className="comm-style">{agent.commStyle}</p>
                    </div>

                    <div className="profile-section">
                        <h3>Sample Voice</h3>
                        <blockquote className="sample-voice">"{agent.sampleVoice}"</blockquote>
                    </div>

                    <div className="profile-section">
                        <h3>Current Status</h3>
                        <div className="status-info">
                            <div className="status-row">
                                <span>Current Task</span>
                                <span>Active Monitoring</span>
                            </div>
                            <div className="status-row">
                                <span>Tokens Today</span>
                                <span>1,240</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </aside>
    );
}
