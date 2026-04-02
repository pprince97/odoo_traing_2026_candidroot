/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.CountryState = publicWidget.Widget.extend({
    selector: '.o_country_state_form',

    start() {
        console.log("Hello start", this);
        this._bindEvents();
        return this._super(...arguments);
    },

    _bindEvents() {
        console.log("Hello Bind");
        const countrySelect = this.el.querySelector('.country_select');
        const stateSelect = this.el.querySelector('.state_select');
        const companySelect = this.el.querySelector('.company_select');
        const categorySelect = this.el.querySelector('.category_select');

        if (countrySelect) {
            countrySelect.addEventListener('change', (ev) => {
                const countryId = ev.target.value;
                this._loadStates(countryId);
            });
        }

        if (stateSelect) {
            stateSelect.addEventListener('change', (ev) => {
                const stateId = ev.target.value;
                this._loadCities(stateId);
            });
        }
        if (companySelect) {
            companySelect.addEventListener('change', (ev) => {
                const companyId = ev.target.value;
                this._loadCategory(companyId);
            });
        }
        if (categorySelect) {
            categorySelect.addEventListener('change', (ev) => {
                const categoryId = ev.target.value;
                this._loadService(categoryId);
            });
        }
    },

    _loadStates(countryId) {
        console.log("Hello Load", countryId);
        const stateSelect = this.el.querySelector('.state_select');
        console.log("stateSelect", stateSelect);

        if (!stateSelect) return;

        stateSelect.innerHTML = '<option value="">Select State</option>';

        if (!countryId) return;

        rpc('/get_states', {
            country_id: countryId,
        }).then((states) => {

            if (!states) return;

            states.forEach((state) => {
                const option = document.createElement('option');
                option.value = state.id;
                option.textContent = state.name;
                stateSelect.appendChild(option);
            });

        });
    },

    _loadCities(stateId) {
        console.log("Hello State", stateId);
        const citySelect = this.el.querySelector('.city_select');
        // const cityName = this.el.querySelector('.city_name');

        if (!citySelect) return;

        citySelect.innerHTML = '<option value="">Select Cities</option>';

        if (!stateId) return;

        rpc('/get_cities', {
            state_id: stateId,
        }).then((cities) => {

            // if (cities.length == 0) {
            //     console.log(cities.length, "len not");
            //     citySelect.style.display = 'none';
            //     cityName.style.display = 'block';
            //     return;
            // } else {
                console.log(cities.length, "len");
                // cityName.style.display = 'none';
                // citySelect.style.display = 'block';
                cities.forEach((city) => {
                    const option = document.createElement('option');
                    option.value = city.id;
                    option.textContent = city.name;
                    citySelect.appendChild(option);
                });
            // }

        });

    },

    _loadCategory(companyId) {
        console.log("Hello Company", companyId);
        const categorySelect = this.el.querySelector('.category_select');
        console.log("categorySelect", categorySelect);

        if (!categorySelect) return;

        categorySelect.innerHTML = '<option value="">Select Category</option>';

        if (!companyId) return;

        rpc('/get_category', {
            company_id: companyId,
        }).then((categories) => {

            if (!categories) return;

            categories.forEach((category) => {
                const option = document.createElement('option');
                option.value = category.id;
                option.textContent = category.service_name;
                categorySelect.appendChild(option);
            });
        });
    },

    _loadService(categoryId) {
        console.log("Hello Category", categoryId);
        const serviceSelect = this.el.querySelector('.service_select');
        console.log("serviceSelect", serviceSelect);

        if (!serviceSelect) return;

        serviceSelect.innerHTML = '<option value="">Select Service</option>';

        if (!categoryId) return;

        rpc('/get_services', {
            service_category_id: categoryId,
        }).then((services) => {

            if (!services) return;

            services.forEach((service) => {
                const option = document.createElement('option');
                option.value = service.id;
                option.textContent = service.name;
                serviceSelect.appendChild(option);
            });

        });
    },
});