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

    async saveDetails() {
        try {
            const currentOrder = this.pos.getOrder();
            if (!currentOrder) return;
            const guestData = this.state.guests.map(g => ({
                age: g.age,
                gender: g.gender,
                nationality: g.nationality ? Number(g.nationality) : false,
            }));
            const guestIds = await this.orm.create("guest.details", guestData);
            // const guestIds = await this.orm.create("guest.details", [{
            //     age:22,nationality:13,gender:'male'
            // }]);
            currentOrder.no_of_male = this.props.order_data.male;
            currentOrder.no_of_female = this.props.order_data.female;
            currentOrder.total_no_of_guests = this.props.total;
            currentOrder.guest_ids = [...guestIds]
            console.log(currentOrder)
            for (const guestId of guestIds) {
                await this.orm.write("guest.details", [guestId], {
                    order_id: currentOrder.id
                });
                console.log(currentOrder.id)
            }
            this.props.close({confirmed: true});
        } catch (error) {
            console.error("Failed to create guests immediately:", error);
            this.props.close({confirmed: false});
        }
    }
}
