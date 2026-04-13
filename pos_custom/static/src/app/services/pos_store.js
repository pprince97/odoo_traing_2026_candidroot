import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { PosStore } from "@point_of_sale/app/services/pos_store";
import { patch } from "@web/core/utils/patch";
import { AddGuestNumberDetailsPopup } from "@pos_custom/app/components/popup/guest_number_details";

patch(PosStore.prototype, {
    async pay() {
        const dialogService = this.env.services.dialog;
        const config = this.config;
        // const tableOrder = this.models["pos.order"].find((order) => order.table_id && order.table_id.id === table.id);
        // const alreadyFilled = tableOrder && tableOrder.total_no_of_guests > 0;
        const isRequired = config.guest_details_required;
        if (config.guest_details && config.guest_details_timing === "order_after") {
            const result = await dialogService.add(AddGuestNumberDetailsPopup, {
                initial_male: 0,
                initial_female: 0,
            });
            if (result?.confirmed) {
                return super.pay(...arguments);
            }
        }
        if(!config.guest_details || (config.guest_details && config.guest_details_timing==="order_after")){
            return super.pay(...arguments);
        }
    },
});
    // async pay() {
    //     const dialogService = this.env.services.dialog;
    //     const confirmed = await new Promise((resolve) => {
    //         dialogService.add(AddGuestNumberDetailsPopup, {
    //             initial_male: 0,
    //             initial_female: 0,
    //             confirm: (data) => {
    //                 console.log("Details saved:", data);
    //                 resolve(true);
    //             },
    //             cancel: () => {
    //                 resolve(false);
    //             }
    //         });
    //     });
    //     if (confirmed) {
    //         return super.pay();
    //     }
    //     console.log("Payment flow stopped by user.");
    // },
    // async pay() {
    //    const config = this.config;
    //    if(config.guest_details && config.guest_details_timing === "order_after"){
    //         const dialogService = this.env.services.dialog;
    //         if (dialogService) {
    //             dialogService.add(AddGuestNumberDetailsPopup, {
    //                 initial_male: 0,
    //                 initial_female: 0,
    //                 close: () => {
    //                     return super.pay();
    //                     console.log("Cancelled");
    //                 },
    //             });
    //         } else {
    //             return super.pay();
    //         }
    //     }
    // },