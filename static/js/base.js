document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle functionality
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const nav = document.querySelector('.base-layout-nav');

    if (mobileMenuToggle && nav) {
        mobileMenuToggle.addEventListener('click', function() {
            nav.classList.toggle('active');
            this.classList.toggle('active');
        });
    }

    // Close message functionality
    const closeButtons = document.querySelectorAll('.close-message');

    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const message = this.closest('.message');
            message.style.opacity = '0';
            message.style.transform = 'translateY(-20px)';

            setTimeout(() => {
                message.remove();
            }, 300);
        });
    });

    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.message');

    if (messages.length > 0) {
        setTimeout(() => {
            messages.forEach(message => {
                message.style.opacity = '0';
                message.style.transform = 'translateY(-20px)';

                setTimeout(() => {
                    message.remove();
                }, 300);
            });
        }, 5000);
    }
});
