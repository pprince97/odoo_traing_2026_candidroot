/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Dialog } from "@web/core/dialog/dialog";

document.addEventListener("click", function (ev) {
    if (ev.target.classList.contains("open-second-wizard")) {

        const dialog = new Dialog(null, {
            title: "Second Wizard",
            body: "<div>Second popup content here</div>",
            buttons: [
                { text: "Close", close: true }
            ],
        });

        dialog.open();
    }
});