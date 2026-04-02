import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { Component } from "@odoo/owl";

export class RoundedField extends Component {
    static template = "owl_js_practice.RoundedField";
    static props = {
        ...standardFieldProps,
    };

    async onInputChange(ev) {
        const rawValue = parseFloat(ev.target.value) || 0;
        const ceilValue = Math.round(rawValue);
        await this.props.record.update({ [this.props.name]: ceilValue });
    }
}

export const RoundedFieldItem = {
    component: RoundedField,
    displayName: "RoundUp",
    supportedTypes: ["float"],
};

registry.category("fields").add("roundup", RoundedFieldItem);