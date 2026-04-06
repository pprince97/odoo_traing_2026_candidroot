/** @odoo-module */

import {patch} from "@web/core/utils/patch";
import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import {ControlButtons} from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import {useService} from "@web/core/utils/hooks";

export class AddCustomerPopup extends Component {
    static template = "AddCustomerPopup";
    static components = { Dialog };

    setup() {
        this.orm = useService("orm");
        this.state = useState({ name: "", email: "", address: "" });
    }

    async confirm() {
        if (!this.state.name) return;
        await this.orm.create("res.partner", [{
            name: this.state.name,
            email: this.state.email,
        }]);
        this.props.close();
    }
}

patch(ControlButtons.prototype, {
    setup() {
        super.setup();
        this.dialogService = useService("dialog");
    },

    onClickPopup() {
        const result = this.dialog.add(AddCustomerPopup, {
            title: "Add Customer",
        });
    },
});