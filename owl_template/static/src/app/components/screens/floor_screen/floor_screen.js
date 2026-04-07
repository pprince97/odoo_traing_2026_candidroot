/** @odoo-module **/
import {FloorScreen} from "@pos_restaurant/app/screens/floor_screen/floor_screen";
import {patch} from "@web/core/utils/patch";
import {onMounted, onWillUnmount, useState} from "@odoo/owl";

patch(FloorScreen.prototype, {
    setup() {
        super.setup();
        this.timerState = useState({currentTime: new Date()});
        let interval;
        onMounted(() => {
            interval = setInterval(() => {
                this.timerState.currentTime = new Date();
            }, 1000);
        });

        onWillUnmount(() => {
            clearInterval(interval);
        });
    },

    getTableDuration(table) {
        const order = this.pos.models['pos.order'].find(o => o.table_id && o.table_id.id === table.id);
        if (!order) return "";
        if (order.start_time) {
            const start = new Date(order.start_time);
            const diff = Math.floor((this.timerState.currentTime - start) / 1000);

            const hours = Math.floor(diff / 3600);
            const minutes = Math.floor((diff % 3600) / 60);
            const seconds = diff % 60;

            return `${hours > 0 ? hours + ':' : ''}${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }
        else{
            return "00:00"
        }
    }
});
