import { Component, useRef } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";

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
        skip: Function,
        save: Function,
        male:Number,
        female:Number,
        guests:Number,
    };

    setup(){
        this.pos = usePos();
        this.maleRef = useRef('male_c')
        this.femaleRef = useRef('female_c')
        this.guestRef = useRef('guest_c')
    }

    next(){
        if (parseInt(this.guestRef.el.value) === 0){
            this.env.services.notification.add(`Missing required fields`, {type: 'danger'});
        }
        else{
           this.props.close();
           this.props.save(this.maleRef.el.value,this.femaleRef.el.value,this.guestRef.el.value);
        }
    }

    skip_view(){
        this.props.close();
        this.props.skip();
    }

    guest_no(){
        this.guestRef.el.value = parseInt(this.maleRef.el?.value || 0) + parseInt(this.femaleRef.el?.value || 0);
    }
}