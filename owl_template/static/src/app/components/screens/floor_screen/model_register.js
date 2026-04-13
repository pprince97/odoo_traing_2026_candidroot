// import { registry } from "@web/core/registry";
// import { Base } from "@point_of_sale/app/models/related_models";
// // import { PosSession } from "@point_of_sale/../tests/unit/data/pos_session.data";
// import { patch } from "@web/core/utils/patch";
// // import { PosOrder } from "@point_of_sale/app/models/pos_order";
//
//
// export class PosGuest extends Base {
//     static pythonModel = "pos.guest";
//     static fields = ["id", "age", "gender", "country_id", "order_id"];
//
//     setup(vals) {
//         return super.setup(vals);
//     }
// }
// registry.category("pos_available_models").add(PosGuest.pythonModel, PosGuest);
//
// // PosOrder.fields.push({
// //     name: "guest_ids",
// //     model: "pos.guest",
// //     multi: true
// // });
//
// // patch(PosOrder, {
// //     get fields() {
// //         const result = super.fields;
// //         // Check if already added to prevent infinite loops/duplicates
// //         if (!result.find(f => f.name === "guest_ids")) {
// //             result.push({ name: "guest_ids", model: "pos.guest", multi: true });
// //         }
// //         return result;
// //     }
// // });
//
//
//
// // patch(PosSession.prototype, {
// //     _load_pos_data_models() {
// //         return [
// //             ...super._load_pos_data_models(),
// //             "pos.guest"
// //         ];
// //     },
// // });
// //
//
//
//
// // import { PosDataModel } from "@point_of_sale/app/models/pos_data_model";
// // import { register_model } from "@point_of_sale/app/models/pos_data_model";
// //
// // class PosGuest extends PosDataModel {
// //     // This is the missing piece causing your error
// //     _serialize() {
// //         return {
// //             age: this.age,
// //             gender: this.gender,
// //             nationality_id: this.nationality_id,
// //             pos_order_uuid: this.pos_order_uuid,
// //             uuid: this.uuid, // Odoo 19 requires the record's own UUID too
// //         };
// //     }
// // }
// //
// // // Make sure it's registered
// // register_model("pos.order.guest", PosOrderGuest);
