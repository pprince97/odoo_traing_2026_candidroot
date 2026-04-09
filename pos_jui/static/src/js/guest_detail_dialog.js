import { Component, useRef } from "@odoo/owl";
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
        save: Function,
        male:Number,
        female:Number,
        guests:Number,
    };

    setup(){
        this.maleRef = useRef('male_c')
        this.femaleRef = useRef('female_c')
        this.guestRef = useRef('guest_c')
    }

    next(){
        this.props.close();
        this.props.save(this.maleRef.el.value,this.femaleRef.el.value,this.guestRef.el.value);
    }

    guest_no(){
        this.guestRef.el.value = parseInt(this.maleRef.el?.value || 0) + parseInt(this.femaleRef.el?.value || 0);
    }
}