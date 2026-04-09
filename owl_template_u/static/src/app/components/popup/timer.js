/** @odoo-module **/
import {FloorScreen} from "@pos_restaurant/app/screens/floor_screen/floor_screen";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import {patch} from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import {onMounted, onWillUnmount, useState} from "@odoo/owl";
import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { PosStore } from "@point_of_sale/app/services/pos_store";
import { serializeDateTime } from "@web/core/l10n/dates";
import OrderPaymentValidation from "@point_of_sale/app/utils/order_payment_validation";
const { DateTime } = luxon;

patch(FloorScreen.prototype, {
    setup() {
        super.setup();
        console.log("helloooo 1111");
        // this.pos = usePos();
        // console.log(this.pos.data);
        this.timerState = useState({currentTime: new Date()});
        let interval;

        this.pos = usePos();

        onMounted(() => {
            interval = setInterval(() => {
                this.timerState.currentTime = new Date();
            }, 1000);
        });

        onWillUnmount(() => {
            // console.log('>>>>>>>>>>>>>unmount');
            clearInterval(interval);
        });
    },

    getTableDuration(table) {

        const order = this.pos.models['pos.order'].find(o => o.table_id && o.table_id.id === table.id);
        // console.dir(order);
        // const order = this.pos.openOrder;
        // console.dir(this.pos, "possssssss");
        // console.log("ORDER>?>>>", order);
        // console.log("Selected Order:", this.pos.selectedOrder);
        if (!order) return "";

        const start = new Date(order.start_time);
        const diff = Math.floor((this.timerState.currentTime - start) / 1000);

        const hours = Math.floor(diff / 3600);
        const minutes = Math.floor((diff % 3600) / 60);
        const seconds = diff % 60;

        return `${hours > 0 ? hours + ':' : ''}${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
});

// patch(PosOrder.prototype, {
//     setup(_defaultObj, options) {
//         super.setup(...arguments);
//         this.start_time = this.start_time || null;
//         this.end_time = this.end_time || null;
//         console.log("calledddddsssssssssss", this.start_time);
//         console.log("calleddddd", this.end_time);
//
//     },
//
//     export_as_JSON() {
//         const json = super.export_as_JSON(...arguments);
//         if (json) {
//             json.start_time = this.start_time;
//             json.end_time = this.end_time;
//             console.log("this.enddddddddddddd", this.start_time);
//             console.log("this.enddddddddddddd", this.end_time);
//         }
//         return json;
//     },
//
//     init_from_JSON(json) {
//         super.init_from_JSON(...arguments);
//         this.start_time = json.start_time;
//         this.end_time = json.end_time;
//         console.log("this.enddddddddddddd", this.end_time);
//         console.log("this.enddddddddddddd", this.start_time);
//     },
// });

patch(ProductScreen.prototype, {
    async addProductToOrder(product, options) {
        const result =await super.addProductToOrder(...arguments);
        const order = this.currentOrder;
        console.log('dfdfdfdfdfdffd', order)
        if (!order.start_time && order.lines.length > 0) {
            order.start_time = serializeDateTime(DateTime.now());
        }
        return result;
    },
});


// patch(OrderPaymentValidation.prototype, {
//     async validateOrder() {
//         if (!this.order.end_time) {
//             this.order.end_time = serializeDateTime(DateTime.now());
//         }
//         return await super.validateOrder(...arguments);
//     },
// });

