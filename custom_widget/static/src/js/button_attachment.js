/** @odoo-module */

import { Component } from "@odoo/owl";
import {Dialog} from "@web/core/dialog/dialog";

export class MyAttachmentDialog extends Component {
    static components = {Dialog};
    static template = "custom_widget.MyAttachmentDialog";

    setup() {}

    confirm() {
        console.log("Confirmed with selected attachment");
        this.props.close();
    }

    cancel() {
        this.props.close();
    }
}