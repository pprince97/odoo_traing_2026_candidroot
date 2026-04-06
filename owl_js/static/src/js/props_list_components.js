/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, xml } from "@odoo/owl";

class ProductCard extends Component {
    static props = ["name", "price", "image"];

    static template = xml`
        <div class="card">
            <div class="row">
                <div class="col-4">
                    <t t-esc="props.image"/>
                </div>
                <div class="col-8">
                    <h3><t t-esc="props.name"/></h3>
                    <p>₹ <t t-esc="props.price"/></p>
                </div>
            </div>
        </div>
    `;
}

class Root extends Component {
    static components = { ProductCard };

    static template = xml`
        <div class="product-grid">
            <t t-foreach="products" t-as="p" t-key="p.id">
                <ProductCard 
                    name="p.name" 
                    price="p.price" 
                    image="p.image"
                />
                <ProductCard 
                    name="p.name" 
                    price="p.price" 
                    image="p.image"
                />
            </t>
        </div>
    `;

    setup() {
        this.products = [
            { id: 1, name: "Wireless Headphones", price: 79.99, image: "🎧" },
            { id: 2, name: "Mechanical Keyboard", price: 129.99, image: "⌨" },
            { id: 3, name: "USB-C Hub", price: 49.99, image: "" },
            { id: 4, name: "Webcam HD", price: 59.99, image: "📷" },
            { id: 5, name: "Phone", price: 100, image: "📱" },
        ];
    }
}
registry.category("actions").add("owl_js.props_action", Root);