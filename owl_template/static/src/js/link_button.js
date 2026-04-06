import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {ConfirmationDialog} from "@web/core/confirmation_dialog/confirmation_dialog";
import {Component} from "@odoo/owl";
import {CustomDialog} from "./custom_dialog";

export class LinkButtonCustom extends Component {
    static template = "owl_template.linkbuttoncustom";


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

// this.props.record.model.config.context.default_res_ids
// this.props.record.model.config.context.default_model

export const linkButtonCustom = {
    component: LinkButtonCustom,
};
registry.category("fields").add("link_button", linkButtonCustom);

// async openConfirmDialog(recordId) {
//     // Fetch specific fields from the backend record
//     const [recordData] = await this.orm.read("your.model", [recordId], ["display_name", "some_field"]);
//
//     this.dialogService.add(ConfirmationDialog, {
//         title: "Confirm Action",
//         body: `Are you sure you want to process ${recordData.display_name}? Current value: ${recordData.some_field}`,
//         confirm: () => {
//             // Your logic here
//         },
//         cancel: () => {},
//     });
// }
