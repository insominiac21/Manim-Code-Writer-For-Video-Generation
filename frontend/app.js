/**
 * MentorBocAI - Frontend Application
 * Handles form submission, job polling, and video playback
 */

// Configuration - Local Python backend
const API_BASE = '';

// State
let jobs = [];
let pollingIntervals = {};

// DOM Elements
const form = document.getElementById('generateForm');
const submitBtn = document.getElementById('submitBtn');
const jobsList = document.getElementById('jobsList');
const durationSlider = document.getElementById('duration');
const durationValue = document.getElementById('durationValue');
const videoModal = document.getElementById('videoModal');
const modalTitle = document.getElementById('modalTitle');
const videoPlayer = document.getElementById('videoPlayer');
const downloadLink = document.getElementById('downloadLink');
const closeModal = document.getElementById('closeModal');

// ========================================
// Event Listeners
// ========================================

// Duration slider update
durationSlider.addEventListener('input', () => {
    durationValue.textContent = `${durationSlider.value}s`;
});

// Form submission
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    await generateVideo();
});

// Modal close
closeModal.addEventListener('click', () => {
    videoModal.classList.remove('active');
    videoPlayer.pause();
    videoPlayer.src = '';
});

// Click outside modal to close
videoModal.addEventListener('click', (e) => {
    if (e.target === videoModal) {
        videoModal.classList.remove('active');
        videoPlayer.pause();
        videoPlayer.src = '';
    }
});

// Initialize - Load saved jobs from localStorage
document.addEventListener('DOMContentLoaded', () => {
    loadJobsFromStorage();
    renderJobs();
    initPlanModal();
    
    // Clear history button
    document.getElementById('clearHistoryBtn')?.addEventListener('click', () => {
        if(confirm('Are you sure you want to clear all video history? This cannot be undone.')) {
            localStorage.removeItem('mentorbocai_jobs');
            jobs = [];
            renderJobs();
            showNotification('History cleared', 'success');
        }
    });
});

// ========================================
// Plan Modal Functions
// ========================================

function initPlanModal() {
    const planModal = document.getElementById('planModal');
    const closePlanModal = document.getElementById('closePlanModal');
    const tabs = document.querySelectorAll('.tab');
    const copyPlanBtn = document.getElementById('copyPlanBtn');
    const copyCodeBtn = document.getElementById('copyCodeBtn');

    // Close modal
    closePlanModal?.addEventListener('click', () => {
        planModal.classList.remove('active');
    });

    planModal?.addEventListener('click', (e) => {
        if (e.target === planModal) {
            planModal.classList.remove('active');
        }
    });

    // Tab switching
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            const planContent = document.getElementById('planContent');
            const codeContent = document.getElementById('codeContent');

            if (tab.dataset.tab === 'plan') {
                planContent.style.display = 'block';
                codeContent.style.display = 'none';
            } else {
                planContent.style.display = 'none';
                codeContent.style.display = 'block';
            }
        });
    });

    // Copy buttons
    copyPlanBtn?.addEventListener('click', () => {
        const text = document.getElementById('planContent').textContent;
        navigator.clipboard.writeText(text);
        copyPlanBtn.textContent = '✓ Copied!';
        setTimeout(() => copyPlanBtn.textContent = '📋 Copy JSON', 2000);
    });

    copyCodeBtn?.addEventListener('click', () => {
        const text = document.getElementById('codeContent').textContent;
        navigator.clipboard.writeText(text);
        copyCodeBtn.textContent = '✓ Copied!';
        setTimeout(() => copyCodeBtn.textContent = '📋 Copy Code', 2000);
    });
}

