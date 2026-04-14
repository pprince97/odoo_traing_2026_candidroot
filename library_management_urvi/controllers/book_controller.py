# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.http import request
import base64


class BookController(http.Controller):

    @http.route(['/book', '/book/page/<int:page>'], type='http', auth='public', website=True)
    def public_controller(self, page=0, filterby='all', sortby='date_desc', min_price=None, max_price=None, search=None,
                          **post):
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

            searchbar_sortings = {
                'date_desc': {'label': 'Newest First', 'order': 'create_date desc'},
                'date_asc': {'label': 'Oldest First', 'order': 'create_date asc'},
                'name_asc': {'label': 'Name (A-Z)', 'order': 'name asc'},
                'price_asc': {'label': 'Price (Low to High)', 'order': 'borrow_price asc'},
            }

            if sortby not in searchbar_sortings:
                sortby = 'date_desc'

            order = searchbar_sortings[sortby]['order']

            selected_category = request.httprequest.args.getlist('category')
            selected_states = request.httprequest.args.getlist('state')
            # max_limit = request.env['library.book'].search([], order='borrow_price desc', limit=1).borrow_price or 1000
            # min_p = float(post.get('min_price', 0))
            # max_p = float(post.get('max_price', max_limit))
            all_prices = request.env['library.book'].search([]).mapped('borrow_price')
            available_min = min(all_prices) if all_prices else 0
            available_max = max(all_prices) if all_prices else 100
            curr_min = float(min_price) if min_price is not None and min_price != "" else available_min
            curr_max = float(max_price) if max_price is not None and max_price != "" else available_max
            # try:
            #     curr_min = float(min_price) if min_price else available_min
            #     curr_max = float(max_price) if max_price else available_max
            # except ValueError:
            #     # Fallback to defaults if something weird is passed in the URL
            #     curr_min = available_min
            #     curr_max = available_max
            # try:
            #     curr_min = float(min_price) if min_price and min_price.strip() else available_min
            #     curr_max = float(max_price) if max_price and max_price.strip() else available_max
            # except ValueError:
            #     curr_min, curr_max = available_min, available_max

            category = ['mystery', 'horror', 'romantic', 'science', 'history', 'biography']
            state_options = request.env['library.book']._fields['state'].selection

            search_domain = []
            if search:
                search_domain += ['|', '|', ('name', 'ilike', search), ('barcode', 'ilike', search),
                                  ('category', 'ilike', search)]

            if selected_category:
                search_domain += [('category', 'in', selected_category)]

            if selected_states:
                search_domain += [('state', 'in', selected_states)]

            # if min_price > 0:
            #     search_domain += [('list_price', '>=', min_price)]
            #
            # if max_price > 0:
            #     search_domain += [('list_price', '<=', max_price)]

            filter_domain = searchbar_filters.get(filterby, searchbar_filters['all'])['domain']
            domain = search_domain + filter_domain + [('borrow_price', '>=', curr_min),
                                                      ('borrow_price', '<=', curr_max)]
            book_count = Book.search_count(domain)
            pager = request.website.pager(
                url='/book',
                total=book_count,
                url_args={
                    'search': search,
                    'filterby': filterby,
                    'sortby': sortby,
                    'min_price': min_price,
                    'max_price': max_price,
                    'category': selected_category,
                    'state': selected_states,
                },
                page=page,
                step=6,
            )
            book_records = Book.search(domain,
                                       limit=6,
                                       offset=pager['offset'],
                                       order=order,
                                       )
            # offset = pager['offset']
            # books = books[offset: offset + 3]
            return request.render('library_management_urvi.template_view_all_books',
                                  {'books': book_records, 'pager': pager, 'selected_states': selected_states,
                                   'available_min_price': available_min,
                                   'available_max_price': available_max,
                                   'min_price': curr_min,
                                   'max_price': curr_max,
                                   'search': search, 'searchbar_filters': searchbar_filters, 'filterby': filterby,
                                   'category': category, 'selected_category': selected_category,
                                   'state_options': state_options, 'searchbar_sortings': searchbar_sortings,
                                   'sortby': sortby})

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

# from odoo import http
# from odoo.http import request
#
# class BookController(http.Controller):
#     @http.route(['/books'], type='http', auth="public", website=True)
#     def list_books(self, **post):
#         # 1. Get selected author IDs from the URL/Form (sent as a list)
#         selected_author_ids = request.httprequest.args.getlist('author_id')
#
#         # 2. Build the search domain
#         domain = []
#         if selected_author_ids:
#             # Convert string IDs from request to integers
#             author_ids = [int(x) for x in selected_author_ids]
#             domain += [('author_id', 'in', author_ids)]
#
#         # 3. Fetch data
#         books = request.env['my.book.model'].search(domain)
#         authors = request.env['res.partner'].search([('is_author', '=', True)])  # Adjust based on your model
#
#         # 4. Render the template with the current filters
#         values = {
#             'books': books,
#             'authors': authors,
#             'selected_author_ids': [int(x) for x in selected_author_ids],
#         }
#         return request.render("your_module.book_page_template", values)
