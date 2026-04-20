from odoo import http
from odoo.http import request


class BorrowController(http.Controller):

    @http.route('/my/booking', type='http', auth='user', website=True)
    def list_borrow_records(self, **kw):
        booking_records = []
        if request.env.user.has_group('car_rental_management_urvi.group_service_customer'):
            booking_records = request.env['car.rental.booking'].search([('customer_id', '=', request.env.user.partner_id.id)])
        elif request.env.user.has_group('car_rental_management_urvi.group_service_user'):
            booking_records = request.env['car.rental.booking'].search(['|',('customer_id', '=', request.env.user.partner_id.id),('driver_id','=', request.env.user.partner_id.id)])
        else:
            booking_records = request.env['car.rental.booking'].search([])
        return request.render('car_rental_management_urvi.booking_list_template',
                                  {'booking_records': booking_records})

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
