from odoo import http, models, fields, tools, _
from odoo.http import request
from odoo.addons.website.controllers.main import Website

from requests import session
import base64


# Book form controller
class BookingForm(http.Controller):
    # Books data
    @http.route('/booking/data', type='http', auth='public', website=True)
    def booking_form_data(self):
        if request.session.uid:
            docs = request.env['booking.management'].sudo().search([])
            return request.render('car_management_amitkumar.portal_my_orders', {'docs': docs})
        else:
            return request.render('website.homepage')

    @http.route(['/book/print'], type='http', auth="public", website=True)
    def book_print_func(self, **kwargs):
        report = request.env.ref('car_management_amitkumar.action_book_pdf').sudo()
        print(report)

        # all book
        books = request.env['booking.management'].sudo().search([])
        docids = books.ids

        pdf, _ = report._render_qweb_pdf(report, docids)

        return request.make_response(
            pdf,
            headers=[
                ('Content-Type', 'application/pdf'),
                ('Content-Length', str(len(pdf))),
                ('Content-Disposition', 'attachment; filename="Booking_Report.pdf"')
            ],
        )