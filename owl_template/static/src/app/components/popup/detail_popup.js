// import {Component, useState, useRef} from "@odoo/owl";
// import {Dialog} from "@web/core/dialog/dialog";
// import {useService} from "@web/core/utils/hooks";
// import {usePos} from "@point_of_sale/app/hooks/pos_hook";
// // import { Command } from "@web/../tests/web_test_helpers";
// // import { Command } from "@web/core/utils/patch";
// import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";
//
// export class DetailPopup extends Component {
//     static props = {
//         guest_no : Number,
//         close : Function,
//         getPayload: Function,
//     }
//     static template = "pos_restaurant.DetailPopup";
//     static components = {
//         Dialog
//     };
//
//     setup() {
//         this.dialogService = useService("dialog");
//         this.state_array = useState({arr: [], guest_no: this.props.guest_no,})
//         this.pos = usePos();
//         for (let i = 1; i <= this.props.guest_no; i++) {
//             this.state_array.arr.push(i);
//         }
//         this.countries = this.pos.models["res.country"].getAll();
//         this.root = useRef("popup_root");
//     }
//     confirm() {
//         this.props.getPayload(this.state);
//         this.props.close();
//     }
//     next_up() {
//
//
//         // rows.forEach((row) => {
//             // const record = [0,0,{
//             //     age: row.querySelector(".guest-age").value,
//             //     nationality: row.querySelector(".guest-nationality").value,
//             //     gender: row.querySelector(".guest-gender").value,
//             // }];
//             // console.log(row.querySelector(".guest-nationality").value);
//             // const record = Command.create({
//             //     age: parseInt(row.querySelector(".guest-age").value),
//             //     nationality: row.querySelector(".guest-nationality").value,
//             //     gender: row.querySelector(".guest-gender").value,
//             // });
//
//         //     guests.push(record);
//         // });
//         // console.log('>>>>>>>>>>>>>>>>', guests)
//         // this.props.data.guest_ids = guests
//         // console.log("All Guest Records:", guests);
//         this.props.getPayload(this.state_array);
//         this.props.close()
//     }
//
//     previous() {
//         this.props.close()
//     }
//
// }

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
        const guests = [];
        const rows = this.root.el.querySelectorAll(".guest-row");
        rows.forEach((row) => {
            const record = this.pos.models["pos.guest"].create({
                age: row.querySelector(".guest-age").value,
                country_id: parseInt(row.querySelector(".guest-nationality").value),
                gender: row.querySelector(".guest-gender").value,
            });
            guests.push(record);
        });
        this.props.data.guest_ids = guests
        this.props.close()
        this.props.next(this.props.data)
    }

    previous() {
        this.props.close()
    }

}