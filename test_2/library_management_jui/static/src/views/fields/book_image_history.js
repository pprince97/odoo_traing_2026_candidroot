/** @odoo-module **/

import { registry } from "@web/core/registry";
import { BinaryField, binaryField } from "@web/views/fields/binary/binary_field";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";

patch(BinaryField.prototype, {
    setup() {
        super.setup();
        this.actionService = useService("action");
    },

    onHistoryClick() {
//        console.log("History button clicked");
        this.actionService.doAction({
            name: 'File Upload History',
            type: 'ir.actions.act_window',
            res_model: 'library.book.history',
            view_mode: [[false,'list']],
            target: 'new'
        })
    },
});