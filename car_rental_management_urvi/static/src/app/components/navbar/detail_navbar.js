import {Navbar} from "@point_of_sale/app/components/navbar/navbar";
import {patch} from "@web/core/utils/patch";
import {useService} from "@web/core/utils/hooks";
import {
    CashMoveListPopup
} from "@point_of_sale/app/components/popups/cash_move_popup/cash_move_list_popup/cash_move_list_popup";
import {DateTime} from "@web/core/l10n/dates";
import { user } from "@web/core/user";
import {onWillStart} from "@odoo/owl";


patch(Navbar.prototype, {
    setup() {
        super.setup();
        this.dialog = useService("dialog");
        this.stateu = { hasDetailGroup: false };
        onWillStart(async () => {
            this.stateu.hasDetailGroup = await user.hasGroup("car_rental_management_urvi.group_sm");
        });
    },

    async openDetails_bar() {
        console.log("Opening details...");

        const cashMoves = await this.pos.data.call(
            "pos.session",
            "get_cash_in_out_list",
            [this.pos.session.id]
        );

        this.dialog.add(CashMoveListPopup, {
            cashMoves: cashMoves.map((m) => ({
                ...m,
                date: DateTime.fromSQL(m.date, {zone: "UTC"}).setZone("local"),
            })),
            partnerId: this.pos.cashier.partner_id[0] || this.pos.cashier.id,
        });
    },
});
