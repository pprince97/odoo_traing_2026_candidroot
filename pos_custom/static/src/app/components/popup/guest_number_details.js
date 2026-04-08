import { Dialog } from "@web/core/dialog/dialog";
import { Component, useState } from "@odoo/owl";

export class AddGuestNumberDetialsPopup extends Component {
    static template = "pos_custom.AddGuestNumberDetialsPopup";
    static components = { Dialog };
    static props = { close: Function }; // pass currentOrder from POS

    setup() {
        this.state = useState({
            male: 0,
            female: 0,
            total_no_of_guests: 0,
        });
    }

    compute_total() {
        this.state.total_no_of_guests = Number(this.state.male || 0) + Number(this.state.female || 0);
    }

   async openCustomerDetialsPopUp() {
         await this.env.services.dialog.add(GuestDetialsPopUp, {
             total : this.state.total_no_of_guests
         });
    }
}

// import { Dialog } from "@web/core/dialog/dialog";
// import { Component, useState } from "@odoo/owl";
//
// export class AddGuestNumberDetialsPopup extends Component {
//     static template = "pos_custom.AddGuestNumberDetialsPopup";
//     static components = { Dialog };
//     static props = { close: Function };
//
//     setup() {
//         this.state = useState({
//             male: 0,
//             female: 0,
//             total_no_of_guests: 0
//         });
//     }
//
//     compute_total(male,female){
//         this.total_no_of_guests = male + female;
//     }
//
//     async save_guest_number_details() {
//         await this.env.services.orm.call(
//             "pos.order",
//             "write",
//             [this.currentOrder.id, {  // replace with real order id
//                 no_of_male: this.state.male,
//                 no_of_female: this.state.female,
//             }]
//         );
//         this.props.close();
//     }
// }