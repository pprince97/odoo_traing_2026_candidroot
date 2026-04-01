//import { BinaryField, binaryField } from "@web/views/fields/binary/binary_field";
//import { useService } from "@web/core/utils/hooks";
//import { patch } from "@web/core/utils/patch";
//////
//////
//patch(BinaryField.prototype, {
//    setup() {
//        this.actionService = useService("action");
//    }
////////
//    onHistoryClick() {
//        console.log("History button clicked", this);
//
////        this.actionService.doAction({
////            name: 'File Upload History',
////            type: 'ir.actions.act_window',
////            res_model: 'file.upload.history'
////            view_mode: 'list',
////            target: 'new',
//////            domain: [('book_id', '=', self.id)]
////        })
//
//    },
//});
////
////
////
import { ImageField } from "@web/views/fields/image/image_field";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";

patch(ImageField.prototype, {

    setup() {
        super.setup();
        this.actionService = useService("action");
    },

    onHistoryClick() {
        // Your logic here (e.g., calling a python method or showing a notification)
        console.log("Custom image button clicked!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>");
        this.actionService.doAction({
            name: 'Book Image History',
            type: 'ir.actions.act_window',
            res_model: 'library.image.history',
            views: [[false, "list"]],
            target: 'new',
            domain: [['book_id', '=', this.props.record.resId]]
        })


        // Example: Call a method on the current record
        // await this.props.record.save();
    },
});

//    // Add this to your module's assets or a script tag
//document.getElementById('add_line').addEventListener('click', function() {
//    var table = document.getElementById('borrow_lines_table').getElementsByTagName('tbody')[0];
//    var firstRow = table.getElementsByClassName('line_row')[0];
//    var newRow = firstRow.cloneNode(true);
//
//    // Clear inputs in the new row
//    var inputs = newRow.getElementsByTagName('input');
//    for (var i = 0; i < inputs.length; i++) { inputs[i].value = "1"; }
//
//    table.appendChild(newRow);
//});
//
//// Use event delegation for delete buttons
//document.addEventListener('click', function(e) {
//    if (e.target && (e.target.classList.contains('remove_line') || e.target.parentElement.classList.contains('remove_line'))) {
//        var rows = document.getElementsByClassName('line_row');
//        if (rows.length > 1) {
//            e.target.closest('tr').remove();
//        } else {
//            alert("At least one line is required.");
//        }
//    }
//});
