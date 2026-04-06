/** @odoo-module **/

import {Component, useState} from "@odoo/owl";
import {Dialog} from "@web/core/dialog/dialog";

export class CustomerDialog extends Component {
    static components = {Dialog};
    static template = "pos_sale.CustomerDialog";

    setup() {
        console.log("In The Set up");
        this.state = useState({
            name: "",
            phone: "",
            street: "",
        });
    }

    async confirm() {
        const data = {
            name: this.state.name,
            phone: this.state.phone,
            street: this.state.street,
        };
        if (this.props.confirm) {
            await this.props.confirm(data);
        }
        this.props.close();
    }

    cancel() {
        this.props.close({confirmed: false});
    }
}