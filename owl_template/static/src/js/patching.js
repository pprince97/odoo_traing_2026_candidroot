/** @odoo-module **/

import { FormController } from "@web/views/form/form_controller";
import { patch } from "@web/core/utils/patch";
import { ListController } from "@web/views/list/list_controller";

patch(FormController.prototype, {
    setup() {
        super.setup();

        console.log("I am From Form Controller!");
    },

    async saveButtonClicked(params = {}) {
        // debugger

        // Fields validation
        const saleModel = this.model.root.resModel;
        console.log(this.model.root.data.user_id.display_name);

        if (saleModel === 'sale.order') {

            if (!this.model.root.data.user_id) {
                alert("Sales Person field is required!");
                return;
            }
        }

        // Total Amount - 0 validation
        console.log(this.model.root.data.order_line.records)

        const amounts = this.model.root.data.order_line.records
        const total_amt = amounts.map(rec => rec.data.price_total).reduce((a, b) => a + b, 0)

        if(total_amt === 0.0) {
            alert("Total amount not must be 0 !")
            return;
        }

        return super.saveButtonClicked();
    },

    async discard() {
        alert("Why are you leave the form, bro!");

        return super.discard();
    },

    async deleteRecord() {
        alert("Why are you delete the record, bro!");

        return super.deleteRecord();
    }
});


patch(ListController.prototype, {
    setup() {
        super.setup()

        console.log("I am From List Controller!")
    },

    async onClickCreate() {
        alert("I think you need to create form, Right!");

        return super.onClickCreate();
    }
})