/** @odoo-module **/
//import publicWidget from "@web/legacy/js/public/public_widget";
//import { loadJS } from "@web/core/assets";
//publicWidget.registry.WebsiteCustomerContactRequestForm = publicWidget.Widget.extend({
//   selector: ".s_website_form_required",
//   init: function (parent, options) {
//       this._super.apply(this, arguments);
//      // Load Select2 dynamically (ensure it's included)
//    loadJS("https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.13/js/select2.min.js").then(() => {
//Const selects = document.querySelectorAll('.s_website_form_required select');
//          $(".s_website_form_required select").select2({
//            placeholder: "Select an option",
//        allowClear: true
//          });
//       }).catch(err => console.error("Error loading Select2:", err));
//


import { loadJS } from "@web/core/assets";
// Inside your widget/component
loadJS("https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.13/js/select2.min.js").then(() => {
    $(".advanced-select").select2({
        placeholder: "Search...",
        allowClear: true,
    });
});
