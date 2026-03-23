from odoo import http, models, fields, tools, api , _
from odoo.http import request

class WebsiteDetail(http.Controller):
    @http.route('/faqs', type='http', auth='user', website=True)

    def faq_page(self ,**kwargs):
        rental_orders =request.env['rental.order'].sudo().search([])
        values = {
            'rental_orders': rental_orders,
        }
        """faq page"""
        return request.render('rental_management_sankit.faqs', values)

    @http.route('/rental', type='http', auth='public', website=True)
    def rental_page(self ,**kwargs):
        """rental page"""
        rental_orders = request.env['rental.order'].sudo().search([])
        values = {
            'rental_orders': rental_orders,
        }
        if request.session.uid:
            return request.render('rental_management_sankit.rental', values)
        else:
            return request.render('website.homepage', values)

    @http.route('/rental/create', type='http', auth='public', methods=['POST'], website=True)
    def rental_create(self, **post):
        request.env['res.partner'].sudo().create({
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
        })
        return request.render('rental_management_sankit.rental_create')

    @http.route('/rental_order', type='http', auth='public', website=True)
    def rental_order_list(self, **kwargs):
        """rental order  page"""
        # rental_orders = request.env['rental.order'].search([]).read(['rental_number', 'customer_id', 'rent_start_date', 'rent_end_date' , 'total_amount'])
        rental_orders = request.env['rental.order'].sudo().search([])
        values = {
            'rental_orders': rental_orders,
        }
        print("==============")
        print(rental_orders)
        print(values)
        return request.render('rental_management_sankit.rental_order', values)

    @http.route('/rental_order/form', type='http', auth='public', website=True)
    def rental_order_form(self, **kwargs):
        """rental order form"""
        return request.render('rental_management_sankit.rental_order_form', {})

    @http.route('/rental_order/create', type='http', auth='public', methods=['POST'], website=True)
    def rental_order_create_page(self, **post):
        """rental order  page"""
        request.env['rental.order'].sudo().create({
            'customer_id': post.get('customer_id'),
            'rent_start_date': post.get('rent_start_date'),
            'rent_end_date': post.get('rent_end_date'),
            'total_amount': post.get('total_amount'),
        })
        return request.render('website.contactus_thanks')
    #
    # @http.route('/inherit', type='http', auth='public', website=True)
    # def rental_inherit(self, **kwargs):
    #     """rental order form"""
    #     return request.render('rental_management_sankit.my_inherit_view', {})

    #
    # @http.route('/faqs', type='http', auth='public', website=True)
    # def faq_page_public(self):
    #     """faq page"""
    #     return request.render('rental_management_sankit.faqs', {})


    # @http.route('/faqs/info', type='http', auth='user', website=True)
    # def faqs_info(self, **kwargs):
    #     print('----------2---------')
    #     "faqs info"
    #     raise ValueError("This is error")