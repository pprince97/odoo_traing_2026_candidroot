import {patch} from "@web/core/utils/patch";
import {FormController} from "@web/views/form/form_controller";
import {AttachmentDialog} from "./attachment_dialog";

patch(FormController.prototype, {
    async beforeExecuteActionButton(params) {
        debugger
        if (params.name === "attachment_button") {
            const composerContext = this.props.context;
            const active_model = composerContext.default_model; //sale.order
            const active_id = composerContext.default_res_ids[0]; // sale order id
            await this.env.services.dialog.add(AttachmentDialog, {
                active_model,
                active_id,
                record : this.model.root,
                close: () => {}
            });
            return false;
        }
        return super.beforeExecuteActionButton(...arguments);
    }
});