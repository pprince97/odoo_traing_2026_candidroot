/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";
import { useService } from "@web/core/utils/hooks";


patch(FormController.prototype, {
    setup() {
        super.setup();
        this.notification = useService("notification");
    },

    async saveButtonClicked(params = {}) {

        // this.model.config.resModel

        // console.log(this.model.config.resModel !== "sale.order");

        if (this.model.config.resModel !== "sale.order"){
            return await super.saveButtonClicked(...arguments);
        }


        // debugger
        const data =  this.model.root.data.order_line.records;
        // console.log(data[1].data.price_subtotal, "records");

        if(data.length === 0) {
            this.notification.add("Please add a product!", {
                    type: "danger",
                });
                return false;
        }

        let total = 0;

        for (const record of data) {
            total += record.data.price_subtotal;
        }

        if (total <= 0) {
            this.notification.add("Please add quantity!", {
                type: "danger",
            });
            return false;
        }

        return await super.saveButtonClicked(...arguments);
    },
});