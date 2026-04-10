import {ReceiptScreen} from "@point_of_sale/app/screens/receipt_screen/receipt_screen";
import {patch} from "@web/core/utils/patch";
import {useService} from "@web/core/utils/hooks";
import {usePos} from "@point_of_sale/app/hooks/pos_hook";
import {onWillUnmount} from "@odoo/owl";


patch(ReceiptScreen.prototype, {
    setup() {
        super.setup();
        this.dialog = useService("dialog");
        this.orm = useService("orm");
        this.pos = usePos();

    },

    async isContinueSplitting() {

        // Call the original orderDone first
        const order = this.currentOrder;
        const table = order?.table_id;

        // const table = order ? order.table : null;
        console.log("--------1-1-------", table)
        const result = await super.isContinueSplitting(...arguments);

        if (table && table.is_first_time) {
            try {
                console.log("-------table.is_first_time-------", table.is_first_time)
                const orm1 = this.env.services.orm;
                // In PosStore, the orm service is available on 'this.orm'
                await orm1.write("restaurant.table", [table.id], {
                    is_first_time: false,
                });

                // Update local cache
                table.is_first_time = false;
                console.log(`Table ${table.table_number} reset for next guest.`);
            } catch (error) {
                console.error("Failed to reset table status in PosStore:", error);
            }
        }

        return result;
    },
});
