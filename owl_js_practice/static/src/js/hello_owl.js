import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

class Root extends Component {
    static template = "owl_js_practice.Root";

    setup(){
        this.state = useState({
            appName:'Owl!!'
        });
    }
}
registry.category("actions").add("owl_js_practice.practice_action", Root);
