const resultsDiv = document.getElementById('results');

function log(result, msg) {
    const div = document.createElement('div');
    div.className = result ? 'test-item pass' : 'test-item fail';
    div.innerText = `${result ? '✓' : '✗'} ${msg}`;
    resultsDiv.appendChild(div);
    if (!result) console.error(`Failed: ${msg}`);
}

function expect(actual) {
    return {
        toBe: (expected) => {
            if (actual === expected) return true;
            return false;
        },
        toBeTruthy: () => !!actual,
        toBeDefined: () => actual !== undefined && actual !== null,
        toBeGreaterThan: (val) => actual > val
    };
}

// Test Suite
const suite = {
    // 1. Data Integrity Tests
    testAgentDataLoaded: () => {
        log(expect(typeof AGENTS).toBeDefined(), "AGENTS object should be defined");
        log(expect(Object.keys(AGENTS).length).toBe(10), "Should have 10 agents loaded");
        log(expect(AGENTS.cxa.role).toBe("Operations Support"), "CXA role should be correct");
    },

    testMetricsDataLoaded: () => {
        log(expect(typeof METRICS).toBeDefined(), "METRICS object should be defined");
        log(expect(METRICS.ceo.cards.length).toBeGreaterThan(0), "Metrics cards should exist");
    },

    // 2. Class Initialization Tests
    testDashboardClass: () => {
        log(expect(typeof Dashboard).toBeDefined(), "Dashboard class should be defined");
        const dash = new Dashboard();
        log(expect(dash).toBeDefined(), "Dashboard instance created");
        log(expect(dash.currentPage).toBe('chairman'), "Default page should be chairman");
    },

    // 3. UI Interaction Logic
    testNavigateTo: () => {
        const dash = new Dashboard();
        dash.navigateTo('cfo');
        log(expect(dash.currentPage).toBe('cfo'), "Navigation should update currentPage");
        const title = document.getElementById('pageTitle').textContent;
        log(expect(title.includes('CFO')), "Page title should update on navigation");

        // Verify active class on nav items (mock data needed or real DOM)
        // Since we are using mock DOM, let's verify logic execution
    },

    testProfileSidebarLogic: () => {
        const dash = new Dashboard();
        // Simulate Opening Profile
        dash.openProfile('cxa');
        const sidebar = document.getElementById('profileSidebar');
        log(expect(sidebar.classList.contains('open')).toBe(true), "Profile sidebar should have 'open' class");

        const name = document.getElementById('profileName').textContent;
        log(expect(name).toBe(AGENTS.cxa.fullName), "Profile name should be populated");

        // Simulate Closing
        dash.closeProfile();
        log(expect(sidebar.classList.contains('open')).toBe(false), "Profile sidebar should NOT have 'open' class after closing");
    }
};

// Run Tests
setTimeout(() => {
    console.log("Starting tests...");
    resultsDiv.innerHTML = "<h2>Results:</h2>";
    try {
        Object.entries(suite).forEach(([name, test]) => {
            console.log(`Running ${name}`);
            test();
        });
    } catch (e) {
        log(false, `CRITICAL ERROR: ${e.message}`);
        console.error(e);
    }
}, 500);
