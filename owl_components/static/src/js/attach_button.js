import {registry} from "@web/core/registry";
import {Component} from "@odoo/owl";
import {AlertDialog} from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";


export class AttachButtonWidgetComponent extends Component {

    static template = "owl_components.AttachButtonWidget";

    setup() {
        super.setup();
    }

    onAttachClick() {
        console.log("Attach Button Clicked!");
        this.env.services.dialog.add(AlertDialog, {
            title: _t("Add Files Dialog"),
            body: _t("Body of dialog"),
        });
    }

}

export const attachButtonWidget = {
    component: AttachButtonWidgetComponent,

};

registry.category("fields").add("attach_button", attachButtonWidget);