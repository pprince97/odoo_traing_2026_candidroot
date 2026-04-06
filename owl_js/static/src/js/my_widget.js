import { registry } from "@web/core/registry";
import { CharField } from "@web/views/fields/char/char_field";

export class CapitalizeWidget extends CharField {
    mounted() {
        super.mounted();
        if (this.el) {
            this.el.addEventListener("blur", this.onBlur.bind(this));
        }
    }
    onBlur(ev) {
        const inputEl = ev.target;
        const capitalized = inputEl.value.toUpperCase();
        this.props.record.update({ [this.props.name]: capitalized });
    }
}
registry.category("fields").add("capitalize_widget", {
    component: CapitalizeWidget,
});

// import { registry } from "@web/core/registry";
// import { Component } from "@odoo/owl";
// import { standardFieldProps } from "@web/views/fields/standard_field_props";
//
// export class MyCustomWidget extends Component {
//     onClick() {
//         alert('clicked');
//     }
// }
// MyCustomWidget.template = "my_custom_widget.MyCustomWidget";
// MyCustomWidget.props = standardFieldProps;
//
// registry.category("fields").add("my_custom_widget", {
//     component: MyCustomWidget,
// });