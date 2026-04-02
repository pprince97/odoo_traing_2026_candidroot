import {Component, useState,onWillStart, onWillRender, onRendered, onMounted, onWillUpdateProps, onWillPatch, onPatched, onWillUnmount, onWillDestroy } from "@odoo/owl";
import { registry } from "@web/core/registry";
import {browser} from "@web/core/browser/browser";

class Counter extends Component{
    static template = "owl_js_practice.Counter"
    setup(){
        const savedValue = browser.localStorage.getItem("my_persistent_count");
        this.state = useState({
            count:savedValue ? parseInt(savedValue,10):0
        });

        onWillStart(()=>{
            const date = new Date;
            console.log(`The onWillStart is executed at ${date.toLocaleTimeString()}`);
        });

        onWillRender(()=>{
            const date = new Date;
            console.log(`The onWillRender is executed at ${date.toLocaleTimeString()}`);
        });

        onRendered(()=>{
            const date = new Date;
            console.log(`The onRendered is executed at ${date.toLocaleTimeString()}`);
        });

        onMounted(()=>{
            const date = new Date;
            console.log(`The onMounted is executed at ${date.toLocaleTimeString()}`);
        });

        onWillUpdateProps(()=>{
            const date = new Date;
            console.log(`The onWillUpdateProps is executed at ${date.toLocaleTimeString()}`);
        });

        onWillPatch(()=>{
            const date = new Date;
            console.log(`The onWillPatch is executed at ${date.toLocaleTimeString()}`);
        });

        onPatched(()=>{
            const date = new Date;
            console.log(`The onPatched is executed at ${date.toLocaleTimeString()}`);
        });

        onWillUnmount(()=>{
            const date = new Date;
            console.log(`The onWillUnmount is executed at ${date.toLocaleTimeString()}`);
        });

        onWillDestroy(()=>{
            const date = new Date;
            console.log(`The onWillDestroy is executed at ${date.toLocaleTimeString()}`);
        });

    }
    _update(val){
        this.state.count = val;
        browser.localStorage.setItem("my_persistent_count",this.state.count);
    }
    increment(){
       this._update(this.state.count + 1);
    }
    decrement(){
       this._update(this.state.count - 1);
    }
    reset(){
        this._update(0);
    }
}
registry.category("actions").add("owl_js_practice.counter_action", Counter);