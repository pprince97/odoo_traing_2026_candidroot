/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.IndiaTheme = publicWidget.Widget.extend({
    selector: '#wrap',

    start() {
        console.log("India Theme Loaded 🇮🇳");

        this._initScrollAnimation();
        this._initSmoothScroll();

        return this._super(...arguments);
    },

    _initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(link => {
            link.addEventListener('click', function (e) {
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    },

    _initScrollAnimation() {
        if (!('IntersectionObserver' in window)) return;

        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        });
    },
});