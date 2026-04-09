/** @odoo-module **/
import {FloorScreen} from "@pos_restaurant/app/screens/floor_screen/floor_screen";
import {patch} from "@web/core/utils/patch";
import {onMounted, onWillUnmount, useState} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";
import {GuestPopup} from "../../popup/guest_popup"
import {DetailPopup} from "../../popup/detail_popup";

patch(FloorScreen.prototype, {
    setup() {
        super.setup();
        this.timerState = useState({currentTime: new Date()});
        this.dialogService = useService("dialog");
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
        if (this.pos.tableHasOrders(table)) {
            const order = this.pos.models['pos.order'].find(o => o.table_id && o.table_id.id === table.id && !o.finalized);
            if (order && order.start_time) {
                const start = new Date(order.start_time);
                const diff = Math.floor((this.timerState.currentTime - start) / 1000);

                const hours = Math.floor(diff / 3600);
                const minutes = Math.floor((diff % 3600) / 60);
                const seconds = diff % 60;

                return `${hours > 0 ? hours + ':' : ''}${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            } else {
                return "00:00"
            }
        } else {
            return "00:00"
        }
    },

    async onClickTable(table, ev) {
        if (this.pos.config.guest_details && this.pos.config.timing === 'before' && !this.pos.tableHasOrders(table)) {
            const closeGuestPopup = this.dialogService.add(GuestPopup, {
                data : {},
                next: async (data) => {
                    await this.dialogService.add(DetailPopup, {
                        data : data,
                        next: async (data) => {
                            await super.onClickTable(table, ev)
                            const order = table.getOrder()
                            console.log('>>>>>>>>>>>>>>',data.guest_ids)
                            order.guest_ids = [[0, 0, {'gender': 'male', 'age': 15}]]
                            console.log('>>>>>>>>>>>>>',order.guest_ids)
                            order.update(data)
                            closeGuestPopup();
                        },
                    });
                }
            });

        } else {
            return super.onClickTable(table, ev)
        }
    }
});
