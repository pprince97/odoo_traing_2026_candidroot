/** @odoo-module */

import {patch} from "@web/core/utils/patch"
import {useService} from "@web/core/utils/hooks";
import {GuestOuterInfo} from "./guest_outer_info";
import {GuestInnerInfo} from "./guest_inner_info";
import {makeAwaitable} from "@point_of_sale/app/utils/make_awaitable_dialog";
import {usePos} from "@point_of_sale/app/hooks/pos_hook";
import {PaymentScreen} from "@point_of_sale/app/screens/payment_screen/payment_screen";


patch(PaymentScreen.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
        this.dialog = useService("dialog");
        this.orm = useService("orm");
    },

    async validateOrder(force) {
        const config = this.pos.config;

        const guest_detail = config.guest_details;
        const guest_required = config.guest_details_required;
        const guest_timing = config.guest_details_timing;

        if (guest_detail && guest_timing === "order_after") {
            await makeAwaitable(this.dialog, GuestOuterInfo, {
                title: "No of Guest",

                confirm: async (guestCounts) => {
                    const order = this.pos.getOrder();

                    order.no_of_male = guestCounts.no_of_male;
                    order.no_of_female = guestCounts.no_of_female;
                    order.no_of_total = guestCounts.no_of_total;

                    await makeAwaitable(this.dialog, GuestInnerInfo, {
                        title: "Guest Details",
                        totalGuests: guestCounts.no_of_total,

                        next: async (guests) => {
                            const order = this.pos.getOrder();

                            order.guest_ids = guests.map(guest => ({
                                age: guest.age,
                                nationality: guest.nationality,
                                gender: guest.gender,
                            }));

                            const orm = this.env.services.orm;
                            for (const guest in order.guest_ids) {
                                try {
                                    const newIds = await orm.create("pos.order.guest", [{
                                        age: parseInt(order.guest_ids.map(rec => rec.age)[guest]),
                                        nationality: order.guest_ids.map(rec => rec.nationality)[guest],
                                        gender: order.guest_ids.map(rec => rec.gender)[guest],
                                        order_id: order.id,
                                    }]);
                                    console.log("Created record IDs:", newIds);
                                } catch (error) {
                                    console.error("ORM Create Failed:", error);
                                }
                            }
                        }
                    });
                }
            });
        }
        await super.validateOrder(...arguments);
    }
});