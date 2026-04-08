import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {Component} from "@odoo/owl";
import {CustomDialog} from "./custom_dialog";

export class LinkButtonCustom extends Component {
    static template = "owl_template_u.linkbuttoncustom";


    setup() {
        super.setup();
        this.dialogService = useService("dialog");
    }

    ButtonClicked(ev) {
        this.dialogService.add(CustomDialog, {
            record: this.props.record,
            data: {
                ids: this.props.record.model.config.context.default_res_ids,
                model: this.props.record.model.config.context.default_model
            },
        });
        ev.currentTarget.blur();
    }

}

export const linkButtonCustom = {
    component: LinkButtonCustom,
};
registry.category("fields").add("link_button", linkButtonCustom);