import {Component, useState} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";
import {Dialog} from "@web/core/dialog/dialog";

export class GuestCountDialog extends Component {
    static template = "library_management.GuestCountDialog";
    static components = {Dialog};
    static props = {
        close: {type: Function},
        onNext: {type: Function},
        initialData: {type: Object, optional: true},
        savedGuestDetails: {type: Array, optional: true},
        is_required: { type: Boolean, optional: true },
    };

    setup() {
        this.state = useState({
            male: this.props.initialData?.male || 0,
            female: this.props.initialData?.female || 0,
        });
    }

    get totalCount() {
        return (this.state.male || 0) + (this.state.female || 0);
    }

    _onNext() {
        if (this.totalCount > 0) {
            this.props.onNext({
                male: this.state.male,
                female: this.state.female,
                total: this.totalCount
            }, this.props.savedGuestDetails);
            this.props.close();
        }
    }
    
    _onSkip() {
        if (this.props.is_required) {
            this.env.services.notification.add("Guest details are required to proceed.", {
                type: "danger"
            });
            return;
        }
        this.props.close();
    }
}

export class GuestDetailsDialog extends Component {
    static template = "library_management.GuestDetailsDialog";
    static components = {Dialog};
    static props = {
        close: {type: Function},
        onConfirm: {type: Function},
        onPrevious: {type: Function},
        totalCount: {type: Number},
        initialGuestDetails: {type: Array, optional: true},
        is_required: { type: Boolean, optional: true },
    };

    setup() {
        this.pos = useService("pos");
        const initial = this.props.initialGuestDetails || [];
        const syncedGuests = Array.from({length: this.props.totalCount}, (_, i) => {
            return initial[i] ? initial[i] : {id: i + 1, age: 0, nationality: "", gender: ""};
        });
        this.state = useState({guests: syncedGuests});
        const rawCountries = this.pos.models["res.country"] || [];
        this.countries = rawCountries
            .filter(c => c.id !== undefined)
            .sort((a, b) => (a.name || "").localeCompare(b.name || ""));
    }

    _onConfirm() {
        this.props.onConfirm(this.state.guests);
        this.props.close();
    }

    _onPrevious() {
        this.props.onPrevious(this.state.guests);
        this.props.close();
    }

     _onSkip() {
        if (this.props.is_required) {
            this.env.services.notification.add("Guest details are required to proceed.", {
                type: "danger"
            });
            return;
        }
        this.props.close();
    }
}


// export class GuestDetailsDialog extends Component {
//     static template = "library_management.GuestDetailsDialog";
//     static components = { Dialog };
//
//     static props = {
//         close: { type: Function },
//         onSave: { type: Function },
//     };
//
//     setup() {
//         this.state = useState({
//             step: 1,
//             male: 0,
//             female: 0,
//             guests: [],
//         });
//     }
//
//     get totalCount() {
//         return (this.state.male || 0) + (this.state.female || 0);
//     }
//
//     _nextStep() {
//         if (this.totalCount > 0) {
//             this.state.guests = Array.from({ length: this.totalCount }, (_, i) => ({
//                 id: i + 1,
//                 age: "",
//                 nationality: "  ",
//                 gender: "",
//             }));
//             this.state.step = 2;
//         }
//     }
//
//     _onConfirm() {
//         this.props.onSave({
//             count: {
//                 male: this.state.male,
//                 female: this.state.female,
//                 total: this.totalCount
//             },
//             details: this.state.guests,
//         });
//         this.props.close();
//     }
// }
