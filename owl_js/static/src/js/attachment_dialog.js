import {Component, useState} from "@odoo/owl";
import {Dialog} from "@web/core/dialog/dialog";

export class AttachmentDialog extends Component {
    static props = {
        active_model: {type: String, required: true},
        active_id: {type: Number, required: true},
        // wizard_id: {type: Number, required: true},
        close: {type: Function, required: true},
    };
    static components = {Dialog}
    static template = "owl_js.AttachmentDialog";

    setup() {
        this.state = useState({
            attachments: [],
            selected: new Set(),
        });
        this.loadAttachments();
    }

    async loadAttachments() {
        const {active_model, active_id} = this.props;

        const result = await this.env.services.orm.call(
            "mail.compose.message",
            "get_record_attachments",
            [active_model, active_id]
        );
        this.state.attachments = result;
    }

    toggleSelection(id) {
        if (this.state.selected.has(id)) {
            this.state.selected.delete(id);
            console.log("Remove");
        } else {
            this.state.selected.add(id);
            console.log("Add");
        }
    }

    async confirm() {
        console.log("ACTIVE ID:", this.props.resId);
        await this.env.services.orm.call(
            "mail.compose.message",
            "add_selected_attachments",
            [this.props.wizard_id, [...this.state.selected]]  // ✅ correct
        );
        this.props.close();
    }
}