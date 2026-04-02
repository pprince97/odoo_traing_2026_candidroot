import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class Counter extends Component {
    setup() {
        this.counter_state = useState({
            count: 0
        });
    }

    increment_counter() {
        this.counter_state.count++;
    }

    decrement_counter() {
        this.counter_state.count--;
    }

    // increment_fontsize() {
    //     var p_tag = document.querySelector("p");
    // }
}

Counter.template = "owl_components.CounterTemplate";

registry.category("actions").add("owl_components.counter_action", Counter);