from odoo import http
from odoo.http import request


class BorrowController(http.Controller):

    @http.route('/my/booking', type='http', auth='user', website=True)
    def list_borrow_records(self, **kw):
        booking_records = []
        if request.env.user.has_group('car_rental_management_urvi.group_service_admin'):
            booking_records = request.env['car.rental.booking'].search([])
        elif request.env.user.has_group('car_rental_management_urvi.group_service_user'):
            booking_records = request.env['car.rental.booking'].search([('customer_id', '=', request.env.user.partner_id.id)])
        else:
            booking_records = request.env['car.rental.booking'].search([('customer_id', '=', request.env.user.partner_id.id)])
        return request.render('car_rental_management_urvi.booking_list_template',
                                  {'booking_records': booking_records})

    @http.route('/my/booking/<int:record_id>', auth='user', website=True)
    def display_borrow_record(self, record_id):
        booking_record = request.env['car.rental.booking'].browse(record_id)
        if not booking_record.exists():
            return request.render('website.404')
        return request.render('car_rental_management_urvi.booking_record_view_template', {
            'record': booking_record
        })

    @http.route('/create/booking', type='http', auth="user", website=True)
    def borrow_form(self, **kwargs):
        drivers = request.env['res.partner'].search([('is_driver', '=', True)])
        vehicles = request.env['product.product'].search([('type', '=', 'vehicle')])
        return request.render("car_rental_management_urvi.create_booking_request_template", {
            'drivers': drivers,
            'vehicles': vehicles,
        })

    @http.route('/report/download/<int:record_id>', type='http', auth="user")
    def download_report(self, record_id, **kwargs):
        report_action = request.env.ref('sale.action_report_saleorder')
        pdf_content, _ = report_action._render_qweb_pdf('car_rental_management_urvi.action_report_booking_receipt',
                                                        [record_id])
        pdf_http_headers = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf_content)),
            ('Content-Disposition', 'attachment; filename="report.pdf";')
        ]
        return request.make_response(pdf_content, headers=pdf_http_headers)

    @http.route('/save/booking', type='http', auth="public", methods=['POST'], website=True)
    def submit_booking(self, **post):
        vehicle_ids = request.httprequest.form.getlist('vehicle_id')
        driver_ids = request.httprequest.form.getlist('driver_id')
        start_kms = request.httprequest.form.getlist('start_km')
        end_kms = request.httprequest.form.getlist('end_km')

        booking_lines = []
        for i in range(len(vehicle_ids)):
            if vehicle_ids[i]:  # Ensure a vehicle was actually selected
                booking_lines.append((0, 0, {
                    'vehicle_id': int(vehicle_ids[i]),
                    'driver_id': int(driver_ids[i]),
                    'start_km': float(start_kms[i] or 0),
                    'end_km': float(end_kms[i] or 0),
                }))

        booking_vals = {
            'customer_id': request.env.user.partner_id.id,
            'start_date': post.get('start_date'),
            'end_date': post.get('end_date'),
            'trip_details': post.get('trip_details'),
            'state': 'draft',
            'booking_lines': booking_lines,
        }

        new_booking = request.env['car.rental.booking'].create(booking_vals)
        return request.redirect('/my/booking')
