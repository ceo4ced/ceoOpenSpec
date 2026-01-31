
document.addEventListener('DOMContentLoaded', () => {
    let currentStep = 1;
    const totalSteps = 4;

    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const progressFill = document.getElementById('progressFill');

    // Initialize
    updateUI();

    // Event Listeners
    nextBtn.addEventListener('click', () => {
        if (currentStep < totalSteps) {
            if (validateStep(currentStep)) {
                currentStep++;
                updateUI();
            }
        } else {
            // Final Step - Launch
            launchSystem();
        }
    });

    prevBtn.addEventListener('click', () => {
        if (currentStep > 1) {
            currentStep--;
            updateUI();
        }
    });

    // Inputs for summary
    document.getElementById('creatorName').addEventListener('input', updateSummary);
    document.getElementById('bizName').addEventListener('input', updateSummary);
    document.getElementById('opMode').addEventListener('change', updateSummary);

    function updateUI() {
        // Toggle Steps
        document.querySelectorAll('.form-step').forEach(step => {
            step.classList.remove('active');
        });
        document.getElementById(`step${currentStep}`).classList.add('active');

        // Update Progress Bar
        const percentage = ((currentStep - 1) / (totalSteps - 1)) * 100;
        progressFill.style.width = `${percentage}%`;

        // Update Step Indicators
        document.querySelectorAll('.step').forEach(step => {
            const stepNum = parseInt(step.dataset.step);
            if (stepNum <= currentStep) {
                step.classList.add('active');
            } else {
                step.classList.remove('active');
            }
        });

        // Button States
        prevBtn.disabled = currentStep === 1;

        if (currentStep === totalSteps) {
            nextBtn.textContent = "Initialize System";
            nextBtn.classList.add('pulse-btn');
            updateSummary();
        } else {
            nextBtn.textContent = "Continue";
            nextBtn.classList.remove('pulse-btn');
        }
    }

    function validateStep(step) {
        let valid = true;

        if (step === 1) {
            const name = document.getElementById('creatorName').value;
            if (!name) { shakeField('creatorName'); valid = false; }
        }

        if (step === 2) {
            const biz = document.getElementById('bizName').value;
            if (!biz) { shakeField('bizName'); valid = false; }
        }

        return valid;
    }

    function shakeField(id) {
        const field = document.getElementById(id);
        field.style.borderColor = '#f87171';
        field.classList.add('shake');
        setTimeout(() => {
            field.classList.remove('shake');
            field.style.borderColor = '#30363d';
        }, 500);
    }

    function updateSummary() {
        document.getElementById('sumCreator').textContent = document.getElementById('creatorName').value || 'Unknown';
        document.getElementById('sumBiz').textContent = document.getElementById('bizName').value || 'Pending';
        document.getElementById('sumMode').textContent = document.getElementById('opMode').value;
    }

    function launchSystem() {
        nextBtn.innerHTML = "Initializing...";
        nextBtn.disabled = true;

        // Simulate initialization delay
        setTimeout(() => {
            // Save state (mock)
            localStorage.setItem('csuite_initialized', 'true');
            window.location.href = 'index.html';
        }, 2000);
    }
});
