import { patch } from "@web/core/utils/patch";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { useService } from "@web/core/utils/hooks";
import { CustomerDetail } from './custom_dialog';

patch(ControlButtons.prototype,{
    setup() {
        super.setup();
        this.dialogService = useService("dialog");
    },

    async fill_details() {
        this.dialogService.add(CustomerDetail, {
            title: "Customer Details",
            close: ()=>{},
            order: this.currentOrder,
        });
    }
})