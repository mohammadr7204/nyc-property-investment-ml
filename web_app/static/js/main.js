// NYC Property Investment ML - Main JavaScript Functions

function showToast(message, type = 'info') {
    // Simple alert for now - can be enhanced with toast notifications
    alert(message);
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0
    }).format(amount);
}

function formatNumber(number) {
    return new Intl.NumberFormat('en-US').format(number);
}

// Loading animations
function showLoadingSpinner(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>';
    }
}

function hideLoadingSpinner(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '';
    }
}

// Utility functions for score display
function getScoreClass(score) {
    if (score >= 80) return 'score-high';
    if (score >= 60) return 'score-medium';
    return 'score-low';
}

function getRiskClass(risk) {
    if (risk === 'Low') return 'score-high';
    if (risk === 'Medium') return 'score-medium';
    return 'score-low';
}

// Animation helpers
function fadeIn(element) {
    element.classList.add('fade-in');
}

function scrollToElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

// Global utilities
window.PropertyAnalysisUtils = {
    showToast,
    formatCurrency,
    formatNumber,
    showLoadingSpinner,
    hideLoadingSpinner,
    getScoreClass,
    getRiskClass,
    fadeIn,
    scrollToElement
};
