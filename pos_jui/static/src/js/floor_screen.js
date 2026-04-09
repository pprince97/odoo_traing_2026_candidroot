import { FloorScreen } from "@pos_restaurant/app/screens/floor_screen/floor_screen";
import { patch } from "@web/core/utils/patch";
import { onWillUnmount, onMounted } from "@odoo/owl";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { PosOrder } from "@point_of_sale/app/models/pos_order";
import OrderPaymentValidation from "@point_of_sale/app/utils/order_payment_validation";
import { serializeDateTime } from "@web/core/l10n/dates";
import {GuestDetail} from "./guest_detail_dialog";
import {GuestInfo} from "./guest_info";
const { DateTime } = luxon;
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";


patch(PosOrder.prototype, {
    setup(_defaultObj, options) {
        super.setup(...arguments);
        this.start_date = this.start_date || null;
        this.end_date = this.end_date || null;
    },
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        if (json) {
            json.start_date = this.start_date;
            json.end_date = this.end_date;
            json.guest_ids = (this.guest_ids || []).map(guest => [0, 0, {
                age: guest.age,
                nationality_id: guest.nationality_id,
                gender: guest.gender
            }]);
            json.male_count = this.male_count;
            json.female_count = this.female_count;
            json.customer_count = this.customer_count;
            }
        return json;
    },
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.start_date = json.start_date;
        this.end_date = json.end_date;
        this.male_count = json.male_count || 0;
        this.female_count = json.female_count || 0;
        this.customer_count = json.customer_count || 0;

        // Initialize guest_ids as an array
        this.guest_ids = [];
        if (json.guest_ids) {
            // json.guest_ids is usually an array of IDs or objects from the backend
            // In POS, we typically store the actual record objects in the field
            for (let guestData of json.guest_ids) {
                // If it's the standard Odoo command [0, 0, {...}]
                const values = Array.isArray(guestData) ? guestData[2] : guestData;

                // We create/get the local record to keep the model consistent
                const guestRecord = this.models["pos.order.guest"].create(values);
                this.guest_ids.push(guestRecord);
            }
        }
    },
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
        this.orm = useService("orm");
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
                    close: async () => {
                        await super.onClickTable(table, ev);
                    },
                    save: async (male_no, female_no, guests_no) => {
                        this.dialogService.add(GuestInfo, {
                            title: "Guest Details",
                            close: () => {},
                            save: async (male_no, female_no, guests_no,guest_data) => {
                                await super.onClickTable(...arguments);
                                const order = this.pos.models["pos.order"].filter((o) => o.table_id?.id === table.id && !o.finalized);
                                const order_obj = this.pos.models["pos.order"].getBy("uuid", order[0].uuid);
                                const guest_ids = [];
                                for (const g of guest_data) {
                                    const newGuest = await this.pos.models["pos.order.guest"].create({
                                        'age': parseInt(g.age),
                                        'nationality_id': parseInt(g.nationality_id),
                                        'gender': g.gender
                                    });
                                    guest_ids.push(newGuest);
                                }
                                order_obj.update({
                                    'male_count': male_no,
                                    'female_count': female_no,
                                    'customer_count': guests_no,
                                    'guest_ids': guest_ids,
                                });
                                console.log(this.pos.models['pos.order.guest'].getAll());
                                console.log(order_obj.customer_count, '>>>>>>>', order_obj.male_count, '>>>>>>>>', order_obj.female_count,order_obj.guest_ids)
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