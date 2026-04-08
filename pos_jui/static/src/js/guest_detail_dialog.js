import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class GuestDetail extends Component {
    static template = "pos_jui.guest_detail_dialog";
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

    setup(){
        this.state = useState({
            guest: 0,
        });
    }

    save(){
        this.props.close();
    }

    guest_no(ev){
        console.log(ev.currentTarget)
        this.state.guest = parseInt(document.getElementById('male').value) + parseInt(document.getElementById('female').value);
    }
}