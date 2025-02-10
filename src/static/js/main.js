document.addEventListener('DOMContentLoaded', function() {
    // Enable Bootstrap form validation
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Add input masks and validation
    const zipcodeInput = document.querySelector('input[name="zipcode"]');
    if (zipcodeInput) {
        zipcodeInput.addEventListener('input', function(e) {
            // Only allow numbers
            this.value = this.value.replace(/[^0-9]/g, '');
            // Limit to 5 digits
            if (this.value.length > 5) {
                this.value = this.value.slice(0, 5);
            }
        });
    }

    const yearInput = document.querySelector('input[name="year"]');
    if (yearInput) {
        yearInput.addEventListener('input', function(e) {
            // Only allow numbers
            this.value = this.value.replace(/[^0-9]/g, '');
            // Limit to 4 digits
            if (this.value.length > 4) {
                this.value = this.value.slice(0, 4);
            }
        });
    }

    // Add loading state to submit button
    const form = document.querySelector('form');
    const submitBtn = form.querySelector('input[type="submit"]');
    
    if (form && submitBtn) {
        form.addEventListener('submit', function() {
            if (form.checkValidity()) {
                submitBtn.value = 'Checking...';
                submitBtn.disabled = true;
            }
        });
    }
}); 