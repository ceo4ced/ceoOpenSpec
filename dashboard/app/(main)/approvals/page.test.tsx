import React from 'react';
import { render, screen } from '@testing-library/react';
import ApprovalsPage from './page';

describe('Approvals Page', () => {
    it('renders page title', () => {
        render(<ApprovalsPage />);
        expect(screen.getByText('Approvals')).toBeInTheDocument();
    });

    it('renders placeholder message', () => {
        render(<ApprovalsPage />);
        expect(screen.getByText('Pending and historical approval logs coming soon.')).toBeInTheDocument();
    });

    it('renders within dashboard content container', () => {
        const { container } = render(<ApprovalsPage />);
        const contentDiv = container.querySelector('.dashboard-content');
        expect(contentDiv).toBeInTheDocument();
    });
});
