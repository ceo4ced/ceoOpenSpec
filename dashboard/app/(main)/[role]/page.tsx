
'use client';

import React, { useState } from 'react';
import { notFound, useParams } from 'next/navigation';
import ProfileSidebar from '@/components/ProfileSidebar';
import {
    ChairmanDashboard,
    MetricsGrid
} from '@/components/RoleDashboards';
import CSuiteDashboard from '@/components/CSuiteDashboard';
import { AGENTS } from '@/lib/data';


export default function RolePage() {
    const params = useParams();
    const role = (Array.isArray(params.role) ? params.role[0] : params.role) || 'chairman';

    // Validate role
    if (!AGENTS[role] && role !== 'chairman') {
        // Note: chairman is in AGENTS, but just to be safe if Logic changes
    }

    const [selectedAgent, setSelectedAgent] = useState<string | null>(null);
    const [isProfileOpen, setIsProfileOpen] = useState(false);

    const handleAgentClick = (agentId: string) => {
        setSelectedAgent(agentId);
        setIsProfileOpen(true);
    };

    const closeProfile = () => {
        setIsProfileOpen(false);
    };

    // Render logic
    const renderContent = () => {
        // Chairman gets special dashboard
        if (role === 'chairman') {
            return <ChairmanDashboard onAgentClick={handleAgentClick} />;
        }

        // All other C-Suite roles get the new dashboard with activity console
        const cSuiteRoles = ['ceo', 'cfo', 'cmo', 'coo', 'cio', 'clo', 'cpo', 'cto', 'cxa'];
        if (cSuiteRoles.includes(role)) {
            return <CSuiteDashboard role={role} />;
        }

        // Fallback
        return <div className="p-4">Dashboard not found for {role}</div>;
    };

    const agentName = AGENTS[role]?.name || 'Chairman';
    const pageTitle = `${agentName} Dashboard`;

    return (
        <>
            <main className="main-content">
                <header className="main-header">
                    <div className="header-left">
                        <h1 className="page-title" id="pageTitle">{pageTitle}</h1>
                    </div>
                    <div className="header-right">
                        <div className="last-updated" id="lastUpdated">Last Updated: Just now</div>
                        <button className="btn btn-secondary" onClick={() => window.location.reload()}>Refresh</button>
                        <button className="btn btn-danger" onClick={() => window.location.href = '/red-phone'}>🚨 RED PHONE</button>
                    </div>
                </header>

                <div className="dashboard-content" id="dashboardContent">
                    {/* Metrics for ALL roles */}
                    <MetricsGrid role={role} />

                    {/* Role Specific Content */}
                    {renderContent()}
                </div>
            </main>

            <ProfileSidebar
                agentId={selectedAgent}
                isOpen={isProfileOpen}
                onClose={closeProfile}
            />
        </>
    );
}
