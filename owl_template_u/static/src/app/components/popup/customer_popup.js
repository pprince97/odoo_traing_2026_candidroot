/** @odoo-module **/

import {Component, useRef} from "@odoo/owl";
import {Dialog} from "@web/core/dialog/dialog";
import {useService} from "@web/core/utils/hooks";
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


        const partner_id = await this.orm.create("res.partner", [{
                name: name,
                phone: phone,
                comment: notes,
            }],
        );

        const order = this.pos.selectedOrder;
        order.general_customer_note += (" " + notes);

        this.props.close({partner_id});
    }
}

