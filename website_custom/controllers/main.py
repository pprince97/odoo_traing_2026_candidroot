from odoo import http
from odoo.http import request

class PartnerFormController(http.Controller):

    @http.route('/partner/form', type='http', auth='public', website=True)
    def partner_form(self, **kwargs):
        return request.render('website_custom.partner_form_template')

    @http.route('/borrow', type='http', auth='public', website=True)
    def borrow_requests(self, **post):
        requests = request.env['library.book.borrow'].sudo().search([('librarian_id', '=', 1)])

        return request.render('website_custom.website_book_borrow_template', {
            'requests': requests
        })

    @http.route('/contactus', type='http', auth='public', website=True)
    def contact_us(self, **kwargs):
        return request.render('website.contactus')

    @http.route('/partner/form/submit', type='http', auth='public', methods=['POST'], website=True)
    def partner_form_submit(self, **post):

        request.env['res.partner'].sudo().create({
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone')
        })

        return request.render('website.partner_form_template')

    @http.route('/partner/table', type='http', auth='public', methods=['GET'], website=True)
    def partner_table(self, **post):
        partners = request.env['res.partner'].sudo().search([])

        return request.render('website_custom.website_partner_template', {
            'partners': partners
        })