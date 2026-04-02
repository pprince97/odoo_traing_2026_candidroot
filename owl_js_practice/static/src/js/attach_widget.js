import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { BinaryField, binaryField } from "@web/views/fields/binary/binary_field";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { CustomFileUpload } from "./custom_file_dialog";
import { useService } from "@web/core/utils/hooks"; // Added this

export class AttachInternalFiles extends BinaryField {
    static template = "owl_js_practice.attach_internal_files";

    setup() {
        super.setup();
        this.dialogService = useService("dialog");
    }

    async onBtnClick() {
        this.dialogService.add(CustomFileUpload, {
            title: "Select Attachments",
            confirm: () => {
//                this.props.fileUpload.xhr.abort();
            },
            close: ()=>{},
            confirmLabel: "✔️ Confirm",
            cancelLabel:"Cancel",
        });
    }
}

export const AttachInternalFilesItem = {
    ...binaryField,
    component: AttachInternalFiles,
};

registry.category("fields").add("internal_files", AttachInternalFilesItem);
