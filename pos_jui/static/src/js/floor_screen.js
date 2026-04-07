import { FloorScreen } from "@pos_restaurant/app/screens/floor_screen/floor_screen";
import { patch } from "@web/core/utils/patch";
import { onWillUnmount, onMounted } from "@odoo/owl";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { PosStore } from "@point_of_sale/app/services/pos_store";
import { PosOrder } from "@point_of_sale/app/models/pos_order";
import OrderPaymentValidation from "@point_of_sale/app/utils/order_payment_validation";
import { serializeDateTime } from "@web/core/l10n/dates";
const { DateTime } = luxon;



patch(PosOrder.prototype, {
    setup(_defaultObj, options) {
        super.setup(...arguments);
        this.start_date = this.start_date || null;
        this.end_date = this.end_date || null;
    },
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        if (json) {
            json.start_date = this.start_date;
            json.end_date = this.end_date;
        }
        return json;
    },
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.start_date = json.start_date;
        this.end_date = json.end_date;
    },
});

patch(ProductScreen.prototype, {
    async addProductToOrder(product, options) {
        const result =await super.addProductToOrder(...arguments);
        const order = this.currentOrder;
        if (!order.start_date && order.lines.length > 0) {
            this.order.start_date = serializeDateTime(DateTime.now());
        }
        return result;
    },
});

patch(OrderPaymentValidation.prototype, {
    async validateOrder() {
        if (!this.order.end_date) {
            this.order.end_date = serializeDateTime(DateTime.now());
        }
        return await super.validateOrder(...arguments);
    },
});

patch(FloorScreen.prototype, {
    setup() {
        super.setup();
        this.state.tableTimers = {};
        let interval;

        onMounted(()=>{
            interval = setInterval(() => {
                const floor = this.pos.models["restaurant.floor"].get(this.state.selectedFloorId);

                floor.table_ids.forEach((table) => {
                    let order = this.pos.models["pos.order"].filter(
                        (o) => o.table_id?.id === table.id && !o.finalized
                    );
                    order = order[0]
                    if (order && order.lines.length > 0) {

                        const diff = Math.floor((new Date() - new Date(order.start_date)) / 1000);
                        const mins = Math.floor(diff / 60).toString().padStart(2, '0');
                        const secs = (diff % 60).toString().padStart(2, '0');
                        this.state.tableTimers[table.id] = `${mins}:${secs}`;
                    } else {
                        this.state.tableTimers[table.id] = '00:00';
                    }
                });
            }, 1000);
        });

        onWillUnmount(() => {if(interval){clearInterval(interval)}});
    }
});