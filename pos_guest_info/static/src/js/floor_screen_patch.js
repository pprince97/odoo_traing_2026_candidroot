/** @odoo-module **/

import {FloorScreen} from "@pos_restaurant/app/screens/floor_screen/floor_screen";
import {patch} from "@web/core/utils/patch";
import {useService} from "@web/core/utils/hooks";
import {usePos} from "@point_of_sale/app/hooks/pos_hook";
import {CustomerDialog} from "./customer_dialog";
import {makeAwaitable} from "@point_of_sale/app/utils/make_awaitable_dialog";

patch(FloorScreen.prototype, {

    setup() {
        super.setup();
        this.dialog = useService("dialog");
        this.pos = usePos();
        this.pos.guestData = {};
    },

    async onClickTable(table, ev) {

        let order = table.getOrder();

        if (this.pos.config.guest_details && this.pos.config.guest_details_timing === 'order_before' && !order) {

            const guestData = await makeAwaitable(this.dialog, CustomerDialog);
            if(!guestData){
                return false
            }
            await super.onClickTable(table, ev);
            const order = this.pos.getOrder();
            const customers = guestData.details.customers
            const newIds = [];
            for (const guest of customers) {
                const newGuest = await this.pos.models["pos.guest"].create({
                    age: guest.age,
                    gender: guest.gender,
                    country: guest.country,
                });


                newIds.push(newGuest.id);
            }

            order.guest_ids = newIds;

        } else {
            await super.onClickTable(table, ev);
        }
    }
});