/** @odoo-module **/

import {registry} from "@web/core/registry";
import {Component, useState} from "@odoo/owl";

class MyClientAction extends Component {
    setup() {
        this.state = useState({
            products: [
                {id: 1, name: "Wireless Headphones", price: 79.99, qty: 1, image: "🎧"},
                {id: 2, name: "Mechanical Keyboard", price: 129.99, qty: 1, image: "⌨️"},
                {id: 3, name: "USB-C Hub", price: 49.99, qty: 1, image: "🔌"},
                {id: 4, name: "Webcam HD", price: 59.99, qty: 1, image: "📷"},
                // {id: 5, name: "Bluetooth Speaker", price: 39.99, qty: 1, image: "🔊"},
                // {id: 6, name: "Smart Watch", price: 149.99, qty: 1, image: "⌚"},
                // {id: 7, name: "Gaming Mouse", price: 29.99, qty: 1, image: "🖱️"},
                // {id: 8, name: "Laptop Stand", price: 24.99, qty: 1, image: "💻"},
                // {id: 9, name: "External Hard Drive", price: 89.99, qty: 1, image: "💾"},
                // {id: 10, name: "Portable Charger", price: 19.99, qty: 1, image: "🔋"},
                // {id: 11, name: "LED Monitor", price: 199.99, qty: 1, image: "🖥️"},
                // {id: 12, name: "Desk Lamp", price: 14.99, qty: 1, image: "💡"},
                // {id: 13, name: "Office Chair", price: 249.99, qty: 1, image: "🪑"},
                // {id: 14, name: "Tablet", price: 299.99, qty: 1, image: "📱"},
                // {id: 15, name: "Router", price: 59.99, qty: 1, image: "📡"},
                // {id: 16, name: "Microphone", price: 79.99, qty: 1, image: "🎤"},
                // {id: 17, name: "Graphics Tablet", price: 129.99, qty: 1, image: "✏️"},
                // {id: 18, name: "VR Headset", price: 399.99, qty: 1, image: "🥽"},
                // {id: 19, name: "Smart TV Stick", price: 49.99, qty: 1, image: "📺"},
            ]
        });
    }

    increaseQty(product) {
        product.qty++;
    }

    decreaseQty(product) {
        if (product.qty > 1) {
            product.qty--;
        }
    }

    getTotal(product) {
        return (product.price * product.qty).toFixed(2);
    }
}

MyClientAction.template = "my_module.MyClientActionTemplate";

registry.category("actions").add("my_client_action", MyClientAction);