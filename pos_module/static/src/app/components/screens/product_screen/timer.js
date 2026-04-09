import { patch } from "@web/core/utils/patch";
import { Component, useState } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";

export class Timer extends Component {

    setup() {
        this.pos = usePos();
        this.state = useState({timer: ""});
    }



}