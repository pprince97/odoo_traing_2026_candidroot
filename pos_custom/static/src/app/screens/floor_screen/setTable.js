import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";

patch(ProductScreen.prototype, {
    async addProductToOrder(product, options) {
        const result = await super.addProductToOrder(product, options);
        const order = this.currentOrder;
        if (order.lines.length >= 0 && !order.table_selected) {
            order.table_selected = new Date().toISOString().replace('T', ' ').slice(0, 19);
            console.log(`Table timer started at ${order.table_selected}`);
        }
        return result;
    },
});
patch(PaymentScreen.prototype, {
   async validateOrder(isForceValidate) {
       const order = this.currentOrder;
       if (order && !order.table_left) {
           order.table_left = new Date().toISOString().replace('T', ' ').slice(0, 19);
       }
       return await super.validateOrder(isForceValidate);
   }
});