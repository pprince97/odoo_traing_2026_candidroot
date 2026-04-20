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



    # @http.route(['/booking/print'], type='http', auth="public", website=True)
    # def order_print_func(self, **kwargs):
    #     report = request.env.ref('car_rental_sankit.action_report_car_booking').sudo()
    #     print(report)
    #     # all book
    #     orders = request.env['car.booking'].sudo().search([])
    #     print("orders -----------", orders)
    #     docids = orders.ids
    #
    #     pdf, _ = report._render_qweb_pdf('car_rental_sankit.action_report_car_booking', docids)
    #
    #     return request.make_response(
    #         pdf,
    #         headers=[
    #             ('Content-Type', 'application/pdf'),
    #             ('Content-Length', str(len(pdf))),
    #             ('Content-Disposition', 'attachment; filename="car_rental_report.pdf"')
    #         ],
    #     )

    @http.route(['/booking/print', '/booking/print/<int:order_id>'], type='http', auth="public", website=True)
    def order_print_func(self, order_id=None, **kwargs):
        report = request.env.ref('car_rental_sankit.action_report_car_booking').sudo()

        if order_id:
            # Print only ONE specific booking
            orders = request.env['car.booking'].sudo().browse(order_id)
            filename = f"Booking_{order_id}.pdf"
        else:
            # Print ALL bookings
            orders = request.env['car.booking'].sudo().search([])
            filename = "All_Bookings_Report.pdf"

        if not orders:
            return request.not_found()

        docids = orders.ids
        pdf, _ = report._render_qweb_pdf('car_rental_sankit.action_report_car_booking', docids)

        return request.make_response(
            pdf,
            headers=[
                ('Content-Type', 'application/pdf'),
                ('Content-Length', str(len(pdf))),
                ('Content-Disposition', f'attachment; filename="{filename}"')
            ],
        )

    @http.route(['/my/booking/details/<int:booking_id>'], type='http', auth="user", website=True)
    def car_booking_portal_detail(self, booking_id, **kw):
        # Fetch the booking record
        booking = request.env['car.booking'].sudo().browse(booking_id)

        if not booking.exists():
            return request.render('website.404')

        # Ensure the logged-in user only sees their own bookings
        if booking.customer_id != request.env.user.partner_id:
            return request.render('website.403')

        return request.render("car_rental_sankit.car_booking_details_template", {
            'booking': booking,
            'page_name': 'car_booking_details',
        })

