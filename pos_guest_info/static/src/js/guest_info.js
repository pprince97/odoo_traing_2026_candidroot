/** @odoo-module **/

import {Component, useState} from "@odoo/owl";
import {Dialog} from "@web/core/dialog/dialog";

export class CustomerDialog extends Component {
    static components = {Dialog};
    static template = "pos_guest_info.CustomerDialog";

    setup() {
        console.log("In The Set up");

        this.state = useState({
            no_of_male: 0,
            no_of_female: 0,
            no_of_guest: 0,
        });
    }

    updateGuestCount() {
        if (this.state.no_of_male >= 0 && this.state.no_of_female >= 0) {
            this.state.no_of_guest = Number(this.state.no_of_male) + Number(this.state.no_of_female);
        }
        else {
            alert("Person is not negative")
            this.state.no_of_male = 0
            this.state.no_of_female = 0
            this.state.no_of_guest = 0
        }
    }



    async confirm() {
        const data = {
            no_of_male: this.state.no_of_male,
            no_of_female: this.state.no_of_female,
            no_of_guest: this.state.no_of_guest,
        };
        if (this.props.confirm) {
            await this.props.confirm(data);
        }
        this.props.close();
    }

    cancel() {
        this.props.close({confirmed: false});
    }
}