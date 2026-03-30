/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

publicWidget.registry.AddressForm = publicWidget.Widget.extend({
    selector: '#partner_form',

    events: {
        'click #submit_btn ': '_onFormSubmit',
        'change #country_id': '_onCountryChange',
        'change #state_id': '_onStateChange',
        'change #resume': '_onResumeUpload',
    },

    start() {
        this._resetState();
        this._resetCity();
        return this._super(...arguments);
    },

    init() {
        this._super(...arguments);
        this.dialogService = this.bindService("dialog");
    },

    _resetState() {
        this.$('#state_id').empty().append('<option value="">Select State</option>');
    },

     _resetCity() {
        this.$('#city_dropdown').hide();
        this.$('#city_input').show().val('');
    },

    async _onCountryChange(ev) {
        const country_id = ev.currentTarget.value;
        this._resetState();
        this._resetCity();
        if (!country_id) return;
        const states = await rpc('/get_states', { country_id });
        const state = this.$('#state_id');
        states.forEach(s => {
            state.append(`<option value="${s.id}">${s.name}</option>`);
        });
    },

    async _onStateChange(ev) {
        const state_id = ev.currentTarget.value;
        this._resetCity();
        if (!state_id) return;
        const cities = await rpc('/get_cities', { state_id });
        const dropdown = this.$('#city_dropdown');
        const input = this.$('#city_input');
        if (cities.length > 0) {
            dropdown.show().empty().append('<option value="">Select City</option>');
            input.hide();
            cities.forEach(c => dropdown.append(`<option value="${c.id}">${c.name}</option>`));
        } else {
            dropdown.hide();
            input.show();
        }
    },

    async _onResumeUpload(ev) {
        const file = ev.currentTarget.files[0];
        const maxsize = 10 * 1024 * 1024;
        const $errorMsg = this.$('.file_error_msg');

        if(file){
            const isPdf = file.type === 'application/pdf' || file.name.toLowerCase().endsWith(".pdf");
            if (!isPdf || file.size>maxsize){
                $errorMsg.text('SAHI FILE UPLOAD KIJIYE').removeClass('d-none');;
                ev.currentTarget.value='';
            }
            else{
                $errorMsg.addClass('d-none');
            }
        }
    },

   async _onFormSubmit(ev) {
        ev.preventDefault();
        const name = this.$('#name').val();
        const email = this.$('#email').val();
        if (!name || !email) {
            alert("Please fill out all required fields (Name and Email).");
            return;
        }
        const params = {
            name: name,
            email: email,
            phone: this.$('#phone').val(),
            gender: this.$('#gender').val(),
            country_id: parseInt(this.$('#country_id').val()) || false,
            state_id: parseInt(this.$('#state_id').val()) || false,
            city: this.$('#city_dropdown').is(':visible') ?
                  this.$('#city_dropdown option:selected').text() :
                  this.$('#city_input').val(),
            zip: this.$('#zip').val() || false,
        };
        const result = await rpc("/librarians/create", { params });

        if (result.success) {
            const ask = window.confirm("Librarian created successfully! \n\nClick 'OK' to view list, or 'Cancel' to reset form.");

            if (ask) {
                window.location.href = result.redirection_url;
            } else {
                this.$el[0].reset();
                this._resetState();
                this._resetCity();
            }
        } else {
            alert("Error: " + result.message);
        }
    },

//    async _onFormSubmit(){
//        const params = {
//            name: this.$('#name').val(),
//            email: this.$('#email').val(),
//            phone: this.$('#phone').val(),
//            gender: this.$('#gender').val(),
//            country_id: parseInt(this.$('#country_id').val()) || false,
//            state_id: parseInt(this.$('#state_id').val()) || false,
//            city: this.$('#city_id').length > 0 ?
//            this.$('#city_id option:selected').text() :
//            this.$('#city_input').val() || false,
//            zip: this.$('#zip').val() || false,
//        };
//        const result = await rpc("/librarians/create", {params});
//        if (result.success) {
//            alert("Profile created successfully!");
//            window.location.href = result.redirection_url;
//        } else {
//            alert("Error: " + result.message);
//        }
//    },

});
