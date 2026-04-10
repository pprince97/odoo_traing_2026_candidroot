import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class Counter extends Component {
    setup() {
        this.state = useState({
            count: 0
        });
    }
    increment() {
        this.state.count++;
    }
    decrement() {
        this.state.count--;
    }
    reset() {
        this.state.count = 0;
    }
    multiplication() {
        this.state.count *= 2;
    }
    division() {
        this.state.count /= 2;
    }
    modulo() {
        this.state.count %= 2;
    }
}

Counter.template = "owl_template.Counter";

registry.category("actions").add("owl_template.counter_action", Counter);