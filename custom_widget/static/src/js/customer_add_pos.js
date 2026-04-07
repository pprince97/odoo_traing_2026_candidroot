/** @odoo-module **/
console.log("Add POS loaded.");
import {patch} from "@web/core/utils/patch";
import {ControlButtons} from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import {useService} from "@web/core/utils/hooks";
import {CustomerDialog} from "./customer_popup";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";

console.log("Add POS  loaded sucess ");

patch(ControlButtons.prototype, {
    setup() {
        super.setup();
        this.dialog = useService("dialog");
        this.orm = useService("orm");
        this.pos = usePos();
        console.log("Setup file loaded.");
    },

    async onClickCustomer() {
        this.dialog.add(CustomerDialog, {
            // We pass the function that should run when 'Save' is clicked
            confirm: async (data) => {
                // ORM logic now lives safely inside this callback
                console.log("Load First Is Not Allowed")
                // await this.orm.create("res.partner", [{
                //     name: data.name,
                //     phone: data.phone,
                //     street: data.street,
                // }]);

                const order = this.pos.getOrder();
                order.general_customer_note += "\n" +data.name +"\n" +data.phone+"\n"+data.phone
                console.log(order.general_customer_note)


                // const [partner] = await this.orm.read("res.partner", [partner_id], ["name"]);
                //
                // // Set the partner in the POS order
                // const order = this.pos.get_order();
                // if (order) {
                //     order.set_partner(partner);
                // }
            },
        });
    },
});