// FitBuddy — Client-side interactivity
// No API keys or sensitive data in this file

document.addEventListener('DOMContentLoaded', () => {
    // === Form Validation (index.html) ===
    const workoutForm = document.getElementById('workoutForm');
    if (workoutForm) {
        workoutForm.addEventListener('submit', (e) => {
            let isValid = true;
            
            // Clear previous errors
            document.querySelectorAll('.form-error').forEach(el => el.textContent = '');
            
            // Name validation
            const name = document.getElementById('name');
            if (name && !name.value.trim()) {
                document.getElementById('nameError').textContent = 'Name is required';
                isValid = false;
            }
            
            // User ID validation
            const userId = document.getElementById('user_id');
            if (userId && !userId.value.trim()) {
                document.getElementById('userIdError').textContent = 'User ID is required';
                isValid = false;
            }
            
            // Age validation
            const age = document.getElementById('age');
            if (age) {
                const ageVal = parseInt(age.value);
                if (!age.value || isNaN(ageVal) || ageVal < 1 || ageVal > 119) {
                    document.getElementById('ageError').textContent = 'Age must be between 1 and 119';
                    isValid = false;
                }
            }
            
            // Weight validation
            const weight = document.getElementById('weight');
            if (weight) {
                const weightVal = parseFloat(weight.value);
                if (!weight.value || isNaN(weightVal) || weightVal <= 0) {
                    document.getElementById('weightError').textContent = 'Weight must be greater than 0';
                    isValid = false;
                }
            }
            
            // Goal validation
            const goal = document.getElementById('goal');
            if (goal && !goal.value) {
                document.getElementById('goalError').textContent = 'Please select a fitness goal';
                isValid = false;
            }
            
            // Intensity validation
            const intensityChecked = document.querySelector('input[name="intensity"]:checked');
            if (!intensityChecked) {
                document.getElementById('intensityError').textContent = 'Please select an intensity level';
                isValid = false;
            }
            
            if (!isValid) {
                e.preventDefault();
                return;
            }
            
            // Show loading overlay
            const overlay = document.getElementById('loadingOverlay');
            if (overlay) overlay.classList.add('active');
            
            // Disable submit button
            const submitBtn = document.getElementById('submitBtn');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Generating...';
            }
        });
    }
    
    // === Feedback Form Loading State ===
    const feedbackForm = document.getElementById('feedbackForm');
    if (feedbackForm) {
        feedbackForm.addEventListener('submit', (e) => {
            const feedback = document.getElementById('feedback');
            if (feedback && feedback.value.trim().length < 3) {
                e.preventDefault();
                document.getElementById('feedbackError').textContent = 'Feedback must be at least 3 characters';
                return;
            }
            
            const overlay = document.getElementById('loadingOverlay');
            if (overlay) {
                overlay.querySelector('.loading-text').textContent = 'Updating your plan...';
                overlay.classList.add('active');
            }
            
            const updateBtn = document.getElementById('updateBtn');
            if (updateBtn) {
                updateBtn.disabled = true;
                updateBtn.textContent = 'Updating...';
            }
        });
    }
    
    // === Admin: Search/Filter ===
    const searchInput = document.getElementById('adminSearch');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            const rows = document.querySelectorAll('.admin-table tbody tr.user-row');
            rows.forEach(row => {
                const name = row.dataset.name || '';
                const userId = row.dataset.userId || '';
                const match = name.toLowerCase().includes(query) || userId.toLowerCase().includes(query);
                row.style.display = match ? '' : 'none';
                // Also hide the detail row if the parent is hidden
                const detailRow = row.nextElementSibling;
                if (detailRow && detailRow.classList.contains('detail-row')) {
                    detailRow.style.display = match ? detailRow.style.display : 'none';
                }
            });
        });
    }
    
    // === Admin: Delete Confirmation ===
    document.querySelectorAll('.delete-form').forEach(form => {
        form.addEventListener('submit', (e) => {
            if (!confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
    
    // === Admin: Toggle Plan Details ===
    document.querySelectorAll('.plan-toggle-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.dataset.target;
            const detailRow = document.getElementById(targetId);
            if (detailRow) {
                const isHidden = detailRow.style.display === 'none' || !detailRow.style.display;
                detailRow.style.display = isHidden ? 'table-row' : 'none';
                btn.textContent = isHidden ? 'Hide Plans' : 'View Plans';
            }
        });
    });

    // === Toggle Original Plan on Result Page ===
    const originalPlanToggle = document.getElementById('toggleOriginalPlan');
    if (originalPlanToggle) {
        originalPlanToggle.addEventListener('click', () => {
            const content = document.getElementById('originalPlanContent');
            if (content) {
                content.classList.toggle('expanded');
                originalPlanToggle.textContent = content.classList.contains('expanded') 
                    ? 'Hide Original Plan' 
                    : 'View Original Plan';
            }
        });
    }
});
