import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";


publicWidget.registry.UserInformation = publicWidget.Widget.extend({
    selector: '#user_info_form',

    events: {
        'change #country': '_onChangeCountry',
        'change #state': '_onChangeState',
        'click #user_info_submit_btn': '_onClickSubmit',
        'change #binary_file': '_onChangeFile',
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

    async _onClickSubmit() {

        var dict = {
            name : this.$('#name').val(),
            email : this.$('#email').val(),
            phone : this.$('#phone').val(),
            street : this.$('#address').val(),
            country_id : this.$('#country').val() || false,
            state_id : this.$('#state').val() || false,
            city_id : this.$('#city_id').val() || false,
            city : this.$('#city').val() || false,
            zip : this.$('#zip_code').val() || false
        };
        const values = await rpc('/get/user/information', { 'values': dict });

    },

    async _onChangeFile() {
        var document = this.$('#binary_file')[0].files[0];
        if (!document) return;
        var doc_type = document.type;
        var doc_size = document.size;
        const max_size = 10*1024*1024;
        if (doc_type != 'application/pdf') {
            alert("Document type must be PDF!!")
            return;
        }
        else if (doc_size > max_size) {
            alert("File size must be less or equal to 10MB!!")
            return;
        }
    },

});