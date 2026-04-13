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
        skip: Function,
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

        const guestData = [];
        let validate_male = parseInt(this.props.male);
        let validate_female = parseInt(this.props.female);
        let allfieldstrue = true
        this.guestRange.forEach((num) => {
            guestData.push({
                guest_number: num,
                age: document.getElementById(`age_${num}`).value || 0,
                nationality_id: document.getElementById(`nationality_${num}`).value || null,
                gender: document.getElementById(`gender_${num}`).value || null,
            });
        });
        for (const g of guestData) {
            if(g.gender === 'male'){
                validate_male -= 1
            }
            if(g.gender === 'female'){
                validate_female -= 1
            }
            console.log(g.age,'<<<<<<',g.nationality_id,'>>>>',g.gender)
            if(!g.age || !g.nationality_id || g.gender === null){
                allfieldstrue = false
            }
        }
        if(!allfieldstrue){
            this.env.services.notification.add(`Missing required fields`, {type: 'danger'});
        }
        else{
            if (validate_female === 0 && validate_male === 0){
                this.props.save(parseInt(this.props.male),parseInt(this.props.female),parseInt(this.props.guests),guestData);
                 this.props.close();
            }
            else {
                this.env.services.notification.add(`Details must be entered according to the registered no of male ${this.props.male} and female ${this.props.female}`, {type: 'danger'});
            }
        }
    }

    skip_view(){
        this.props.close();
        this.props.skip();
    }

    get guestRange() {
        return Array.from({ length: parseInt(this.props.guests) }, (_, i) => i + 1);
    }

    prev() {
        this.props.close();
        this.props.previous();
    }
}