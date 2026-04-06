import { Component, useState} from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class CustomerDetail extends Component {
    static template = "pos_jui.custom_dialog";
    static components = { Dialog };
    static props = {
        title: {
            validate: (m) => {
                return (
                    typeof m === "string" ||
                    (typeof m === "object" && typeof m.toString === "function")
                );
            },
            optional: true,
        },
        close: Function,
        save:{ type: Function, optional: true },
    };

    save(){
        this.props.close();
    }
}