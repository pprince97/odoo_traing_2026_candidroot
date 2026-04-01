import { Component, xml } from "@odoo/owl";
import { ProductCard } from "./product_card";
import { registry } from "@web/core/registry";

class Root extends Component {
  static components = { ProductCard };

  static template = xml`
    <div class="container">
        <div class="product-grid">
          <t t-foreach="this.products" t-as="p" t-key="p.id">
            <ProductCard t-props="p"/>
          </t>
        </div>
        <a href="https://odoo.com" class="btn btn-primary">odoo</a>
    </div>
  `;

  products = [
    { id: 1, name: "Wireless Headphones", price: 79.99, image: "🎧" },
    { id: 2, name: "Mechanical Keyboard", price: 129.99, image: "⌨️" },
    { id: 3, name: "USB-C Hub", price: 49.99 },
    { id: 4, name: "Webcam HD", price: 59.99, image: "📷" },
  ];
}

registry.category("actions").add("owl_template1.counter_action", Root);