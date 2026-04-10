import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class MyForm extends Component {
    static template = "owl_template.MyForm";

    setup() {
        // useState makes the entire object reactive
        this.state = useState({
            text: "Initial Text",
            number: 42,
            color: "pink",
            bool: true,
            date: "2026-04-01",
            volume: 75,
            amount: 10
        });
    }

    // Computed property: Uppercase version of the text input
    get uppercaseText() {
        return this.state.text.toUpperCase();
    }

    // Computed property with a Getter and Setter for "Double Amount"
    get doubleAmount() {
        return this.state.amount * 2;
    }

    set doubleAmount(value) {
        // When user types in the "Double" box, we update the base amount
        this.state.amount = value / 2;
    }
}

// Register as a Client Action
registry.category("actions").add("owl_template.form_action", MyForm);
