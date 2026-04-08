import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { GuestPopup } from "./guest_popup";
import { useService } from "@web/core/utils/hooks";

export class DetailPopup extends Component {
    static props = {
        close: Function,
    };
    static template = "pos_restaurant.DetailPopup";
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

    previous(){
        this.dialogService.add(GuestPopup, {});
    }
}