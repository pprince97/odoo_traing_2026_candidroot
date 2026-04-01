import { Component, props} from "@odoo/owl";
import { registry } from "@web/core/registry";

export class ProductCard extends Component {
    static template = "owl_js_practice.ProductCard";
    static props = { name: String, price: Number, "image": { type: String, optional: true } , "*": true };
}
