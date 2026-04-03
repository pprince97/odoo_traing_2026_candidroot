import { registry } from "@web/core/registry";
import { BinaryField, binaryField } from "@web/views/fields/binary/binary_field";
import { CustomFileUpload } from "./custom_file_dialog";
import { useService } from "@web/core/utils/hooks"; // Added this

export class AttachInternalFiles extends BinaryField {
    static template = "owl_js_practice.attach_internal_files";

    setup() {
        super.setup();
        this.dialogService = useService("dialog");
    }

    async onBtnClick() {
    debugger
        this.dialogService.add(CustomFileUpload, {
            title: "Select Attachments",
            resModel: this.props.record.model.config.context.default_model,
            resId: this.props.record.model.config.context.default_res_ids,
            close: ()=>{},
            record: this.props.record,
        });
    }
}

export const AttachInternalFilesItem = {
    ...binaryField,
    component: AttachInternalFiles,
};

registry.category("fields").add("internal_files", AttachInternalFilesItem);
