/** @odoo-module **/

import {Component, useRef} from "@odoo/owl";
import {Dialog} from "@web/core/dialog/dialog";
import {useService} from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";

export class CutomerInfoPopup extends Component {
    static template = "pos_restaurant.CutomerInfoPopup";
    static components = {Dialog};

    setup() {
        this.orm = useService("orm");
        this.pos = usePos();
        this.nameRef = useRef("name");
        this.phoneRef = useRef("phone");
        this.notesRef = useRef("notes");
    }


    async save() {
        const name = this.nameRef.el.value;
        const phone = this.phoneRef.el.value;
        const notes = this.notesRef.el.value;

        console.log("Captured:", {name, phone, notes});

        const partner_id = await this.orm.create("res.partner", [{
                name: name,
                phone: phone,
                comment: notes,
            }],
        );

        const order = this.pos.selectedOrder;
        order.general_customer_note += (" " + notes);
        console.log(typeof(order.general_customer_note));
        console.log(order.general_customer_note);

        // await this.orm.write("pos.order", [1], {
        //     general_customer_note: notes,
        // });

        console.log("Created Partner ID:", partner_id);

        this.props.close({partner_id});
    }
}

