import { DataServiceOptions } from "@point_of_sale/app/models/data_service_options";
import { patch } from "@web/core/utils/patch";

patch(DataServiceOptions.prototype, {
    get dynamicModels() {
        const models = super.dynamicModels;
        if (!models.includes("guest.details")) {
            models.push("guest.details");
        }
        return models;
    },
});


// import { DataServiceOptions } from "@point_of_sale/app/models/data_service_options";
// import { patch } from "@web/core/utils/patch";
//
// patch(DataServiceOptions.prototype, {
//
//     get dynamicModels() {
//         const models = super.dynamicModels;
//         console.log(models)
//         if (!models.includes("guest.details")) {
//             models.push("guest.details");
//             console.log("Hii")
//         }
//         return models;
//     }
// });
