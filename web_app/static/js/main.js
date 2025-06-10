// NYC Property Investment ML - Main JavaScript Functions

// Toast notification system (can be enhanced with proper toast library later)
function showToast(message, type = 'info') {
    // For now, use styled alerts - can be replaced with proper toast notifications
    const alertClass = {
        'info': 'alert-info',
        'success': 'alert-success', 
        'warning': 'alert-warning',
        'error': 'alert-danger'
    }[type] || 'alert-info';
    
    // Simple alert for now - TODO: implement proper toast system
    alert(message);
}

// Currency formatting
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0
    }).format(amount);
}

// Number formatting with commas
function formatNumber(number) {
    return new Intl.NumberFormat('en-US').format(number);
}

// Percentage formatting
function formatPercentage(number, decimals = 1) {
    return `${number.toFixed(decimals)}%`;
}

// Loading animations
function showLoadingSpinner(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `
            <div class="d-flex justify-content-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
        `;
    }
}

function hideLoadingSpinner(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '';
    }
}

// Score classification utilities
function getScoreClass(score) {
    if (score >= 80) return 'score-high';
    if (score >= 60) return 'score-medium';
    return 'score-low';
}

function getScoreEmoji(score) {
    if (score >= 80) return '🟢';
    if (score >= 60) return '🟡';
    return '🔴';
}

function getRiskClass(risk) {
    const riskMap = {
        'Low': 'score-high',
        'Medium': 'score-medium', 
        'High': 'score-low'
    };
    return riskMap[risk] || 'score-medium';
}

function getRiskEmoji(risk) {
    const riskMap = {
        'Low': '🟢',
        'Medium': '🟡',
        'High': '🔴'
    };
    return riskMap[risk] || '🟡';
}

// Animation helpers
function fadeIn(element) {
    if (element) {
        element.classList.add('fade-in');
        // Remove the class after animation completes to allow re-use
        setTimeout(() => {
            element.classList.remove('fade-in');
        }, 500);
    }
}

function slideIn(element, direction = 'up') {
    if (element) {
        element.classList.add(`slide-in-${direction}`);
        setTimeout(() => {
            element.classList.remove(`slide-in-${direction}`);
        }, 500);
    }
}

// Scroll utilities
function scrollToElement(elementId, offset = 0) {
    const element = document.getElementById(elementId);
    if (element) {
        const elementPosition = element.offsetTop - offset;
        window.scrollTo({
            top: elementPosition,
            behavior: 'smooth'
        });
    }
}

function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Modal utilities  
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    }
}

function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        const bsModal = bootstrap.Modal.getInstance(modal);
        if (bsModal) {
            bsModal.hide();
        }
    }
}

// Form utilities
function clearForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.reset();
    }
}

function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function validateAddress(address) {
    // Basic validation for NYC addresses
    const nycKeywords = ['new york', 'ny', 'manhattan', 'brooklyn', 'queens', 'bronx', 'staten island'];
    const addressLower = address.toLowerCase();
    return nycKeywords.some(keyword => addressLower.includes(keyword)) && address.length > 10;
}

// Data processing utilities
function calculateAverage(numbers) {
    if (!numbers || numbers.length === 0) return 0;
    const sum = numbers.reduce((acc, num) => acc + num, 0);
    return sum / numbers.length;
}

function findMinMax(numbers) {
    if (!numbers || numbers.length === 0) return { min: 0, max: 0 };
    return {
        min: Math.min(...numbers),
        max: Math.max(...numbers)
    };
}

// Chart utilities (for future Chart.js integration)
function createScoreChart(canvasId, scores) {
    // Placeholder for Chart.js implementation
    console.log(`Creating chart for ${canvasId} with scores:`, scores);
}

// Local storage utilities (with error handling)
function saveToLocalStorage(key, data) {
    try {
        localStorage.setItem(key, JSON.stringify(data));
        return true;
    } catch (error) {
        console.warn('Could not save to localStorage:', error);
        return false;
    }
}

function loadFromLocalStorage(key) {
    try {
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : null;
    } catch (error) {
        console.warn('Could not load from localStorage:', error);
        return null;
    }
}

// API utilities
async function makeApiRequest(url, options = {}) {
    try {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };
        
        const response = await fetch(url, { ...defaultOptions, ...options });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

// Debounce utility for search inputs
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Copy to clipboard utility
async function copyToClipboard(text) {
    try {
        if (navigator.clipboard && window.isSecureContext) {
            await navigator.clipboard.writeText(text);
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
        }
        showToast('Copied to clipboard!', 'success');
        return true;
    } catch (error) {
        console.error('Failed to copy to clipboard:', error);
        showToast('Failed to copy to clipboard', 'error');
        return false;
    }
}

// Export all utilities to global scope
window.PropertyAnalysisUtils = {
    // Core utilities
    showToast,
    formatCurrency,
    formatNumber,
    formatPercentage,
    
    // Loading states
    showLoadingSpinner,
    hideLoadingSpinner,
    
    // Score utilities
    getScoreClass,
    getScoreEmoji,
    getRiskClass,
    getRiskEmoji,
    
    // Animations
    fadeIn,
    slideIn,
    
    // Navigation
    scrollToElement,
    scrollToTop,
    
    // Modals
    showModal,
    hideModal,
    
    // Forms
    clearForm,
    validateEmail,
    validateAddress,
    
    // Data processing
    calculateAverage,
    findMinMax,
    
    // Charts
    createScoreChart,
    
    // Storage
    saveToLocalStorage,
    loadFromLocalStorage,
    
    // API
    makeApiRequest,
    
    // Utilities
    debounce,
    copyToClipboard
};

// Initialize any global event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling to all anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Add loading class to buttons when clicked
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function() {
            if (this.type === 'submit') {
                this.classList.add('loading');
            }
        });
    });
});

// Add CSS for additional animations if not already present
if (!document.querySelector('#property-analysis-animations')) {
    const style = document.createElement('style');
    style.id = 'property-analysis-animations';
    style.textContent = `
        .slide-in-up {
            animation: slideInUp 0.5s ease-out;
        }
        
        .slide-in-down {
            animation: slideInDown 0.5s ease-out;
        }
        
        .slide-in-left {
            animation: slideInLeft 0.5s ease-out;
        }
        
        .slide-in-right {
            animation: slideInRight 0.5s ease-out;
        }
        
        @keyframes slideInUp {
            from { transform: translateY(50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        @keyframes slideInDown {
            from { transform: translateY(-50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        @keyframes slideInLeft {
            from { transform: translateX(-50px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes slideInRight {
            from { transform: translateX(50px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        .btn.loading {
            position: relative;
            color: transparent;
        }
        
        .btn.loading::after {
            content: "";
            position: absolute;
            width: 16px;
            height: 16px;
            top: 50%;
            left: 50%;
            margin-left: -8px;
            margin-top: -8px;
            border: 2px solid #ffffff;
            border-radius: 50%;
            border-top-color: transparent;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(style);
}
