// Aegis - Frontend Application JavaScript

// ========== Dark Mode Toggle ==========
function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('aegis-theme', newTheme);
}

// Initialize theme from localStorage
function initTheme() {
    const savedTheme = localStorage.getItem('aegis-theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const theme = savedTheme || (prefersDark ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', theme);
}

// Run theme init immediately (before DOMContentLoaded)
initTheme();

document.addEventListener('DOMContentLoaded', function () {
    initFormValidation();
    initModal();
    initLiveRegion();
});

// ========== Form Validation ==========
function initFormValidation() {
    const form = document.getElementById('contact-form');
    if (!form) return;

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        let isValid = true;

        // Validate full name
        const name = document.getElementById('full-name');
        if (name && !name.value.trim()) {
            showError('full-name', 'name-error');
            isValid = false;
        } else if (name) {
            clearError('full-name', 'name-error');
        }

        // Validate email
        const email = document.getElementById('email');
        if (email && (!email.value.trim() || !email.value.includes('@'))) {
            showError('email', 'email-error');
            isValid = false;
        } else if (email) {
            clearError('email', 'email-error');
        }

        // Validate subject
        const subject = document.getElementById('subject');
        if (subject && !subject.value) {
            showError('subject', 'subject-error');
            isValid = false;
        } else if (subject) {
            clearError('subject', 'subject-error');
        }

        // Validate message
        const message = document.getElementById('message');
        if (message && message.value.trim().length < 20) {
            showError('message', 'message-error');
            isValid = false;
        } else if (message) {
            clearError('message', 'message-error');
        }

        const statusDiv = document.getElementById('form-status');
        if (isValid) {
            if (statusDiv) {
                statusDiv.innerHTML = '<div class="alert alert-success" role="status"><span>Form submitted successfully! We\'ll get back to you soon.</span></div>';
            }
            form.reset();
        } else {
            if (statusDiv) {
                statusDiv.innerHTML = '<div class="alert alert-error" role="alert"><span>Please correct the errors above before submitting.</span></div>';
            }
            // Focus first error field
            const firstError = form.querySelector('.has-error input, .has-error select, .has-error textarea');
            if (firstError) firstError.focus();
        }
    });
}

function showError(inputId, errorId) {
    const input = document.getElementById(inputId);
    const error = document.getElementById(errorId);
    if (input) {
        input.parentElement.classList.add('has-error');
        input.setAttribute('aria-invalid', 'true');
        input.setAttribute('aria-describedby', errorId);
    }
    if (error) error.style.display = 'block';
}

function clearError(inputId, errorId) {
    const input = document.getElementById(inputId);
    const error = document.getElementById(errorId);
    if (input) {
        input.parentElement.classList.remove('has-error');
        input.removeAttribute('aria-invalid');
    }
    if (error) error.style.display = 'none';
}

// ========== Modal ==========
function initModal() {
    // Modal can be opened for demo purposes
    document.addEventListener('keydown', function (e) {
        const modal = document.getElementById('modal');
        if (!modal) return;
        
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });
}

function openModal() {
    const modal = document.getElementById('modal');
    if (modal) {
        modal.classList.add('active');
        const firstBtn = modal.querySelector('button');
        if (firstBtn) firstBtn.focus();
    }
}

function closeModal() {
    const modal = document.getElementById('modal');
    if (modal) {
        modal.classList.remove('active');
    }
}

// ========== Live Ticker ==========
let tickerInterval = null;
const tickerMessages = [
    'New scan completed: /about.html - 0 issues found',
    'Issue resolved: Missing alt text on /products.html',
    'New scan started: /checkout.html',
    'Warning: Color contrast issue detected on /landing.html',
    'Scan completed: /contact.html - 2 issues found',
];
let tickerIndex = 0;

function startTicker() {
    const ticker = document.getElementById('live-ticker');
    if (!ticker || tickerInterval) return;

    // BAD: No aria-live attribute on the ticker container
    // (this is intentional for testing - screen readers won't announce updates)
    tickerInterval = setInterval(function () {
        const msg = tickerMessages[tickerIndex % tickerMessages.length];
        ticker.innerHTML = '<p style="color: var(--primary); font-weight:600;">' + msg + '</p>';
        tickerIndex++;
    }, 3000);
}

// ========== Dashboard Actions ==========
function runScan() {
    const status = document.getElementById('dashboard-status');
    if (status) {
        status.textContent = 'Starting new accessibility scan...';
    }
    // Simulated scan
    setTimeout(function () {
        if (status) {
            status.textContent = 'Scan completed. 2 new issues found.';
        }
    }, 2000);
}

function exportReport() {
    const status = document.getElementById('dashboard-status');
    if (status) {
        status.textContent = 'Generating accessibility report...';
    }
    setTimeout(function () {
        if (status) {
            status.textContent = 'Report exported successfully.';
        }
    }, 1500);
}

function clearData() {
    if (confirm('Are you sure you want to clear all data?')) {
        const status = document.getElementById('dashboard-status');
        if (status) {
            status.textContent = 'All data has been cleared.';
        }
    }
}
