/** @odoo-module **/

import {patch} from "@web/core/utils/patch";
import {useService} from "@web/core/utils/hooks";
import {FloorScreen} from "@pos_restaurant/app/floor_screen/floor_screen";
import {Order} from "@point_of_sale/app/store/models";
import {PaymentScreen} from "@point_of_sale/app/screens/payment_screen/payment_screen";

// -------------------
// ORDER TIMER LOGIC
// -------------------
patch(Order.prototype, {
    setup() {
        super.setup(...arguments);
        this.start_time = this.start_time || null;
        this.end_time = this.end_time || null;
    },

    startTimer() {
        if (!this.start_time) {
            this.start_time = Date.now();
            console.log("✅ Timer started:", this.start_time);
        }
    },

    stopTimer() {
        if (!this.end_time) {
            this.end_time = Date.now();
            console.log("🛑 Timer stopped:", this.end_time);
        }
    },

    getElapsedTime() {
        if (!this.start_time) return 0;

        const end = this.end_time || Date.now();
        return Math.floor((end - this.start_time) / 1000);
    }
});

// -------------------
// FLOOR SCREEN PATCH
// -------------------
patch(FloorScreen.prototype, {
    setup() {
        super.setup();
        this.dialogService = useService("dialog");

        // 🔥 Force UI update every second
        setInterval(() => {
            this.env.bus.trigger("update");
        }, 1000);
    },

    onClickTable(table) {
        super.onClickTable(table);

        const order = this.env.pos.get_order();
        if (order) {
            order.startTimer();
        }
    },

    getTableTime(table) {
        const order = this.env.pos.get_order();  // 🔥 use current order

        if (order && order.tableId === table.id) {

            if (!order.start_time) {
                order.startTimer();
            }

            return order.getElapsedTime();
        }

        return 0;
    }
});

// -------------------
// PAYMENT SCREEN PATCH
// -------------------
patch(PaymentScreen.prototype, {
    async validateOrder(isForceValidate) {
        const order = this.env.pos.get_order();

        if (order) {
            order.stopTimer();
        }

        return await super.validateOrder(isForceValidate);
    },
});