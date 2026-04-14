/** @odoo-module **/

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { CustomerDialog } from "./customer_dialog";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";

patch(PaymentScreen.prototype, {
    setup() {
        super.setup(...arguments);
        this.dialog = useService("dialog");
        this.pos = usePos();
        this.pos.guestData = {};
    },

    async validateOrder(force) {
        
        if (this.pos.config.guest_details && this.pos.config.guest_details_timing === 'order_after') {

            const guestData = await makeAwaitable(this.dialog, CustomerDialog);
            if(!guestData && this.pos.config.guest_details_required) {
                return false
            }
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

            const order = this.pos.getOrder();

            order.guest_ids = newIds;

        }

        return await super.validateOrder(...arguments);

    }
});