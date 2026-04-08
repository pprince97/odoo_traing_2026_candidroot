import {patch} from "@web/core/utils/patch";
import {FloorScreen} from "@pos_restaurant/app/screens/floor_screen/floor_screen";
import {useState, onMounted, onWillUnmount} from "@odoo/owl";
import {ProductScreen} from "@point_of_sale/app/screens/product_screen/product_screen";
import {PaymentScreen} from "@point_of_sale/app/screens/payment_screen/payment_screen";
import {serializeDateTime} from "@web/core/l10n/dates";
import {GuestDetailsDialog} from "./guest_details_dialog";

const {DateTime} = luxon;

patch(ProductScreen.prototype, {
    async addProductToOrder(product, options) {
        const result = await super.addProductToOrder(...arguments);
        const order = this.currentOrder;
        if (!order.start_date_time && order.lines.length > 0) {
            order.start_date_time = serializeDateTime(DateTime.now());
        }
        return result;
    },
});

patch(PaymentScreen.prototype, {
    async validateOrder(isForceValidate) {
        const order = this.currentOrder;
        if (order && !order.end_date_time) {
            order.end_date_time = serializeDateTime(DateTime.now());
        }
        return await super.validateOrder(...arguments);
    },
});

patch(FloorScreen.prototype, {
    setup() {
        super.setup();
        this.timeState = useState({currentTime: new Date()});
        let interval;
        onMounted(() => {
            interval = setInterval(() => {
                this.timeState.currentTime = new Date();
            }, 1000);

        });
        onWillUnmount(() => {
            clearInterval(interval);
        });

        this.env.services.dialog.add(GuestDetailsDialog, {});
    },

    getTableTimer(table) {
        if (this.pos.tableHasOrders(table)) {
            const order = table.getOrder();
            if (!order) return "00:00";
            if (order.start_date_time) {
                const start = new Date(order.start_date_time);
                const diff = Math.floor((this.timeState.currentTime - start) / 1000);

                const hours = Math.floor(diff / 3600);
                const minutes = Math.floor((diff % 3600) / 60);
                const seconds = diff % 60;

                return `${hours > 0 ? hours + ':' : ''}${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            }
        } else {
            return "00:00";
        }
    },

});



