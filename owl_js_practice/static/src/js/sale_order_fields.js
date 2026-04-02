import {FormController} from "@web/views/form/form_controller";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(FormController.prototype,{
    setup() {
        super.setup(...arguments);
        this.dialogService = useService("dialog"); // 4. Initialize service
    },
    saveButtonClicked(){
        if(this.modelParams.config.resModel=="sale.order" && this.model.root.data.tax_totals.total_amount == 0){
            this.dialogService.add(AlertDialog, {
                title: "Total amount is mandatory",
                body: "The total amount cannot be 0",
            });
            return;
        }
        super.saveButtonClicked();
    }
});
