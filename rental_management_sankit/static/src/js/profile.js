/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.ProfileMenu = publicWidget.Widget.extend({
    selector:'#wrap',

     start() {
        console.log("Christmas Theme loaded 🎄");
        return this._super(...arguments);
    },
})