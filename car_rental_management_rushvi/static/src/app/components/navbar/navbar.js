// import { patch } from "@web/core/utils/patch";
// import { Navbar } from "@point_of_sale/app/components/navbar/navbar";
//
// patch(Navbar.prototype, {
//     setup() {
//         super.setup();
//     },
//
//     async onClickMyMenu() {
//         console.log("CLICKEDDDDDDDDDD")
//     },
// });
//
// /** @odoo-module **/

import {Navbar} from "@point_of_sale/app/components/navbar/navbar";
import { patch } from "@web/core/utils/patch";
import { CashMoveListPopup } from "@point_of_sale/app/components/popups/cash_move_popup/cash_move_popup";
import { useService } from "@web/core/utils/hooks";

patch(Navbar.prototype, {
    setup() {
        super.setup();
        this.pos = null;
        this.dialog = useService("dialog");
        // this._initPos();
    },

    // _initPos() {
    //     const interval = setInterval(() => {
    //         if (this.env?.services?.pos || this.__owl__.app?.pos) {
    //             this.pos = this.env.services.pos || this.__owl__.app.pos;
    //             clearInterval(interval);
    //         }
    //     }, 200);
    // },
    //
    // async onClickMyMenu() {
    //     if (!this.pos) {
    //         console.warn("POS still not initialized");
    //         return;
    //     }
    //     const cashMoves = await this.pos.data.call(
    //         "pos.session",
    //         "get_cash_in_out_list",
    //         [this.pos.session.id]
    //     );
    //     this.dialog.add(CashMoveListPopup, {
    //         cashMoves,
    //         partnerId: null,
    //     });
    // },
});