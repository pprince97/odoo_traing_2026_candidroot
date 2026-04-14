/** @odoo-module **/

import { registry } from "@web/core/registry";
import { patch } from "@web/core/utils/patch";

const messagingRegistry = registry.category("mail.composer");


for (const comp of messagingRegistry.getAll()) {

    patch(comp.prototype, {
        setup() {
            super.setup();
        },

        mounted() {
            super.mounted();
            const actions = this.el.querySelector(".o-mail-Composer-actions");


            if (actions && !actions.querySelector(".my_attach_btn")) {
                const btn = document.createElement("button");
                btn.innerText = "Attach Files";
                btn.className = "btn btn-secondary my_attach_btn";

                btn.onclick = () => {
                };

                actions.appendChild(btn);
            }
        },
    });
}