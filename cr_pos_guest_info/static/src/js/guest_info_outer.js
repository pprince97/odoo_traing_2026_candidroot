import {Dialog} from "@web/core/dialog/dialog";
import {Component, useState} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

export class GuestNumber extends Component {
    static template = "NumberOfGuest";
    static components = {Dialog};
    // static props = {
    //     title: {type: String, optional: true},
    //     close: Function,
    // };

    setup() {
        this.state = useState({
            male: 0,
            female: 0,
        });
    }

    updateMale(ev) {
        let value = Number(ev.target.value);
        if (value < 0) {
            alert("You cannot enter a negative number for Male!");
            this.state.male = 0;
            return;
        }
        this.state.male = value;
    }

    updateFemale(ev) {
        let value = Number(ev.target.value);
        if (value < 0) {
            alert("You cannot enter a negative number for Female!");
            this.state.female = 0;
            return;
        }
        this.state.female = value;
    }

    get totalGuests() {
        return this.state.male + this.state.female;
    }

    async next() {
        const data = {
            male: this.state.male,
            female: this.state.female,
            total: this.totalGuests,
        };

        console.log("NEXT CLICKED", data);

        if (this.props.next) {
            this.props.next(data);
        }

        this.props.close({confirmed: true, data});
    };

    async skip(){
        this.props.close({
            confirmed: false
        });
    };
}

