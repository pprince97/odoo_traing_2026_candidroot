/** @odoo-module **/
import {FloorScreen} from "@pos_restaurant/app/screens/floor_screen/floor_screen";
import {patch} from "@web/core/utils/patch";
import {onMounted, onWillUnmount, useState} from "@odoo/owl";

patch(FloorScreen.prototype, {
    setup() {
        super.setup();
        this.timerState = useState({currentTime: Date.now()});
        onMounted(() => {
            this.interval = setInterval(() => {
                this.timerState.currentTime = new Date();
            }, 1000);
        });
        onWillUnmount(() => {
            clearInterval(this.interval);
        });
    },

    getTableTimer(table) {
        const order = this.pos.models["pos.order"].find(
            (o) => o.table_id?.id === table.id && !o.finalized
        );
        if (!order || !order.lines?.length || !order.start_timer_at) {
            return null;
        }

        const startTime = new Date(order.start_timer_at.replace(' ', 'T') + "Z").getTime();
        const diffInSeconds = Math.max(0, Math.floor((this.timerState.currentTime - startTime) / 1000));

        const h = Math.floor(diffInSeconds / 3600).toString().padStart(2, '0');
        const m = Math.floor((diffInSeconds % 3600) / 60).toString().padStart(2, '0');
        const s = (diffInSeconds % 60).toString().padStart(2, '0');

        return `${h}:${m}:${s}`;
    }
});
