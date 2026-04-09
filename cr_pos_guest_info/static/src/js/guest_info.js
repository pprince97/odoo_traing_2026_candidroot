/** @odoo-module **/
import {FloorScreen} from "@pos_restaurant/app/screens/floor_screen/floor_screen";
import {patch} from "@web/core/utils/patch";
import {GuestNumber} from "./guest_info_outer"
import {useService} from "@web/core/utils/hooks";

patch(FloorScreen.prototype, {
    setup() {
        super.setup();
        this.dialogService = useService("dialog");
    },

    async onClickTable(table) {
       this.dialogService.add(GuestNumber, {
            title: "Guest",
        });
        await super.onClickTable(table);
    },
});