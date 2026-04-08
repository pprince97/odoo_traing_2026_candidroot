/** @odoo-module **/

import { registry } from "@web/core/registry";
import { patch } from "@web/core/utils/patch";

console.log("PATCH START ✅");

// get messaging components registry
const messagingRegistry = registry.category("mail.composer");

console.log("REGISTRY:", messagingRegistry);

// patch ALL registered composers
for (const comp of messagingRegistry.getAll()) {
    console.log("Patching:", comp);

    patch(comp.prototype, {
        setup() {
            super.setup();
            console.log("Composer patched ✅");
        },

        mounted() {
            super.mounted();

            console.log("Mounted working ✅");
            const actions = this.el.querySelector(".o-mail-Composer-actions");

            console.log("actions working ✅", actions);

            if (actions && !actions.querySelector(".my_attach_btn")) {
                const btn = document.createElement("button");
                btn.innerText = "Attach Files";
                btn.className = "btn btn-secondary my_attach_btn";

                btn.onclick = () => {
                    console.log("BUTTON CLICKED ✅");
                };

                actions.appendChild(btn);
            }
        },
    });
}