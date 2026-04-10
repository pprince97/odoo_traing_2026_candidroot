import {registry} from "@web/core/registry";
import {Component} from "@odoo/owl";
import {CustomDialog} from "./custom_dialog.js";
import {useService} from "@web/core/utils/hooks";

export class AttachButtonWidgetComponent extends Component {

    static template = "library_management.AttachButtonWidget";

    static props = {
        "*": true,
    };

    setup() {
        super.setup();
        this.dialogService = useService("dialog");

    }

    openCustomDialog() {
        this.dialogService.add(CustomDialog, {
            record: this.props.record,
            data: {
                ids: this.props.record.model.config.context.default_res_ids,
                model: this.props.record.model.config.context.default_model
            },
        });
        // this.dialogService.add(CustomDialog, {
        //     confirm: () => {
        //         console.log("Confirmed!");
        //     },
        //     close: () => {
        //
        //     },
        // });
    }
}

export const attachButtonWidget = {
    component: AttachButtonWidgetComponent,
};

registry.category("fields").add("attach_button", attachButtonWidget);

