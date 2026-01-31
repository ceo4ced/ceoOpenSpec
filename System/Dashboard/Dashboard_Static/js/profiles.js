// Agent Profiles Page

class ProfilesPage {
    constructor() {
        this.init();
    }

    init() {
        this.generateProfileCards();
        this.bindEvents();
    }

    generateProfileCards() {
        const agents = ['ceo', 'cfo', 'cmo', 'coo', 'cio', 'clo', 'cpo', 'cto', 'cxa'];
        const container = document.getElementById('profilesGrid');

        let html = '';

        agents.forEach(key => {
            const agent = AGENTS[key];
            const status = AGENT_STATUS[key] || { status: 'online', task: 'Idle', tokens: '0' };

            html += `
                <div class="profile-card" data-agent="${key}">
                    <div class="profile-card-image">
                        <img src="${agent.imagePath}" alt="${agent.name}" 
                             onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                        <div class="profile-card-placeholder ${key}" style="display: none;">
                            <span>${agent.icon}</span>
                        </div>
                        <div class="profile-card-status">
                            <span class="status-dot ${status.status}"></span>
                            <span>${status.status.charAt(0).toUpperCase() + status.status.slice(1)}</span>
                        </div>
                    </div>
                    <div class="profile-card-body">
                        <h3 class="profile-card-name">${agent.fullName}</h3>
                        <p class="profile-card-role">${agent.name} • ${agent.role}</p>
                        <div class="profile-card-personality">
                            <span class="mini-tag">${agent.personality.enneagram}</span>
                            <span class="mini-tag">${agent.personality.mbti}</span>
                            <span class="mini-tag">${agent.personality.western}</span>
                        </div>
                        <p class="profile-card-task">
                            <span>●</span>
                            <span>${status.task}</span>
                        </p>
                    </div>
                </div>
            `;
        });

        container.innerHTML = html;

        // Handle image fallbacks after DOM is ready
        setTimeout(() => {
            document.querySelectorAll('.profile-card-image img').forEach(img => {
                if (!img.complete || img.naturalHeight === 0) {
                    img.style.display = 'none';
                    img.nextElementSibling.style.display = 'flex';
                }
            });
        }, 100);
    }

    bindEvents() {
        // Profile cards click to open modal
        document.querySelectorAll('.profile-card').forEach(card => {
            card.addEventListener('click', () => {
                const agentKey = card.dataset.agent;
                this.openAgentModal(agentKey);
            });
        });

        // Featured card click
        document.querySelector('.featured-card')?.addEventListener('click', () => {
            this.openAgentModal('chairman');
        });

        // Modal close
        document.querySelectorAll('.close-modal').forEach(btn => {
            btn.addEventListener('click', () => {
                document.getElementById('agentModal').classList.remove('open');
            });
        });

        // Click outside modal to close
        document.getElementById('agentModal').addEventListener('click', (e) => {
            if (e.target.id === 'agentModal') {
                e.target.classList.remove('open');
            }
        });
    }

    openAgentModal(agentKey) {
        const agent = AGENTS[agentKey];
        const status = AGENT_STATUS[agentKey] || { status: 'online', task: 'Idle', tokens: '0' };

        // Populate modal
        document.getElementById('modalName').textContent = agent.fullName;
        document.getElementById('modalRole').textContent = `${agent.name} • ${agent.role}`;
        document.getElementById('modalEnneagram').textContent = agent.personality.enneagram;
        document.getElementById('modalMbti').textContent = agent.personality.mbti;
        document.getElementById('modalWestern').textContent = agent.personality.western;
        document.getElementById('modalChinese').textContent = agent.personality.chinese;
        document.getElementById('modalCommStyle').textContent = agent.commStyle;
        document.getElementById('modalVoice').textContent = agent.sampleVoice;
        document.getElementById('modalTask').textContent = status.task;
        document.getElementById('modalTokens').textContent = status.tokens;
        document.getElementById('modalDecisions').textContent = Math.floor(Math.random() * 20) + 5;
        document.getElementById('modalIcon').textContent = agent.icon;

        // Set image
        const imgEl = document.getElementById('modalImage');
        const placeholderEl = document.getElementById('modalPlaceholder');

        imgEl.src = agent.imagePath;
        imgEl.style.display = 'block';
        placeholderEl.style.display = 'none';

        imgEl.onerror = function () {
            this.style.display = 'none';
            placeholderEl.style.display = 'flex';
        };

        // Set dashboard link
        if (agentKey !== 'chairman') {
            document.getElementById('modalDashboardLink').href = `index.html#${agentKey}`;
        } else {
            document.getElementById('modalDashboardLink').href = 'index.html';
        }

        // Open modal
        document.getElementById('agentModal').classList.add('open');
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.profilesPage = new ProfilesPage();
});
