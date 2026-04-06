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
            // Update the state every second to trigger a re-render
            interval = setInterval(() => {
                this.timerState.currentTime = new Date();
            }, 1000);
        });

        onWillUnmount(() => {
            clearInterval(interval);
        });
    },

    getTableDuration(table) {
        // console.log('>>>>>>>>>>>>>>>>>>>>')
        const order = this.pos.models['pos.order'].find(o => o.table_id && o.table_id.id === table.id);
        if (!order) return "";
        //
        //     // Calculate difference between now and order creation
        const start = new Date(order.date_order);
        const diff = Math.floor((this.timerState.currentTime - start) / 1000);
        // console.log(start, '>>>>>>>>>>', this.state.currentTime)
        //
        const hours = Math.floor(diff / 3600);
        const minutes = Math.floor((diff % 3600) / 60);
        const seconds = diff % 60;
        //
        return `${hours > 0 ? hours + ':' : ''}${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
});
