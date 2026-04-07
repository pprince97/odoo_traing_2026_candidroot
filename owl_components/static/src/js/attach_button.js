import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { CustomDialog } from "./custom_dialog";
import { useService } from "@web/core/utils/hooks";


export class AttachButtonWidgetComponent extends Component {

    static template = "owl_components.AttachButtonWidget";

    setup() {
        super.setup();
        this.dialogService = useService("dialog");
    }

    openCustomDialog() {
        this.dialogService.add(CustomDialog, {
            close: "Close Button",
        });
    }

}

export const attachButtonWidget = {
    component: AttachButtonWidgetComponent,
};

registry.category("fields").add("attach_button", attachButtonWidget);
