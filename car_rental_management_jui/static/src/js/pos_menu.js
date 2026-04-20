import { PosStore } from "@point_of_sale/app/services/pos_store";
import { patch } from "@web/core/utils/patch";
import { CashMoveListPopup } from "@point_of_sale/app/components/popups/cash_move_popup/cash_move_list_popup/cash_move_list_popup";
const { DateTime } = luxon;

patch(PosStore.prototype, {
    setup() {
        super.setup(...arguments);
    },
    async cashMoveDetails(){
        const dialogService = this.env.services.dialog;
        const cashMoves = await this.data.call("pos.session", "get_cash_in_out_list", [
            this.session.id,
        ]);
        dialogService.add(CashMoveListPopup, {
            cashMoves: cashMoves.map((m) => ({
                ...m,
                date: DateTime.fromSQL(m.date, { zone: "UTC" }).setZone("local"),
            })),
            partnerId: this.user.partner_id.id,
        });
    }
});