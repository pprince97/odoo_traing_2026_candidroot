/** @odoo-module **/
import {FloorScreen} from "@pos_restaurant/app/screens/floor_screen/floor_screen";
import {onMounted, onWillUnmount, useState} from "@odoo/owl";
import {patch} from "@web/core/utils/patch";
import {ControlButtons} from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import {useService} from "@web/core/utils/hooks";
import {usePos} from "@point_of_sale/app/hooks/pos_hook";
import {CustomerDialog} from "./guest_info";
import {CustomerDetail} from "./customer_detail";
import { makeAwaitable} from "@point_of_sale/app/utils/make_awaitable_dialog";

console.log("Guest Import is Loaded ... .. ");


patch(FloorScreen.prototype, {
    setup() {
        super.setup();
        this.dialog = useService("dialog");
        this.orm = useService("orm");
        this.pos = usePos();

        onWillUnmount(() => {

        });
    },


    async onClickTable(table, ev) {

        if (table.is_first_time === undefined || table.is_first_time === false) {

            const guestData = await makeAwaitable(this.dialog, CustomerDialog);
            console.log(guestData, "guest");

            // const order = this.pos.getOrder();
            //
            // order.no_of_male = parseInt(guestData.no_of_male) || 0;
            // order.no_of_female = parseInt(guestData.no_of_female) || 0;
            // order.no_of_guest = parseInt(guestData.no_of_guest) || 0;
            //
            // const customerDetails = await makeAwaitable(this.dialog, CustomerDetail, {
            //     no_of_guest: order.no_of_guest,
            // });
            //
            // console.log("Customer Details:", customerDetails);
            //
            // table.is_first_time = true;
        }

        return super.onClickTable(table, ev);
    }
});