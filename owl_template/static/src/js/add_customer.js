/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";

export class AddCustomerPopup extends Component {
    static template = "AddCustomerPopup";
    static components = { Dialog };

    setup() {
        this.orm = useService("orm");
        this.pos = usePos();
        this.state = useState({ name: "", email: "", address: "" });
    }

    async confirm() {

        // Res partner created
        if (!this.state.name) return;
        const partnerID = await this.orm.create("res.partner", [{
            name: this.state.name,
            email: this.state.email,
            street: this.state.address
        }]);

        console.log("Customer created!", partnerID);
        this.props.close();

        // Add general Customer note
        const str = this.state.name + "\n" + this.state.email + "\n" + this.state.address + "\n";

        const order = this.pos.getOrder();
        const str1 = order.general_customer_note;

        if (order.general_customer_note) {
            const str2 = order.general_customer_note;
            order.setGeneralCustomerNote(str);
            order.general_customer_note += str2;
        }
        else {
            order.setGeneralCustomerNote(str);
        }
    }
}


patch(ControlButtons.prototype, {
    setup() {
        super.setup();
        this.dialogService = useService("dialog");
        this.state = useState({ name: "", email: "", address: "" });
    },

    onClickPopup() {
        const result = this.dialog.add(AddCustomerPopup, {
            title: "Add Customer",
        });
    },

});