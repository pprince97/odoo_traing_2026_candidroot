// import { PosDataModel } from "@point_of_sale/app/models/pos_data_model";
// import { register_model } from "@point_of_sale/app/models/pos_data_model";
//
// class PosOrderGuest extends PosDataModel {
//     _serialize() {
//         return {
//             age: this.age,
//             gender: this.gender,
//             nationality_id: this.nationality_id,
//             pos_order_uuid: this.pos_order_uuid,
//             uuid: this.uuid, // Odoo 19 requires the record's own UUID too
//         };
//     }
// }
//
// // Make sure it's registered
// register_model("pos.order.guest", PosOrderGuest);