import { Component, useState } from "@odoo/owl";

export class CustomFileUpload extends Component {
    static props = {
        acceptedFiles: { type: String, optional: true },
        onChangeFileInput: { type: Function, optional: true  },
        selectFileLabel: { type: String, optional: true },
        close: { type: Function },
        confirm: { type: Function },
        send: { type: Function , optional: true },
        title: { type: String },
        confirmLabel: { type: String },
        cancelLabel: { type: String },
    };
    setup() {
        this.state = useState({
            files: [],          // Array of {id, name, type, url, size}
            selectedFile: null, // The file currently showing in the right pane
        });
        console.log('>>>>>>>>>>>>>>>>>>..')
    }
    static template = "owl_js_practice.CustomFileUpload";
}

//    static components = { FileUploader }; // Register the uploader component
//
//    setup() {
//        this.state = useState({
//            files: [],          // Array of {id, name, type, url, size}
//            selectedFile: null, // The file currently showing in the right pane
//        });
//    }
//
//    /**
//     * Logic when a new file is added via the FileUploader
//     */
//    async onFileUploaded(file) {
//        // Create a local URL for the preview (works for images/PDFs)
//        const fileUrl = URL.createObjectURL(file.data);
//
//        const newFile = {
//            id: Date.now(),
//            name: file.name,
//            type: file.type,
//            size: (file.size / 1024).toFixed(2) + " KB",
//            url: fileUrl,
//            data: file.data, // Raw data for saving later
//        };
//
//        this.state.files.push(newFile);
//        this.state.selectedFile = newFile; // Auto-select the newest file
//    }
//
//    /**
//     * Logic when user clicks a file in the left sidebar
//     */
//    onFileClick(file) {
//        this.state.selectedFile = file;
//    }
//
//    /**
//     * Optional: Logic for the 'Confirm' button to pass files back
//     */
//    onConfirm() {
//        this.props.confirm(this.state.files);
//        this.props.close();
//    }
//}