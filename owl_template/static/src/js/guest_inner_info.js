/** @odoo-module */

import { Dialog } from "@web/core/dialog/dialog";
import { Component, useState } from '@odoo/owl';

export class GuestInnerInfo extends Component {
    static template = "GuestInnerInfo";
    static components = { Dialog };
    static props = {
        title: String,
        close: Function,
        getPayload: { type: Function, optional: true },
        totalGuests: { type: Number, optional: true },
    };

    setup() {
        super.setup();
        this.state = useState({
            guests: this.createGuestRows(this.props.totalGuests || 0),
        });
    }

    createGuestRows(totalGuests) {
        return Array.from({ length: totalGuests }, (_, index) => ({
            id: index + 1,
            age: 0,
            nationality: "Indian",
            gender: "",
        }));
    }

    async next() {
        console.log("Guest Info : ", this.state.guests);
        this.props.close();
    }

    async previous() {
        this.props.close();
    }

    async skip() {
        this.props.close();
    }
}
