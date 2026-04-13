/** @odoo-module */

import { DataServiceOptions } from "@point_of_sale/app/models/data_service_options";
import { patch } from "@web/core/utils/patch";

patch(DataServiceOptions.prototype, {
    get dynamicModels() {
        const models = super.dynamicModels;
        if (!models.includes("pos.guest")) {
            models.push("pos.guest");
        }
        return models;
    }
});
