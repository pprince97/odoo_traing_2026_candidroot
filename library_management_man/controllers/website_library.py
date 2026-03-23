from odoo import models, http, fields, api
from odoo.http import request


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

