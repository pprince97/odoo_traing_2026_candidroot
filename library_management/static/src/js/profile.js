/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";


publicWidget.registry.UserProfile = publicWidget.Widget.extend({
    selector: '#user_profile_form',

    start() {
        console.log("Christmas Theme loaded");
        console.log("Christmas loaded");
        console.log("Christmas Theme ");

//        const country = document.getElementById("inputCountry");
//        const state = document.getElementById("inputState");
//        const city = document.getElementById("inputCity");
//        const txt = document.getElementByID("h1_user")
//
//
//        txt.addEventListener("click", function() {
//            console.log("==========>", txt);
//        })

        return this._super(...arguments);
    }
});
