import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";


publicWidget.registry.UserInformation = publicWidget.Widget.extend({
    selector: '#service_request_form',

    events: {
        'change #category': '_onChangeCategory',
        'change #country': '_onChangeCountry',
        'change #state': '_onChangeState',
        'click #request_service_submit_btn': '_onClickSubmit',
    },

    async start() {
        const customer = await rpc('/get/customer/details');
        const country = this.$('#country_block');
        const state = this.$('#state_block');
        const city = this.$('#city_block');
        const street = this.$('#street_address');
        if (customer.country) {
            country.empty().append(`<input id="country" type="char" class="form-control" name="country" style="width: 400px" readonly="1" value="${customer.country}"/>`);
        }
        if (customer.state) {
            state.empty().append(`<input id="state" type="char" class="form-control" name="state" style="width: 400px" readonly="1" value="${customer.state}"/>`);
        }
        if (customer.city) {
            city.empty().append(`<input id="city" type="char" class="form-control" name="city" style="width: 400px" readonly="1" value="${customer.city}"/>`);
        }
        if (customer.street) {
            street.attr('value', customer.street);
            street.attr('readonly', 1);
        }
    },

    async _onChangeCountry(ev) {
        const country_id = this.$('#country').val();

        if (!country_id) return;

        const states = await rpc('/get/states', { country_id });
        const state = this.$('#state');
        var html = '<option hidden="1">Select State</option>'
        this.$('#city_block').empty().append('<select id="city" name="city" class="from-select form-control" style="width: 400px"> <option hidden="1" selected="1">Select City</option></select>');

        states.forEach(state => {
            html+=`<option value="${state.id}">${state.name}</option>`;
        });
        state.empty().append(html)
    },

    async _onChangeState() {
        const state_id = this.$('#state').val();

        if (!state_id) return;

        var html = '';
        const cities = await rpc('/get/cities', { state_id });
        const div = this.$('#city_block');

        if (cities.length==0) {
            html+='<input id="city" type="char" class="form-control" name="city" required="" style="width: 400px"/>';

        } else {
            html+='<select id="city_id" name="city" class="from-select form-control" style="width: 400px"> <option hidden="1" selected="1">Select City</option>';

            cities.forEach(city => {
                html+=`<option value="${city.id}">${city.name}</option>`;
            });
            html+='</select>';
        }
            div.empty().append(html);


    },

    async _onChangeCategory() {
        const category_id = this.$('#category').val();

        if (!category_id) return;

        const services = await rpc('/get/services', { category_id });
        const service = this.$('#service');
        var html = '<option hidden="1">Select State</option>';
        services.forEach(service => {
            html+=`<option value="${service.id}">${service.name}</option>`;
        });
        service.empty().append(html);
    },

    async _onClickSubmit() {

        var dict = {
            date : this.$('#service_date').val(),
            category_id : this.$('#category').val(),
            service_id : this.$('#service').val(),
            country_id : this.$('#country').val() || false,
            state_id : this.$('#state').val() || false,
            city_id : this.$('#city').val() || false,
            street_address : this.$('#street_address').val() || false,
        };
        const values = await rpc('/get/service-request/details', { 'values': dict });

    },

});