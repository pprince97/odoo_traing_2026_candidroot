import {Component, useState, useEffect} from "@odoo/owl";
import {registry} from "@web/core/registry";

export class ShoppingCart extends Component {
    static template = "owl_shoping_cart.ShoppingCart";

    setup() {
        this.state = useState({
            query: "",
            products: [
                {id: 1, name: "Phone", price: 500, qty: 1},
                {id: 34, name: "Laptop", price: 1200, qty: 0},
                {id: 42, name: "Headphones", price: 100, qty: 2},
                {id: 40, name: "TV", price: 700, qty: 1},
            ],
        });

        useEffect(() => {
            console.log("Total updated:", this.total);
        });
    }

    get filteredProducts() {
        const q = this.state.query.toLowerCase();
        return this.state.products.filter((p) =>
            p.name.toLowerCase().includes(q)
        );
    }

    get total() {
        return this.state.products.reduce((sum, p) => {
            return sum + p.price * p.qty;
        }, 0);
    }

    // increase(product, increment) {
    //     product.qty += increment;
    // }
    increase(product, increment) {
        product.qty += increment;
    }

    decrease(product, decrease) {
        if (product.qty > 0) {
            product.qty -= decrease;
        } else {
            // To access the Close button element
            let closebtn = document.getElementById("closebtn");

            // To acces the popup element
            let popup = document.querySelector(".popup");
            popup.style.display = "block";


            closebtn.addEventListener("click", () => {
                popup.style.display = "none";

            });
            // alert("Number is Zero")
        }
    }
}

registry.category("actions").add(
    "owl_shoping_cart.counter_action",
    ShoppingCart
);