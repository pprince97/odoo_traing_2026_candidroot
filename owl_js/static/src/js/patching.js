import { ListController } from "@web/views/list/list_controller";
import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(ListController.prototype, {

    async onClickCreate() {
        if (this.props.resModel === "sale.order") {
            alert("Create button clicked on Sale Order!");
        }
        return await super.onClickCreate(...arguments);
    },

});

patch(FormController.prototype, {
    async saveButtonClicked() {
        if (this.props.resModel === "sale.order") {
            const record = this.model.root;
            const total = record.data.tax_totals.total_amount;
            if (total === 0) {
                this.env.services.dialog.add(ConfirmationDialog, {
                    title: "Validation Error",
                    body: "You cannot create a Sale Order with total amount 0."
                });
                return false;
            }

        }
        return await super.saveButtonClicked(...arguments);
    },
});