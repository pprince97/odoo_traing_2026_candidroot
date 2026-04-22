import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.carRentalBookingForm = publicWidget.Widget.extend({
    selector: '#car_rental_booking_form',
    events: {
        'change #rent_date': '_onDateChange',
        'change #return_date': '_onDateChange',
        'change #new_start_km': '_onKmChange',
        'change #new_end_km': '_onKmChange',
    },
    start() {
        console.log("_______________");
        return this._super.apply(this, arguments);
    },

    async _onKmChange() {
        const startKm =parseInt(this.$('#new_start_km').val())
        const endKm =parseInt(this.$('#new_end_km').val())
        if(startKm < 0){
            alert("Start Km cannot be negative")
            this.$('#new_start_km').val("");
        }
        if(endKm < 1){
            alert("End Km cannot be 0 or less than 0")
            this.$('#new_end_km').val("");
        }
        if(endKm < startKm){
            alert("End Km cannot be smaller than Start Km")
            this.$('#new_end_km').val("");
        }
    },

    async _onDateChange() {
        const rentDateStr =this.$('#rent_date').val()
        const returnDateStr =this.$('#return_date').val()
        let rentDate = null
        let returnDate = null
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        if (rentDateStr){
            rentDate = new Date(rentDateStr);
            if (rentDate < today) {
                alert("Rent date cannot be in the past");
                this.$('#rent_date').val("");
            }
        }
        if(returnDateStr){
            returnDate = new Date(returnDateStr);
            if(returnDate < today){
                alert("Return date cannot be in the past");
                this.$('#return_date').val("");
            }
        }
        if (rentDate && returnDate){
            if (rentDate >= returnDate) {
                alert("Rent date must be earlier than the return date");
                this.$('#rent_date').val("");
                this.$('#return_date').val("");
            } else {
                const formattedRentDate = rentDate.toISOString().split('T')[0];
                const formattedReturnDate = returnDate.toISOString().split('T')[0];
                const result = await rpc("/availability/domain/filter", {
                    rent_date_s: formattedRentDate,
                    return_date_s: formattedReturnDate,
                });
                let vehicles = result.available_vehicles;
                let select_veh = document.querySelector('select[name="new_vehicle_id"]');
                select_veh.innerHTML = '<option value="">Select Vehicle...</option>';
                vehicles.forEach(veh => {
                    let option = document.createElement('option');
                    option.value = veh.id;
                    option.text = veh.display_name;
                    select_veh.appendChild(option);
                });
                let drivers = result.available_drivers;
                let select_driver = document.querySelector('select[name="new_driver_id"]');
                select_driver.innerHTML = '<option value="">Select Driver...</option>';
                drivers.forEach(driver => {
                    let option = document.createElement('option');
                    option.value = driver.id;
                    option.text = driver.display_name;
                    select_driver.appendChild(option);
                });
            }
        }
    },
})