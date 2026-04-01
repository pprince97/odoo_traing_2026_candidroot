import {Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import {browser} from "@web/core/browser/browser"

class Counter extends Component{
    static template = "owl_js_practice.Counter"
    setup(){
        const savedValue = browser.localStorage.getItem("my_persistent_count");
        this.state = useState({
            count:savedValue ? parseInt(savedValue,10):0
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