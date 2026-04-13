import { Dialog } from "@web/core/dialog/dialog";
import { Component } from "@odoo/owl";

export class AddCustomerDetailsPopup extends Component {
    static template = "pos_custom.AddCustomerDetailsPopup";
    static components = { Dialog };
    static props = { close : Function };

    setup() {
        console.log("CUSTOM POPUP");
    }
}