/** @odoo-module **/

import {FormController} from "@web/views/form/form_controller";
import {MyAttachmentDialog} from "./button_attachment";

console.log("the mail ");
import {patch} from "@web/core/utils/patch";
import {AlertDialog} from "@web/core/confirmation_dialog/confirmation_dialog";
import {Dialog} from "@web/core/dialog/dialog";
import {useService} from "@web/core/utils/hooks";
import {onMounted} from "@odoo/owl";

patch(FormController.prototype, {
    setup() {
        console.log("This is Set Up");
        super.setup();
        // Correct way to get the dialog service in Odoo 19
        this.dialogService = useService("dialog");
        console.log("This is Dialog Box");

        onMounted(() => {
            const btn = document.querySelector('.o_custom_dialog_btn');
            if (btn) {
                btn.addEventListener('click', (ev) => {
                    // Stop Odoo from trying to handle this as a standard action
                    ev.preventDefault();
                    ev.stopImmediatePropagation();
                    this.openMyDialog();
                });
            }
        });
    },

    openMyDialog() {
        console.log("Opening dialog...");
        this.dialogService.add(MyAttachmentDialog, {});
    }
});
