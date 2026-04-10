/** @odoo-module **/
import { PosStore } from "@point_of_sale/app/services/pos_store";
import { patch } from "@web/core/utils/patch";

patch(PosStore.prototype, {
    async removeOrder(order) {
        const tableId = order.table_id?.id;
        const result = await super.removeOrder(...arguments);
        if (tableId) {
            await this._clearTimerOnServer(tableId);
        }
        return result;
    },

    async selectNextOrder() {
        const currentOrder = this.get_order();
        if (currentOrder && currentOrder.is_paid() && currentOrder.table_id) {
            await this._clearTimerOnServer(currentOrder.table_id.id);
        }
        return await super.selectNextOrder(...arguments);
    },

    async _clearTimerOnServer(tableId) {
        const table = this.models["restaurant.table"].get(tableId);
        if (table) {
            table.start_date = false;
            await this.env.services.orm.write("restaurant.table", [tableId], {
                start_date: false,
            });
        }
    }
});
