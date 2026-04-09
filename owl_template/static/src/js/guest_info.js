/** @odoo-module */

import {patch} from "@web/core/utils/patch"
import {useService} from "@web/core/utils/hooks";
import {FloorScreen} from "@pos_restaurant/app/screens/floor_screen/floor_screen";
import {GuestOuterInfo} from "./guest_outer_info";
import {GuestInnerInfo} from "./guest_inner_info";
import {makeAwaitable} from "@point_of_sale/app/utils/make_awaitable_dialog";


patch(FloorScreen.prototype, {
    setup() {
        super.setup();
        this.state.no_of_male = 0;
        this.state.no_of_female = 0;
        this.state.no_of_total = 0;

        this.state.age = 0;
        this.state.nationality = "Indian";
        this.state.gender = "";

        // this.dialogService = useService("dialog");
        this.dialog = useService("dialog");
    },

    async onClickTable(table) {
        console.log(this.pos.config);
        console.log("Guest details  =>", this.pos.config.guest_details);
        console.log("Guest details Required =>", this.pos.config.guest_details_required);
        console.log("Guest details Timing =>", this.pos.config.guest_details_timing);

        const guest_detail = this.pos.config.guest_details;
        const guest_required = this.pos.config.guest_details_required;
        const guest_timing = this.pos.config.guest_details_timimng;

        await makeAwaitable(this.dialog, GuestOuterInfo, {
            title: "No of Guest",

            confirm: async (guestCounts) => {
                await makeAwaitable(this.dialog, GuestInnerInfo, {
                    title: "Guest Details",
                    totalGuests: guestCounts.no_of_total,
                });
            }
        });

    }
});
