/** @odoo-module **/
// import OrderPaymentValidation from "@point_of_sale/app/utils/order_payment_validation";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import {onMounted, onWillUnmount, useState} from "@odoo/owl";
import {patch} from "@web/core/utils/patch";
import {ControlButtons} from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import {useService} from "@web/core/utils/hooks";
import {usePos} from "@point_of_sale/app/hooks/pos_hook";
import {CustomerDialog} from "./guest_info";
import {CustomerDetail, CustomerDetailRequired} from "./customer_detail";
import {makeAwaitable} from "@point_of_sale/app/utils/make_awaitable_dialog";

console.log("Guest Import is Loaded ... .. ");


patch(PaymentScreen.prototype, {
    setup() {
        super.setup();
        this.dialog = this.env.services.dialog;
        this.orm = this.env.services.orm;
        this.pos =  usePos();
        console.log("--- set up done ----")

        this.states_info = useState({
            guests: [],
            counting : 0,
        });

        onWillUnmount(() => {

        });
    },


    async validateOrder(isForceValidate = false) {
        console.log("validateOrder ---->  ")
        console.log("this.pos.config.guest_details ---->  ", this.pos.config.guest_details)
        console.log("this.pos.config.guest_details_timing ---->  ", this.pos.config.guest_details_timing)
        console.log("this.pos.config.guest_details_required ---->  ", this.pos.config.guest_details_required)
        const guest_details = this.pos.config.guest_details
        const guest_details_timing = this.pos.config.guest_details_timing
        const guest_details_required = this.pos.config.guest_details_required
        console.log("guest_details_required ----- >   ",guest_details_required);

        const order = this.pos.getOrder();

        if (guest_details && guest_details_timing === 'order_after') {
            console.log("data.no_of_guest ::::>>>   ", this.pos.getOrder().no_of_guest)
            if (this.pos.getOrder().no_of_guest === undefined || this.pos.getOrder().no_of_guest === 0) {
                // if (table.is_first_time === undefined || table.is_first_time === false) {
                await makeAwaitable(this.dialog, CustomerDialog, {
                    confirm: async (data) => {

                        // ORM logic now lives safely inside this callback
                        console.log("Load First Is Not Allowed")
                        console.log("data.no_of_male ::::>>>   ", data.no_of_male)
                        console.log("data.no_of_female ::::>>>   ", data.no_of_female)
                        console.log("data.no_of_guest ::::>>>   ", data.no_of_guest)
                        console.log("type of  ::::>>>   ", typeof data.no_of_guest)
                        if (guest_details_required === false) {
                            await makeAwaitable(this.dialog, CustomerDetail, {
                                no_of_male: data.no_of_male,
                                no_of_female: data.no_of_female,
                                no_of_guest: data.no_of_guest,
                                confirm: async (data) => {
                                    console.log("this is CustomerDetail------>   ", data)

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
                                    for (const guest of data.guests) {
                                        console.log(guest.age, guest.country, guest.gender);
                                        try {
                                            const newIds = await orm.create("guest.detail", [{
                                                age: parseInt(guest.age),
                                                country: guest.country,
                                                gender: guest.gender,
                                                pos_order_id: order_id,
                                            }]);
                                            console.log("Created record IDs:", newIds);
                                        } catch (error) {
                                            console.error("ORM Create Failed:", error);
                                        }
                                    }
                                }
                            })
                        }
                        else{
                            await makeAwaitable(this.dialog, CustomerDetailRequired, {
                                required: true,
                                no_of_male: data.no_of_male,
                                no_of_female: data.no_of_female,
                                no_of_guest: data.no_of_guest,
                                confirm: async (data) => {
                                    console.log("this is CustomerDetailRequired ------>   ", data)

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
                                    for (const guest of data.guests) {
                                        console.log(guest.age, guest.country, guest.gender);
                                        try {
                                            const newIds = await orm.create("guest.detail", [{
                                                age: parseInt(guest.age),
                                                country: guest.country,
                                                gender: guest.gender,
                                                pos_order_id: order_id,
                                            }]);
                                            console.log("Created record IDs:", newIds);
                                        } catch (error) {
                                            console.error("ORM Create Failed:", error);
                                        }
                                    }
                                }
                            })
                        }
                    },
                });
                // }
            }
        }

        // return test;
        return await super.validateOrder(...arguments);
    },
});