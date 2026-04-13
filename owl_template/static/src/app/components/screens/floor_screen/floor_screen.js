/** @odoo-module **/
import {FloorScreen} from "@pos_restaurant/app/screens/floor_screen/floor_screen";
import {patch} from "@web/core/utils/patch";
import {onMounted, onWillUnmount, useState} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";
import {GuestPopup} from "../../popup/guest_popup"
import {DetailPopup} from "../../popup/detail_popup";
// import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { DataServiceOptions } from "@point_of_sale/app/models/data_service_options";


patch(DataServiceOptions.prototype, {
    get dynamicModels() {
        const models = super.dynamicModels;
        if (!models.includes("pos.guest")) {
            models.push("pos.guest");
            console.log('>>>>>>>>>>>>inside if')
        }
        return models;
    }
});

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

    // async onClickTable(table, ev) {
    //     if (this.pos.config.guest_details && this.pos.config.timing === 'before' && !this.pos.tableHasOrders(table)) {
    //
    //           // const payload = await makeAwaitable(this.dialog, GuestPopup, {});
    //           // var order = this.pos.getOrder()
    //           // if (!order){
    //           //     order = this.pos.addNewOrder()
    //           // }
    //           // if (payload){
    //           //     var line = await this.pos.models["pos.guest"].create({
    //           //           age: 145,
    //           //           gender: 'male',
    //           //           order_id : order
    //           //     });
    //           // }
    //           // debugger
    //           // // order.update({ guest_ids: [["set", line]] });
    //           // await this.pos.syncAllOrders({ orders: [order] });
    //           // await super.onClickTable(table, ev)
    //
    //         // const closeGuestPopup = this.dialogService.add(GuestPopup, {
    //         //     data: {},
    //         //     next: async (data) => {
    //         //         await this.dialogService.add(DetailPopup, {
    //         //             data: data,
    //         //             next: async (data) => {
    //         //                 await super.onClickTable(table, ev)
    //         //                 const order = table.getOrder()
    //         //                 this.pos.models["pos.guest"].create({
    //         //                     'age': 145,
    //         //                     'gender': 'male',
    //         //                     'order_id': order
    //         //                 });
    //         //                 // console.log('>>>>>>>>>>>>>', newGuest.id)
    //         //                 // // guest_ids.push(newGuest.id);
    //         //                 // // order.guest_ids = guest_ids;
    //         //                 // order.update(data)
    //         //                 // order.update({
    //         //                 //     guest_ids: [newGuest.id]
    //         //                 // });
    //         //                 // // order.update({guest_ids:[newGuest]})
    //         //                 // console.log('>>>>>>>>>>>>>>>>>>>>>>')
    //         //                 closeGuestPopup();
    //         //             },
    //         //         });
    //         //     }
    //         // });
    //
    //     } else {
    //         await super.onClickTable(table, ev)
    //     }
    // }

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


