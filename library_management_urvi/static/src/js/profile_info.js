//import { publicWidget } from "@web/legacy/js/public/public_widget";
////import { jsonrpc } from "@web/core/network/rpc_service";
//
//publicWidget.registry.ProfileInfo = publicWidget.Widget.extend({
//    selector: 'form',
////    events: {
////        'click #add_task': '_onAddTask',
////    },
//    start() {
//          print('>>>>>>>>>>>>>>>>>>')
////        this._renderTasks();
//           return this._super(...arguments);
//    }
////    async _renderTasks() {
////        const tasks = await jsonrpc('/todo/list', {});
////        // Logic to update DOM with tasks
////    },
////    async _onAddTask() {
////        const name = $('#new_task_name').val();
////        await jsonrpc('/todo/create', { name: name });
////        this._renderTasks(); // Refresh list
////    },
//});

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";


publicWidget.registry.PersonalInfoWidget = publicWidget.Widget.extend({
    selector: '#profile_info',
        events: {
        'change #country_id': '_onchangeCountry',
        'change #state_id': '_onchangeState',
        'change #file_input': '_onFileChange',
        'click #btn': '_onclickbtn',
    },
    start(){
        this._renderInfo();
    },
//
//    async _renderInfo() {
//        const partner = await rpc("/get_partner_info", {});
//        if (partner) {
//            this.$('#name').val(partner.name);
//            this.$('#email').val(partner.email);
//            this.$('#phone').val(partner.phone);
//            this.$('#gender').val(partner.gender);
//            this.$('#country_id').val(partner.country_id);
//            this.$('#state_id').val(partner.state_id);
//       }
//    },

    async _renderInfo(){
        const selected_state = this.$('#state_id')
        const selected_city = this.$('#city_id')
        selected_state.html('<option value="" hidden="1">Select State...</option>');
        selected_city.html('<label for="city" class="form-label">City</label><input type="tel" name="city" class="form-control" id="city"/>')
    },

    async _onchangeCountry(){
        const country = this.$('#country_id').val();
        const selected_state = this.$('#state_id')

        if (country) {
        const allowed_state = await rpc("/get_states",{country : parseInt(country)});
            let html = '<option value="" hidden="1">Select State...</option>';
            allowed_state.forEach(state => {
                html += `<option value="${state.id}">${state.name}</option>`;
            });
            selected_state.html(html);
        }
        },

    async _onchangeState(){
        const country = this.$('#country_id').val();
        const state = this.$('#state_id').val();
        const selected_city = this.$('#city_id')

        if(state){
            const allowed_city = await rpc("/get_city",{country : parseInt(country),state : parseInt(state)})
            console.log('>>>>>>>>>>>>>>>>>',allowed_city)
            if (allowed_city.length!=0)
            {let html = '<label for="city_id" class="form-label">City</label><select name="city_id" class="form-select form-select-sm" id="city_id"><option value="" hidden="1">Select City...</option>';
            allowed_city.forEach(city => {
                html += `<option value="${city.id}">${city.name}</option>`;
            });
            html +='</select>'
            selected_city.html(html);
            }
            }
        },

    async _onclickbtn(){
        const $fileInput = this.$('#file_input')[0];
        let imageData = false;

        // 1. Check if a file was selected
        if ($fileInput.files.length > 0) {
            const file = $fileInput.files[0];
            // 2. Convert File to Base64
            imageData = await this._fileToBase64(file);
        }

        const params = {
            name: this.$('#name').val(),
            email: this.$('#email').val(),
            phone: this.$('#phone').val(),
            gender: this.$('#gender').val(),
            country_id: parseInt(this.$('#country_id').val()) || false,
            state_id: parseInt(this.$('#state_id').val()) || false,
            city_id: parseInt(this.$('#city_id').val()) || false,
            city: this.$('#city').val(),
            street: this.$('#street').val(),
            zip: this.$('#zip').val(),
            pdffile: imageData ? imageData.split(',')[1] : false,
        };

            const result = await rpc("/create_partner", {params});
            if (result.success) {
                alert("Profile created successfully!");
            } else {
                alert("Error: " + result.message);
            }
    },

    // Helper to read file as Base64
    _fileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => resolve(reader.result);
            reader.onerror = error => reject(error);
        });
    },

    _onFileChange: function (ev) {
    const file = ev.currentTarget.files[0];
    const $errorMsg = this.$('#file_error');
    $errorMsg.hide().text('');
    $(ev.currentTarget).removeClass('is-invalid');
    console.log('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>........')
    if (file) {
        const maxSize = 10 * 1024 * 1024
        let errorMessage = "";
        if (file.type !== "application/pdf") {
            errorMessage = "Only PDF files are allowed!";
        } else if (file.size > maxSize) {
            errorMessage = "File is too large! Maximum size allowed is 10MB.";
        }
        if (errorMessage) {
            $errorMsg.text(errorMessage).fadeIn();
            $(ev.currentTarget).addClass('is-invalid');
            ev.currentTarget.value = "";
        }
    }
},
})

publicWidget.registry.BookPriceFilter = publicWidget.Widget.extend({
    selector: '.js_attributes',
    events: {
        'change .range-with-input': '_onRangeChange',
    },

    _onRangeChange: function (ev) {
        // Odoo's slider stores values as a comma-separated string: "min,max"
        const values = $(ev.currentTarget).val().split(',');
        if (values.length === 2) {
            this.$('#min_price_hidden').val(values[0]);
            this.$('#max_price_hidden').val(values[1]);

            // Optional: Auto-submit the form as soon as user lets go
            this.$el.submit();
        }
    },
});


