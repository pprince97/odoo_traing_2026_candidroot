/** @odoo-module **/
import {FloorScreen} from "@pos_restaurant/app/screens/floor_screen/floor_screen";
import {onMounted, onWillUnmount, useState} from "@odoo/owl";
import {patch} from "@web/core/utils/patch";
import {ControlButtons} from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import {useService} from "@web/core/utils/hooks";
import {usePos} from "@point_of_sale/app/hooks/pos_hook";
import {CustomerDialog} from "./guest_info";
import {CustomerDetail} from "./customer_detail";
import {makeAwaitable} from "@point_of_sale/app/utils/make_awaitable_dialog";
import {PosOrder} from "@point_of_sale/app/models/pos_order";

console.log("Guest Import is Loaded ... .. ");


patch(FloorScreen.prototype, {
    setup() {
        super.setup();
        this.dialog = useService("dialog");
        this.orm = useService("orm");
        this.pos = usePos();


        this.states_info = useState({
            guests: [],
            counting: 0,
        });
    },


    async onClickTable(table, ev) {
        console.log("this.pos.config.guest_details ---->  ", this.pos.config.guest_details)
        console.log("this.pos.config.guest_details_timing ---->  ", this.pos.config.guest_details_timing)
        console.log("this.pos.config.guest_details_required ---->  ", this.pos.config.guest_details_required)
        const guest_details = this.pos.config.guest_details
        const guest_details_timing = this.pos.config.guest_details_timing

        console.log(table, "------table ")
        const test = super.onClickTable(table, ev);

        // this.pos.models['pos.order'].filter(o => !o.finalized).forEach(order => {
        //     if (!order.table_number) {
        //         if (order.table_number !== table.table_number) {
        //             // console.log(" table parent id  -- - -  - --  -",table.parent_id)
        //         }
        //     }
        //     // console.log(" table parent id  -- - -  - --  -",table.parent_id)
        // });
        // console.log(`Table number ${table.table_number} clicked!`)
        //
        // console.log("\n\n\n=========  table.is_first_time =========>", table.is_first_time)
        console.log(guest_details);

        const order = this.pos.getOrder();

        if (guest_details && guest_details_timing === 'order_before') {
            console.log("data.no_of_guest ::::>>>   ", this.pos.getOrder().no_of_guest)
            if (this.pos.getOrder().no_of_guest === undefined || this.pos.getOrder().no_of_guest === 0) {
                // if (table.is_first_time === undefined || table.is_first_time === false) {
                await makeAwaitable(this.dialog, CustomerDialog, {
                    // this.dialog.add(CustomerDialog, {
                    // We pass the function that should run when 'Save' is clicked
                    confirm: async (data) => {
                        // table.is_first_time = true

                        // const orm1 = this.env.services.orm;
                        // await orm1.write('restaurant.table', [table.id], {
                        //     is_first_time: true,
                        // });
                        // table.is_first_time = true;
                        // console.log("table ---->   ",table)
                        // console.log("is_first_time ---->   ",table.is_first_time)

                        // ORM logic now lives safely inside this callback
                        console.log("Load First Is Not Allowed")
                        console.log("data.no_of_male ::::>>>   ", data.no_of_male)
                        console.log("data.no_of_female ::::>>>   ", data.no_of_female)
                        console.log("data.no_of_guest ::::>>>   ", data.no_of_guest)
                        console.log("type of  ::::>>>   ", typeof data.no_of_guest)

                        // const order = this.pos.getOrder();
                        // order.no_of_male = parseInt(data.no_of_male) || 0
                        // order.no_of_female = parseInt(data.no_of_female) || 0
                        // order.no_of_guest = parseInt(data.no_of_guest) || 0
                        // order.customer_count = order.no_of_guest

                        // const order_id = order.id;
                        // console.log("order---1--->   ", order)
                        // console.log("order_id---1--->   ", order_id)

                        // order = await this.sendDraftOrderToServer();
                        // Force sync to the server to create a record and get a real ID
                        // await this.pos.sync_orders();
                        // console.log("serverId---1--->   ", order.id)


                        // const orm = this.env.services.orm;
                        //
                        // try {
                        //     const newIds = await orm.create("guest.count", [{
                        //         no_of_male: parseInt(data.no_of_male) || 0,
                        //         no_of_female: parseInt(data.no_of_female) || 0,
                        //         no_of_guest: parseInt(data.no_of_guest) || 0,
                        //     }]);
                        //     console.log("Created record IDs:", newIds);
                        // } catch (error) {
                        //     console.error("ORM Create Failed:", error);
                        // }

                        // console.log("Guest Count Created", order.customer_count)
                        // this.dialog.add(CustomerDetail, {
                        await makeAwaitable(this.dialog, CustomerDetail, {
                            no_of_male: data.no_of_male,
                            no_of_female: data.no_of_female,
                            no_of_guest: data.no_of_guest,
                            confirm: async (data) => {
                                console.log("data------>   ", data)

                                // const order = this.pos.getOrder();
                                console.log("data.no_of_male ::::>>>   ", data.no_of_male)
                                console.log("data.no_of_female ::::>>>   ", data.no_of_female)
                                console.log("data.no_of_guest ::::>>>   ", data.no_of_guest)

                                order.no_of_male = parseInt(data.no_of_male) || 0
                                order.no_of_female = parseInt(data.no_of_female) || 0
                                order.no_of_guest = parseInt(data.no_of_guest) || 0
                                order.customer_count = order.no_of_guest

                                const order_id = order.id;
                                console.log("order_id------>   ", order_id)
                                console.log("order_id type------>   ", typeof order_id)
                                order.guests = data.guests;
                                // this.state.guests = data.guests
                                console.log("guests------>   ", order.guests)

                                const orm = this.env.services.orm;
                                const newIds = [];
                                for (const guest of data.guests) {
                                    console.log(guest.age, guest.country, guest.gender);
                                    try {
                                        // const newIds = await orm.create("guest.detail", [{
                                        //     age: parseInt(guest.age),
                                        //     country: guest.country,
                                        //     gender: guest.gender,
                                        //     pos_order_id: order_id,
                                        // }]);
                                        const newGuest = await this.pos.models["guest.detail"].create({
                                            age: parseInt(guest.age),
                                            country: guest.country,
                                            gender: guest.gender,
                                        });
                                        console.log("Before the Push");
                                        newIds.push(newGuest.id);
                                        console.log("Created record IDs:", newIds);
                                    } catch (error) {
                                        console.error("ORM Create Failed:", error);
                                    }
                                }
                                order.guest_detail_ids = newIds;
                            }
                        })
                    },
                });
                // }
            }
            // let counting = 0
            // if(typeof order.id === "string" && this.states_info.counting === 0){
            //     console.log("\n\n\n\n\n\n\n\n\n\n\n\n\n Hello this is created order");
            //     console.log("Before counting : ",this.states_info.counting);
            //     this.states_info.counting++;
            //     console.log("After counting : ",this.states_info.counting);
            // }
        }

        return test;
    },
});


patch(PosOrder.prototype, {
    setup() {
        super.setup(...arguments);
        this.guest_detail_ids = this.guest_detail_ids || [];
    },

    toJSON() {
        const json = super.toJSON(...arguments);
        json.guest_detail_ids = this.guest_detail_ids;
        return json;
    }

});