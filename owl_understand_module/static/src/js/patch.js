import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";

patch(FormController.prototype, {

    async create() {
        alert("New button clicked");

        return super.create(...arguments);
    },

    async save() {
        const data = this.model.root.data;

        if (!data.partner_id) {
            alert("Customer is required");
            return;
        }

        if (data.amount_total === 0) {
            alert("Total cannot be 0");
            return;
        }

        return super.save(...arguments);
    },

});