import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
import { renderToElement } from "@web/core/utils/render";

publicWidget.registry.ServiceRequestForm = publicWidget.Widget.extend({
    selector: '#service_request_form',
    events: {
        'change #s_country_id': '_onCountryChange',
        'change #s_state_id': '_onStateChange',
        'change #s_category_id': '_onCategoryChange',
        'change #s_services_id': '_onServicesChange',
        'click #save_details': '_onClickSave',
        'click #close_modal': '_onClickClose',
        'click #close_submit_modal': '_onSubmitClose',
    },
    start() {
        console.log("_______________");
        return this._super.apply(this, arguments);
    },

    async _onCountryChange() {
        const countryValue =this.$('#s_country_id').val()
        const result = await rpc("/update/country", {
            country_key: countryValue,
        });

        let optionsHtml = `
        <label class="col-form-label label-optional" for="s_state_id">State*</label>
        <select id="s_state_id" name="state_id" class="form-select">
            <option value="">State...</option>`;

        if (result.states && result.states.length > 0) {
            result.states.forEach(s => {
                optionsHtml += `<option value='${s.id}'>${s.name}</option>`;
            });
        }
        optionsHtml += `</select>`;

        document.getElementById('div_state').innerHTML = optionsHtml;

    },
    async _onStateChange() {

        const stateValue =this.$('#s_state_id').val()
        const result = await rpc("/update/state", {
            state_key: stateValue,
        });

        if (result.cities && result.cities.length > 0){
            let optionsHtml = `
            <label class="col-form-label" for="s_city_id">City*</label>
            <select id="s_city_id" name="city_id" class="form-select">
                option value="">City...</option>`;

            if (result.cities && result.cities.length > 0) {
                result.cities.forEach(s => {
                    optionsHtml += `<option value='${s.id}'>${s.name}</option>`;
                });
            }
            optionsHtml += `</select>`;

            document.getElementById('div_city').innerHTML = optionsHtml;
        }
        else
        {
            document.getElementById('div_city').innerHTML = `<label class="col-form-label" for="s_city">City</label>
                                                             <input id="s_city" type="text" name="city" class="form-control"/>`
        }

    },

    async _onCategoryChange() {
        const catgValue =this.$('#s_category_id').val()
        const result = await rpc("/update/category", {
            catg_key: catgValue,
        });
        let optionsHtml = `
        <label class="col-form-label" for="s_services_id">Services*</label>
        <select id="s_services_id" name="service_id" class="form-select">
            option value="">Services...</option>`;

        if (result.services && result.services.length > 0) {
            result.services.forEach(s => {
                optionsHtml += `<option value='${s.id}'>${s.name}</option>`;
            });
        }
        optionsHtml += `</select>`;

        document.getElementById('div_services').innerHTML = optionsHtml;
    },

    async _onServicesChange() {
        const serviceValue =this.$('#s_services_id').val()
        const result = await rpc("/update/service", {
            service_key: serviceValue,
        });
        let optionsHtml = `<p>This service is provided by `;
        if(result.company){
            result.company.forEach(s => {
                optionsHtml += `<p id='s_company_id'>${s.company_id_s[1]}</p>`;
            });
        }
        optionsHtml += `</p>`;
        document.getElementById('div_company').innerHTML = optionsHtml;
    },

    async _onClickSave() {
        var state = this.$('input[name="state"]:checked').val();
        var customer_id = this.$('#s_customer_id').val();
        var country_id = this.$('#s_country_id').val();
        var category_id = this.$('#s_category_id').val();
        var street = this.$('#s_street').val();

        var services_id = this.$('#s_services_id').val();
        var city_id = this.$('#s_city_id').val();
        var city = this.$('#s_city').val();
        var state_id = this.$('#s_state_id').val();
        var date = this.$('#s_date').val();

        if(date && customer_id && country_id && category_id && street && services_id && state_id && (city_id || city)){
            if (city_id){
                rpc("/service/form/submit", {
                    details_dict: {
                        'state': state,
                        'customer_id': customer_id,
                        'country_id': country_id,
                        'city': "",
                        'city_id': city_id,
                        'category_id': category_id,
                        'street': street,
                        'services_id': services_id,
                        'state_id': state_id,
                        'date':date,
                    },
                });
            }
            else{
                rpc("/service/form/submit", {
                    details_dict: {
                        'state': state,
                        'customer_id': customer_id,
                        'country_id': country_id,
                        'city': city,
                        'city_id': 0,
                        'category_id': category_id,
                        'street': street,
                        'services_id': services_id,
                        'state_id': state_id,
                        'date':date,
                    },
                });
            }
            document.getElementById("mySubmitModal").style.display = "block";
        }
        else{
            document.getElementById("myModal").style.display = "block";
        }
    },

    async _onClickClose() {
        document.getElementById("myModal").style.display = "none";
    },

    async _onSubmitClose() {
        document.getElementById("mySubmitModal").style.display = "none";
    },
})