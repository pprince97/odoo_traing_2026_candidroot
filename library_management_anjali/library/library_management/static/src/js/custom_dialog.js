import {Component, onWillStart, useState} from "@odoo/owl";
import {Dialog} from "@web/core/dialog/dialog";
import {useService} from "@web/core/utils/hooks";

export class CustomDialog extends Component {

    static template = "library_management.CustomDialog";
    static components = {Dialog};

    // static props = {
    //   confirm: { type: Function },
    //   close: { type: Function },
    // };
    static props = {
        data: Object,
        close: Function,
        record: Object,
    };

    setup() {
        super.setup();
        this.orm = useService("orm");
        this.state = useState({
            attachments: [],
            selectedIds: new Set(),
        });

        onWillStart(async () => {
            debugger
            this.state.attachments = await this.orm.searchRead(
                "ir.attachment",
                [
                    ["res_model", "=", this.props.data.model],
                    ["res_id", "in", this.props.data.ids]
                ],
                ["id", "name", "mimetype", "datas"]
            );
            console.log('>>>>>>>>>>>>>>>>>>>>>>>>>>>> ',this.state.attachments);
        });
    }

    toggleSelection(id) {
        if (this.state.selectedIds.has(id)) {
            this.state.selectedIds.delete(id);
            console.log('>>>>>>>>>>>>>>>>>>>>>>>>>>>> Delete ');
        } else {
            this.state.selectedIds.add(id);
            console.log('>>>>>>>>>>>>>>>>>>>>>>>>>>>> Add ');
        }
    }

    async onSave() {
        const ids = [...this.state.selectedIds];
        console.log("Selected Attachments:", ids);
        if (ids.length > 0 && this.props.record) {
            console.log('>>>>>>>>>>>>>>>>>>>',this.props.record)
            const commands = ids.map(id => [4, id]);
            await this.props.record.update({
                attachment_ids: commands
            });
            await this.props.record.save();
        }
        this.props.close();
    }








    // async onSave() {
    //     // const selectedList = this.state.attachments.filter(a =>
    //     //     this.state.selectedIds.has(a.id)
    //     // );
    //     const selectedIds = Array.from(this.state.selectedIds);
    //     console.log("Selected Attachments:", selectedIds);
    //     if (selectedIds.length > 0 && this.props.record) {
    //         const resModel = this.props.record.data.res_model;
    //         const resId = this.props.record.data.res_id;
    //         await this.orm.write("ir.attachment", selectedIds, {
    //             res_model: resModel,
    //             res_id: resId,
    //         });
    //         console.log('>>>>>>>>>>>>>>>>>>>>>>>>>>>> 1 ',resModel);
    //         console.log('>>>>>>>>>>>>>>>>>>>>>>>>>>>> 2 ',resId);
    //
    //         const commands = selectedIds.map(id => [4, id]);
    //         await this.props.record.update({
    //             attachment_ids: commands
    //         });
    //     }
    //     this.props.close();
    // }
}