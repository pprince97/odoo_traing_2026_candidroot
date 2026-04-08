import { Component, useState, onWillStart } from "@odoo/owl";


export class GuestDetailsDialog extends Component {

    static template = "pos_custom_tanisha.GuestDetailsDialog";
    
    setup() {
        super.setup();
        console.log("GuestDialog: setup called");
    }

}
