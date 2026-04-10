/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class HoverUppercaseWidget extends Component {
    static template = "hover_char.HoverUppercaseWidget";
    static props = { ...standardFieldProps };

    state = useState({
        value: this.props.record.data[this.props.name] || "",
        hover: false,
    });

    onInput(ev) {
        this.state.value = ev.target.value;
        this.props.record.update({ [this.props.name]: this.state.value });
    }

    onMouseEnter() { this.state.hover = true; }
    onMouseLeave() { this.state.hover = false; }

    onBlur() {
        this.state.value = (this.state.value || "").toUpperCase();
        this.props.record.update({ [this.props.name]: this.state.value });
    }

    get styleString() {
        let style = "padding:4px 8px; border:1px solid #ccc; border-radius:4px; transition: all 0.2s; width:180px;";
        if (this.state.hover) {
            style += " box-shadow:0 4px 8px rgba(0,0,0,0.2);";
        }
        return style;
    }
}

registry.category("fields").add("hover_uppercase_widget", {
    component: HoverUppercaseWidget,
    supportedTypes: ["char"],
});