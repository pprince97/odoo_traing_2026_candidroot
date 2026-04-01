/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.CustomPopUp = publicWidget.Widget.extend({
    selector: '#wrap',

    start() {
        console.log("Custom pop up loaded");
        let showbtn = document.getElementById("showbtn");
        // To access the Close button element
        let closebtn = document.getElementById("closebtn");

        // To acces the popup element
        let popup = document.querySelector(".popup");


        // To show the popup on click
        showbtn.addEventListener("click", () => {
            popup.style.display = "block";
            showbtn.style.display = "none";
        });

        // To close the popup on click
        closebtn.addEventListener("click", () => {
            popup.style.display = "none";
            showbtn.style.display = "block";
        });
        return this._super(...arguments);
    },
})