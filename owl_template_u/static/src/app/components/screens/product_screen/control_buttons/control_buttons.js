import { patch } from "@web/core/utils/patch";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { useService } from "@web/core/utils/hooks";
import { CutomerInfoPopup } from "../../../popup/customer_popup"
import {useState} from "@odoo/owl";

patch(ControlButtons.prototype, {
    /**
     * @override
     */
    setup() {
        super.setup(...arguments);
        this.dialogService = useService("dialog");
    },

    custominfo() {
        console.log('>>>>>>>>>>>>>>>>>>>')
        this.dialogService.add(CutomerInfoPopup, {
        });
    }


});
