/** @odoo-module **/

import { Component } from "@odoo/owl";

export class ProductCard extends Component {
    static template = "owl_template.ProductCard";

    static props = {
        name: String,
        price: Number,
        image: { type: String, optional: true },
    };
}