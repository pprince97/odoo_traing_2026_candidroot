/** @odoo-module **/
console.log('>>>>>>>>>>>>>>>>>>>>>>')
import { registry } from "@web/core/registry";
import { CharField, charField } from "@web/views/fields/char/char_field";

export class UpperCharField extends CharField {

    /** Override **/
    async onBlur(ev) {
        super.onBlur(ev);
        const newValue = ev.target.value.toUpperCase();
        ev.target.value = newValue;
        console.log('>>>>>>>>>>>>',this.props.name)
        await this.props.record.update({ [this.props.name]: newValue });
    }
}

export const upper_field = {
    ...charField,
    component: UpperCharField,
};

registry.category("fields").add("upper", upper_field);
