/** @odoo-module **/
import { registry } from "@web/core/registry";
import { FormViewDialog } from "@web/views/view_dialogs/form_view_dialog";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";

/**
 * Step 1: Create an OWL component that will have a button
 */
class FormViewDialogTestButton extends Component {
    setup() {
        this.dialogService = useService("dialog");
        this.action = useService("action"); // needed to close action if required
    }

    openDialog() {
        this.dialogService.add(FormViewDialog, {
            resModel: "res.users", // model to open
            resId: 1,              // record id
            onRecordSaved: async (record) => {
                console.log("Record saved:", record);
                // example: close the dialog or perform an action
                await this.action.doAction({
                    type: "ir.actions.act_window_close",
                });
            },
        });
    }
}

// Step 2: Template for the button
FormViewDialogTestButton.template = "my_module.FormViewDialogButtonTemplate";

/**
 * Step 3: Register in the backend registry
 */
registry.category("views").add("my_form_dialog_button", FormViewDialogTestButton);