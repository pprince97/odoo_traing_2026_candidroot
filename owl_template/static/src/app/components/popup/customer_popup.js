import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class CutomerInfoPopup extends Component {
    static props = {
        order: Object,
        close: Function,
    };
    static template = "pos_restaurant.CutomerInfoPopup";
    static components = {
        Dialog
    };

    setup() {

        // onWillStart(async () => {
        //     await this.loadAttachments();
        // });
        console.log('custom dialog setup')
    }

//     async loadAttachments() {
//         // Example: fetching for a specific record passed via props
//         this.state.attachments = await this.orm.searchRead(
//             "ir.attachment",
//             [
//                 ["res_model", "=", this.props.data.model],
//                 ["res_id", "in", this.props.data.ids]
//             ],
//             ["id", "name", "mimetype",'datas']
//         );
//         console.log(this.state.attachments[0])
//     }
//
//     clear(ev) {
//         const dataToSend = ev.currentTarget.parentElement.parentElement.querySelectorAll("input")
//         for(let d of dataToSend) {
//             d.checked = false
//         }
//         // this.props.close();
//     }
//
//
    async save(ev) {
//         const dataToSend = ev.currentTarget.parentElement.parentElement.querySelectorAll("input")
//         for(let d of dataToSend){
//             if (d.checked){
//                 const att = this.state.attachments.find(att => att.id == d.value);
//                 const thread = await this.mailStore.Thread.insert({
//                     model: this.props.data.model,
//                     id: this.props.data.ids[0],
//                 });
//                 // const t=att.mimetype
//                 const file = new File([dataUrlToBlob(att.datas, att.mimetype)], att.name, {type:att.mimetype});
//                 const attachment = await this.attachmentUploadService.upload(thread, thread.composer, file);
//                 if (attachment) {
//                     await this.operations.saveRecord([attachment.id]);
//                 }
//             }
//         }
        debugger
        console.log('>>>>>>>>>>>>>>>>',this.props.order)
        this.props.order.general_customer_note += "2156496103"
        this.props.close();
}
}