function openPlanPreview(jobId) {
    const job = jobs.find(j => j.job_id === jobId);
    if (!job) return;

    const planModal = document.getElementById('planModal');
    const planModalTitle = document.getElementById('planModalTitle');
    const planContent = document.getElementById('planContent');
    const codeContent = document.getElementById('codeContent');

    planModalTitle.textContent = `Animation Plan: ${job.concept}`;
    planContent.textContent = job.plan ? JSON.stringify(job.plan, null, 2) : 'Plan not available';
    codeContent.textContent = job.manim_code || 'Code not available';

    // Reset tabs to plan view
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelector('.tab[data-tab="plan"]')?.classList.add('active');
    planContent.style.display = 'block';
    codeContent.style.display = 'none';

    planModal.classList.add('active');
}

// ========================================
// API Functions
// ========================================

/**
 * Generate a new video
 */
async function generateVideo() {
    const formData = {
        concept: document.getElementById('concept').value.trim(),
        goal: document.getElementById('goal').value.trim(),
        duration_seconds: parseInt(durationSlider.value),
        max_scenes: parseInt(document.getElementById('maxScenes').value),
        detail_level: document.getElementById('detailLevel').value,
        style: document.getElementById('style').value,
        allow_speaker_notes: document.getElementById('speakerNotes').checked
    };

    // Validate
    if (!formData.concept || !formData.goal) {
        showNotification('Please fill in all required fields', 'error');
        return;
    }

    // Disable button
    submitBtn.disabled = true;
    submitBtn.classList.add('loading');
    submitBtn.innerHTML = '<span class="spinner"></span> Generating...';

    try {
        const response = await fetch(`${API_BASE}/api/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to generate video');
        }

        const data = await response.json();

        // Add job to list
        const job = {
            job_id: data.job_id,
            concept: formData.concept,
            status: data.status,
            progress: 0,
            video_url: null,
            error: null,
            created_at: new Date().toISOString()
        };

        jobs.unshift(job);
        saveJobsToStorage();
        renderJobs();

        // Start polling
        startPolling(data.job_id);

        // Clear form
        form.reset();
        durationValue.textContent = '30s';

        showNotification('Video generation started!', 'success');

    } catch (err) {
        console.error('Generate error:', err);
        showNotification(err.message, 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.classList.remove('loading');
        submitBtn.innerHTML = '<span class="btn-icon">✨</span> Generate Video';
    }
}

/**
 * Poll job status
 */
async function pollJobStatus(jobId) {
    try {
        const response = await fetch(`${API_BASE}/api/status/${jobId}`);

        if (!response.ok) {
            throw new Error('Failed to get status');
        }

        const data = await response.json();

        // Update job in list
        const jobIndex = jobs.findIndex(j => j.job_id === jobId);
        if (jobIndex !== -1) {
            jobs[jobIndex] = { ...jobs[jobIndex], ...data };
            saveJobsToStorage();
            renderJobs();

            // Stop polling if done or failed
            if (data.status === 'done' || data.status === 'failed') {
                stopPolling(jobId);

                if (data.status === 'done') {
                    showNotification('Video ready!', 'success');
                } else if (data.status === 'failed') {
                    showNotification(`Generation failed: ${data.error}`, 'error');
                }
            }
        }

    } catch (err) {
        console.error('Poll error:', err);
    }
}

/**
 * Start polling for a job
 */
function startPolling(jobId) {
    if (pollingIntervals[jobId]) return;

    pollingIntervals[jobId] = setInterval(() => {
        pollJobStatus(jobId);
    }, 3000);

    // Initial poll
    pollJobStatus(jobId);
}

/**
 * Stop polling for a job
 */
function stopPolling(jobId) {
    if (pollingIntervals[jobId]) {
        clearInterval(pollingIntervals[jobId]);
        delete pollingIntervals[jobId];
    }
}

// ========================================
// UI Functions
// ========================================

/**
 * Render jobs list
 */
function renderJobs() {
    if (jobs.length === 0) {
        jobsList.innerHTML = `
      <div class="empty-state">
        <span class="empty-icon">📽️</span>
        <p>No videos generated yet. Create your first one above!</p>
      </div>
    `;
        return;
    }

    jobsList.innerHTML = jobs.map(job => `
    <div class="job-card ${job.status}" data-job-id="${job.job_id}">
      <div class="job-icon">${getStatusIcon(job.status)}</div>
      <div class="job-info">
        <div class="job-concept">${escapeHtml(job.concept)}</div>
        <div class="job-meta">${formatTime(job.created_at)}</div>
        ${job.status !== 'done' && job.status !== 'failed' ? `
          <div class="job-progress">
            <div class="job-progress-bar" style="width: ${job.progress || 0}%"></div>
          </div>
        ` : ''}
      </div>
      ${job.status === 'done' ? `
        <button class="btn-view-plan" onclick="event.stopPropagation(); openPlanPreview('${job.job_id}')">📋 View Plan</button>
      ` : ''}
      <div class="job-status ${job.status}">${formatStatus(job.status)}</div>
    </div>
  `).join('');

    // Resume polling for in-progress jobs
    jobs.forEach(job => {
        if (!['done', 'failed'].includes(job.status)) {
            startPolling(job.job_id);
        }
    });
}

/**
 * Open video modal
 */
function openVideo(jobId) {
    const job = jobs.find(j => j.job_id === jobId);
    if (!job || !job.video_url) return;

    modalTitle.textContent = job.concept;
    videoPlayer.src = job.video_url;
    downloadLink.href = job.video_url;
    downloadLink.download = `${job.concept.replace(/\s+/g, '_')}.mp4`;

    videoModal.classList.add('active');
}

/**
 * Get icon for status
 */
function getStatusIcon(status) {
    const icons = {
        queued: '⏳',
        planning: '🧠',
        validating: '✅',
        rendering: '🎬',
        merging: '🔗',
        done: '✅',
        failed: '❌'
    };
    return icons[status] || '⏳';
}

/**
 * Format status for display
 */
function formatStatus(status) {
    const labels = {
        queued: 'Queued',
        planning: 'Planning',
        validating: 'Validating',
        rendering: 'Rendering',
        merging: 'Merging',
        done: 'Ready',
        failed: 'Failed'
    };
    return labels[status] || status;
}

/**
 * Format timestamp
 */
function formatTime(isoString) {
    const date = new Date(isoString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffMins < 1440) return `${Math.floor(diffMins / 60)}h ago`;
    return date.toLocaleDateString();
}

/**
 * Escape HTML for safe rendering
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Show notification toast
 */
function showNotification(message, type = 'info') {
    // Simple alert for now - can be replaced with toast library
    console.log(`[${type.toUpperCase()}] ${message}`);

    if (type === 'error') {
        alert(message);
    }
}

// ========================================
// Storage Functions
// ========================================

/**
 * Save jobs to localStorage
 */
/**
 * Save jobs to localStorage (Filtered to prevent size issues)
 */
function saveJobsToStorage() {
    try {
        // Strip heavy fields (code, plans) to prevent localStorage size limits (4KB - 5MB)
        const simplifiedJobs = jobs.map(job => {
            const { manim_code, plan, understanding, ...essential } = job;
            return essential;
        });
        localStorage.setItem('mentorbocai_jobs', JSON.stringify(simplifiedJobs));
    } catch (e) {
        console.warn('Failed to save to localStorage:', e);
        // If storage is full, try clearing it
        if (e.name === 'QuotaExceededError') {
            localStorage.removeItem('mentorbocai_jobs');
        }
    }
}

/**
 * Load jobs from localStorage
 */
function loadJobsFromStorage() {
    try {
        const saved = localStorage.getItem('mentorbocai_jobs');
        if (saved) {
            jobs = JSON.parse(saved);
        }
    } catch (e) {
        console.error('Corruption detected in localStorage. Clearing cache...', e);
        localStorage.removeItem('mentorbocai_jobs');
        jobs = [];
    }
}

// Make openVideo global for onclick
window.openVideo = openVideo;
