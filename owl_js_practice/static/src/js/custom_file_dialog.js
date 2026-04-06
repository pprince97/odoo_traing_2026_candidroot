import { Component, useState,onWillStart } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";
import { dataUrlToBlob } from "@mail/core/common/attachment_uploader_hook";
import { useX2ManyCrud } from "@web/views/fields/relational_utils";

export class CustomFileUpload extends Component {
    static template = "owl_js_practice.custom_file_upload";
    static components = { Dialog };
    static props = {
        title: {
            validate: (m) => {
                return (
                    typeof m === "string" ||
                    (typeof m === "object" && typeof m.toString === "function")
                );
            },
            optional: true,
        },
        acceptedFiles: { type: String, optional: true },
        close: Function,
        resModel: String,
        resId: Array,
        record: Object,
    };

    setup() {
        this.state = useState({
            files: [],
            selectedFileId: null,
            previewUrl: null,
            previewType: null,
        });

        this.mailStore = useService("mail.store");
        this.attachmentUploadService = useService("mail.attachment_upload");
        this.operations = useX2ManyCrud(() => {
            return this.props.record.data["attachment_ids"];
        }, true);

        onWillStart(async () => {
            this.state.files = await rpc("/web/dataset/call_kw/ir.attachment/search_read", {
                model: "ir.attachment",
                method: "search_read",
                args: [[
                    ["res_model", "=", this.props.record.model.config.context.default_model],
                    ["res_id", "in", this.props.record.model.config.context.default_res_ids],
                ]],
                kwargs: {
                    fields: ["name", "res_model", "res_id", "mimetype", "create_date","datas"],
                    order: "create_date desc",
               },
            });
        });
    }

    async selectFile(file) {
        this.state.selectedFileId = file.id;
        this.state.previewType = file.mimetype.includes('image') ? 'image' : 'pdf';
        this.state.previewUrl = `data:${file.mimetype};base64,${file.datas}`;
    }

    async onConfirm(ev) {
        for (const rec of ev.currentTarget.parentElement.parentElement.querySelectorAll('input')) {
            if(rec.checked){
                for(let file of this.state.files){
                    if(rec.value == file.id){
                        const thread = await this.mailStore.Thread.insert({
                            model: this.props.record.model.config.context.default_model,
                            id: this.props.record.model.config.context.default_res_ids[0],
                        });
                        const file_s = new File([dataUrlToBlob(file.datas, file.mimetype)], file.name, { type: file.mimetype });
                        const attachment = await this.attachmentUploadService.upload(thread, thread.composer, file_s);
                        if (attachment) {
                            await this.operations.saveRecord([attachment.id]);
                        }
                    }
                }
            }
        }
        this.props.close();
    }
}