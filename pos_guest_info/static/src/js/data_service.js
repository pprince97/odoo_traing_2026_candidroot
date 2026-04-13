
import {DataServiceOptions} from "@point_of_sale/app/models/data_service_options";
import {patch} from "@web/core/utils/patch";
patch(DataServiceOptions.prototype, {
    get dynamicModels() {
        const models = super.dynamicModels;
        console.log("CAlled dataservice for push", models)
        if (!models.includes("guest.detail")) {
            models.push("guest.detail");
        }
        console.log("CAlled dataservice", models)
        return models;
    }
});

