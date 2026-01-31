import React from 'react';
import { render, screen } from '@testing-library/react';
import AgentsPage from './page';

describe('Agents Page', () => {
    it('renders page title', () => {
        render(<AgentsPage />);
        expect(screen.getByText('Agents')).toBeInTheDocument();
    });

    it('renders placeholder message', () => {
        render(<AgentsPage />);
        expect(screen.getByText('Detailed agent configuration and monitoring coming soon.')).toBeInTheDocument();
    });

    it('renders within dashboard content container', () => {
        const { container } = render(<AgentsPage />);
        const contentDiv = container.querySelector('.dashboard-content');
        expect(contentDiv).toBeInTheDocument();
    });
});
