import React from 'react';
import { render, screen } from '@testing-library/react';
import MetricCard from './MetricCard';

describe('MetricCard', () => {
    it('renders metric card with all props', () => {
        render(
            <MetricCard
                label="Revenue"
                value="$45.2K"
                change="+12.5%"
                trend="up"
                icon="💰"
            />
        );

        expect(screen.getByText('Revenue')).toBeInTheDocument();
        expect(screen.getByText('$45.2K')).toBeInTheDocument();
        expect(screen.getByText('+12.5%')).toBeInTheDocument();
        expect(screen.getByText('💰')).toBeInTheDocument();
    });

    it('applies positive class for upward trend', () => {
        const { container } = render(
            <MetricCard
                label="Growth"
                value="25%"
                change="+5%"
                trend="up"
                icon="📈"
            />
        );

        const metricValue = container.querySelector('.metric-value.positive');
        expect(metricValue).toBeInTheDocument();
        expect(screen.getByText('↑')).toBeInTheDocument();
    });

    it('applies negative class for downward trend', () => {
        const { container } = render(
            <MetricCard
                label="Churn Rate"
                value="3.2%"
                change="-0.5%"
                trend="down"
                icon="📉"
            />
        );

        const metricValue = container.querySelector('.metric-value.negative');
        expect(metricValue).toBeInTheDocument();
        expect(screen.getByText('↓')).toBeInTheDocument();
    });

    it('applies no special class for neutral trend', () => {
        const { container } = render(
            <MetricCard
                label="Users"
                value="1,234"
                change="0%"
                trend="neutral"
                icon="👥"
            />
        );

        const metricValue = container.querySelector('.metric-value');
        expect(metricValue).toBeInTheDocument();
        expect(metricValue).not.toHaveClass('positive');
        expect(metricValue).not.toHaveClass('negative');
        expect(screen.getByText('•')).toBeInTheDocument();
    });

    it('renders trend change with correct styling', () => {
        const { container } = render(
            <MetricCard
                label="Test"
                value="100"
                change="+10%"
                trend="up"
                icon="🎯"
            />
        );

        const changeElement = container.querySelector('.metric-change.up');
        expect(changeElement).toBeInTheDocument();
    });
});
