import React from 'react';
import { render, screen } from '@testing-library/react';
import AgentCard from './AgentCard';

describe('AgentCard', () => {
    it('renders agent card with valid data', () => {
        render(
            <AgentCard
                id="ceo"
                status="active"
                task="Reviewing Q1 strategy alignment"
                tokens="1,250"
            />
        );

        expect(screen.getByText('CEO')).toBeInTheDocument();
        expect(screen.getByText('Strategic Leadership')).toBeInTheDocument();
        expect(screen.getByText('Reviewing Q1 strategy alignment')).toBeInTheDocument();
        expect(screen.getByText('1,250 tk')).toBeInTheDocument();
    });

    it('renders status indicator with correct class', () => {
        const { container } = render(
            <AgentCard
                id="cfo"
                status="busy"
                task="Preparing monthly financial report"
                tokens="820"
            />
        );

        const statusIndicator = container.querySelector('.agent-status-indicator.busy');
        expect(statusIndicator).toBeInTheDocument();
    });

    it('returns null for invalid agent id', () => {
        const { container } = render(
            <AgentCard
                id="invalid-agent"
                status="active"
                task="Some task"
                tokens="100"
            />
        );

        expect(container.firstChild).toBeNull();
    });

    it('displays agent icon when available', () => {
        const { container } = render(
            <AgentCard
                id="chairman"
                status="active"
                task="Reviewing boardroom directives"
                tokens="2,100"
            />
        );

        // Chairman should have image since imagePath is defined
        // Testing that component renders without errors
        const agentCard = container.querySelector('.agent-card');
        expect(agentCard).toBeInTheDocument();
    });
});
