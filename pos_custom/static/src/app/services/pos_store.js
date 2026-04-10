import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { PosStore } from "@point_of_sale/app/services/pos_store";
import { patch } from "@web/core/utils/patch";
import { AddGuestNumberDetailsPopup } from "@pos_custom/app/components/popup/guest_number_details";

patch(PosStore.prototype, {
    async pay() {
        const dialogService = this.env.services.dialog;

        const result = await dialogService.add(AddGuestNumberDetailsPopup, {
            initial_male: 0,
            initial_female: 0,
        });

        if (result?.confirmed) {
        const order = this.getOrder();

        if (order) {
            order.no_of_male = result.male;
            order.no_of_female = result.female;
            order.total_no_of_guests = result.total;
            order.guest_ids = result.guest_details;
        }

        return super.pay(...arguments);
    }
        console.log("Payment stopped");
    },
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
});
    // async pay() {
    //    const config = this.config;
    //     if (config.guest_details && config.guest_details_timing === "order_after") {
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
patch(PosOrder.prototype, {
    async finalize() {
        const result = await super.finalize(...arguments);

        if (this._pendingGuests && this._pendingGuestsOrm && this.server_id) {
            try {
                const guestRecords = this._pendingGuests.map(g => ({
                    order_id: this.server_id,
                    age: g.age,
                    gender: g.gender,
                    nationality: g.nationality ? Number(g.nationality) : false,
                }));
                await this._pendingGuestsOrm.create("guest.details", guestRecords);
                console.log("✅ Guests saved after order finalized");
                this._pendingGuests = null;
                this._pendingGuestsOrm = null;
            } catch (e) {
                console.error("Failed to save pending guests:", e);
            }
        }
        return result;
    }
});