import {patch} from "@web/core/utils/patch";
import {PosOrder} from "@point_of_sale/app/models/pos_order";
import { useState, onMounted } from "@odoo/owl";
import {FloorScreen} from "@pos_restaurant/app/screens/floor_screen/floor_screen";

patch(PosOrder.prototype, {

    setup() {
        super.setup(...arguments);
        console.log("PosOrder: setup called")
    },

    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.start_date_time = this.start_date_time || new Date().toISOString();
        json.end_date_time = this.end_date_time;
        return json;
    },

    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.start_date_time = json.start_date_time;
        this.end_date_time = json.end_date_time;
    },

    finalize() {
        this.end_date_time = new Date().toISOString();
        return super.finalize(...arguments);
    },

});

patch(FloorScreen.prototype, {
    setup() {
        super.setup();
        console.log("FloorScreen: setup called");

        this.datetimestate = useState({ currenttime: new Date() });
        let interval;
        onMounted(() => {
            interval = setInterval(() => {
                this.datetimestate.currenttime = new Date();
            }, 1000);
        });


    },

    getTableTimer(table) {
        const order = this.pos.models['pos.order'].find(o => o.table_id && o.table_id.id === table.id);
        if (!order) return "00:00";
        console.log(order);

        // if (!order.length) {
        //     return "00:00";
        // }


        // const start = new Date(order.start_date_time);

        // const timediff = Math.floor((this.datetimestate.currenttime - start) / 1000);
        //
        // const minutes = String(Math.floor(elapsed / 60)).padStart(2, "0");
        // const seconds = String(elapsed % 60).padStart(2, "0");
        //
        // return `${minutes}:${seconds}`;
    },
})
