
/** @odoo-module **/
import { onWillStart, useState } from "@odoo/owl";
import { Navbar } from "@point_of_sale/app/components/navbar/navbar";
import { CashMovePopup } from "@point_of_sale/app/components/popups/cash_move_popup/cash_move_popup";
import { CashMoveListPopup } from "@point_of_sale/app/components/popups/cash_move_popup/cash_move_list_popup/cash_move_list_popup";

import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { user } from "@web/core/user";
import { Dialog } from "@web/core/dialog/dialog";// Use the service hook

patch(Navbar.prototype, {
    setup() {
        super.setup();
        this.pos = useService("pos");
        this.dialog = useService("dialog");
        this.state = useState({ canSeeHistory: false });

        onWillStart(async () => {
            // Replace with your actual module and group ID
            this.state.canSeeHistory = await user.hasGroup("car_rental_sankit.group_rental_manager");
            console.log("this.canSeeHistory ----> ",this.state.canSeeHistory)
        });
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



