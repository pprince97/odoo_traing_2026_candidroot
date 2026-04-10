import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { serializeDateTime } from "@web/core/l10n/dates";
const { DateTime } = luxon;

patch(ProductScreen.prototype, {
    async addProductToOrder(product, options) {
        const result =await super.addProductToOrder(...arguments);
        const order = this.currentOrder;
        if (!order.start_date && order.lines.length > 0) {
            order.start_date = serializeDateTime(DateTime.now());
        }
        return result;
    },
});

patch(PaymentScreen.prototype, {
    async validateOrder(isForceValidate) {
        const order = this.currentOrder;
        if (order && !order.end_date) {
            order.end_date = serializeDateTime(DateTime.now());
            console.log('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.')
        }
        return await super.validateOrder(...arguments);
    },
});



















// import { PosOrder } from "@point_of_sale/app/models/pos_order";

// patch(PosOrder.prototype, {
//     setup(_defaultObj, options) {
//         super.setup(...arguments);
//         this.start_date = this.start_date || null;
//         this.end_date = this.end_date || null;
//     },
//     export_as_JSON() {
//         const json = super.export_as_JSON(...arguments);
//         if (json) {
//             json.start_date = this.start_date;
//             json.end_date = this.end_date;
//         }
//         return json;
//     },
//     init_from_JSON(json) {
//         super.init_from_JSON(...arguments);
//         this.start_date = json.start_date;
//         this.end_date = json.end_date;
//     },
// });


// /** @odoo-module **/
//
// import { PosStore } from "@point_of_sale/app/services/pos_store";
// import { patch } from "@web/core/utils/patch";
//
// patch(PosStore.prototype, {
//     async removeOrder(order) {
//         const result = await super.removeOrder(...arguments);
//         if (order) {
//             await this._setEndDate(order);
//         }
//         return result;
//     },
//
//     async selectNextOrder() {
//         const currentOrder = this.get_order();
//         if (currentOrder && currentOrder.is_paid()) {
//             await this._setEndDate(currentOrder);
//         }
//         return await super.selectNextOrder(...arguments);
//     },
//
//     async _setEndDate(order) {
//         if (!order) return;
//         if (!order.backendId) return;
//         if (order.end_date) return;
//         const nowStr = new Date().toISOString().replace('T', ' ').slice(0, 19);
//         order.end_date = nowStr;
//         await this.env.services.orm.write("pos.order", [order.backendId], {
//             end_date: nowStr,
//         });
//     }
// });