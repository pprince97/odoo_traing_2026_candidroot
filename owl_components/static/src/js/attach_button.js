import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { CustomDialog } from "./custom_dialog";
import { useService } from "@web/core/utils/hooks";


export class AttachButtonWidgetComponent extends Component {

    static template = "owl_components.AttachButtonWidget";

    setup() {
        super.setup();
        this.dialogService = useService("dialog");
    }

    openCustomDialog() {
        this.dialogService.add(CustomDialog, {
            close: "Close Button",
        });
    }

}

export const attachButtonWidget = {
    component: AttachButtonWidgetComponent,
};

registry.category("fields").add("attach_button", attachButtonWidget);


// import {Component, onWillStart, useState} from "@odoo/owl";
//
// import {Dialog} from "@web/core/dialog/dialog";
//
// import {useService} from "@web/core/utils/hooks";
//
// export class CustomDialog extends Component {
//
//     static template = "library_management.CustomDialog";
//
//     static components = {Dialog};
//
//     // static props = {
//
//     //   confirm: { type: Function },
//
//     //   close: { type: Function },
//
//     // };
//
//     static props = {
//
//         data: Object,
//
//         close: Function,
//
//         record: Object,
//
//     };
//
//     setup() {
//
//         super.setup();
//
//         this.orm = useService("orm");
//
//         this.state = useState({
//
//             attachments: [],
//
//             selectedIds: new Set(),
//
//         });
//
//         onWillStart(async () => {
//
//             debugger
//
//             this.state.attachments = await this.orm.searchRead(
//
//                 "ir.attachment",
//
//                 [
//
//                     ["res_model", "=", this.props.data.model],
//
//                     ["res_id", "in", this.props.data.ids]
//
//                 ],
//
//                 ["id", "name", "mimetype", "datas"]
//
//             );
//
//             console.log('>>>>>>>>>>>>>>>>>>>>>>>>>>>> ',this.state.attachments);
//
//         });
//
//     }
//
//     toggleSelection(id) {
//
//         if (this.state.selectedIds.has(id)) {
//
//             this.state.selectedIds.delete(id);
//
//             console.log('>>>>>>>>>>>>>>>>>>>>>>>>>>>> Delete ');
//
//         } else {
//
//             this.state.selectedIds.add(id);
//
//             console.log('>>>>>>>>>>>>>>>>>>>>>>>>>>>> Add ');
//
//         }
//
//     }
//
//     async onSave() {
//
//         const ids = [...this.state.selectedIds];
//
//         console.log("Selected Attachments:", ids);
//
//         if (ids.length > 0 && this.props.record) {
//
//             console.log('>>>>>>>>>>>>>>>>>>>',this.props.record)
//
//             const commands = ids.map(id => [4, id]);
//
//             await this.props.record.update({
//
//                 attachment_ids: commands
//
//             });
//
//             await this.props.record.save();
//
//         }
//
//         this.props.close();
//
//     }
//












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
