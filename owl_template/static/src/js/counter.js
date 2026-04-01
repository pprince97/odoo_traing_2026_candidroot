/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class Counter extends Component {
    setup() {
        this.stateu = useState({
            count: 0
        });
    }

    inc_counter() {
        this.stateu.count++;
    }
}

Counter.template = "owl_template.Counter";

// Register as client action
registry.category("actions").add("owl_template.counter_action", Counter);