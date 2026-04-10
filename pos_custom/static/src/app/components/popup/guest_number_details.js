import {Dialog} from "@web/core/dialog/dialog";
import {Component, useState} from "@odoo/owl";
import { GuestDetailsPopUp } from "@pos_custom/app/components/popup/guest_details";

export class AddGuestNumberDetailsPopup extends Component {
    static template = "pos_custom.AddGuestNumberDetailsPopup";
    static components = {Dialog};
    static props = {initial_male:Number,
                        initial_female:Number,
                        confirm: { type: Function, optional: true },
                        cancel: { type: Function, optional: true },
                        close: Function
                    };
    setup() {
        this.state = useState({
            male: Number(this.props.initial_male) || 0,
            female: Number(this.props.initial_female) || 0,
            total_no_of_guests: 0,
        });
        this.compute_total();
    }

    compute_total() {
        this.state.total_no_of_guests = Number(this.state.male || 0) + Number(this.state.female || 0);
        console.log(this.state.total_no_of_guests);
    }
    async guestDetailsPopUp() {
    const result = await this.env.services.dialog.add(GuestDetailsPopUp, {
        total: this.state.total_no_of_guests,
        order_data: {
            male: this.state.male,
            female: this.state.female,
        },
    });
    if (result?.back) {
        return;
    }
   if (result?.confirmed) {
    const order = this.pos.getOrder();
    if (order) {
        order.no_of_male = this.state.male;
        order.no_of_female = this.state.female;
        order.total_no_of_guests = this.state.total_no_of_guests;
        order.guest_details = result.guests;
    }
    this.props.close({
        confirmed: true,
        male: this.state.male,
        female: this.state.female,
        total: this.state.total_no_of_guests,
        guest_details: result.guests,
    });
}
}

    // async guestDetailsPopUp() {
    //     this.props.close();
    //     await this.env.services.dialog.add(GuestDetailsPopUp, {
    //         total: this.state.total_no_of_guests,
    //         order_data: { male: this.state.male,
    //             female: this.state.female },
    //         previous: ()=> { this.env.services.dialog.add(AddGuestNumberDetailsPopup, {
    //             initial_male: Number(this.state.male),
    //             initial_female:Number(this.state.female)
    //             });
    //         }
    //     });
    // }
}