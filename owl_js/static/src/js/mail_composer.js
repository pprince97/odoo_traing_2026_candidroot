import {patch} from "@web/core/utils/patch";
import {FormController} from "@web/views/form/form_controller";
import {AttachmentDialog} from "./attachment_dialog";

patch(FormController.prototype, {
    async beforeExecuteActionButton(params) {
        if (params.name === "attachment_button") {
            const composerContext = this.props.context;
            const active_model = composerContext.default_model;
            const active_id = composerContext.default_res_ids[0];
            await this.env.services.dialog.add(AttachmentDialog, {
                active_model,
                active_id,
                // wizard_id: this.props.resId[0],
                close: () => {}
            });
            return false;
        }
        return super.beforeExecuteActionButton(...arguments);
    }
});

// this.env.services.dialog.close()