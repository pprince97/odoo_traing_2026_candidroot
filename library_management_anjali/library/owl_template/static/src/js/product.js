import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class ProductCard extends Component {
    static template = "owl_template.ProductCard";
    static props = {
        name: String,
        price: Number,
        image: { type: String, optional: true },
    };
}

export class ProductViewer extends Component {
    static components = { ProductCard };
    static template = "owl_template.ProductViewer";

    setup() {
        this.state = useState({
            searchQuery: "",
            products: [
                { id: 1, name: "Wireless Headphones", price: 79.99, image: "🎧" },
                { id: 2, name: "Mechanical Keyboard", price: 129.99, image: "⌨️" },
                { id: 3, name: "USB-C Hub", price: 49.99 },
                { id: 4, name: "Webcam HD", price: 59.99, image: "📷" },
                { id: 5, name: "Phone", price: 99.99, image: "📱" },
                { id: 6, name: "Laptop", price: 199.99, image: "💻" },
            ],
        });
    }

    get filteredProducts() {
        const query = this.state.searchQuery.toLowerCase();
        return this.state.products.filter(p =>
            p.name.toLowerCase().includes(query)
        );
    }
}

registry.category("actions").add("owl_template.product_action", ProductViewer);
