# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.http import request
import base64


class BookController(http.Controller):

    @http.route(['/book', '/book/page/<int:page>'], type='http', auth='public', website=True)
    def public_controller(self, page=0, filterby='all',search=None):
        if request.env.user._is_public():
            return request.render("library_management_urvi.book_template_public")
        else:
            Book = request.env['library.book'].search([])
            searchbar_filters = {
                'all': {
                    'label': 'All',
                    'domain': [],
                },
                'published': {
                    'label': 'Published',
                    'domain': [('state', '=', 'published')],
                },
                'unpublished': {
                    'label': 'unpublished',
                    'domain': [('state', '=', 'unpublished')],
                },
            }
            search_domain = []
            if search:
                search_domain += ['|','|',('name', 'ilike', search),('barcode', 'ilike', search),('category', 'ilike', search)]
            filter_domain = searchbar_filters.get(filterby, searchbar_filters['all'])['domain']
            domain =  search_domain + filter_domain
            book_count = Book.search_count(domain)
            pager = request.website.pager(
                url='/book',
                total=book_count,
                url_args={
                    'search': search,
                    'filterby': filterby,
                },
                page=page,
                step=6,
            )
            book_records = Book.search(domain,
                limit = 6,
                offset = pager['offset'],
                order = 'name asc',
            )
        # offset = pager['offset']
        # books = books[offset: offset + 3]
        return request.render('library_management_urvi.template_view_all_books', {'books': book_records, 'pager': pager,
            'search': search,'searchbar_filters': searchbar_filters,'filterby': filterby,})

    @http.route(['/book/submit'], type='http', auth="user", website=True, sitemap=False)
    def book_form_submit(self, **post):
        if post.get('image'):
            post['image'] = base64.b64encode(post['image'].read())
        request.env['library.book'].create({
            'name': post.get('name'),
            'barcode': post.get('barcode'),
            'description': post.get('description'),
            'state': post.get('state'),
            'category': post.get('category'),
            'copies': int(post.get('copies') or 0),
            'borrow_price': float(post.get('borrow_price') or 0.0),
            'maximum_day_limit': int(post.get('maximum_day_limit') or 0),
            'image': post['image'] if post.get('image') else False,
        })
        books = request.env['library.book'].search([])
        return request.render("library_management_urvi.template_view_all_books", {'books': books})

    @http.route(['/create/book'], type='http', auth='user', website=True)
    def book_create(self):
        return request.render("library_management_urvi.template_create_book")

    @http.route(['/my/profile'], type='http', auth="user", website=True)
    def edit_partner_profile(self, **post):
        # Get the partner record of the current logged-in user
        partner = request.env.user.partner_id
        values = {
            'partner': partner,
        }
        return request.render("library_management_urvi.partner_edit_template", values)

    @http.route(['/my/profile/update'], type='http', auth="user", website=True)
    def update_partner_profile(self, **post):
        partner = request.env.user.partner_id
        partner.update(
            {'name': post.get('name') or '', 'email': post.get('email') or '', 'phone': post.get('phone') or '',
             'gender': post.get('gender') or ''})
        values = {
            'partner': partner,
        }
        return request.redirect("/my/profile")

    @http.route(['/profile'], type='http', auth="user", website=True)
    def get_profile_form(self):
        return request.render("library_management_urvi.partner_info_template")

    @http.route('/get_partner_info', type='jsonrpc', auth='user')
    def get_info(self):
        partner = http.request.env.user.partner_id
        return {
            'part': partner,
            'name': partner.name,
            'email': partner.email,
            'phone': partner.phone,
            'gender': partner.gender,
            'country_id': partner.country_id.id,
            'state_id': partner.state_id.id,
        }

    @http.route('/get_states', type='jsonrpc', auth='user')
    def get_states(self, country):
        states = request.env['res.country.state'].search_read([('country_id', '=', country)], ['id', 'name'])
        return states

    @http.route('/get_city', type='jsonrpc', auth='user')
    def get_city(self, country, state):
        city = request.env['res.city'].search_read([('country_id', '=', country), ('state_id', '=', state)],
                                                   ['id', 'name'])
        return city

    @http.route('/create_partner', type='jsonrpc', auth='user', website=True)
    def create_partner(self, params):
        # partner = http.request.env.user.partner_id
        print('>>>>>>>>>>>>>>>>>>', params)
        request.env['res.partner'].create(params)
        print('>>>>>>>>>>>>>>>>>py')
        return {'success': True}
