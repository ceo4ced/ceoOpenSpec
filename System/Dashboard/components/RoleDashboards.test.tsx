
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { ChairmanDashboard, CEODashboard, CMODashboard, CFODashboard } from './RoleDashboards';
import { RED_PHONE_ALERTS, AGENT_STATUS } from '@/lib/data';

// Mock data if needed, but we are using real data from lib/data.ts which describes the UI state.

describe('RoleDashboards Components', () => {

    describe('ChairmanDashboard', () => {
        it('renders Red Phone alerts and they are clickable', () => {
            const onAgentClick = jest.fn();
            render(<ChairmanDashboard onAgentClick={onAgentClick} />);

            // Check if Red Phone section exists if there are alerts
            if (RED_PHONE_ALERTS.length > 0) {
                expect(screen.getByText('RED PHONE ALERTS')).toBeInTheDocument();

                const acknowledgeButtons = screen.getAllByRole('button', { name: /Acknowledge/i });
                expect(acknowledgeButtons.length).toBeGreaterThan(0);

                // Ensure they are clickable
                acknowledgeButtons.forEach(btn => {
                    fireEvent.click(btn);
                    // Currently no side effect is bound, but it should not crash
                });
            }
        });

        it('triggers onAgentClick when an agent card is clicked', () => {
            const onAgentClick = jest.fn();
            render(<ChairmanDashboard onAgentClick={onAgentClick} />);

            // Chairman sees all agents (except himself? No, list includes 'ceo', 'cfo', etc. in the map)
            // The map in ChairmanDashboard is: ['ceo', 'cfo', 'cmo', 'coo', 'cio', 'clo', 'cpo', 'cto', 'cxa']

            const ceoCard = screen.getByText(AGENT_STATUS.ceo.task); // Task text is unique enough or use name if available
            // AgentCard renders name? logic says: name={AGENT_STATUS[key].name} inside AgentCard? 
            // We'd better verify structure. AgentCard usually shows name or role.
            // Let's click the container. 

            // We can find by text of the token count or task, or role name.
            // The layout code: onClick={() => onAgentClick(key)}

            // Let's assume AgentCard renders the ID or Role Name.
            // Looking at AgentCard usage: id={key} ...
            // We probably need to know what AgentCard renders. 
            // But simpler: we just find something we know is in the card.

            // CEO task: "Reviewing Q1 strategy alignment"
            const ceoTask = screen.getByText('Reviewing Q1 strategy alignment');
            fireEvent.click(ceoTask);

            expect(onAgentClick).toHaveBeenCalledWith('ceo');
        });

        it('renders approvals and buttons are clickable', () => {
            render(<ChairmanDashboard />);
            const checks = screen.getAllByText('✓');
            const crosses = screen.getAllByText('✗');

            expect(checks.length).toBeGreaterThan(0);
            expect(crosses.length).toBeGreaterThan(0);

            fireEvent.click(checks[0]);
            fireEvent.click(crosses[0]);
        });
    });

    describe('CEODashboard', () => {
        it('renders token usage and performance metrics', () => {
            render(<CEODashboard />);

            // CEO dashboard shows token usage
            expect(screen.getByText("Today's Tokens")).toBeInTheDocument();
            expect(screen.getByText("24.5K")).toBeInTheDocument();

            // Shows performance metrics
            expect(screen.getByText("Task Success Rate")).toBeInTheDocument();
            expect(screen.getByText("94%")).toBeInTheDocument();
        });

        it('renders recent tasks', () => {
            render(<CEODashboard />);

            expect(screen.getByText("Analyzed Q4 Financial Reports")).toBeInTheDocument();
            expect(screen.getByText("Prepared Executive Summary")).toBeInTheDocument();
            expect(screen.getByText("Reviewing Strategic Initiatives")).toBeInTheDocument();
        });
    });

    describe('CMODashboard', () => {
        it('switches tabs between Acquisition and Engagement', () => {
            render(<CMODashboard />);

            // Default is Acquisition
            expect(screen.getByRole('button', { name: /Acquisition/i })).toHaveClass('active');
            expect(screen.getByText('ROAS by Channel')).toBeInTheDocument();
            expect(screen.queryByText('Social Media Sentiment')).not.toBeInTheDocument();

            // Click Engagement
            fireEvent.click(screen.getByRole('button', { name: /Engagement & Brand/i }));

            // Expect content change
            expect(screen.getByText('Social Media Sentiment')).toBeInTheDocument();
            expect(screen.queryByText('ROAS by Channel')).not.toBeInTheDocument();

            // Toggle back
            fireEvent.click(screen.getByRole('button', { name: /Acquisition/i }));
            expect(screen.getByText('ROAS by Channel')).toBeInTheDocument();
        });
    });

    describe('CFODashboard', () => {
        it('has clickable control buttons', () => {
            render(<CFODashboard />);

            const pauseBtn = screen.getByRole('button', { name: /Emergency Pause/i });
            const adjustBtn = screen.getByRole('button', { name: /Adjust Budgets/i });
            const costBtn = screen.getByRole('button', { name: /Cost Mode/i });

            expect(pauseBtn).toBeInTheDocument();
            expect(adjustBtn).toBeInTheDocument();
            expect(costBtn).toBeInTheDocument();

            fireEvent.click(pauseBtn);
            fireEvent.click(adjustBtn);
            fireEvent.click(costBtn);
        });
    });
});
