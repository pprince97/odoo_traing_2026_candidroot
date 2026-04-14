/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.IndiaTheme = publicWidget.Widget.extend({
    selector: '#wrap',

    start() {

        return this._super(...arguments);
    }
});