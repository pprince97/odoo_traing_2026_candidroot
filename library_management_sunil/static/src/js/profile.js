/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.rootforms = publicWidget.Widget.extend({

    selector: '#profile_form',

    events: {
        'change select[name="country"]': '_onChangeCountry',
        'change select[name="state"]': '_onChangeState',
    },

    init: function () {
        this._super.apply(this, arguments);
        this.form = document.querySelector('#profile_form');
    },

    start() {
        console.log("===============🎄");
        return this._super(...arguments);
    },

    _onChangeCountry: function (ev) {
        return this._changeCountry();
    },

    async _changeCountry() {
        const countryId = parseInt(this.form.country.value);

        const selectStates = this.form.state;
        const stateText = document.getElementById("state_text");
        const selectCities = document.getElementById("city_dropdown");
        const cityText = document.getElementById("city_text");

        selectStates.options.length = 0;
        selectStates.style.display = "none";
        stateText.style.display = "none";

        selectCities.options.length = 0;
        selectCities.style.display = "none";
        cityText.style.display = "none";

        if (!countryId) {
            return;
        }

        const states = await rpc("/get-states", { country_id: countryId });

        if (states.length > 0) {
            let placeholder = new Option("Select State", "");
            selectStates.appendChild(placeholder);

            states.forEach((state) => {
                let option = new Option(state.name, state.id);
                selectStates.appendChild(option);
            });

            selectStates.style.display = "block";
            stateText.style.display = "none";
        } else {
            stateText.style.display = "block";
        }

        cityText.style.display = "block";
    },

    _onChangeState: function (ev) {
        return this._changeState();
    },

    async _changeState() {
        const stateId = parseInt(this.form.state.value);
        const selectCities = document.getElementById("city_dropdown");
        const cityText = document.getElementById("city_text");

        selectCities.options.length = 0;

        if (!stateId) {
            selectCities.style.display = "none";
            cityText.style.display = "block";
            return;
        }

        const cities = await rpc("/get-cities", { state_id: stateId });

        if (cities.length > 0) {
            let placeholder = new Option("Select City", "");
            selectCities.appendChild(placeholder);

            cities.forEach((city) => {
                let option = new Option(city.name, city.id);
                selectCities.appendChild(option);
            });

            selectCities.style.display = "block";
            cityText.style.display = "none";
        } else {
            selectCities.style.display = "none";
            cityText.style.display = "block";
        }
    },

});