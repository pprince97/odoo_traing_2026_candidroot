import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { CustomDialog } from "@library_management/app/components/popup/custom_popup";

patch(ControlButtons.prototype, {
    setup() {
        super.setup(...arguments);
        this.dialogService = useService("dialog");
    },
    async onCustomButtonClick() {
        console.log("Custom Button !!");
        this.dialogService.add(CustomDialog, {
            onSave: (data) => {
                console.log("Data:", data);
            },
        });
    },
});
