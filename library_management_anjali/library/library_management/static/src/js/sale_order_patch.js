import {ListController} from "@web/views/list/list_controller";
import {FormController} from "@web/views/form/form_controller";
import {patch} from "@web/core/utils/patch";
import {ConfirmationDialog} from "@web/core/confirmation_dialog/confirmation_dialog";

patch(ListController.prototype, {
    onClickCreate() {
        if (this.props.resModel === "sale.order") {
            console.log("New button clicked in Sale Order List View!");
            alert("New button clicked in Sale Order List View!");
        }
        return super.onClickCreate(...arguments);
    },
});

patch(FormController.prototype, {
    setup() {
        super.setup(...arguments);
        if (this.props.resModel === "sale.order") {
            console.log("Sale Order Form View has been opened!");
        }

    },
});

patch(FormController.prototype, {
    async saveButtonClicked() {
        // debugger
        if (this.props.resModel === "sale.order") {
            const record = this.model.root;
            const totalAmount = record.data.tax_totals.total_amount;
            const origin = record.data.origin;
            const origin_order = origin.toLowerCase().includes("order");
            let error_messages = [];
            console.log('>>>>>>>>>>>>>>>', totalAmount)
            if (totalAmount <= 0) {
                error_messages.push('Total amount must be greater than 0.');
            }
            if (!origin_order) {
                error_messages.push('Origin must contain the word order.');
            }
            if (error_messages.length > 0) {
                this.env.services.dialog.add(ConfirmationDialog, {
                    'title': 'Warning',
                    'body': error_messages.join('\n')
                });
                return false;
            }
        }
        return await super.saveButtonClicked(...arguments);
    },
});


// this.env.services.dialog.add(ConfirmationDialog,{
//     'title' : 'Error',
//     'body' : 'Total amount must be greater than 0.'
// });
// this.env.services.notification.add(
//     "Total amount must be greater than 0.",
//     { type: "danger" }
// );