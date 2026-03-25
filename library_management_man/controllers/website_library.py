from odoo import models, http, fields, api
from odoo.http import request
from odoo.addons.website.controllers.main import Website
# from odoo.addons.portal.controllers.portal import CustomerPortal, pager as website_pager


class WebsiteLibrary(http.Controller):

    @http.route('/books', type='http', auth='public', website=True)
    def fetch_books(self, **kwargs):
        books = request.env['library.book'].sudo().search([])
        return request.render('library_management_man.website_book_menu_view',
                              {'books': books})

    @http.route('/book/form', type='http', auth='public', methods=['GET'], website=True)
    def book_form(self, **kwargs):
        return request.render('library_management_man.book_form_view')

    @http.route(['/book/create'], type='http', auth="public", methods=['POST'], website=True, csrf=True)
    def create_book(self, **post):
        request.env['library.book'].sudo().create({
            'name': post.get('name'),
            'book_currency': post.get('book_currency'),
            'category_id': post.get('category_id'),
            'available_copies': post.get('available_copies'),
            'fine_amount': post.get('fine_amount'),
            'stock': post.get('stock'),
            'borrow_price': post.get('borrow_price'),
            'maximum_day_limit': post.get('maximum_day_limit'),
            # 'cover_image': post.get('cover_image'),
        })
        return request.redirect('/books')


class MultipleWebsite(Website):
    # @http.route('/', type='http', auth='public', website=True)
    # def index(self, **kw):
    #     super(MultipleWebsite, self).index(**kw)
    #     if request.website.name == "My Website 1":
    #         return request.render('library_management_man.inherit_home_page_1')
    #     elif request.website.name == "My Website 2":
    #         return request.render('library_management_man.inherit_home_page_2')
    #     else:
    #         return request.render('library_management_man.inherit_home_page')

    @http.route('/', type='http', auth='public', website=True)
    def index(self, **kw):
        response = super(MultipleWebsite, self).index(**kw)
        top_products = request.env['product.template'].search([
            ('website_published', '=', True),
        ], limit=4)
        response.qcontext['products'] = top_products
        return response

    @http.route(['/product', '/product/page/<int:page>'], type='http', auth='public', website=True)
    def index(self, page=1, **kwargs):
        product = request.env['product.template']
        step = 4
        total = product.search_count([])

        pager = request.website.pager(
            url="/product",
            total=total,
            page=page,
            step=step,
        )
        products = product.sudo().search([], limit=step, offset=pager['offset'])
        return request.render(
            'library_management_man.published_product_menu',
            {
                'products': products,
                'pager': pager,
            }
        )

