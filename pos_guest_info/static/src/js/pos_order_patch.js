/** @odoo-module **/

import {patch} from "@web/core/utils/patch";
import {PosOrder} from "@point_of_sale/app/models/pos_order";

patch(PosOrder.prototype, {
    setup() {
        super.setup(...arguments);
        this.guest_ids = this.guest_ids || [];
    },

    toJSON() {
        const json = super.toJSON(...arguments);
        json.guest_ids = this.guest_ids;
        return json;
    }
});