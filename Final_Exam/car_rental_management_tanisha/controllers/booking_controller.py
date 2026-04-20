from odoo.http import request
from odoo import http

class BookingController(http.Controller):

    @http.route('/my/rental-bookings', type="http", auth='user', website=True)
    def tile_rental_bookings(self):
        res_user_id = self.env['res.users'].context_get()['uid']
        res_user = self.env['res.users'].browse(res_user_id)
        if self.env.ref('car_rental_management_tanisha.group_car_rental_customer').id in res_user['group_ids'].ids:
            bookings = self.env['rental.booking'].search([('customer_id','=',res_user_id)])
            return request.render('car_rental_management_tanisha.car_rental_booking_list',{'bookings':bookings})
        elif self.env.ref('car_rental_management_tanisha.group_car_rental_manager').id in res_user['group_ids'].ids:
            bookings = self.env['rental.booking'].search([])
            return request.render('car_rental_management_tanisha.car_rental_booking_list',{'bookings':bookings})
        else:
            return request.render('car_rental_management_tanisha.car_rental_booking_list',{'bookings':[]})

    @http.route('/my/rental-booking/view', type="http", auth='user', website=True)
    def tile_rental_bookings_view(self):
        bookings = self.env['rental.booking'].search([])
        return request.render('car_rental_management_tanisha.car_rental_booking_report_view')

    @http.route('/booking/form', type="http", auth='user', website=True)
    def booking_form_template(self):
        return request.render('car_rental_management_tanisha.car_rental_booking_form_template')

    @http.route('/get/booking-details', type="jsonrpc", auth='user', website=True)
    def get_booking_details(self, values):
        return request.env['rental.booking'].create(values)
