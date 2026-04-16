import { CashMovePopup } from "@point_of_sale/app/components/popups/cash_move_popup/cash_move_popup";
import { CashMoveListPopup } from "@point_of_sale/app/components/popups/cash_move_popup/cash_move_list_popup/cash_move_list_popup";
import { patch } from "@web/core/utils/patch";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";


patch(CashMovePopup.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
        this.dialog = useService("dialog");
    },

    get partnerId() {
        return this.pos.user.partner_id.id;
    },

    async openMoneyList() {
        console.log("+==========================> ", this.pos.session.id);
        const cashMoves = await this.pos.data.call("pos.session", "get_cash_in_out_list", [
            this.pos.session.id,
        ]);
        this.dialog.add(CashMoveListPopup, {
            cashMoves: cashMoves.map((m) => ({
                ...m,
                date: DateTime.fromSQL(m.date, { zone: "UTC" }).setZone("local"),
            })),
            partnerId: this.partnerId,
        });
        return await super.openDetails();
    }
});


    // async openDetails() {
    //     const cashMoves = await this.pos.data.call("pos.session", "get_cash_in_out_list", [
    //         this.pos.session.id,
    //     ]);
    //     this.dialog.add(CashMoveListPopup, {
    //         cashMoves: cashMoves.map((m) => ({
    //             ...m,
    //             date: DateTime.fromSQL(m.date, { zone: "UTC" }).setZone("local"),
    //         })),
    //         partnerId: this.partnerId,
    //     });
    // }