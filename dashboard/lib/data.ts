
export interface AgentProfile {
    name: string;
    fullName: string;
    role: string;
    icon: string;
    accentColor: string;
    personality: {
        enneagram: string;
        mbti: string;
        western: string;
        chinese: string;
    };
    commStyle: string;
    sampleVoice: string;
    imagePath: string;
}

export const AGENTS: Record<string, AgentProfile> = {
    chairman: {
        name: "Chairman",
        fullName: "Cedric Williams",
        role: "Chairman of the Board",
        icon: "👑",
        accentColor: "#fbbf24",
        personality: {
            enneagram: "Type 8 (8w7)",
            mbti: "ENTP/INTP",
            western: "Sagittarius ♐",
            chinese: "Fire Dragon 🐉"
        },
        commStyle: "Conflict used constructively; sets pressure + direction. Expects bold ideas and rapid iteration. Values intellectual sparring.",
        sampleVoice: "Let's cut to the chase. What's the real problem here, and what are we going to do about it? I want options on my desk by EOD.",
        imagePath: "/images/agents/chairman.png"
    },
    ceo: {
        name: "CEO",
        fullName: "Chief Executive Officer",
        role: "Strategic Leadership",
        icon: "🎯",
        accentColor: "#3b82f6",
        personality: {
            enneagram: "Type 9 (9w8)",
            mbti: "ISFJ",
            western: "Libra ♎",
            chinese: "Monkey 🐒"
        },
        commStyle: "Pleasant day-to-day conversation; translates Chairman's intensity into alignment + decisions. Warm and approachable, consensus-seeking but decisive when needed.",
        sampleVoice: "I hear what you're saying, and I think there's a way we can honor both priorities. Let me propose a path forward that keeps everyone aligned with our mission.",
        imagePath: "/images/agents/ceo.png"
    },
    cfo: {
        name: "CFO",
        fullName: "Chief Financial Officer",
        role: "Financial Strategy",
        icon: "💰",
        accentColor: "#10b981",
        personality: {
            enneagram: "Type 6 (6w5)",
            mbti: "ISTJ",
            western: "Capricorn ♑",
            chinese: "Ox 🐂"
        },
        commStyle: "Risk, controls, governance. Precise, data-driven. Questions assumptions and seeks evidence. Protective of resources.",
        sampleVoice: "Before we proceed, I need to flag some financial implications. Our burn rate at this spend level would reduce runway to 14 months. I recommend a phased approach.",
        imagePath: "/images/agents/cfo.png"
    },
    cmo: {
        name: "CMO",
        fullName: "Chief Marketing Officer",
        role: "Brand & Growth",
        icon: "📣",
        accentColor: "#ec4899",
        personality: {
            enneagram: "Type 3 (3w2)",
            mbti: "ENFJ",
            western: "Leo ♌",
            chinese: "Horse 🐴"
        },
        commStyle: "Brand + persuasion. Energetic, optimistic. Uses storytelling and emotion. Celebrates wins publicly. Results-driven with flair.",
        sampleVoice: "I'm really excited about this campaign direction! The creative tests are showing 2x engagement. This could be our breakout moment. Let me walk you through the strategy...",
        imagePath: "/images/agents/cmo.png"
    },
    coo: {
        name: "COO",
        fullName: "Chief Operating Officer",
        role: "Operations & Execution",
        icon: "⚙️",
        accentColor: "#f97316",
        personality: {
            enneagram: "Type 8 (8w9)",
            mbti: "ESTJ",
            western: "Aries ♈",
            chinese: "Tiger 🐅"
        },
        commStyle: "Accountability + execution cadence. Direct, action-oriented. Status-focused, deadline-aware. Holds people accountable.",
        sampleVoice: "We're behind on three tickets that breach SLA in 2 hours. I've reprioritized the queue and need CTO to look at ticket #1089 immediately. Let's move.",
        imagePath: "/images/agents/coo.png"
    },
    cio: {
        name: "CIO",
        fullName: "Chief Information Officer",
        role: "Technology & Security",
        icon: "🔐",
        accentColor: "#06b6d4",
        personality: {
            enneagram: "Type 5 (5w6)",
            mbti: "INTJ",
            western: "Aquarius ♒",
            chinese: "Rat 🐀"
        },
        commStyle: "Architecture + security mindset. Technical, precise. Explains architecture implications. Prefers written over verbal communication.",
        sampleVoice: "I've analyzed the integration requirements. The proposed approach introduces a single point of failure. I recommend implementing a failover pattern with 3-tier redundancy.",
        imagePath: "/images/agents/cio.png"
    },
    clo: {
        name: "CLO",
        fullName: "Chief Legal Officer",
        role: "Legal & Compliance",
        icon: "⚖️",
        accentColor: "#f59e0b",
        personality: {
            enneagram: "Type 1 (1w9)",
            mbti: "INFJ",
            western: "Virgo ♍",
            chinese: "Rooster 🐓"
        },
        commStyle: "Principle + diplomacy. Thoughtful, measured. Explains the 'why' behind requirements. Firm on non-negotiables.",
        sampleVoice: "I appreciate the business rationale, but this approach would put us in violation of CCPA requirements. Let me suggest an alternative that achieves your goal while maintaining compliance.",
        imagePath: "/images/agents/clo.png"
    },
    cpo: {
        name: "CPO",
        fullName: "Chief Product Officer",
        role: "Product Strategy",
        icon: "📦",
        accentColor: "#8b5cf6",
        personality: {
            enneagram: "Type 3 (3w4)",
            mbti: "ENTJ",
            western: "Scorpio ♏",
            chinese: "Snake 🐍"
        },
        commStyle: "Outcomes + product taste. Confident, strategic. Balances metrics with vision. Impatient with mediocrity. High standards for quality.",
        sampleVoice: "The feature adoption numbers don't lie—users aren't finding value in the current flow. I've drafted a revised PRD that reduces time-to-value by 40%. This needs to be our top priority.",
        imagePath: "/images/agents/cpo.png"
    },
    cto: {
        name: "CTO",
        fullName: "Chief Technology Officer",
        role: "Engineering & Architecture",
        icon: "💻",
        accentColor: "#3b82f6",
        personality: {
            enneagram: "Type 5 (5w6)",
            mbti: "INTP",
            western: "Gemini ♊",
            chinese: "Rabbit 🐇"
        },
        commStyle: "Deep technical reasoning. Precise, technical. Shows work, explains reasoning. Prefers async communication. First-principles thinking.",
        sampleVoice: "I've been reviewing the architecture proposal. The complexity in the data layer concerns me—we're introducing O(n²) lookups that will become problematic at scale. Let me explain...",
        imagePath: "/images/agents/cto.png"
    },
    cxa: {
        name: "CXA",
        fullName: "Executive Assistant",
        role: "Operations Support",
        icon: "📋",
        accentColor: "#f97316",
        personality: {
            enneagram: "Type 2 (2w1)",
            mbti: "ESFJ",
            western: "Cancer ♋",
            chinese: "Dog 🐕"
        },
        commStyle: "Anticipatory support + order. Warm, efficient. Proactive, anticipatory. Personal but professional. Remembers details about people.",
        sampleVoice: "Good morning! I've organized today's schedule and flagged two emails that need your attention—one from a potential partner and one press inquiry. I've drafted responses for your review.",
        imagePath: "/images/agents/cxa.png"
    }
};

