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
                this.pos.models['pos.order'].filter(o => !o.finalized).forEach(order => {
                    this._setOrderDuration(order);
                });
            }, 1000);
        });

        onWillUnmount(() => {
            clearInterval(interval);
        });
    },

    // async addProductToOrder(product)

    _setOrderDuration(order) {
        if (!order || !order.date_order || (order.amount_total === undefined)) return;
        // if (order.date_order === order.date_table) return ;
        const start = new Date(order.date_table);
        console.log(order.date_table,"-------order.date_table")
        console.log(order.date_order,"-------order.date_order")
        console.log(order.amount_total,"-------order.amount_total")
        // console.log(new Date(),"-------new Date()")
        // console.log(start,"-------start")
        const diff = Math.floor((new Date() - start) / 1000);
        // console.log(diff,"-------diff")
        const h = Math.floor(diff / 3600);
        const m = Math.floor((diff % 3600) / 60);
        const s = diff % 60;

        // Directly setting this property allows Odoo to sync it to the backend field
        order.table_duration = `${h > 0 ? h + ':' : ''}${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    },

    getTableDuration(table) {
        const order = this.pos.models['pos.order'].find(o => o.table_id && o.table_id.id === table.id && !o.finalized);
        return order ? order.table_duration : "";
    }
});
