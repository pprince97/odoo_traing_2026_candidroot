/** @odoo-module **/

import {patch} from "@web/core/utils/patch";
import {FormController} from "@web/views/form/form_controller";

patch(FormController.prototype, {
    setup() {
        super.setup();
        console.log("Patch setup is loaded");
        document.addEventListener("click", this.onClose);
    },
    //
    onClose() {
        let closebtn = document.getElementById("closebtn");
        if (!closebtn) {return}
        let popup = document.querySelector(".popup");
        popup.style.display = "none";

                // console.log("popup : ",popup)
                // popup.style.display = "block";
                // closebtn.addEventListener("click", () => {
                //     popup.style.display = "none";
                //     console.log("click : ")
                // });
    },

    // async saveButtonClicked() {
    //     console.log("Custom Save called");
    //     const modelName = this.model.root.resModel;
    //     console.log("Method name is :", modelName);
    //     console.log("Total Price is  :", this.model.root.data.sale_order_template_id);
    //     const lines = this.model.root.data.order_line || [];
    //
    //     const subtotals = lines.records.map(record => record.data.price_subtotal);
    //     const totalSum = subtotals.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
    //
    //
    //     // Log all subtotals
    //     console.log(subtotals);
    //     console.log(totalSum);
    //
    //     console.log("lines", lines);
    //     console.log("lines records ", lines.records);
    //     // Apply only to service.category
    //     if (modelName === "sale.order") {
    //         // if (!this.model.root.data.order_line) {
    //         //     alert("Name is required!");
    //         //     return; // Stop saving
    //         // }
    //          if (totalSum === 0.0) {
    //              let popup = document.querySelector(".popup");
    //             popup.style.display = "block";
    //              // alert("Total Amount is Zero");
    //              return; // Stop saving
    //         }
    //     }
    //
    //     // Call the original save
    //     return super.saveButtonClicked();
    // },

});