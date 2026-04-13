import { FloorScreen } from "@pos_restaurant/app/screens/floor_screen/floor_screen";
import { patch } from "@web/core/utils/patch";
import { onWillUnmount, onMounted } from "@odoo/owl";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import OrderPaymentValidation from "@point_of_sale/app/utils/order_payment_validation";
import { serializeDateTime } from "@web/core/l10n/dates";
import {GuestDetail} from "./guest_detail_dialog";
import {GuestInfo} from "./guest_info";
const { DateTime } = luxon;
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { PosStore } from "@point_of_sale/app/services/pos_store";
import { DataServiceOptions } from "@point_of_sale/app/models/data_service_options";

patch(DataServiceOptions.prototype, {
    get dynamicModels() {
        const models = super.dynamicModels;
        console.log("Called dataservice", models)
        if (!models.includes("pos.order.guest")) {
            models.push("pos.order.guest");
        }
        console.log("Called dataservice", models)
        return models;
    }
});

patch(PosStore.prototype, {
    setup() {
        super.setup(...arguments);
    },
    async pay() {
        const dialogService = this.env.services.dialog;
        const order = this.getOrder();
        if(this.config.guest_details && this.config.guest_details_timing === 'order_after') {
            const showGuestDetail = (initialData = {}) => {
                dialogService.add(GuestDetail, {
                    title: "No of Guests",
                    male: initialData.male || 0,
                    female: initialData.female || 0,
                    guests: initialData.guests || 0,
                    skip: async()=>{ await super.pay(); },
                    save: async (male_no, female_no, guests_no) => {
                        dialogService.add(GuestInfo, {
                            title: "Guest Details",
                            skip: async()=>{ await super.pay(); },
                            save: async (male_no, female_no, guests_no,guest_data) => {
                                await super.pay();
                                const order_obj = this.models["pos.order"].getBy("uuid", order.uuid);
                                const guest_ids_commands = [];
                                for (const g of guest_data) {
                                    const newGuest = await this.models["pos.order.guest"].create({
                                        'age': parseInt(g.age),
                                        'nationality_id': parseInt(g.nationality_id),
                                        'gender': g.gender
                                    });
                                    guest_ids_commands.push(newGuest.id);
                                }
                                order_obj.update({
                                    'male_count': male_no,
                                    'female_count': female_no,
                                    'customer_count': guests_no,
                                    'guest_ids': guest_ids_commands,
                                });
                            },
                            male: male_no,
                            female: female_no,
                            guests: guests_no,
                            previous: async () => {
                                showGuestDetail({male: parseInt(male_no), female: parseInt(female_no), guests: parseInt(guests_no)});
                            }
                        })
                    }
                });
            }
            showGuestDetail();
        } else {
            await super.pay();
        }
    }
});

patch(ProductScreen.prototype, {
    async addProductToOrder(product, options) {
        const result =await super.addProductToOrder(...arguments);
        const order = this.currentOrder;
        if (!order.start_date && order.lines.length > 0) {
            order.start_date = serializeDateTime(DateTime.now());
        }
        return result;
    },
});

patch(OrderPaymentValidation.prototype, {
    async validateOrder() {
        if (!this.order.end_date) {
            this.order.end_date = serializeDateTime(DateTime.now());
        }
        return await super.validateOrder(...arguments);
    },
});

patch(FloorScreen.prototype, {
    setup() {
        super.setup();
        this.state.tableTimers = {};
        let interval;
        this.dialogService = useService("dialog");
        this.pos=usePos();

        onMounted(()=>{
            interval = setInterval(() => {
                const floor = this.pos.models["restaurant.floor"].get(this.state.selectedFloorId);

                floor.table_ids.forEach((table) => {
                    let order = this.pos.models["pos.order"].filter(
                        (o) => o.table_id?.id === table.id && !o.finalized
                    );
                    order = order[0]
                    if (order && order.lines.length > 0 && order.start_date) {
                        const diff = Math.floor((new Date() - new Date(order.start_date)) / 1000);
                        const mins = Math.floor(diff / 60).toString().padStart(2, '0');
                        const secs = (diff % 60).toString().padStart(2, '0');
                        this.state.tableTimers[table.id] = `${mins}:${secs}`;
                    } else {
                        this.state.tableTimers[table.id] = '00:00';
                    }
                });
            }, 1000);
        });

        onWillUnmount(() => {if(interval){clearInterval(interval)}});
    },
    async onClickTable(table, ev){
        let order=table.getOrder();
        if(this.pos.config.guest_details && this.pos.config.guest_details_timing === 'order_before' && !order) {
            const showGuestDetail = (initialData = {}) => {
                this.dialogService.add(GuestDetail, {
                    title: "No of Guests",
                    male: initialData.male || 0,
                    female: initialData.female || 0,
                    guests: initialData.guests || 0,
                    skip: async()=>{ await super.onClickTable(table, ev); },
                    save: async (male_no, female_no, guests_no) => {
                        this.dialogService.add(GuestInfo, {
                            title: "Guest Details",
                            skip: async()=>{ await super.onClickTable(table, ev); },
                            save: async (male_no, female_no, guests_no,guest_data) => {
                                await super.onClickTable(...arguments);
                                let order=table.getOrder();
                                const order_obj = this.pos.models["pos.order"].getBy("uuid", order.uuid);
                                const guest_ids_commands = [];
                                for (const g of guest_data) {
                                    const newGuest = await this.pos.models["pos.order.guest"].create({
                                        'age': parseInt(g.age),
                                        'nationality_id': parseInt(g.nationality_id),
                                        'gender': g.gender
                                    });
                                    guest_ids_commands.push(newGuest.id);
                                }
                                order_obj.update({
                                    'male_count': male_no,
                                    'female_count': female_no,
                                    'customer_count': guests_no,
                                    'guest_ids': guest_ids_commands,
                                });
                            },
                            male: male_no,
                            female: female_no,
                            guests: guests_no,
                            previous: async () => {
                                showGuestDetail({male: parseInt(male_no), female: parseInt(female_no), guests: parseInt(guests_no)});
                            }
                        })
                    }
                });
            }
            showGuestDetail();
        } else {
            await super.onClickTable(...arguments);
        }
    },
});