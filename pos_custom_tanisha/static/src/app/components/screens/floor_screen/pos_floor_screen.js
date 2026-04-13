import {patch} from "@web/core/utils/patch";
import {FloorScreen} from "@pos_restaurant/app/screens/floor_screen/floor_screen";
import {useState, onMounted, onWillUnmount} from "@odoo/owl";
import {ProductScreen} from "@point_of_sale/app/screens/product_screen/product_screen";
import {PaymentScreen} from "@point_of_sale/app/screens/payment_screen/payment_screen";
import {serializeDateTime} from "@web/core/l10n/dates";
import {NoOfGuestDialog} from "./guest_details_dialog";
import {GuestDetailsDialog} from "./guest_details_dialog";
import {DataServiceOptions} from "@point_of_sale/app/models/data_service_options";


patch(DataServiceOptions.prototype, {
    get dynamicModels() {
        const models = super.dynamicModels;
        console.log(">>>>>>>>>>>>>", models);
        console.log(models.includes("guest.details"),models.length);
        if (!models.includes("guest.details")) {
            models.push("guest.details");
            console.log("iffffffffffffffffff");
        }
        return models;
    }
});

const {DateTime} = luxon;

patch(ProductScreen.prototype, {
    async addProductToOrder(product, options) {
        const result = await super.addProductToOrder(...arguments);
        const order = this.currentOrder;
        if (!order.start_date_time && order.lines.length > 0) {
            order.start_date_time = serializeDateTime(DateTime.now());
        }
        return result;
    },
});

patch(PaymentScreen.prototype, {
    async validateOrder(isForceValidate) {
        const order = this.currentOrder;
        if (order && !order.end_date_time) {
            order.end_date_time = serializeDateTime(DateTime.now());
        }
        return await super.validateOrder(...arguments);
    },
});

patch(FloorScreen.prototype, {
    setup() {
        super.setup();
        this.dialogState = useState({dialogOpened: false});
        this.timeState = useState({currentTime: new Date()});
        let interval;
        onMounted(() => {
            interval = setInterval(() => {
                this.timeState.currentTime = new Date();
            }, 1000);

        });
        onWillUnmount(() => {
            clearInterval(interval);
        });

    },

    getTableTimer(table) {
        if (this.pos.tableHasOrders(table)) {
            const order = table.getOrder();
            if (order.start_date_time) {
                const start = new Date(order.start_date_time);
                const diff = Math.floor((this.timeState.currentTime - start) / 1000);

                const hours = Math.floor(diff / 3600);
                const minutes = Math.floor((diff % 3600) / 60);
                const seconds = diff % 60;

                return `${hours > 0 ? hours + ':' : ''}${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            } else {
                return "00:00";
            }
        } else {
            return "00:00";
        }

    },

    async onClickTable(table, ev) {
        if (this.pos.config.guest_details_bool && this.pos.config.guest_details_timing === "order_before") {
            if (!this.pos.tableHasOrders(table)) {
                const no_of_guest = this.env.services.dialog.add(NoOfGuestDialog, {
                    onNext: () => {
                        this.env.services.dialog.add(GuestDetailsDialog, {
                            onNext: () => {
                                super.onClickTable(table, ev);
                                const order = table.getOrder();
                                const male = document.getElementById('no_of_male');
                                const female = document.getElementById('no_of_female');
                                const guest = document.getElementById('no_of_guest');
                                if (male && female && guest) {
                                    order.update({
                                        no_of_male: parseInt(male.value),
                                        no_of_female: parseInt(female.value),
                                        customer_count: parseInt(guest.value),
                                    })
                                }
                                no_of_guest();
                            },
                            onPrevious: () => {
                                if (!this.dialogState.dialogOpened) {
                                    this.onClickTable(table, ev);
                                }
                            },
                        });
                        this.dialogState.dialogOpened = true;
                    },
                    onSkip: () => {
                        this.dialogState.dialogOpened = false;
                    }
                });
            } else {
                super.onClickTable(table, ev);
            }
        } else {
            super.onClickTable(table, ev);
        }
    },

});


