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
    getTableTimer(table) {
        const order = this.pos.models['pos.order'].find(o => o.table_id && o.table_id.id === table.id && !o.finalized);
        if (!order || !order.start_date) return "00:00";
        if (order.start_date) {
            const start = new Date(order.start_date);
            const diff = Math.floor((this.timerState.currentTime - start) / 1000);

            const hours = Math.floor(diff / 3600);
            const minutes = Math.floor((diff % 3600) / 60).toString().padStart(2, '0');
            const seconds = (diff % 60).toString().padStart(2, '0');

            return `${hours > 0 ? hours + ':' : ''}${minutes}:${seconds}`;
        }
    }
});























// /** @odoo-module **/
//
// import { FloorScreen } from "@pos_restaurant/app/screens/floor_screen/floor_screen";
// import { patch } from "@web/core/utils/patch";
// import { onMounted, onWillUnmount, useState } from "@odoo/owl";
//
// patch(FloorScreen.prototype, {
//     setup() {
//         super.setup();
//         this.timerState = useState({ currentTime: Date.now() });
//         onMounted(() => {
//             this.interval = setInterval(() => {
//                 this.timerState.currentTime = new Date();
//             }, 1000);
//         });
//         onWillUnmount(() => {
//             clearInterval(this.interval);
//         });
//     },
//
//     getTableTimer(table) {
//         const orders = this.pos.getTableOrders(table.id);
//         if (!orders || !orders.length) {
//             return "00:00:00";
//         }
//         const order = orders.find(o => !o.finalized) || orders[0];
//         if (!order) {
//             return "00:00:00";
//         }
//         if (!order.start_date) {
//             const nowStr = new Date().toISOString().replace('T', ' ').slice(0, 19);
//             order.start_date = nowStr;
//             if (order.backendId) {
//                 this.env.services.orm.write("pos.order", [order.backendId], {
//                     start_date: nowStr
//                 });
//             }
//         }
//         let startTimeRaw = order.start_date;
//         if (!startTimeRaw) return "00:00:00";
//         // let startTime;
//         // if (typeof startTimeRaw === 'string') {
//         //     startTime = new Date(startTimeRaw.replace(' ', 'T') + "Z").getTime();
//         // } else {
//         //     startTime = new Date(startTimeRaw).getTime();
//         // }
//         const currentTime = this.timerState.currentTime;
//         const diffInSeconds = Math.max(0, Math.floor((currentTime - startTimeRaw) / 1000));
//         const h = Math.floor(diffInSeconds / 3600).toString().padStart(2, '0');
//         const m = Math.floor((diffInSeconds % 3600) / 60).toString().padStart(2, '0');
//         const s = (diffInSeconds % 60).toString().padStart(2, '0');
//         return `${h}:${m}:${s}`;
//     }
// });
//
