from odoo import http, _,fields
from odoo.http import request
from odoo.exceptions import AccessError

class CarRentalManagementController(http.Controller):

    @http.route(['/my/car/rental/bookings','/my/car/rental/bookings/page/<int:page>'], type='http', auth='user', website=True)
    def car_rental_bookings_controller(self,page=0, **kwargs):
        domain = []
        total = request.env['vehicle.booking'].search_count(domain)
        pager = request.website.pager(
            url='/my/car/rental/bookings',
            total=total,
            page=page,
            step=3,
        )
        offset = pager['offset']
        values = request.env['vehicle.booking'].search(domain)
        values = values[offset: offset + 3]

        return request.render('car_rental_management_jui.car_rental_bookings_template_list',{'requests': values,'pager': pager,
            'default_url': '/my/car/rental/bookings'})

    @http.route(['/my/car/rental/bookings/view/<int:res_id>'], type='http', auth='user',website=True)
    def car_rental_bookings_view_controller(self, res_id, **kwargs):
        record = request.env['vehicle.booking'].browse(res_id)
        return request.render('car_rental_management_jui.car_rental_bookings_template_view', {
            'record': record,
        })

    @http.route(['/my/rental/print/<int:invoice_id>'], type='http', auth="user", website=True)
    def print_rental_invoice(self, invoice_id, **kw):
        invoice = request.env['account.move'].sudo().browse(invoice_id)
        if not invoice.exists():
            return request.not_found()
        pdf, _ = request.env['ir.actions.report']._render_qweb_pdf('car_rental_management_jui.report_invoice', [invoice_id])

        pdf_http_headers = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf)),
            ('Content-Disposition', 'attachment; filename="Invoice_%s.pdf"' % invoice.name)
        ]
        return request.make_response(pdf, headers=pdf_http_headers)