// Agent Activity & Status Types
export type AgentStatus = 'active' | 'idle' | 'error';

export interface AgentActivity {
    id: string;
    agentRole: string;
    agentName: string;
    status: AgentStatus;
    activity: string;
    timestamp: string;
    duration?: string;
}

export interface AgentCurrentStatus {
    role: string;
    name: string;
    status: AgentStatus;
    currentTask: string | null;
    lastActive: string;
    idleTime?: number; // minutes
}

// Mock agent activity data
export const AGENT_ACTIVITIES: AgentActivity[] = [
    {
        id: 'act-1',
        agentRole: 'ceo',
        agentName: 'CEO',
        status: 'active',
        activity: 'Analyzing Q4 financial reports and preparing executive summary',
        timestamp: new Date(Date.now() - 2 * 60 * 1000).toISOString(),
    },
    {
        id: 'act-2',
        agentRole: 'cfo',
        agentName: 'CFO',
        status: 'active',
        activity: 'Processing expense reconciliation for January',
        timestamp: new Date(Date.now() - 5 * 60 * 1000).toISOString(),
    },
    {
        id: 'act-3',
        agentRole: 'cmo',
        agentName: 'CMO',
        status: 'idle',
        activity: 'Completed campaign performance analysis',
        timestamp: new Date(Date.now() - 23 * 60 * 1000).toISOString(),
        duration: '12m'
    },
    {
        id: 'act-4',
        agentRole: 'coo',
        agentName: 'COO',
        status: 'active',
        activity: 'Monitoring service health metrics and incident tickets',
        timestamp: new Date(Date.now() - 1 * 60 * 1000).toISOString(),
    },
    {
        id: 'act-5',
        agentRole: 'cio',
        agentName: 'CIO',
        status: 'idle',
        activity: 'Idle',
        timestamp: new Date(Date.now() - 45 * 60 * 1000).toISOString(),
    },
    {
        id: 'act-6',
        agentRole: 'cto',
        agentName: 'CTO',
        status: 'active',
        activity: 'Reviewing deployment pipeline and test results',
        timestamp: new Date(Date.now() - 8 * 60 * 1000).toISOString(),
    },
    {
        id: 'act-7',
        agentRole: 'clo',
        agentName: 'CLO',
        status: 'active',
        activity: 'Auditing compliance documentation and policy updates',
        timestamp: new Date(Date.now() - 15 * 60 * 1000).toISOString(),
    },
    {
        id: 'act-8',
        agentRole: 'cpo',
        agentName: 'CPO',
        status: 'idle',
        activity: 'Task completed: Product roadmap review',
        timestamp: new Date(Date.now() - 18 * 60 * 1000).toISOString(),
        duration: '23m'
    },
    {
        id: 'act-9',
        agentRole: 'cxa',
        agentName: 'CXA',
        status: 'active',
        activity: 'Processing customer feedback analysis for January',
        timestamp: new Date(Date.now() - 10 * 60 * 1000).toISOString(),
    },
];

export const AGENT_CURRENT_STATUS: Record<string, AgentCurrentStatus> = {
    ceo: {
        role: 'ceo',
        name: 'CEO',
        status: 'active',
        currentTask: 'Analyzing Q4 financial reports',
        lastActive: new Date(Date.now() - 2 * 60 * 1000).toISOString(),
    },
    cfo: {
        role: 'cfo',
        name: 'CFO',
        status: 'active',
        currentTask: 'Processing expense reconciliation',
        lastActive: new Date(Date.now() - 5 * 60 * 1000).toISOString(),
    },
    cmo: {
        role: 'cmo',
        name: 'CMO',
        status: 'idle',
        currentTask: null,
        lastActive: new Date(Date.now() - 23 * 60 * 1000).toISOString(),
        idleTime: 23,
    },
    coo: {
        role: 'coo',
        name: 'COO',
        status: 'active',
        currentTask: 'Monitoring service health',
        lastActive: new Date(Date.now() - 1 * 60 * 1000).toISOString(),
    },
    cio: {
        role: 'cio',
        name: 'CIO',
        status: 'idle',
        currentTask: null,
        lastActive: new Date(Date.now() - 45 * 60 * 1000).toISOString(),
        idleTime: 45,
    },
    cto: {
        role: 'cto',
        name: 'CTO',
        status: 'active',
        currentTask: 'Reviewing deployment pipeline',
        lastActive: new Date(Date.now() - 8 * 60 * 1000).toISOString(),
    },
    clo: {
        role: 'clo',
        name: 'CLO',
        status: 'active',
        currentTask: 'Auditing compliance docs',
        lastActive: new Date(Date.now() - 15 * 60 * 1000).toISOString(),
    },
    cpo: {
        role: 'cpo',
        name: 'CPO',
        status: 'idle',
        currentTask: null,
        lastActive: new Date(Date.now() - 18 * 60 * 1000).toISOString(),
        idleTime: 18,
    },
    cxa: {
        role: 'cxa',
        name: 'CXA',
        status: 'active',
        currentTask: 'Processing customer feedback',
        lastActive: new Date(Date.now() - 10 * 60 * 1000).toISOString(),
    },
};
