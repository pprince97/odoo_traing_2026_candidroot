import {Component, useState, useRef} from "@odoo/owl";
import {Dialog} from "@web/core/dialog/dialog";
import {useService} from "@web/core/utils/hooks";
import {usePos} from "@point_of_sale/app/hooks/pos_hook";

export class DetailPopup extends Component {
    static props = {
        data: Object,
        next: Function,
        close: Function,
    };

    static template = "pos_restaurant.DetailPopup";
    static components = {
        Dialog
    };

    setup() {
        this.dialogService = useService("dialog");
        this.state_array = useState({arr: []})
        this.pos = usePos();
        for (let i = 1; i <= this.props.data.guest_no; i++) {
            this.state_array.arr.push(i);
        }
        this.countries = this.pos.models["res.country"].getAll();
        this.root = useRef("popup_root");
    }

    next_up() {
        if (!this.root.el) return;
        const guests = [];
        const rows = this.root.el.querySelectorAll(".guest-row");

        rows.forEach((row) => {
            const record = [0,0,{
                age: row.querySelector(".guest-age").value,
                nationality: row.querySelector(".guest-nationality").value,
                gender: row.querySelector(".guest-gender").value,
            }];
            guests.push(record);
        });
        console.log('>>>>>>>>>>>>>>>>',guests)
        this.props.data.guest_ids = guests
        console.log("All Guest Records:", guests);
        this.props.close()
        this.props.next(this.props.data)
    }

    previous() {
        this.props.close()
    }

}