import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class CustomDialog extends Component {
    static components = { Dialog };
    static template = "library_management.CustomDialog";

    static props = {
        onSave: {type: Function},
        close: {type: Function},
    };

    setup() {
        this.state = useState({
            name: "",
            phone: "",
            note: ""
        });
    }

    _onConfirm() {
        this.props.onSave({ ...this.state });
        this.props.close();
    }

    _onCancel() {
        this.props.close();
    }
}
