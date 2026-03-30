import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
import { renderToElement } from "@web/core/utils/render";

publicWidget.registry.CustomerDetails = publicWidget.Widget.extend({
    selector: '.customer_detail_form',
    events: {
        'change #c_country_id': '_onCountryChange',
        'change #c_state_id': '_onCityChange',
        'change #c_document': '_onDocumentChange',
        'click #save_details': '_onClickSave',
    },
    start() {
        console.log("_______________");
        return this._super.apply(this, arguments);
    },

    async _onDocumentChange() {
        const file = document.getElementById('c_document').files[0];
        const maxSize = 10 * 1024 * 1024;
        const allowedType = 'application/pdf';

        if (file.type !== allowedType) {
            alert("Invalid file type! Please upload a PDF.");
            document.getElementById('c_document').value = "";
        }

        if(file.size > maxSize) {
           alert("File is too large! Maximum size allowed is 10MB.");
           document.getElementById('c_document').value = "";
        }

    },

    async _onCountryChange() {
//      var countryValue = $(ev.currentTarget).val();
        const countryValue =this.$('#c_country_id').val()
        const result = await rpc("/update/country", {
            country_key: countryValue,
        });

        let optionsHtml = `
        <label class="col-form-label label-optional" for="c_state_id">State / Province</label>
        <select id="c_state_id" name="state_id" class="form-select">
            <option value="">State / Province...</option>`;

        if (result.countries && result.countries.length > 0) {
            result.countries.forEach(s => {
                optionsHtml += `<option value='${s.id}'>${s.name}</option>`;
            });
        }
        optionsHtml += `</select>`;

        document.getElementById('div_state').innerHTML = optionsHtml;

    },
    async _onCityChange() {

        const cityValue =this.$('#c_state_id').val()
        const result = await rpc("/update/city", {
            city_key: cityValue,
        });

        if (result.cities && result.cities.length > 0)
        {
            let optionsHtml = `
            <label class="col-form-label" for="c_city_id">City</label>
            <select id="c_city_id" name="city_id" class="form-select">
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
            document.getElementById('div_city').innerHTML = `<label class="col-form-label" for="c_city">City</label>
                                                             <input id="c_city" type="text" name="city" class="form-control"/>`
        }


    },
    async _onClickSave() {
            var name = this.$('#c_name').val();
            var email = this.$('#c_email').val();
            var phone = this.$('#c_phone').val();
            var city = this.$('#c_city').val();
            var city_id = this.$('#c_city_id').val();

            var zip = this.$('#c_zip').val();
            var country = this.$('#c_country_id').val();
            var state = this.$('#c_state_id').val();

            const file = document.getElementById('c_image').files[0];
            const file_doc = document.getElementById('c_document').files[0];

            const readFileAsBase64 = (file) => {
                return new Promise((resolve, reject) => {
                    const reader = new FileReader();
                    reader.onload = (e) => resolve(e.target.result.split(',')[1]);
                    reader.onerror = (err) => reject(err);
                    reader.readAsDataURL(file);
                });
            };

            if (city_id){
                Promise.all([
                    readFileAsBase64(file),
                    readFileAsBase64(file_doc)
                ]).then(([imgBase64, docBase64]) => {

                    rpc("/details/submit", {
                        details_dict: {
                            'name': name,
                            'email': email,
                            'phone': phone,
                            'city': "",
                            'city_id': city_id,
                            'zip': zip,
                            'country': country,
                            'state': state,
                            'img': imgBase64,
                            'document': docBase64,
                            'file_name': file_doc.name
                        },
                    });

                }).catch(err => console.error("Error reading files:", err));
            }
            else{
                Promise.all([
                    readFileAsBase64(file),
                    readFileAsBase64(file_doc)
                ]).then(([imgBase64, docBase64]) => {

                    rpc("/details/submit", {
                        details_dict: {
                            'name': name,
                            'email': email,
                            'phone': phone,
                            'city': city,
                            'city_id': 0,
                            'zip': zip,
                            'country': country,
                            'state': state,
                            'img': imgBase64,
                            'document': docBase64,
                            'file_name': file_doc.name
                        },
                    });

                }).catch(err => console.error("Error reading files:", err));
            }
    },
})