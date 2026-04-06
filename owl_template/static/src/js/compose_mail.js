/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Composer } from "@mail/components/composer/composer";

patch(Composer.prototype, "custom_attachment_button", {
    mounted() {
        super.mounted();

        const btn = this.el.querySelector(".o_custom_attach_btn");
        if (btn) {
            btn.addEventListener("click", () => {
                this.openFileDialog();
            });
        }
    },

    openFileDialog() {
        const input = document.createElement("input");
        input.type = "file";
        input.multiple = true;

        input.onchange = async (ev) => {
            const files = ev.target.files;

            for (let file of files) {
                console.log("Selected file:", file);

                // OPTIONAL: upload to existing Odoo route
                await this.uploadFile(file);
            }
        };

        input.click();
    },

    async uploadFile(file) {
        const formData = new FormData();
        formData.append("ufile", file);

        await fetch("/web/binary/upload_attachment", {
            method: "POST",
            body: formData,
        });
    },
});