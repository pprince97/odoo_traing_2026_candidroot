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

Counter.template = "owl_template_u.Counter";

// Register as client action
registry.category("actions").add("owl_template_u.counter_action", Counter);