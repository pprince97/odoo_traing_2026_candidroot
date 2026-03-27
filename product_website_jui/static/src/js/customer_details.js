import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
import { renderToElement } from "@web/core/utils/render";

publicWidget.registry.CustomerDetails = publicWidget.Widget.extend({
    selector: '.customer_detail_form',
    events: {
        'change #c_country_id': '_onCountryChange',
        'change #c_state_id': '_onCityChange',
        'click #save_details': '_onClickSave',
    },
    start() {
        console.log("_______________");
        return this._super.apply(this, arguments);
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

            if (this.$('#c_city')){
                var city = this.$('#c_city').val();
            }else{
                if(this.$('#c_city_id')){
                var city = this.$('#c_city_id').val();
                }
            }

            var zip = this.$('#c_zip').val();
            var country = this.$('#c_country_id').val();
            var state = this.$('#c_state_id').val();

            const file = document.getElementById('c_image').files[0];

            if (file){
            const reader = new FileReader();
            reader.readAsDataURL(file);

            reader.onload = function(e) {
                    const base64Data = e.target.result.split(',')[1];

                    const result =rpc("/details/submit", {
                        details_dict: {'name':name,'email':email,'phone':phone,'city':city,'zip':zip,'country':country,'state':state,'img':base64Data},
                    });
                }.bind(this);
            }

    },
})