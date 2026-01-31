import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Onboarding from './page';

// Mock Next.js navigation
jest.mock('next/navigation', () => ({
    useRouter: jest.fn(),
}));

const { useRouter } = require('next/navigation');

describe('Onboarding Page', () => {
    const mockPush = jest.fn();

    beforeEach(() => {
        mockPush.mockClear();
        useRouter.mockReturnValue({
            push: mockPush,
        });
    });

    it('renders initial step (step 1)', () => {
        render(<Onboarding />);

        expect(screen.getByText('Initialize C-Suite')).toBeInTheDocument();
        expect(screen.getByText('Creator Identity')).toBeInTheDocument();
        expect(screen.getByPlaceholderText('e.g. Jane Doe')).toBeInTheDocument();
    });

    it('displays correct step labels in progress bar', () => {
        render(<Onboarding />);

        expect(screen.getByText('Identity')).toBeInTheDocument();
        expect(screen.getByText('Vision')).toBeInTheDocument();
        expect(screen.getByText('Config')).toBeInTheDocument();
        expect(screen.getByText('Launch')).toBeInTheDocument();
    });

    it('navigation to step 2 works when validation passes', () => {
        render(<Onboarding />);

        const nameInput = screen.getByPlaceholderText('e.g. Jane Doe');
        fireEvent.change(nameInput, { target: { value: 'John Doe' } });

        const continueButton = screen.getByRole('button', { name: /Continue/i });
        fireEvent.click(continueButton);

        expect(screen.getByText('Company Vision')).toBeInTheDocument();
    });

    it('prevents navigation when required field is empty', () => {
        render(<Onboarding />);

        const continueButton = screen.getByRole('button', { name: /Continue/i });
        fireEvent.click(continueButton);

        // Should still be on step 1
        expect(screen.getByText('Creator Identity')).toBeInTheDocument();
    });

    it('back button is disabled on step 1', () => {
        render(<Onboarding />);

        const backButton = screen.getByRole('button', { name: /Back/i });
        expect(backButton).toBeDisabled();
    });

    it('back button navigates to previous step', () => {
        render(<Onboarding />);

        // Go to step 2
        const nameInput = screen.getByPlaceholderText('e.g. Jane Doe');
        fireEvent.change(nameInput, { target: { value: 'John Doe' } });
        fireEvent.click(screen.getByRole('button', { name: /Continue/i }));

        expect(screen.getByText('Company Vision')).toBeInTheDocument();

        // Go back to step 1
        const backButton = screen.getByRole('button', { name: /Back/i });
        fireEvent.click(backButton);

        expect(screen.getByText('Creator Identity')).toBeInTheDocument();
    });

    it('button text changes to "Initialize System" on final step', async () => {
        render(<Onboarding />);

        // Fill step 1
        fireEvent.change(screen.getByPlaceholderText('e.g. Jane Doe'), {
            target: { value: 'John Doe' },
        });
        fireEvent.click(screen.getByRole('button', { name: /Continue/i }));

        // Fill step 2
        fireEvent.change(screen.getByPlaceholderText('e.g. Acme Corp'), {
            target: { value: 'Test Corp' },
        });
        fireEvent.click(screen.getByRole('button', { name: /Continue/i }));

        // Step 3 - no required fields
        fireEvent.click(screen.getByRole('button', { name: /Continue/i }));

        // On step 4
        expect(screen.getByRole('button', { name: /Initialize System/i })).toBeInTheDocument();
    });

    it('redirects to root on launch completion', async () => {
        jest.useFakeTimers();
        render(<Onboarding />);

        // Navigate to final step
        fireEvent.change(screen.getByPlaceholderText('e.g. Jane Doe'), {
            target: { value: 'John Doe' },
        });
        fireEvent.click(screen.getByRole('button', { name: /Continue/i }));

        fireEvent.change(screen.getByPlaceholderText('e.g. Acme Corp'), {
            target: { value: 'Test Corp' },
        });
        fireEvent.click(screen.getByRole('button', { name: /Continue/i }));
        fireEvent.click(screen.getByRole('button', { name: /Continue/i }));

        // Click launch
        fireEvent.click(screen.getByRole('button', { name: /Initialize System/i }));

        // Fast-forward timers
        jest.advanceTimersByTime(2000);

        await waitFor(() => {
            expect(mockPush).toHaveBeenCalledWith('/chairman');
        });

        jest.useRealTimers();
    });

    it('updates form data correctly', () => {
        render(<Onboarding />);

        const nameInput = screen.getByPlaceholderText('e.g. Jane Doe');
        fireEvent.change(nameInput, { target: { value: 'Test User' } });

        expect(nameInput).toHaveValue('Test User');
    });

    it('displays step 3 configuration options', async () => {
        render(<Onboarding />);

        // Navigate to step 3
        fireEvent.change(screen.getByPlaceholderText('e.g. Jane Doe'), {
            target: { value: 'John Doe' },
        });
        fireEvent.click(screen.getByRole('button', { name: /Continue/i }));

        fireEvent.change(screen.getByPlaceholderText('e.g. Acme Corp'), {
            target: { value: 'Test Corp' },
        });
        fireEvent.click(screen.getByRole('button', { name: /Continue/i }));

        expect(screen.getByText('System Configuration')).toBeInTheDocument();
        expect(screen.getByText('Operating Mode')).toBeInTheDocument();
    });

    it('displays summary on step 4', async () => {
        render(<Onboarding />);

        // Navigate to step 4
        fireEvent.change(screen.getByPlaceholderText('e.g. Jane Doe'), {
            target: { value: 'John Doe' },
        });
        fireEvent.click(screen.getByRole('button', { name: /Continue/i }));

        fireEvent.change(screen.getByPlaceholderText('e.g. Acme Corp'), {
            target: { value: 'Acme Corp' },
        });
        fireEvent.click(screen.getByRole('button', { name: /Continue/i }));
        fireEvent.click(screen.getByRole('button', { name: /Continue/i }));

        expect(screen.getByText('Ready to Launch')).toBeInTheDocument();
        expect(screen.getByText('John Doe')).toBeInTheDocument();
        expect(screen.getByText('Acme Corp')).toBeInTheDocument();
    });
});
