import { patch } from "@web/core/utils/patch";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";
import { Component, useState } from "@odoo/owl";

export class InformationPopup extends Component {
    static template = "info_display";
    static components = { Dialog };

    setup() {
        this.orm = useService("orm");
        this.state = useState({ name: "", email: "" });
    }

    async confirm() {
        if (!this.state.name) return;
        await this.orm.create("res.partner", [{
            name: this.state.name,
            email: this.state.email,
        }]);
        this.props.close(); // Dialog service provides the close prop
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