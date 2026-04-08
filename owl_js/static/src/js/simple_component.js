import { registry } from "@web/core/registry";
import { Component, xml, useState } from "@odoo/owl";

class Counter extends Component {
    static template = xml`
        <div class="counter">
            <span><h6><t t-esc="state.count"/></h6></span>
        </div>
        <button t-on-click="increment" class="btn">+</button>
        <button t-on-click="decrement" class="btn">-</button>
        <button t-on-click="multiply" class="btn">*2</button>
        <button t-on-click="divide" class="btn">/2</button>
    `;
    setup() {
        this.state = useState({ count: 0 });
    }
    increment() {
        this.state.count++;
    }
    decrement() {
        this.state.count--;
    }
    multiply(){
        this.state.count *= 2;
    }
    divide(){
        this.state.count /= 2;
    }
}

class Root extends Component {
    static components = { Counter };
    static template = xml`
        <div>
            <Counter/>
        </div>
    `;
}

registry.category("actions").add("owl_js.counter_action", Root);