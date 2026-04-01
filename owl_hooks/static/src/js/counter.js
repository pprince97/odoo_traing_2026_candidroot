import { Component, useState, onMounted, onWillUnmount,onWillDestroy,onWillStart,onWillRender,onRendered,onWillPatch,onPatched} from "@odoo/owl";
import { registry } from "@web/core/registry";

export class Counter extends Component {
    static template = "owl_hooks.Counter"
    setup() {
        console.log("setupppp",new Date().toLocaleTimeString())
        this.state = useState({ value: 0 });

        onWillStart(()=>{
            console.log("on will start",new Date().toLocaleTimeString())
        })

        onWillRender(()=>{
            console.log("on will renderrr",new Date().toLocaleTimeString())
        });

        onRendered(()=>{
            console.log("on renderrrrr",new Date().toLocaleTimeString())
        });

        onMounted(() => {
            console.log("Counter mounted at:", new Date().toLocaleTimeString());
        });
        //
        onWillUnmount(() => {
            console.log("Counter is being removed.",new Date().toLocaleTimeString());
        });

        onWillDestroy(()=>{
            console.log("on will destroyyyyy!",new Date().toLocaleTimeString())
        });

        onWillPatch(()=>{
            console.log("on will patch",new Date().toLocaleTimeString())
        })

        onPatched(()=>{
            console.log("on patcheddd",new Date().toLocaleTimeString())
        })
    }

    increment() {
        this.state.value++;
    }

    decrement() {
        this.state.value--;
    }

    reset() {
        this.state.value = 0;
    }
}

registry.category("actions").add("owl_hooks.my_counter_action", Counter);