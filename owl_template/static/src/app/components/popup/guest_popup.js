import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
// import { DetailPopup } from "./detail_popup";
import { useService } from "@web/core/utils/hooks";

export class GuestPopup extends Component {
    static props = {
        close: Function,
    };
    static template = "pos_restaurant.GuestPopup";
    static components = {
        Dialog
    };

    setup() {

        // onWillStart(async () => {
        //     await this.loadAttachments();
        // });
        this.dialogService = useService("dialog");
        console.log('custom dialog setup')
    }

    next(){
        // this.dialogService.add(DetailPopup, {});
    }
}