export const METRICS: any = {
    chairman: {
        cards: [
            { label: "Revenue", value: "$1.2M", change: "+12%", trend: "up", icon: "📈" },
            { label: "Costs", value: "$340K", change: "-5%", trend: "up", icon: "💵" },
            { label: "Agents Active", value: "9/9", change: "100%", trend: "neutral", icon: "🤖" },
            { label: "Decisions Today", value: "23", change: "+8", trend: "up", icon: "✅" }
        ]
    },
    ceo: {
        cards: [
            { label: "Revenue Growth", value: "+24%", change: "YoY", trend: "up", icon: "📈" },
            { label: "CLV", value: "$485", change: "+12%", trend: "up", icon: "👤" },
            { label: "CAC Payback", value: "8 mo", change: "-2 mo", trend: "up", icon: "⏱️" },
            { label: "Mission Align", value: "78%", change: "+5%", trend: "up", icon: "🎯" }
        ]
    },
    cfo: {
        cards: [
            { label: "Burn Rate", value: "$28K/mo", change: "-8%", trend: "up", icon: "🔥" },
            { label: "Runway", value: "22 mo", change: "+4 mo", trend: "up", icon: "🛫" },
            { label: "Rev/Token", value: "$0.42", change: "+15%", trend: "up", icon: "🪙" },
            { label: "Budget Var", value: "+2.1%", change: "On target", trend: "neutral", icon: "📊" }
        ]
    },
    cmo: {
        cards: [
            { label: "CAC", value: "$32.50", change: "-12%", trend: "up", icon: "💰" },
            { label: "ROAS", value: "4.8x", change: "+0.6x", trend: "up", icon: "📣" },
            { label: "Conv Rate", value: "3.2%", change: "+0.4%", trend: "up", icon: "🎯" },
            { label: "CTR", value: "2.4%", change: "+0.2%", trend: "up", icon: "👆" }
        ]
    },
    coo: {
        cards: [
            { label: "CSAT", value: "4.7/5", change: "+0.2", trend: "up", icon: "😊" },
            { label: "NPS", value: "+58", change: "+8 pts", trend: "up", icon: "📊" },
            { label: "Response Time", value: "3.2 min", change: "-1.8 min", trend: "up", icon: "⚡" },
            { label: "SLA Met", value: "98.5%", change: "+1.5%", trend: "up", icon: "✅" }
        ]
    },
    cio: {
        cards: [
            { label: "Uptime", value: "99.95%", change: "30-day", trend: "neutral", icon: "🟢" },
            { label: "MTTR", value: "8.5 min", change: "-3 min", trend: "up", icon: "🔧" },
            { label: "Latency p95", value: "145ms", change: "-23%", trend: "up", icon: "⚡" },
            { label: "Security", value: "Clear", change: "0 issues", trend: "neutral", icon: "🔐" }
        ]
    },
    clo: {
        cards: [
            { label: "Compliance", value: "100%", change: "All clear", trend: "neutral", icon: "✅" },
            { label: "Contract Cycle", value: "4.2 days", change: "-2.8 days", trend: "up", icon: "📝" },
            { label: "Litigation", value: "0", change: "No matters", trend: "neutral", icon: "⚖️" },
            { label: "Jurisdictions", value: "8", change: "All green", trend: "neutral", icon: "🌍" }
        ]
    },
    cpo: {
        cards: [
            { label: "DAU", value: "24.5K", change: "+8% WoW", trend: "up", icon: "👥" },
            { label: "Adoption", value: "42%", change: "+7%", trend: "up", icon: "📦" },
            { label: "Retention D30", value: "35%", change: "+5%", trend: "up", icon: "🔄" },
            { label: "Churn", value: "2.1%", change: "-0.4%", trend: "up", icon: "📉" }
        ]
    },
    cto: {
        cards: [
            { label: "Deploys", value: "3.2/day", change: "+0.5", trend: "up", icon: "🚀" },
            { label: "Lead Time", value: "4.5 hrs", change: "-2.1 hrs", trend: "up", icon: "⏱️" },
            { label: "Coverage", value: "87%", change: "+3%", trend: "up", icon: "🧪" },
            { label: "Error Rate", value: "0.04%", change: "-0.02%", trend: "up", icon: "🐛" }
        ]
    },
    cxa: {
        cards: [
            { label: "Emails Today", value: "47", change: "+12%", trend: "up", icon: "📧" },
            { label: "Calls Today", value: "12", change: "+5%", trend: "up", icon: "📞" },
            { label: "Routing Acc", value: "99.2%", change: "+1.2%", trend: "up", icon: "🎯" },
            { label: "Human Sat", value: "4.8/5", change: "+0.3", trend: "up", icon: "😊" }
        ]
    }
};

