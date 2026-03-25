from odoo import http
from odoo.http import request


class LibraryWebsite(http.Controller):

    @http.route('/books', type='http', auth='public', website=True)
    def fetch_book_data(self):
        books = request.env['library.books'].sudo().search([])
        return request.render('library_management.book_form_menu_view',{'books':books})

    @http.route('/books/form', type='http', auth='public',methods=['GET'], website=True)
    def book_form(self):
        return request.render('library_management.book_form_view')

    @http.route('/books/create', type='http', auth='public', methods=['POST'], website=True)
    def book_create(self, **post):
        request.env['library.books'].sudo().create({
            'name': post.get('name'),
            'state': post.get('state'),
            'category': post.get('category'),
            'stock': post.get('stock'),
            'maximum_day_limit': post.get('maximum_day_limit'),
            'burrow_price': post.get('burrow_price'),
        })
        return request.redirect('/books')

