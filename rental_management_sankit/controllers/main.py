from odoo import http, models, fields, tools, api , _
from odoo.http import request

from odoo.addons.website.controllers.main import Website
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class WebsiteInherit(Website):
    @http.route()
    def index(self, **kw):
        response = super(WebsiteInherit, self).index(**kw)
        rental_orders = request.env['rental.order'].sudo().search([] , limit=1)
        response.qcontext['rental_orders'] = rental_orders
        return response



class WebsiteDetail(http.Controller):
    # @http.route('/', type='http', auth='public', website=True)
    # def homepage_view(self, **kwargs):
    #     if request.website.id == request.env.ref('rental_management_sankit.website_one').id:
    #         return request.render('rental_management_sankit.template_home1', {})
    #     elif request.website.id == request.env.ref('rental_management_sankit.website_two').id:
    #         return request.render('rental_management_sankit.template_home2', {})
    #     else:
    #         return request.render('website.homepage', {})

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

    @http.route(['/rental_order','/rental_order/page/<int:page>'], type='http', auth='public', website=True)
    def rental_order_list(self,page=1, search=None, search_in='all', **kwargs):
        """rental order  page"""
        # rental_orders = request.env['rental.order'].search([]).read(['rental_number', 'customer_id', 'rent_start_date', 'rent_end_date' , 'total_amount'])
        rental_orders = request.env['rental.order'].sudo().search([])
        total_orders = rental_orders.search_count([])
        step = 3
        pager = portal_pager(
            url='/rental_order',
            total=total_orders,
            page=page,
            step=step,
        )
        rental_records = rental_orders.search(
            [],
            limit=step,
            offset=pager['offset'],
            order='id asc',
        )

        # Edit
        values = {
            'rental_orders': rental_orders,
            'rental_records': rental_records,
            'page_name': 'rental_order',
            'default_url': '/rental_order',
            'pager': pager,
        }
        print("==============")
        print(rental_orders)
        print(values)
        return request.render('rental_management_sankit.rental_order', values)

    @http.route('/rental_order/form', type='http', auth='public', website=True)
    def rental_order_form(self, **kwargs):
        """rental order form"""
        # products = request.env['product.product'].sudo().search([])
        # data = {
        #     'products': products,
        # }
        return request.render('rental_management_sankit.rental_order_form', {})

    @http.route('/rental_order/create', type='http', auth='public', methods=['POST'], website=True)
    def rental_order_create_page(self, **post):
        tag_ids = request.httprequest.form.getlist('tag_ids')
        # tag_ids = list(map(int, tag_ids)) if tag_ids else []
        """rental order  page"""
        request.env['rental.order'].sudo().create({
            'customer_id': post.get('customer_id'),
            'rent_start_date': post.get('rent_start_date'),
            'rent_end_date': post.get('rent_end_date'),
            'total_amount': post.get('total_amount'),
            'tag_ids': [(6, 0, [int(t) for t in tag_ids])] if tag_ids else False,
        })
        return request.render('website.contactus_thanks')

    # User Profile
    @http.route('/user-profile/form', type='http', auth='public', website=True)
    def user_profile_form(self, **kwargs):
        # values = {
        #     'user': request.env['user.profile'].sudo().search([])
        # }
        return request.render('rental_management_sankit.user_profile_form')

    @http.route('/user-profile/create', type='http', auth='public', methods=['POST'],website=True)
    def user_profile_create(self, **post):
        request.env['user.profile'].sudo().create({
            'name': post.get('name'),
            'email': post.get('email'),
            'country_id': post.get('country_id'),
            'state_id': post.get('state_id'),
            'city_id': post.get('city_id'),
        })
        return request.render('website.contactus_thanks')








    # @http.route('/get_product_categories', auth="public", type='jsonrpc',
    #             website=True)
    # def get_product_category(self):
    #     """Get the website categories for the snippet."""
    #     public_categs = request.env[
    #         'product.public.category'].sudo().search_read(
    #         [('parent_id', '=', False)], fields=['name', 'image_1920', 'id']
    #     )
    #     values = {
    #         'categories': public_categs,
    #     }
    #     return values