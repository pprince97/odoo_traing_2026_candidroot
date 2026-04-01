/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";


const { status } = owl;

export class Counter extends Component {
    setup() {
        this.state = useState({
            count: 0,
            count1: 0
        });
    }

    increment() {
        this.state.count++;
        this.state.count1++;
    }
}

Counter.template = "owl_template.Counter";

// Register as client action
registry.category("actions").add("owl_template.counter_action", Counter);