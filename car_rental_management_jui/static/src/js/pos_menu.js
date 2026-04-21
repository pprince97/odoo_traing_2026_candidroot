import { PosStore } from "@point_of_sale/app/services/pos_store";
import { patch } from "@web/core/utils/patch";
import { CashMoveListPopup } from "@point_of_sale/app/components/popups/cash_move_popup/cash_move_list_popup/cash_move_list_popup";
import { user } from "@web/core/user";
const { DateTime } = luxon;

patch(PosStore.prototype, {
    setup() {
        super.setup(...arguments);
    },
    get isCashManager() {
        user.hasGroup("car_rental_management_jui.group_pos_cash_manager")
        .then(result => {
            this.cashManager = result;
        });
        return this.cashManager;
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