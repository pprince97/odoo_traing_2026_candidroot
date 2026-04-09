import {Component} from "@odoo/owl";
import {Dialog} from "@web/core/dialog/dialog";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";


export class NoOfGuestDialog extends Component {

    static template = "pos_custom_tanisha.NoOfGuestDialog";
    static components = {Dialog};
    static props = {
        close: Function,
        onNext: Function,
    };

    next() {
        this.props.onNext();
    }

    onChangeInput() {
        const male = document.getElementById('no_of_male').value;
        const female = document.getElementById('no_of_female').value;
        document.getElementById('no_of_guest').value = parseInt(male) + parseInt(female);
    }

}

export class GuestDetailsDialog extends Component {

    static template = "pos_custom_tanisha.GuestDetailsDialog";
    static components = {Dialog};
    static props = {
        close: Function,
        onNext: Function,
    };

    setup() {
        this.pos = usePos();
        this.countries = this.pos.models["res.country"].getAll();
    }

    next() {
        this.props.close();
        this.props.onNext();
    }

}
