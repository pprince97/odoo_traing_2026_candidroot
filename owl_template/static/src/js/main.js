/** @odoo-module **/

import { Component, xml, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { ProductCard } from "./product_card";
// import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";


export class Root extends Component {
    static components = { ProductCard };

    static template = xml`
        <div class="product-grid">
            <div>
                <input id="name" type="text" placeholder="product name"/>
                <input id="price" placeholder="product price"/>
                <input id="img" placeholder="product image"/>
                <button t-on-click="addProduct">Add</button>
            </div>
       
          <t t-foreach="products" t-as="p" t-key="p.id">
            <ProductCard    
                name="p.name"
                price="p.price"
                image="p.image" />
          </t>
        </div>
    `;

    nextId = 6;

    setup() {
        this.products = useState([
            { id: 1, name: "Wireless Headphones", price: 79.99, image: "🎧" },
            { id: 2, name: "Mechanical Keyboard", price: 129.99, image: "⌨️" },
            { id: 3, name: "USB-C Hub", price: 49.99, image: "📱" },
            { id: 4, name: "Webcam HD", price: 59.99, image: "📷" },
            { id: 5, name: "Laptop", price: 5560.99, image: "💻" },
        ]);

        // this.rpc = useService("rpc")
    }

    addProduct(ev) {
        if (ev.type === "click" || ev.key === "Enter") {
            const names = document.getElementById("name")
            const prices = document.getElementById("price")
            const imgs = document.getElementById("img")

            const txt1 = names.value;
            const txt2 = parseFloat(prices.value);
            const txt3 = imgs.value;

            console.log("Thik hai yaha tak!")

            if (txt1 && txt2 && txt3) {
                this.products.push({ id: this.nextId++, name: txt1, price:txt2, image: txt3 });

                rpc("/owl/save_data", {
                    name: txt1,
                    price: txt2,
                    image: txt3
                }).then((res) => {
                    console.log("Data Saved!", res)
                })
            }
            else {
                alert("Some data was missing!")
            }
        }
    }
}

registry.category("actions").add("owl_template.product_action", Root);



// import { useService } from "@web/core/utils/hooks";
//
// setup() {
//     this.orm = useService("orm");
// }
//
// async saveData(data) {
//     await this.orm.call("your.model", "create", [{
//         name: data.name,
//         field_name: data.value,
//     }]);
// }
