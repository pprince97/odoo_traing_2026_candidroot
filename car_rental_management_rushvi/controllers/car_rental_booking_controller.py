from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.fields import Domain

class CarRentalPortal(CustomerPortal):

    @http.route(['/my/my-car/download/<int:booking_id>'], type='http', auth="public", website=True)
    def download_sale_order_report(self, booking_id, access_token=None, **kw):
        try:
            booking = self._document_check_access('car.rent.booking', booking_id, access_token=access_token)
        except Exception:
            return request.redirect('/my/home')
        return self._show_report(
            model=booking,
            report_type='pdf',
            report_ref='car_rental_management_rushvi.action_report_car_booking',
            download=True
        )

    @http.route(['/my/car-rentals'], type='http', auth='user', website=True)
    def view_my_car_rentals(self):
        car_rentals = request.env['car.rent.booking'].search([])
        return request.render('car_rental_management_rushvi.car_rentals_template', {
            'car_rentals': car_rentals,
            'user': request.env.user,
            'car_rentals_count': len(car_rentals),
            'page_name': 'car_rental',
        })

    @http.route(['/my/car-rentals/<int:id>'], type='http', auth='user', website=True)
    def view_borrow_request_form(self, id, **post):
        car_rental = request.env['car.rent.booking'].sudo().browse(id)
        return request.render('car_rental_management_rushvi.car_rentals_template_form', {
            'car_rental': car_rental,
            'page_name': 'car_rental',
            'car_rentals_lines': car_rental.booking_vehicle_ids,
            'user': request.env.user,
        })

    @http.route('/my/car-rentals/create', type='http', auth='public', methods=['POST'], website=True)
    def create_car_rentals(self, **post):
        vals = {
            'trip_start_date': post.get('trip_start_date'),
            'trip_end_date': post.get('trip_end_date'),
            'state': 'draft',
            'trip_details': post.get('trip_description'),
            'customer_id': request.env.user.partner_id.id,
        }
        request.env['car.rent.booking'].create(vals)
        return request.redirect('/my/car-rentals')

    @http.route(['/my/car-rental-request/'],type='http', auth='public', website=True)
    def redirect_to_form(self):
        return request.render('car_rental_management_rushvi.car_rental_request',{
            'user': request.env.user,
        })