import {Dialog} from "@web/core/dialog/dialog";
import {Component, useState, onWillStart} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";
import {usePos} from "@point_of_sale/app/hooks/pos_hook";

export class GuestDetailsPopUp extends Component {
    static template = "pos_custom.GuestDetailsPopUp";
    static components = {Dialog};
    static props = {total: Number, close: Function, order_data: Object};

    setup() {
        this.orm = useService("orm");
        this.pos = usePos();
        this.state = useState({
            countries: [],
            guests: Array.from({length: this.props.total}, () => ({
                nationality: "",
                gender: "male",
                age: 0,
            })),
        });

        onWillStart(async () => {
            this.state.countries = await this.orm.searchRead(
                "res.country",
                [],
                ["id", "display_name"]
            );
        });
    }

    // async saveDetails() {
    //     try {
    //         const currentOrder = this.pos.getOrder();
    //
    //         if (currentOrder) {
    //             currentOrder.no_of_male = this.props.order_data.male;
    //             currentOrder.no_of_female = this.props.order_data.female;
    //             currentOrder.total_no_of_guests = this.props.total;
    //         } else {
    //             this.pos.temp_guest_details = {
    //                 male: this.props.order_data.male,
    //                 female: this.props.order_data.female,
    //                 total: this.props.total,
    //             };
    //         }
    //         this.props.close({ confirmed: true });
    //     } catch (error) {
    //         console.error("Failed to save guest details:", error);
    //          this.props.close({ confirmed: false });
    //     }
    // }

    async saveDetails() {
        try {
            const currentOrder = this.pos.getOrder();
            if (!currentOrder) return;
            const guestIds = this.pos.models["guest.details"];
            let guests = []
            const guestData = this.state.guests.map(g => ({
                age: g.age,
                gender: g.gender,
                nationality: g.nationality ? Number(g.nationality) : false,
            }));
            console.log(guestData)
            for (const rec of guestData) {
                const guestData = guestIds.create({
                    age: rec.age,
                    gender: rec.gender,
                    nationality: rec.nationality ? Number(rec.nationality) : false,
                });
                guests.push(guestData)
            }
            console.log(guestIds)
            currentOrder.no_of_male = this.props.order_data.male;
            currentOrder.no_of_female = this.props.order_data.female;
            currentOrder.customer_count = this.props.total;
            currentOrder.guest_ids = guests
            this.props.close({confirmed: true});
        } catch (error) {
            console.error("Failed to create guests immediately:", error);
            this.props.close({confirmed: false});
        }
    }

// async saveDetails() {
//     try {
//         const currentOrder = this.pos.getOrder();
//         if (!currentOrder) {
//             this.pos.temp_guest_details = {
//                 male: this.props.order_data.male,
//                 female: this.props.order_data.female,
//                 total: this.props.total,
//                 guest_raw: this.state.guests.map(g => ({
//                     age: g.age,
//                     gender: g.gender,
//                     nationality: g.nationality ? Number(g.nationality) : false,
//                 })),
//             };
//         } else {
//             console.log("else")
//             currentOrder.no_of_male = this.props.order_data.male;
//             currentOrder.no_of_female = this.props.order_data.female;
//             currentOrder.total_no_of_guests = this.props.total;
//             currentOrder.guest_details_raw = this.state.guests.map(g => ({
//                 age: g.age,
//                 gender: g.gender,
//                 nationality: g.nationality ? Number(g.nationality) : false,
//             }));
//         }
//         this.props.close({
//             confirmed: true,
//             guests: this.state.guests,
//         });
//     } catch (error) {
//         console.error("Failed to save guest details:", error);
//         this.props.close({ confirmed: false });
//     }
// }

//     async saveDetails() {
//     try {
//         const currentOrder = this.pos.getOrder();
//
//         if (currentOrder) {
//             currentOrder.no_of_male = this.props.order_data.male;
//             currentOrder.no_of_female = this.props.order_data.female;
//             currentOrder.total_no_of_guests = this.props.total;
//              currentOrder.guest_details = this.state.guests.map(g => ({
//             age: g.age,
//             gender: g.gender,
//             nationality: g.nationality || false,
//         }));
//         } else {
//             this.pos.temp_guest_details = {
//                 male: this.props.order_data.male,
//                 female: this.props.order_data.female,
//                 total: this.props.total,
//             };
//         }
//         this.props.close({
//             confirmed: true,
//             guests: this.state.guests,
//         });
//     } catch (error) {
//         console.error("Failed:", error);
//         this.props.close({ confirmed: false });
//     }
// }
    async previousNumberPopup() {
        this.props.close({back: true});
    }

    // async previousNumberPopup() {
    //     this.props.close();
    //     this.props.previous();
    // }
}

// async saveDetails() {
// try {
//     const currentOrder = this.pos.getOrder();
//
//     currentOrder.no_of_male = this.props.order_data.male;
//     currentOrder.no_of_female = this.props.order_data.female;
//     currentOrder.total_no_of_guests = this.props.total;
//     console.log("Guest details stored in order:", currentOrder);
//     this.props.close();
// } catch (error) {
//     console.error("Failed to save guest details:", error);
// }
// }