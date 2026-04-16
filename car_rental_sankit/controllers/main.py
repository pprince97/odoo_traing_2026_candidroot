from odoo import http, models, fields, tools, api , _
from odoo.http import request


class WebsiteDetail(http.Controller):

    @http.route('/booking', type='http', auth='public', website=True)
    def rental_page(self, **kwargs):
        """booking page"""
        bookings = request.env['car.booking'].sudo().search([])
        values = {
            'bookings': bookings,
        }

        return request.render('car_rental_sankit.car_booking', values)

    @http.route('/booking/form', type='http', auth='public', website=True)
    def car_booking_form(self, **kwargs):
        return request.render('car_rental_sankit.car_booking_form', {})

    @http.route('/booking/create', type='http', auth='public', methods=['POST'], website=True)
    def car_rental_create_page(self, **post):
        record_booking_ids = request.httprequest.form.getlist('record_booking_ids')
        """Car Rental Create page"""
        request.env['car.booking'].sudo().create({
            'customer_id': post.get('customer_id'),
            'customer_aadhar_number': post.get('customer_aadhar_number'),
            'trip_start_date': post.get('trip_start_date'),
            'trip_end_date': post.get('trip_end_date'),
            'state': 'draft',
            'record_booking_ids': [(6, 0, [int(t) for t in record_booking_ids])] if record_booking_ids else False,
        })
        return request.render('website.contactus_thanks')



    @http.route(['/booking/print'], type='http', auth="public", website=True)
    def order_print_func(self, **kwargs):
        report = request.env.ref('car_rental_sankit.action_report_car_booking').sudo()
        print(report)
        # all book
        orders = request.env['car.booking'].sudo().search([])
        print("orders -----------", orders)
        docids = orders.ids

        pdf, _ = report._render_qweb_pdf('car_rental_sankit.action_report_car_booking', docids)

        return request.make_response(
            pdf,
            headers=[
                ('Content-Type', 'application/pdf'),
                ('Content-Length', str(len(pdf))),
                ('Content-Disposition', 'attachment; filename="car_rental_report.pdf"')
            ],
        )
