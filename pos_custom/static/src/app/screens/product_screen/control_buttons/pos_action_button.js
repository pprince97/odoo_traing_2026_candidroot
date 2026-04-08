import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";
import { AddCustomerDetailsPopup } from "@pos_custom/app/components/popup/customer_dialog"

patch(ControlButtons.prototype, {
    setup(){
        super.setup(...arguments);
        this.dialogService = useService("dialog");
    },
    onCustomButtonClick() {
       this.dialogService.add(AddCustomerDetailsPopup,{});
    },
});