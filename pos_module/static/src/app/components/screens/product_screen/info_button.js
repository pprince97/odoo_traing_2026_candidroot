import { patch } from "@web/core/utils/patch";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";
import { Component, useState } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";

export class InformationPopup extends Component {
    static template = "info_display";
    static components = { Dialog };

    setup() {
        this.orm = useService("orm");
        this.pos = usePos();
        this.state = useState({ name: "", email: "" });
    }

    async confirm() {
        if (!this.state.name) return;
        await this.orm.create("res.partner", [{
            name: this.state.name,
            email: this.state.email,
        }]);
        this.props.close();

        const order = this.pos.getOrder();
        const str = this.state.name + "\n" + this.state.email + "\n";


        if (order.general_customer_note) {
            const str1 = order.general_customer_note;
            order.setGeneralCustomerNote(str);
            // console.log(setGeneralCustomerNote);
            order.general_customer_note += str1;
        } else {
            order.setGeneralCustomerNote(str);
        }
    }
}

patch(ControlButtons.prototype, {
    setup() {
        super.setup();
        // Use 'dialog' service instead of 'popup'
        this.dialogService = useService("dialog");
    },
    onclickinfobutton() {
        this.dialogService.add(InformationPopup, {
            title: "Add Details",
        });
    },
});