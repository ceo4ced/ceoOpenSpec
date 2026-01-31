
'use client';

import React, { useState } from 'react';
import { notFound, useParams } from 'next/navigation';
import ProfileSidebar from '@/components/ProfileSidebar';
import {
    ChairmanDashboard,
    CEODashboard,
    CFODashboard,
    CMODashboard,
    COODashboard,
    CIODashboard,
    CLODashboard,
    CPODashboard,
    CTODashboard,
    CXADashboard,
    MetricsGrid
} from '@/components/RoleDashboards';
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
        switch (role) {
            case 'chairman': return <ChairmanDashboard onAgentClick={handleAgentClick} />;
            case 'ceo': return <CEODashboard onAgentClick={handleAgentClick} />;
            case 'cfo': return <CFODashboard />;
            case 'cmo': return <CMODashboard />;
            case 'coo': return <COODashboard />;
            case 'cio': return <CIODashboard />;
            case 'clo': return <CLODashboard />;
            case 'cpo': return <CPODashboard />;
            case 'cto': return <CTODashboard />;
            case 'cxa': return <CXADashboard />;
            default: return <div className="p-4">Dashboard not found for {role}</div>;
        }
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
                    {/* Common Metrics Row */}
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
