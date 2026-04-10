import {FloorScreen} from "@pos_restaurant/app/screens/floor_screen/floor_screen";
import {patch} from "@web/core/utils/patch";
import {onMounted, onWillUnmount, useState} from "@odoo/owl";
import { AddGuestNumberDetailsPopup } from "@pos_custom/app/components/popup/guest_number_details";
import { useService } from "@web/core/utils/hooks";

patch(FloorScreen.prototype, {
    setup() {
        super.setup(...arguments);
        this.timerState = useState({currentTime: Date.now()});
        this.dialogService = useService("dialog");
        onMounted(() => {
            this.timerInterval = setInterval(() => {
                this.timerState.currentTime = Date.now();
            }, 1000);
        });
        onWillUnmount(() => {
            clearInterval(this.timerInterval);
        });
    },

    getTableDuration(table) {
        const order = this.pos.getTableOrders(table.id).find(o => !o.finalized);
        if (!order || !order.table_selected) {
            return "00:00";
        }
        const start = new Date(order.table_selected);
        if (isNaN(start)) return "00:00";
        const totalSeconds = Math.floor((this.timerState.currentTime - start.getTime()) / 1000);
        if (totalSeconds < 0) return "00:00";
        const hrs = Math.floor(totalSeconds / 3600);
        const mins = Math.floor((totalSeconds % 3600) / 60);
        const secs = totalSeconds % 60;
        const displayMins = mins < 10 ? `0${mins}` : mins;
        const displaySecs = secs < 10 ? `0${secs}` : secs;
        if (hrs > 0) { return `${hrs}:${displayMins}:${displaySecs}`; }
        return `${displayMins}:${displaySecs}`;
    },
    async onClickTable(table) {
        const config = this.pos.config;
        if (config.guest_details && config.guest_details_timing === "order_before") {
            const result = await this.env.services.dialog.add(
                AddGuestNumberDetailsPopup,{
                    initial_male: 0,
                    initial_female: 0,
                });
            // console.log(">><<>><<")
            // if (!result?.confirmed) { return; }
            // console.log("?????????")
            const res = await super.onClickTable(table);
            const order = this.pos.getOrder();
            if (order) {
                order.no_of_male = result.male;
                order.no_of_female = result.female;
                order.total_no_of_guests = result.total;
                order.guest_details = result.guests;
            }
            return res;
        }
        return super.onClickTable(table);
    }
    // async onClickTable(table) {
    //     const config = this.pos.config;
    //     let guestData = null;
    //     if (config.guest_details && config.guest_details_timing === "order_before") {
    //         const { confirmed, payload } = await this.env.services.dialog.add(
    //             AddGuestNumberDetailsPopup,
    //             {
    //                 initial_male: 0,
    //                 initial_female: 0,
    //             }
    //         );
    //         if (!confirmed) {
    //             return;
    //         }
    //         guestData = this.pos.temp_guest_details;
    //     }
    //     const result = await super.onClickTable(table);
    //     const currentOrder = this.pos.getOrder();
    //     if (guestData && currentOrder) {
    //         currentOrder.no_of_male = guestData.male;
    //         currentOrder.no_of_female = guestData.female;
    //         currentOrder.total_no_of_guests = guestData.total;
    //         this.pos.temp_guest_details = null;
    //     }
    //     return result;
    // }
    // async onClickTable(table) {
    //     const config = this.pos.config;
    //     let guestData = null;
    //     if (config.guest_details && config.guest_details_timing === "order_before") {
    //         const { confirmed, payload } = await this.env.services.dialog.add(
    //             AddGuestNumberDetailsPopup,
    //             {
    //                 initial_male: 0,
    //                 initial_female: 0,
    //             }
    //         );
    //         if (!confirmed) {
    //             return;
    //         }
    //         guestData = this.pos.temp_guest_details;
    //     }
    //     const result = await super.onClickTable(table);
    //     const currentOrder = this.pos.getOrder();
    //     if (guestData && currentOrder) {
    //         currentOrder.no_of_male = guestData.male;
    //         currentOrder.no_of_female = guestData.female;
    //         currentOrder.total_no_of_guests = guestData.total;
    //         this.pos.temp_guest_details = null;
    //     }
    //     return result;
    // }
    // async onClickTable(table) {
    //     const config = this.pos.config;
    //     if (config.guest_details && config.guest_details_timing === "order_before") {
    //         const { confirmed, payload } = await this.env.services.dialog.add(AddGuestNumberDetailsPopup, {
    //             initial_male: 0,
    //             initial_female: 0
    //         });
    //         if (!confirmed) {
    //             return;
    //         }
    //     }
    //     return super.onClickTable(table);
    // }

    // async onClickTable(table) {
    //     const config = this.pos.config;
    //     if (config.guest_details && config.guest_details_timing === "order_before") {
    //         await this.env.services.dialog.add(AddGuestNumberDetailsPopup, {
    //             initial_male:0,initial_female:0
    //         });
    //     }
    //     return super.onClickTable(table);
    // }
});