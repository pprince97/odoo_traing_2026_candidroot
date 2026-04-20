import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";


publicWidget.registry.BookingInformation = publicWidget.Widget.extend({
    selector: '#booking_form',

    events: {
        'click #booking_create_record': '_onClickSubmit',
    },

    async _onClickSubmit() {
        console.log(">>>>>>>>>>>>>>>");
        var dict = {
            customer_id : this.$('#customer').val() || false,
            start_date : this.$('#start_date').val() || false,
            end_date : this.$('#end_date').val() || false,
            trip_details : this.$('#trip_details').val() || false,
            state : this.$('#state').val() || false,
        };
        const values = await rpc('/get/booking-details', { 'values': dict });

    },

});