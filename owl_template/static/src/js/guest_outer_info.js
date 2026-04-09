/** @odoo-module */

import {Dialog} from "@web/core/dialog/dialog";
import {Component, useState} from '@odoo/owl';


export class GuestOuterInfo extends Component {
    static template = "GuestOuterInfo";
    static components = {Dialog};
    static props = {
        title: String,
        close: Function,
        confirm: { type: Function, optional: true },
        getPayload: { type: Function, optional: true },
    };

    setup() {
        super.setup();
        this.state = useState({no_of_male: 0, no_of_female: 0, no_of_total: 0});
        // this.notification = useService("notification");
    }
    async confirm() {
        // if (!this.isValid) {
        //     this.env.services.notification.add("Please enter valid guest numbers", {type: "warning"});
        //     return;
        // }

        const payload = {
            no_of_male: parseInt(this.state.no_of_male || 0),
            no_of_female: parseInt(this.state.no_of_female || 0),
            no_of_total: parseInt(this.state.no_of_total || 0),
        };

        if(this.props.confirm) {
            await this.props.confirm(payload);
        }

        console.log("No of Guests confirmed!", payload.no_of_male, payload.no_of_female, payload.no_of_total);

        this.props.close();
    }

    onInputChanged() {
        const male = parseInt(this.state.no_of_male || 0);
        const female = parseInt(this.state.no_of_female || 0);
        if (male < 0 || female < 0) {
            this.state.no_of_total = 0;
        } else {
            this.state.no_of_total = male + female;
        }
    }

    get isValid() {
        return this.state.no_of_male >= 0 && this.state.no_of_female >= 0 && this.state.no_of_total > 0;
    }

    async close() {
        console.log("Guest Outer Info closed!");
        this.props.close();
    }

    async skip() {
        console.log("Guest Outer Info skipped!");
        this.props.close();
    }
}