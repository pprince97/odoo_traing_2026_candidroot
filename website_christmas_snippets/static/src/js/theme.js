/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.ChristmasTheme = publicWidget.Widget.extend({
    selector: 'body',

    start() {
        this._initSmoothScroll();
        this._initAnimations();
        console.log("Christmas Theme loaded 🎄");
        return this._super(...arguments);
    },

    _initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(link => {
            link.addEventListener('click', function (e) {
                const href = this.getAttribute('href');
                if (href && href !== '#') {
                    const target = document.querySelector(href);
                    if (target) {
                        e.preventDefault();
                        target.scrollIntoView({ behavior: 'smooth' });
                    }
                }
            });
        });
    },

    _initAnimations() {
        if (!('IntersectionObserver' in window)) {
            return;
        }

        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px',
        });

        document.querySelectorAll(
            '.christmas-card, .christmas-product-card'
        ).forEach(el => observer.observe(el));
    },
});
