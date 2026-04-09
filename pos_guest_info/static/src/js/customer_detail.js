/** @odoo-module **/

import {Component, useState} from "@odoo/owl";
import {Dialog} from "@web/core/dialog/dialog";

export class CustomerDetail extends Component {
    static components = {Dialog};
    static template = "pos_guest_info.CustomerDetail";
    static props = {
        no_of_guest: Number,
        confirm: { type: Function, optional: true },
        close: Function,
        getPayload: Function,
    };

    setup() {

        this.state = useState({
            customers: Array.from({ length: this.props.no_of_guest || 1 }, (_, i) => ({
                id: i,
                age: "",
                country: "",
                gender: "",
            })),
        });
    }

    async confirm() {

        const data = {
            customers: this.state.customers,
        };
        console.log(data, "DATA");
        console.log(this.state.customers, "this.state.customers");

        if (this.props.confirm) {
            await this.props.confirm(data);
        }
        this.props.close(data);
    }

    cancel() {
        this.props.close({confirmed: false});
    }
}