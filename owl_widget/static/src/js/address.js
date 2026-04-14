/** @odoo-module **/


import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class AmountWidget extends Component {

    setup() {
        this.notification = useService("notification");
    }

    increment() {
        const val = this.props.record.data[this.props.name] || 0;
        const newValue = val + 1;
        this.props.record.update({ [this.props.name]: newValue });
    }

    decrement() {
        const val = this.props.record.data[this.props.name] || 0;
        const newValue = val - 1;
        this.props.record.update({ [this.props.name]: newValue });
    }

    onInput(ev) {
        const fieldName = this.props.name;
        const value = parseFloat(ev.target.value) || 0;

        this.props.record.update({
            [fieldName]: value
        });
    }

    validate() {
        const fieldName = this.props.name;
        const value = this.props.record.data[fieldName];

        if (value <= 0) {
            this.notification.add("Amount must be greater than 0", {
                type: "warning",
            });
        }
    }
}

AmountWidget.template = "owl_widget.AmountWidget";

AmountWidget.props = {
    ...standardFieldProps,
};

registry.category("fields").add("amount_widget", {
    component: AmountWidget,
    supportedTypes: ["float"],
});