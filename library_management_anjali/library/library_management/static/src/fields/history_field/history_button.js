import { ImageField } from "@web/views/fields/image/image_field";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";

patch(ImageField.prototype, {

    setup() {
        super.setup();
        this.actionService = useService("action");
    },

    onHistoryClick() {
        console.log("Custom image button clicked!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>");
        this.actionService.doAction({
            name: 'Book Image History',
            type: 'ir.actions.act_window',
            res_model: 'library.image.history',
            views: [[false, "list"]],
            target: 'new'
        })
    },
});