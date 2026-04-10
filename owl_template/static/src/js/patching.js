/** @odoo-module **/

import {patch} from "@web/core/utils/patch";
import {FormController} from "@web/views/form/form_controller";

patch(FormController.prototype, {
    setup() {
        super.setup();
        console.log("Patch is loaded");

    },
    async saveButtonClicked() {
        const modelName = this.model.root.resModel;
        const data = this.model.root.data.origin;
        const orderLine = this.model.root.data.order_line;

        let total = 0;

        // console.log(orderLine)
        orderLine.records.forEach(line => {
            // console.log(line.data.price_total)
            total += line.data.price_total
        });
        // console.log(total)

        //conso
        // if (orderLine && orderLine.length > 0) {
        //     orderLine.forEach(line => {
        //         subTotal += line.data.price_subtotal || 0;
        //     });
        // }

        if (total === 0) {
            alert("you are Not add any Product")
            return;
        }
        // console.log(subTotal)
        // console.log("111111", data);
        // console.log(modelName);

        // if(modelName === "sale.order" ){
        //     alert("you are Creating the sale Order")
        //     // return;
        // }
        if (!data || data.trim() === "") {
            alert("you are Creating the sale Order")
            return;
        }
        return super.saveButtonClicked();
    },
});
