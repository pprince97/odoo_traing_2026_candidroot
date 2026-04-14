import {Component, useState, onWillStart} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";
import {Dialog} from "@web/core/dialog/dialog";
import {dataUrlToBlob} from "@mail/core/common/attachment_uploader_hook";
import {useX2ManyCrud} from "@web/views/fields/relational_utils";

export class CustomDialog extends Component {
    static props = {
        data: Object,
        close: Function,
        record: Object,
    };
    static template = "owl_template_u.custom_dialog";
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
    }

    async loadAttachments() {
        this.state.attachments = await this.orm.searchRead(
            "ir.attachment",
            [
                ["res_model", "=", this.props.data.model],
                ["res_id", "in", this.props.data.ids]
            ],
            ["id", "name", "mimetype", 'datas']
        );
    }

    clear(ev) {
        const dataToSend = ev.currentTarget.parentElement.parentElement.querySelectorAll("input")
        for (let d of dataToSend) {
            d.checked = false
        }
    }


    async save(ev) {
        const dataToSend = ev.currentTarget.parentElement.parentElement.querySelectorAll("input")
        for (let d of dataToSend) {
            if (d.checked) {
                const att = this.state.attachments.find(att => att.id == d.value);
                const thread = await this.mailStore.Thread.insert({
                    model: this.props.data.model,
                    id: this.props.data.ids[0],
                });
                const file = new File([dataUrlToBlob(att.datas, att.mimetype)], att.name, {type: att.mimetype});
                const attachment = await this.attachmentUploadService.upload(thread, thread.composer, file);
                if (attachment) {
                    await this.operations.saveRecord([attachment.id]);
                }
            }
        }
        this.props.close();

    }
}
