/** @odoo-module **/
import {
    Component,
    useState,
    onWillStart,
    onWillRender,
    onRendered,
    onMounted,
    onWillUpdateProps,
    onWillPatch,
    onPatched,
    onWillUnmount,
    onWillDestroy,
} from "@odoo/owl";

import { registry } from "@web/core/registry";

export class FullLifecycleExample extends Component {
    static template = "lifecycle_full.Template";

    setup() {
        console.log("1. setup");

        this.state = useState({ count: 0 });

        onWillStart(() => {
            console.log("2. onWillStart");
        });

        onWillRender(() => {
            console.log("3. onWillRender");
        });

        onRendered(() => {
            console.log("4. onRendered");
        });

        onMounted(() => {
            console.log("5. onMounted");
        });

        onWillUpdateProps(() => {
            console.log("6. onWillUpdateProps");
        });

        onWillPatch(() => {
            console.log("7. onWillPatch");
        });

        onPatched(() => {
            console.log("8. onPatched");
        });

        onWillUnmount(() => {
            console.log("9. onWillUnmount");
        });

        onWillDestroy(() => {
            console.log("10. onWillDestroy");
        });
    }

    increment() {
        this.state.count++;
    }
}

// Register Client Action
registry.category("actions").add("lifecycle_full_action", FullLifecycleExample);