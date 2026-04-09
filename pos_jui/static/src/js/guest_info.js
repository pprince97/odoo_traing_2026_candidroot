import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";


export class GuestInfo extends Component {
    static template = "pos_jui.guest_info_dialog";
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
        guests: String,
        male:String,
        female:String,
        previous: Function,
    };

    setup(){
        this.pos = usePos();
        this.countries = this.pos.models["res.country"].getAll();
        this.gender = {'male':'Male','female':'Female','others':'Others'}
        this.genderEntries = Object.entries(this.gender);
    }

    next(){
        this.props.close();
        const guestData = [];
        this.guestRange.forEach((num) => {
            guestData.push({
                guest_number: num,
                age: document.getElementById(`age_${num}`).value || 0,
                nationality_id: document.getElementById(`nationality_${num}`).value || null,
                gender: document.getElementById(`gender_${num}`).value || null,
            });
        });
        this.props.save(parseInt(this.props.male),parseInt(this.props.female),parseInt(this.props.guests),guestData);
    }

    get guestRange() {
        return Array.from({ length: parseInt(this.props.guests) }, (_, i) => i + 1);
    }

    prev() {
        this.props.close();
        this.props.previous();
    }
}