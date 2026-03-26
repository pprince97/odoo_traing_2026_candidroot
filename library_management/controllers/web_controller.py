from odoo import http, models, fields, tools, _
from odoo.http import request
from odoo.addons.website.controllers.main import Website
from odoo.addons.portal.controllers.portal import pager as portal_pager
from requests import session


# inherit Controller
class WebsiteTopSelling(Website):
    @http.route('/', type='http', auth='public', website=True)
    def index(self, **kw):
        res = super(WebsiteTopSelling, self).index(**kw)

        top_products = request.env['product.template'].search([
            ('website_published', '=', True),
        ], limit=4)

        res.qcontext['top_selling_products'] = top_products
        print("========>", top_products)
        return res


# Book form controller
class BookForm(http.Controller):

    # @http.route('/', type='http', auth='public', website=True)
    # def show_multiple_pages(self, **kwargs):
    #     print(request.website.id)
    #     if request.website.name == "Website A1":
    #         return request.render('library_management.custom_homepage_a1')
    #     elif request.website.name == "Website A2":
    #         return request.render('library_management.custom_homepage_a2')
    #     else:
    #         return request.render('library_management.custom_homepage')

    @http.route('/policy', type='http', auth='public', website=True)
    def cookie_policy_func(self):
        return request.render('website.cookie_policy', {})


    @http.route('/book/data', type='http', auth='public', website=True)
    def book_form_data(self):
        if request.session.uid:
            books = request.env['library.books'].sudo().search([])
            return request.render('library_management.book_data', {'books': books})
        else:
            return request.render('website.homepage')


    @http.route('/book/form', type='http', auth='public', website=True, methods=['GET'])
    def book_form_func(self):
        return request.render('library_management.book_form')


    @http.route('/book-create', type='http', auth='public', website=True, methods=['POST'], csrf=True)
    def create_book(self, **post):\
    #
        request.env['library.books'].sudo().create({
            'id': post.get('id'),
            'student_id': post.get('student_id'),
            'name': post.get('name'),
            'barcode': post.get('barcode'),
            'state': post.get('state'),
            'category': post.get('category'),
            'stock': post.get('stock'),
            'borrow_price': post.get('borrow_price'),
            'maximum_day_limit': post.get('max_day_limit'),
            'description': post.get('description'),
            'cover_image': post.get('cover_image'),
            'book_cover_name': post.get('book_cover_name'),
        })

        return request.redirect('/book/data')


#
# class BookController(http.Controller):
#
#     @http.route('/book/data', type='http', auth='public', website=True)
#     def book_form_data(self, page=1, **kw):
#
#         if not request.session.uid:
#             return request.render('website.homepage')
#
#         books_model = request.env['library.books'].sudo()
#
#         total_books = books_model.search_count([])
#
#         page = int(page)
#         limit = 3
#         offset = (page - 1) * limit
#
#         pager = portal_pager(
#             url='/book/data',
#             total=total_books,
#             page=page,
#             step=limit
#         )
#
#         books = books_model.search([], limit=limit, offset=offset)
#
#         return request.render('library_management.book_data', {
#             'books': books,
#             'pager': pager,
#         })