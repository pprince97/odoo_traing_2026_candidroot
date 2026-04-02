import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";


patch(FormController.prototype, {
    setup() {
        console.log("setup");
        super.setup();

    },

    saveButtonClicked() {
        console.log("save button clicked");
        debugger
        if (this.props.resModel === 'sale.order' && this.model.root.data.tax_totals.total_amount === 0) {
            this.env.services.dialog.add(AlertDialog, {
                title: _t("Unexpected Amount"),
                body: _t("Amount must not be zero."),
            });
        }
        else {
            super.saveButtonClicked();
        }
    },
});