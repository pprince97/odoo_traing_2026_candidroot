/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { CustomerDetail } from "./customer_detail";
import { useService } from "@web/core/utils/hooks";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";

export class CustomerDialog extends Component {
    static components = {Dialog};
    static template = "pos_guest_info.CustomerDialog";
    static props = {
        close : { type: Function },
        getPayload: Function,
    };

    setup() {
        this.dialog = useService("dialog");

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
            alert("Number of person can not be negative!")
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

        const customerDetails = await makeAwaitable(this.dialog, CustomerDetail, {
                no_of_guest: data.no_of_guest,
            });

        this.props.getPayload({details: customerDetails, numbers: data});
        this.props.close();
    }

    cancel() {
        this.props.close({confirmed: false});
    }
}