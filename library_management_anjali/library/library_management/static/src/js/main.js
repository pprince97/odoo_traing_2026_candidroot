/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.CustomJS = publicWidget.Widget.extend({
    selector: '.container',

    start() {
        console.log("JS loaded...");
        return this._super(...arguments);
    },
});