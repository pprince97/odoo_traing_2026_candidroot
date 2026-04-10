import {FloorScreen} from "@pos_restaurant/app/screens/floor_screen/floor_screen";
import {PosStore} from "@point_of_sale/app/services/pos_store";
import {useService} from "@web/core/utils/hooks";
import {GuestCountDialog} from "@library_management/app/components/popup/guest_popup";
import {GuestDetailsDialog} from "@library_management/app/components/popup/guest_popup";
import {patch} from "@web/core/utils/patch";

patch(FloorScreen.prototype, {
    setup() {
        super.setup();
        this.dialogService = useService("dialog");
    },
    async onClickTable(table) {
        console.log('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        const config = this.pos.config;
        // const tableOrder = this.pos.currentOrder;
        const tableOrder = this.pos.models["pos.order"].find((order) => order.table_id && order.table_id.id === table.id);
        const alreadyFilled = tableOrder && tableOrder.guest_total > 0;
        const isRequired = config.guest_details_required;
        if (config.guest_details && config.guest_details_timing === 'order_before' && !alreadyFilled) {
            const openGuestCount = (initialData = {}, savedGuestDetails = []) => {
                this.dialogService.add(GuestCountDialog, {
                    initialData,
                    savedGuestDetails: savedGuestDetails,
                    is_required: isRequired,
                    onNext: async (data, updatedDetails) => {
                        this.dialogService.add(GuestDetailsDialog, {
                            totalCount: data.total,
                            initialGuestDetails: updatedDetails && updatedDetails.length > 0 ? updatedDetails : savedGuestDetails,
                            is_required: isRequired,
                            onConfirm: async (guestDetails) => {
                                await super.onClickTable(table);
                                const order = table.getOrder();
                                if (order) {
                                    const detailLines = guestDetails.map(guest => [0, 0, {
                                        age: parseInt(guest.age) || 0,
                                        nationality_id: parseInt(guest.nationality) || false,
                                        gender: guest.gender || "",
                                    }]);
                                    console.log('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> male',data.male)
                                    console.log('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> female',data.female)
                                    console.log('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> total',data.total)
                                    console.log('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> detailLines',detailLines)
                                    order.update({
                                        guest_male: data.male,
                                        guest_female: data.female,
                                        guest_total: data.total,
                                        guest_detail_ids: detailLines,
                                    });
                                }
                            },
                            onPrevious: (currentDetails) => openGuestCount(data, currentDetails),
                        });
                    },
                });
            };
            openGuestCount();
            return;
        }
        await super.onClickTable(table);
    }
});

patch(PosStore.prototype, {
    async pay() {
        console.log('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        const config = this.config;
        const dialogService = this.env.services.dialog;
        const order = this.currentOrder;
        const alreadyFilled = order && order.guest_total > 0;
        const isRequired = config.guest_details_required;
        if (config.guest_details && config.guest_details_timing === 'order_after' && !alreadyFilled) {
            const openGuestCount = (initialData = {}, savedGuestDetails = []) => {
                dialogService.add(GuestCountDialog, {
                    initialData,
                    savedGuestDetails: savedGuestDetails,
                    is_required: isRequired,
                    onNext: async (data, updatedDetails) => {
                        dialogService.add(GuestDetailsDialog, {
                            totalCount: data.total,
                            initialGuestDetails: updatedDetails && updatedDetails.length > 0 ? updatedDetails : savedGuestDetails,
                            is_required: isRequired,
                            onConfirm: async (guestDetails) => {
                                const activeOrder = this.currentOrder;
                                if (activeOrder) {
                                    const detailLines = guestDetails.map(guest => [0, 0, {
                                        age: parseInt(guest.age) || 0,
                                        nationality_id: parseInt(guest.nationality) || false,
                                        gender: guest.gender || "",
                                    }]);
                                    activeOrder.update({
                                        guest_male: data.male,
                                        guest_female: data.female,
                                        guest_total: data.total,
                                        guest_detail_ids: detailLines,
                                    });
                                }
                                return await super.pay();
                            },
                            onPrevious: (currentDetails) => openGuestCount(data, currentDetails),
                        });
                    },
                });
            };
            openGuestCount();
            return;
        }
        return await super.pay();
    }
});


