
import React from 'react';
import Image from 'next/image';
import { AGENTS } from '@/lib/data';

// Color map for each role (fallback if image doesn't load)
const ROLE_COLORS: Record<string, string> = {
    chairman: 'linear-gradient(135deg, #d4af37, #b8860b)',
    ceo: 'linear-gradient(135deg, #3b82f6, #1d4ed8)',
    cfo: 'linear-gradient(135deg, #10b981, #059669)',
    cmo: 'linear-gradient(135deg, #ec4899, #db2777)',
    coo: 'linear-gradient(135deg, #f59e0b, #d97706)',
    cio: 'linear-gradient(135deg, #06b6d4, #0891b2)',
    clo: 'linear-gradient(135deg, #8b5cf6, #7c3aed)',
    cpo: 'linear-gradient(135deg, #6366f1, #4f46e5)',
    cto: 'linear-gradient(135deg, #0ea5e9, #0284c7)',
    cxa: 'linear-gradient(135deg, #14b8a6, #0d9488)',
};

interface AgentCardProps {
    id: string;
    status: string;
    task: string;
    tokens: string;
}

export default function AgentCard({ id, status, task, tokens }: AgentCardProps) {
    const agent = AGENTS[id];
    const [imageError, setImageError] = React.useState(false);

    if (!agent) return null;

    const bgGradient = ROLE_COLORS[id] || 'linear-gradient(135deg, #6b7280, #4b5563)';

    return (
        <div className="agent-card">
            <div className="agent-avatar" style={imageError ? { background: bgGradient, display: 'flex', alignItems: 'center', justifyContent: 'center' } : {}}>
                {agent.imagePath && !imageError ? (
                    <Image
                        src={agent.imagePath}
                        alt={agent.name}
                        fill
                        style={{ objectFit: 'cover' }}
                        onError={() => setImageError(true)}
                    />
                ) : (
                    <span style={{ fontSize: '1.5rem' }}>{agent.icon || id.toUpperCase().slice(0, 2)}</span>
                )}
                <div className={`agent-status-indicator ${status}`}></div>
            </div>
            <div className="agent-info">
                <div className="agent-name">{agent.name}</div>
                <div className="agent-role">{agent.role}</div>
                <div className="agent-task">{task}</div>
            </div>
            <div className="agent-meta">
                <div className="agent-tokens">{tokens} tk</div>
            </div>
        </div>
    );
}
