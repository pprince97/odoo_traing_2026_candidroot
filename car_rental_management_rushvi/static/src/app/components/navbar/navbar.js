import { patch } from "@web/core/utils/patch";
import { Navbar } from "@point_of_sale/app/components/navbar/navbar";
import { CashMoveListPopup } from "@point_of_sale/app/components/popups/cash_move_popup/cash_move_list_popup/cash_move_list_popup";
import { useService } from "@web/core/utils/hooks";
const { DateTime } = luxon;

patch(Navbar.prototype, {
    setup() {
        super.setup();
        this.dialog = useService("dialog");
        this.onClickMyMenu = this.onClickMyMenu.bind(this);
    },

    async onClickMyMenu() {
        const pos = this.pos;
        const cashMoves = await pos.data.call(
            "pos.session",
            "get_cash_in_out_list",
            [pos.session.id]
        );
        this.dialog.add(CashMoveListPopup, {
            cashMoves: cashMoves.map((m) => ({
                ...m,
                date: DateTime.fromSQL(m.date, { zone: "UTC" }).setZone("local"),
            })),
            partnerId:  pos.cashier?.partner_id?.[0] || pos.cashier?.id,
        });
    },
});