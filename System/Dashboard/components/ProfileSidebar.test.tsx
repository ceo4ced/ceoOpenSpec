import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import ProfileSidebar from './ProfileSidebar';

describe('ProfileSidebar', () => {
    const mockOnClose = jest.fn();

    beforeEach(() => {
        mockOnClose.mockClear();
    });

    it('returns null when agentId is null', () => {
        const { container } = render(
            <ProfileSidebar agentId={null} isOpen={true} onClose={mockOnClose} />
        );
        expect(container.firstChild).toBeNull();
    });

    it('renders sidebar when agent exists', () => {
        render(
            <ProfileSidebar agentId="ceo" isOpen={true} onClose={mockOnClose} />
        );

        expect(screen.getByText('Chief Executive Officer')).toBeInTheDocument();
    });

    it('applies open class when isOpen is true', () => {
        const { container } = render(
            <ProfileSidebar agentId="ceo" isOpen={true} onClose={mockOnClose} />
        );

        const sidebar = container.querySelector('.profile-sidebar.open');
        expect(sidebar).toBeInTheDocument();
    });

    it('does not apply open class when isOpen is false', () => {
        const { container } = render(
            <ProfileSidebar agentId="ceo" isOpen={false} onClose={mockOnClose} />
        );

        const sidebar = container.querySelector('.profile-sidebar.open');
        expect(sidebar).not.toBeInTheDocument();
    });

    it('calls onClose when close button is clicked', () => {
        render(
            <ProfileSidebar agentId="ceo" isOpen={true} onClose={mockOnClose} />
        );

        const closeButton = screen.getByRole('button');
        fireEvent.click(closeButton);

        expect(mockOnClose).toHaveBeenCalledTimes(1);
    });

    it('renders personality profile section', () => {
        render(
            <ProfileSidebar agentId="chairman" isOpen={true} onClose={mockOnClose} />
        );

        expect(screen.getByText('Personality Profile')).toBeInTheDocument();
        expect(screen.getByText('Enneagram')).toBeInTheDocument();
        expect(screen.getByText('MBTI')).toBeInTheDocument();
        expect(screen.getByText('Western')).toBeInTheDocument();
        expect(screen.getByText('Chinese')).toBeInTheDocument();
    });

    it('renders communication style section', () => {
        render(
            <ProfileSidebar agentId="cfo" isOpen={true} onClose={mockOnClose} />
        );

        expect(screen.getByText('Communication Style')).toBeInTheDocument();
    });

    it('renders sample voice section', () => {
        render(
            <ProfileSidebar agentId="cmo" isOpen={true} onClose={mockOnClose} />
        );

        expect(screen.getByText('Sample Voice')).toBeInTheDocument();
    });

    it('renders current status section', () => {
        render(
            <ProfileSidebar agentId="coo" isOpen={true} onClose={mockOnClose} />
        );

        expect(screen.getByText('Current Status')).toBeInTheDocument();
        expect(screen.getByText('Current Task')).toBeInTheDocument();
        expect(screen.getByText('Tokens Today')).toBeInTheDocument();
    });
});
