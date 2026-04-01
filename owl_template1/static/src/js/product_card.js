import { Component, xml } from "@odoo/owl";

export class ProductCard extends Component {
  static template = xml`
    <div class="product-card">
      <span class="product-image" t-out="props.image || '📦'"/>
      <div class="product-info">
        <span class="product-name" t-out="props.name"/>
        <span class="product-price">
          $<t t-out="props.price.toFixed(2)"/>
        </span>
      </div>
    </div>
  `;

  static props = {
    id: {type: Number},
    name: { type: String },
    price: { type: Number },
    image: { type: String, optional: true },
  };

}