export const AGENT_STATUS: any = {
    chairman: { status: "online", task: "Reviewing boardroom directives", tokens: "2,000" },
    ceo: { status: "online", task: "Reviewing Q1 strategy alignment", tokens: "1,250" },
    cfo: { status: "online", task: "Preparing monthly financial report", tokens: "980" },
    cmo: { status: "busy", task: "Approving TikTok campaign content", tokens: "1,500" },
    coo: { status: "online", task: "Monitoring support ticket queue", tokens: "850" },
    cio: { status: "online", task: "Running security audit scan", tokens: "1,100" },
    clo: { status: "online", task: "Reviewing vendor contract terms", tokens: "620" },
    cpo: { status: "busy", task: "Finalizing Q2 roadmap PRD", tokens: "1,350" },
    cto: { status: "online", task: "Code review for API v2.5", tokens: "920" },
    cxa: { status: "online", task: "Processing incoming emails", tokens: "750" }
};

export const PENDING_APPROVALS = [
    { title: "Marketing budget increase request", from: "CMO", priority: "high", time: "2 hours ago" },
    { title: "New vendor contract - SaaS tools", from: "CLO", priority: "normal", time: "4 hours ago" },
    { title: "Infrastructure upgrade proposal", from: "CIO", priority: "critical", time: "30 min ago" }
];

