/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.StudentProfileForm = publicWidget.Widget.extend({
    selector: '#student_form',
    events: {
        'change #country_id': '_onCountryChange',
        'change #state_id': '_onStateChange',
        'change #file_input': '_onFileChange',
        'click #submit_profile_btn': '_onClickBtn',
    },

    async _onCountryChange(ev) {
        const countryId = $(ev.currentTarget).val();
        const $stateSelect = this.$('#state_id');
        $stateSelect.empty().append('<option value="">Select State...</option>').prop('disabled', true);
        this._renderCityField([]);
        if (countryId) {
            const data = await rpc('/get_location_data', { country_id: parseInt(countryId) });
            if (data && data.states.length > 0) {
                data.states.forEach(s => $stateSelect.append(new Option(s.name, s.id)));
                $stateSelect.prop('disabled', false).removeAttr('disabled');
            }
        }
    },

    async _onStateChange(ev) {
        const stateId = $(ev.currentTarget).val();
        if (stateId) {
            const data = await rpc('/get_location_data', { state_id: parseInt(stateId) });
            this._renderCityField(data.cities);
        } else {
            this._renderCityField([]);
        }
    },

     _renderCityField(cities) {
        const $wrapper = this.$('#city_wrapper');
        $wrapper.empty();
        if (cities && cities.length > 0) {
            const $select = $('<select name="city_id" id="city_select_list" class="form-select shadow-none"></select>');
            $select.append('<option value="">Select City from list...</option>');
            cities.forEach(c => $select.append(new Option(c.name, c.id)));
            $wrapper.append($select);
        } else {
            $wrapper.append('<input type="text" name="city_text" id="city_field" class="form-control shadow-none" placeholder="Enter City Name"/>');
        }
    },

    _onFileChange: function (ev) {
        const file = ev.currentTarget.files[0];
        const $errorMsg = this.$('#file_error');
        $errorMsg.hide().text('');
        $(ev.currentTarget).removeClass('is-invalid');
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

    async _onClickBtn(ev){
        const formElement = document.getElementById('student_form');
        if (formElement) {
            if (formElement.checkValidity() === false) {
                ev.preventDefault();
                formElement.reportValidity();
                return;
            }
        } else {
            console.error("Form #student_form not found!");
        }
        ev.preventDefault();

        const fileInput = document.getElementById('file_input');
        let fileData = false;
        let fileName = false;

        if (fileInput && fileInput.files.length > 0) {
            const file = fileInput.files[0];
            fileName = file.name;
            fileData = await new Promise((resolve) => {
                const reader = new FileReader();
                reader.onloadend = () => resolve(reader.result.split(',')[1]);
                reader.readAsDataURL(file);
            });
        }

        const params = {
            name: this.$('#name').val(),
            email: this.$('#email').val(),
            gender: this.$("input[name='gender']:checked").val(),
            phone: this.$('#phone').val() || false,
            zip: this.$('#zip').val() || false,
            street: this.$('#address').val() || false,
            country_id: parseInt(this.$('#country_id').val()) || false,
            state_id: parseInt(this.$('#state_id').val()) || false,
            city: this.$('#city_select_list').length > 0 ?
              this.$('#city_select_list option:selected').text() :
              this.$('#city_field').val() || false,
            company_type: 'person',
            attachment_file: fileData,
            attachment_name: fileName,
        };

        const result = await rpc("/save_student_profile", {params});
        if (result && result.success) {
            alert("Student profile created successfully!");
            window.location.href = result.redirect_url;
        } else {
            alert("Error: " + (result.message || "Could not save profile"));
        }
    },
});
