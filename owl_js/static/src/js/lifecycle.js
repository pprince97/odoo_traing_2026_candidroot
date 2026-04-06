import {registry} from "@web/core/registry";
import {
    Component, useState, onWillUnmount, onWillPatch, onPatched, onRendered, onWillRender, onMounted, onWillStart
} from "@odoo/owl";

export class CounterComponent extends Component {
    setup() {
        console.log("setup");
        this.state = useState({count: 0});

        onWillStart(() => {
            console.log("willStart");
        });

        onWillRender(() => {
            console.log("willRender");
        });

        onRendered(() => {
            console.log("rendered");
        });

        onMounted(() => {
            console.log("on mounted");
        });

        onWillPatch(() => {
            console.log("willPatch");
        });

        onPatched(() => {
            console.log("patched");
        });
        onWillUnmount(() => {
            console.log("willUnmount");
        });
    }

    increment() {
        this.state.count++;
    }
}

CounterComponent.template = "owl_js.CounterComponent";
registry.category("actions").add("owl_js.counter_component_tag", CounterComponent);