import { CashMovePopup } from "@point_of_sale/app/components/popups/cash_move_popup/cash_move_popup";
import { patch } from "@web/core/utils/patch";
import { user } from "@web/core/user";

patch(CashMovePopup.prototype, {
    setup() {
        super.setup();
        this.required_group = "car_rental_management_rushvi.group_car_rental_pos_manager";
        this.hasGroupAccess = false;
        this.checkGroup();
    },
    async checkGroup() {
        this.hasGroupAccess = await user.hasGroup(this.required_group);
        this.render();
    },
});