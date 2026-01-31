
import React from 'react';
import Image from 'next/image';
import { AGENTS } from '@/lib/data';

interface AgentCardProps {
    id: string;
    status: string;
    task: string;
    tokens: string;
}

export default function AgentCard({ id, status, task, tokens }: AgentCardProps) {
    const agent = AGENTS[id];
    if (!agent) return null;

    return (
        <div className="agent-card">
            <div className="agent-avatar">
                {agent.imagePath ? (
                    <Image
                        src={agent.imagePath}
                        alt={agent.name}
                        fill
                        style={{ objectFit: 'cover' }}
                    />
                ) : (
                    <div className="placeholder">{agent.icon}</div>
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
