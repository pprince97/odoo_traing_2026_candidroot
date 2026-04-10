/** @odoo-module **/

import {FloorScreen} from "@pos_restaurant/app/screens/floor_screen/floor_screen";
import {patch} from "@web/core/utils/patch";
import {useService} from "@web/core/utils/hooks";
import {GuestNumber} from "./guest_info_outer";
import {GuestDetails} from "./guest_info_inner";

patch(FloorScreen.prototype, {
    setup() {
        super.setup();
        this.dialogService = useService("dialog");
    },

    async onClickTable(table) {
        console.log("STEP 1");
        this.dialogService.add(GuestNumber, {
            title: "Guest Number",
            next: async (data) => {
                console.log("STEP 2 (CONFIRMED)", data);

                const detailsResult = await this.dialogService.add(GuestDetails, {
                    title: "Guest Details",
                    customers: Array.from(
                        {length: data.total},
                        () => ({
                            age: "",
                            nationality: "",
                            gender: "",
                        })
                    ),
                });

                console.log("STEP 3", detailsResult);
            },
        });
        return super.onClickTable(table);
    },

});