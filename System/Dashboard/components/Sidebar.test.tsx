import React from 'react';
import { render, screen } from '@testing-library/react';
import Sidebar from './Sidebar';

// Mock Next.js navigation
jest.mock('next/navigation', () => ({
    usePathname: jest.fn(),
}));

// Mock data
jest.mock('@/lib/data', () => ({
    SYSTEM_STATUS: {
        statusText: 'All Systems Operational',
        color: '#10b981',
        issueCount: 0
    }
}));

const { usePathname } = require('next/navigation');

describe('Sidebar', () => {
    beforeEach(() => {
        usePathname.mockReturnValue('/');
    });

    it('renders all navigation sections', () => {
        render(<Sidebar />);

        expect(screen.getByText('NAVIGATION')).toBeInTheDocument();
        expect(screen.getByText('COMMAND CENTER')).toBeInTheDocument();
        expect(screen.getByText('C-SUITE')).toBeInTheDocument();
    });

    it('renders all C-suite role links', () => {
        render(<Sidebar />);

        expect(screen.getByText('Chairman')).toBeInTheDocument();
        expect(screen.getByText('CEO')).toBeInTheDocument();
        expect(screen.getByText('CFO')).toBeInTheDocument();
        expect(screen.getByText('CMO')).toBeInTheDocument();
        expect(screen.getByText('COO')).toBeInTheDocument();
        expect(screen.getByText('CIO')).toBeInTheDocument();
        expect(screen.getByText('CLO')).toBeInTheDocument();
        expect(screen.getByText('CPO')).toBeInTheDocument();
        expect(screen.getByText('CTO')).toBeInTheDocument();
        expect(screen.getByText('CXA')).toBeInTheDocument();
    });

    it('applies active class to chairman when on root path', () => {
        usePathname.mockReturnValue('/');
        const { container } = render(<Sidebar />);

        const chairmanLink = container.querySelector('a[href="/"]');
        expect(chairmanLink).toHaveClass('active');
    });

    it('applies active class to chairman when on /chairman path', () => {
        usePathname.mockReturnValue('/chairman');
        const { container } = render(<Sidebar />);

        const chairmanLink = container.querySelector('a[href="/"]');
        expect(chairmanLink).toHaveClass('active');
    });

    it('applies active class to specific role when on role path', () => {
        usePathname.mockReturnValue('/ceo');
        const { container } = render(<Sidebar />);

        const ceoLink = container.querySelector('a[href="/ceo"]');
        expect(ceoLink).toHaveClass('active');
    });

    it('does not apply active class to non-current roles', () => {
        usePathname.mockReturnValue('/cfo');
        const { container } = render(<Sidebar />);

        const ceoLink = container.querySelector('a[href="/ceo"]');
        expect(ceoLink).not.toHaveClass('active');
    });

    it('renders system status indicator', () => {
        render(<Sidebar />);

        expect(screen.getByText('All Systems Operational')).toBeInTheDocument();
    });

    it('renders logo with correct text', () => {
        render(<Sidebar />);

        expect(screen.getByText('C-Suite')).toBeInTheDocument();
        expect(screen.getByText('🍌')).toBeInTheDocument();
    });
});
