// import {Component, useRef, useState} from "@odoo/owl";
// import {Dialog} from "@web/core/dialog/dialog";
// import {useService} from "@web/core/utils/hooks";
// import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";
// import {DetailPopup} from "../popup/detail_popup";
//
// export class GuestPopup extends Component {
//     static template = "pos_restaurant.GuestPopup";
//     static components = {
//         Dialog
//     };
//     static props = {
//         getPayload: Function,
//         close: Function,
//     };
//
//     setup() {
//         this.dialog = useService("dialog");
//         this.state = useState({
//             male_no: 0,
//             female_no: 0,
//             guest_no: 0,
//         });
//     }
//
//     confirm() {
//         this.props.getPayload(this.state);
//         this.props.close();
//     }
//
//     async next_pop(ev) {
//         var a = ev.currentTarget.parentElement.parentElement.querySelectorAll('input')
//         this.state.male_no = parseInt(a[0].value) || 0
//         this.state.female_no = parseInt(a[1].value) || 0
//         this.state.guest_no = parseInt(a[2].value) || 0
//         var payload = await makeAwaitable(this.dialog, DetailPopup, {guest_no : this.state.guest_no});
//         debugger
//         if (payload){
//                this.props.getPayload(this.state);
//                this.props.close();
//            }
//     }
//
//     onchangeGuestMale(ev) {
//         this.state.male_no = parseInt(ev.currentTarget.value) || 0
//         this.state.guest_no = this.state.male_no + this.state.female_no
//     }
//
//
//     onchangeGuestFeMale(ev) {
//         this.state.female_no = parseInt(ev.currentTarget.value) || 0
//         this.state.guest_no = this.state.male_no + this.state.female_no
//     }
// }


import {Component, useRef} from "@odoo/owl";
import {Dialog} from "@web/core/dialog/dialog";
import {useService} from "@web/core/utils/hooks";

export class GuestPopup extends Component {
    static props = {
        data: Object,
        next: Function,
        close: Function,
    };
    static template = "pos_restaurant.GuestPopup";
    static components = {
        Dialog
    };

    setup() {
        this.dialogService = useService("dialog");
        this.notification = useService("notification");
        this.maleRef = useRef("male_no");
        this.femaleRef = useRef("female_no");
        this.totalRef = useRef("guest_no");

    }

    async next_pop() {
        if (!parseInt(this.totalRef.el.value)) {
            this.notification.add("Number of Guest can not be Zero!", {
                type: "danger",
            });
        } else {
            this.props.data.male_no = parseInt(this.maleRef.el.value) || 0
            this.props.data.female_no = parseInt(this.femaleRef.el.value) || 0
            this.props.data.guest_no = parseInt(this.totalRef.el.value) || 0
            this.props.next(this.props.data);
        }
    }

    onchangeGuest() {
        const male = parseInt(this.maleRef.el.value) || 0
        const female = parseInt(this.femaleRef.el.value) || 0
        this.totalRef.el.value = male + female
    }
}