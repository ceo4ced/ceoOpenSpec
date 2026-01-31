import React from 'react';
import { render, screen } from '@testing-library/react';
import FinancePage from './page';

describe('Finance Page', () => {
    it('renders page title', () => {
        render(<FinancePage />);
        expect(screen.getByText('Finance')).toBeInTheDocument();
    });

    it('renders placeholder message', () => {
        render(<FinancePage />);
        expect(screen.getByText('Financial reports and ledgers coming soon.')).toBeInTheDocument();
    });

    it('renders within dashboard content container', () => {
        const { container } = render(<FinancePage />);
        const contentDiv = container.querySelector('.dashboard-content');
        expect(contentDiv).toBeInTheDocument();
    });
});
