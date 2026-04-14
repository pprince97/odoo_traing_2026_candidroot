import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import { dataUrlToBlob } from "@mail/core/common/attachment_uploader_hook";
import { useX2ManyCrud } from "@web/views/fields/relational_utils";

export class CustomDialog extends Component {
    static props = {
        data : Object,
        close: Function,
        record: Object,
    };
    static template = "owl_template.custom_dialog";
    static components = {
        Dialog
    };

    setup() {
        this.orm = useService("orm");
        this.state = useState({
            attachments: [],
        });
        this.mailStore = useService("mail.store");
        this.attachmentUploadService = useService("mail.attachment_upload");
        this.operations = useX2ManyCrud(() => {
            return this.props.record.data["attachment_ids"];
        }, true);

        onWillStart(async () => {
            await this.loadAttachments();
        });
        console.log('custom dialog setup')
    }

    async loadAttachments() {
        // Example: fetching for a specific record passed via props
        this.state.attachments = await this.orm.searchRead(
            "ir.attachment",
            [
                ["res_model", "=", this.props.data.model],
                ["res_id", "in", this.props.data.ids]
            ],
            ["id", "name", "mimetype",'datas']
        );
        console.log(this.state.attachments[0])
    }
    
    clear(ev) {
        const dataToSend = ev.currentTarget.parentElement.parentElement.querySelectorAll("input")
        for(let d of dataToSend) {
            d.checked = false
        }
        // this.props.close();
    }


    async save(ev) {
        const dataToSend = ev.currentTarget.parentElement.parentElement.querySelectorAll("input")
        for(let d of dataToSend){
            if (d.checked){
                const att = this.state.attachments.find(att => att.id == d.value);
                const thread = await this.mailStore.Thread.insert({
                    model: this.props.data.model,
                    id: this.props.data.ids[0],
                });
                // const t=att.mimetype
                const file = new File([dataUrlToBlob(att.datas, att.mimetype)], att.name, {type:att.mimetype});
                const attachment = await this.attachmentUploadService.upload(thread, thread.composer, file);
                if (attachment) {
                    await this.operations.saveRecord([attachment.id]);
                }
            }
        }
        this.props.close();

        // async onSave() {
        // const ids = [...this.state.selectedIds];
        // console.log("Selected Attachments:", ids);
        // if (ids.length > 0 && this.props.record) {
        //     console.log('>>>>>>>>>>>>>>>>>>>',this.props.record)
        //     const commands = ids.map(id => [4, id]);
        //     await this.props.record.update({
        //         attachment_ids: commands
        //     });
        //     await this.props.record.save();
        // }
        // this.props.close();
    // }


//         async selectFile(file) {
//         this.state.selectedFileId = file.id;
//         this.state.previewType = file.mimetype.includes('image') ? 'image' : 'pdf';
//         this.state.previewUrl = `data:${file.mimetype};base64,${file.datas}`;
//     }
// <div class="w-60 p-2 d-flex align-items-center justify-content-center bg-light">
//                     <t t-if="state.previewUrl">
//                         <img t-if="state.previewType === 'image'" t-att-src="state.previewUrl" class="img-fluid border"/>
//                         <iframe t-else="" t-att-src="state.previewUrl" class="w-100 h-100 border"/>
//                     </t>
//                     <t t-else="">
//                         <span class="text-muted">Select a file to preview</span>
//                     </t>
//                 </div>
//             selectedFileId: null,
//


    //     toggleSelection(id) {
    //     if (this.state.selected.has(id)) {
    //         this.state.selected.delete(id);
    //         console.log("Remove");
    //     } else {
    //         this.state.selected.add(id);
    //         console.log("Add");
    //     }
    // }
}
}
