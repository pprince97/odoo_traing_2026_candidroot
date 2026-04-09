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