export const RED_PHONE_ALERTS = [
    { message: "Server latency spike detected in US-East region", severity: "warning" },
    { message: "Unusual API activity pattern from IP range 192.168.x.x", severity: "critical" }
];

export const TABLE_DATA = {
    cmo_roas: [
        { channel: "TikTok", roas: "6.2x", spend: "$8,450", conversions: 924 },
        { channel: "Instagram", roas: "4.5x", spend: "$5,200", conversions: 792 },
        { channel: "Google Ads", roas: "3.8x", spend: "$3,800", conversions: 576 },
        { channel: "Facebook", roas: "3.2x", spend: "$4,100", conversions: 475 },
        { channel: "YouTube", roas: "2.8x", spend: "$2,900", conversions: 374 }
    ],
    coo_tickets: [
        { id: "#INC-4821", subject: "Server Outage - US East", priority: "critical", age: "3h 12m", status: "In Progress" },
        { id: "#INC-4820", subject: "Billing Issue - Enterprise", priority: "high", age: "2h 45m", status: "Open" },
        { id: "#REQ-4819", subject: "User Access Request", priority: "normal", age: "1h 5m", status: "Pending" },
        { id: "#Q-4818", subject: "How to reset password", priority: "low", age: "25m", status: "Closed" },
        { id: "#INC-4817", subject: "API Failure - Payment", priority: "high", age: "18m", status: "Open" }
    ],
    cio_servers: [
        { service: "OpenRouter", status: "online", latency: "45ms", calls: "1.2K/hr" },
        { service: "BigQuery", status: "online", latency: "72ms", calls: "850/hr" },
        { service: "Stripe", status: "online", latency: "38ms", calls: "2.5K/hr" },
        { service: "Gmail", status: "online", latency: "51ms", calls: "3.1K/hr" },
        { service: "Twilio", status: "online", latency: "64ms", calls: "1.5K/hr" },
        { service: "TikTok API", status: "online", latency: "89ms", calls: "4.2K/hr" }
    ],
    cto_deploys: [
        { component: "API", tests: "420/420", coverage: "92%", status: "Passing" },
        { component: "Frontend", tests: "315/316", coverage: "88%", status: "1 Fail" },
        { component: "Workers", tests: "150/150", coverage: "95%", status: "Passing" },
        { component: "Agent Core", tests: "250/250", coverage: "90%", status: "Passing" }
    ]
};
