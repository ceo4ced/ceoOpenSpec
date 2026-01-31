import React from 'react';
import {
    CEODashboard,
    CFODashboard,
    CMODashboard,
    COODashboard,
    CIODashboard,
    CLODashboard,
    CPODashboard,
    CTODashboard,
    CXADashboard
} from './RoleDashboards';
import AgentActivityConsole from './AgentActivityConsole';
import TokenPerformanceCard from './TokenPerformanceCard';

interface CSuiteDashboardProps {
    role: string;
    onAgentClick?: (id: string) => void;
}

export default function CSuiteDashboard({ role, onAgentClick }: CSuiteDashboardProps) {
    const renderOriginalDashboard = () => {
        switch (role) {
            case 'ceo': return <CEODashboard onAgentClick={onAgentClick} />;
            case 'cfo': return <CFODashboard />;
            case 'cmo': return <CMODashboard />;
            case 'coo': return <COODashboard />;
            case 'cio': return <CIODashboard />;
            case 'clo': return <CLODashboard />;
            case 'cpo': return <CPODashboard />;
            case 'cto': return <CTODashboard />;
            case 'cxa': return <CXADashboard />;
            default: return null;
        }
    };

    // Roles that get the token performance card (all except CEO which has its own built-in)
    const rolesWithTokenCard = ['cfo', 'cmo', 'coo', 'cio', 'clo', 'cpo', 'cto', 'cxa'];
    const showTokenCard = rolesWithTokenCard.includes(role);

    return (
        <>
            {/* Original dashboard content */}
            {renderOriginalDashboard()}

            {/* Token Performance Card for non-CEO roles - full width, above activity console */}
            {showTokenCard && <TokenPerformanceCard role={role} />}

            {/* Activity Console at the bottom */}
            <div className="dashboard-grid" style={{ marginTop: showTokenCard ? '0' : '2rem' }}>
                <div className="col-12">
                    <AgentActivityConsole />
                </div>
            </div>
        </>
    );
}
