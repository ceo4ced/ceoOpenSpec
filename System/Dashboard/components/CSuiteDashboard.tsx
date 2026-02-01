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
import PlanSection from './PlanSection';
import FunctionActivitySection from './FunctionActivitySection';

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
        <div className="dashboard-content">
            {/* FLEXIBLE ZONE - Scrollable content area */}
            <div className="flexible-zone">
                {/* Plan Section - Shows role's plan document */}
                <div className="dashboard-grid">
                    <div className="col-12">
                        <PlanSection role={role} />
                    </div>
                </div>

                {/* Function Activity Section - Shows function executions */}
                <div className="dashboard-grid">
                    <div className="col-12">
                        <FunctionActivitySection role={role} />
                    </div>
                </div>

                {/* Original dashboard content */}
                {renderOriginalDashboard()}

                {/* Token Performance Card for non-CEO roles */}
                {showTokenCard && <TokenPerformanceCard role={role} />}
            </div>

            {/* FIXED ZONE - Always at bottom */}
            <div className="fixed-zone">
                <AgentActivityConsole />
            </div>
        </div>
    );
}
