import {FormController} from "@web/views/form/form_controller";
import {patch} from "@web/core/utils/patch";
import {useService} from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import {ConfirmationDialog} from "@web/core/confirmation_dialog/confirmation_dialog";

patch(FormController.prototype, {
    setup() {
        super.setup();
        this.dialogService = useService("dialog");
    },

    saveButtonClicked() {
        if (this.model.config.resModel === 'sale.order' && this.model.root.data.tax_totals.total_amount == 0) {
            this.dialogService.add(ConfirmationDialog, {
                title: "Confirm Amount Action",
                body: "Your Total Amount is 0 \n Are you sure you want to proceed?",
                confirmLabel: _t("Create Order"),
                cancelLabel: _t("Don't Create Order"),
                confirm: () => {
                    super.saveButtonClicked()
                    console.log("confirm")
                },
                cancel: () => {
                    console.log("cancel")
                },
            });

        }
        else
        {
            super.saveButtonClicked()
        }
    }
})