import {Dialog} from "@web/core/dialog/dialog";
import {Component, useState} from "@odoo/owl";

export class GuestDetails extends Component {
    static template = "GuestDetails";
    static components = {Dialog};

    static props = {
        title: {type: String, optional: true},
        customers: {type: Array, optional: true},
        close: Function,
    };

    setup() {
        this.state = useState({
            customers: (this.props.customers || []).map(c => ({
                age: c.age || "",
                nationality: c.nationality || "",
                gender: c.gender || "",
            })),
        });
    }

    updateCustomer = (index, field, ev) => {
        this.state.customers[index][field] = ev.target.value;
    };

    next = () => {
        this.props.close({
            confirmed: true,
            data: this.state.customers,
        });
    };

    skip = () => {
        this.props.close({confirmed: false});
    };

    previous = () => {
        this.props.close({confirmed: false});
    };
}