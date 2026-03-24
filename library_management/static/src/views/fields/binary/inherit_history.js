/** @odoo-module **/

import { BinaryField } from "@web/views/fields/binary/binary_field";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";

patch(BinaryField.prototype, {
    setup() {
        super.setup();
        this.action = useService("action");
    },

    async onHistoryClick() {
        console.log("History button clicked: ", this.props.record.resId)

        const recordId = this.props.record.resId;

        await this.action.doAction({
            type: "ir.actions.act_window",
            name: "File History",
            res_model: "file.upload.history",
            views: [[false, "list"]],
            view_mode: "list",
            target: "new",
            domain: [["book_id", "=", recordId]],
        });
    },
});