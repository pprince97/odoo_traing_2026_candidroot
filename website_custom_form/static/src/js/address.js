/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.CountryState = publicWidget.Widget.extend({
    selector: '.o_country_state_form',

    start() {
        this._bindEvents();
        return this._super(...arguments);
    },

    _bindEvents() {
        const countrySelect = this.el.querySelector('.country_select');
        const stateSelect = this.el.querySelector('.state_select');

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
    },

    _loadStates(countryId) {
        const stateSelect = this.el.querySelector('.state_select');

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
        const citySelect = this.el.querySelector('.city_select');
        const cityName = this.el.querySelector('.city_name');

        if (!citySelect) return;

        citySelect.innerHTML = '<option value="">Select Cities</option>';

        if (!stateId) return;

        rpc('/get_cities', {
            state_id: stateId,
        }).then((cities) => {

            if (cities.length == 0) {
                citySelect.style.display = 'none';
                cityName.style.display = 'block';
                return;
            } else {
                cityName.style.display = 'none';
                citySelect.style.display = 'block';
                cities.forEach((city) => {
                    const option = document.createElement('option');
                    option.value = city.id;
                    option.textContent = city.name;
                    citySelect.appendChild(option);
                });
            }

        });

    },
});