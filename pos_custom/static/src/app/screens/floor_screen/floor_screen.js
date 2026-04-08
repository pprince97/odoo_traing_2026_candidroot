import {FloorScreen} from "@pos_restaurant/app/screens/floor_screen/floor_screen";
import {patch} from "@web/core/utils/patch";
import {onMounted, onWillUnmount, useState} from "@odoo/owl";
import { AddGuestNumberDetialsPopup } from "@pos_custom/app/components/popup/guest_number_details";
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
            await this.env.services.dialog.add(AddGuestNumberDetialsPopup, {});
        }
        return super.onClickTable(table);
    }

    //  async onClickTable(table) {
    //     console.log("TABLE CLICKED UI");
    //
    //         await this.dialog.add(AddGuestNumberDetialsPopup, {});
    //
    //     return super.onClickTable(table);
    // }
});