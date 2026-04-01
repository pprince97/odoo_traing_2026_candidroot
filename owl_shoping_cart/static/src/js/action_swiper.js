/** @odoo-module **/
import {registry} from "@web/core/registry";
import {Component, useState, xml} from "@odoo/owl";
// import { ActionSwiper } from "@web/core/action_swiper/action_swiper";
import {Dropdown} from "@web/core/dropdown/dropdown";
import {DropdownItem} from "@web/core/dropdown/dropdown_item";
import {ShoppingCart} from "./shopping_cart";

export class Counter extends Component {
    static props = ["*"];
    static components = {Dropdown, DropdownItem};
    static template = xml`
                    <div class="d-flex">
                        <Dropdown>
  <!-- The content of the "default" slot is the component's toggle -->
  <button class="my-btn" type="button">
    Click me to toggle the dropdown menu!
  </button>

  <!-- The "content" slot is rendered inside the menu that pops up next to the toggle -->
  <t t-set-slot="content">
    <DropdownItem onSelected="selectItem1">Menu Item 1</DropdownItem>
    <DropdownItem onSelected="selectItem2">Menu Item 2</DropdownItem>
  </t>
</Dropdown>
                    </div>
                `;

}

registry.category("actions").add(
    "owl_shoping_cart.action_swiper",
    Counter
);
