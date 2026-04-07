import { Component, useState, onWillStart } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";


export class CustomDialog extends Component {

    static template = "owl_components.CustomDialog";
    static components = { Dialog };
    static props = {
        close: Function,
    }

    setup() {
        this.orm = useService("orm");
        this.state = useState({
            selectFile: false,
            // selectedAttachmentId: attachment?.id || false,
        });
        super.setup();
        onWillStart(async () => {
            debugger
            console.log("Before", this.orm);
            this.attachments = await this.orm.searchRead(
                "ir.attachment",
                [
                    ["res_model", "=", this.props.resModel],
                    ["res_id", "=", this.props.resId],
                    // ["mimetype", "ilike", "image"],
                ],
                // ["id"]
            );
            // console.log("Attachments", this.attachments);
            // this.state.selectFile = this.props.autoOpen && this.attachments.length;
        });
    }

}
