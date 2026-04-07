import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { serializeDateTime } from "@web/core/l10n/dates";
import OrderPaymentValidation from "@point_of_sale/app/utils/order_payment_validation";
const { DateTime } = luxon;

patch(PosOrder.prototype, {
    setup(_defaultObj, options) {
        super.setup(...arguments);
        this.start_time = this.start_time || null;
        this.end_time = this.end_time || null;
    },
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        if (json) {
            json.start_time = this.start_time;
            json.end_time = this.end_time;
        }
        return json;
    },
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.start_time = json.start_time;
        this.end_time = json.end_time;
    },
});

patch(ProductScreen.prototype, {
    async addProductToOrder(product, options) {
        const result =await super.addProductToOrder(...arguments);
        const order = this.currentOrder;
        if (!order.start_time && order.lines.length > 0) {
            order.start_time = serializeDateTime(DateTime.now());
        }
        return result;
    },
});


patch(OrderPaymentValidation.prototype, {
    async validateOrder() {
        if (!this.order.end_time) {
            this.order.end_time = serializeDateTime(DateTime.now());
        }
        return await super.validateOrder(...arguments);
    },
});

