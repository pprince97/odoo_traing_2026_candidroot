//
// import {CashMovePopup} from "@point_of_sale/app/components/popups/cash_move_popup/cash_move_popup";
// import { ClosePosPopup } from "@point_of_sale/app/components/popups/closing_popup/closing_popup";
// import {patch} from "@web/core/utils/patch";
// patch(CashMovePopup.prototype, {
//     setup() {
//         super.setup();
//     },
//
//     async openDetails() {
//         console.log("--------------------------------1-11-11--2--3-3")
//         return await super.openDetails();
//     }
// });


// import { patch } from "@web/core/utils/patch";
//
// patch(Navbar.prototype, {
//     openDetails() {
//         console.log("Button clicked!");
//         // Your logic here (e.g., opening a popup)
//         return super.openDetails();
//     },
// });


// import { Navbar } from "@point_of_sale/app/navbar/navbar";
/** @odoo-module **/
import { Navbar } from "@point_of_sale/app/components/navbar/navbar";
import { CashMovePopup } from "@point_of_sale/app/components/popups/cash_move_popup/cash_move_popup";
import { CashMoveListPopup } from "@point_of_sale/app/components/popups/cash_move_popup/cash_move_list_popup/cash_move_list_popup";

import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";// Use the service hook

patch(Navbar.prototype, {
    setup() {
        super.setup();
        this.pos = useService("pos");
    },

    async openDetails() {
        console.log("Fetching cash history...");
        const DateTime = luxon.DateTime;

        const cashMoves = await this.pos.data.call("pos.session", "get_cash_in_out_list", [
            this.pos.session.id,
        ]);

        this.dialog.add(CashMoveListPopup, {
            cashMoves: cashMoves.map((m) => ({
                ...m,

                date: DateTime.fromSQL(m.date, { zone: "UTC" }).setZone(this.pos.user.tz || "local"),
            })),

            partnerId: this.partnerId || this.pos.company.id,
        });
    },

});



