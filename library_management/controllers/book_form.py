from odoo import http, models, fields, tools, _
from odoo.http import request


class BookForm(http.Controller):

    @http.route('/', type='http', auth='public', website=True)
    def index(self, **kwargs):
        print(request.website.id)
        if request.website.name == "Website A1":
            return request.render('library_management.custom_homepage_a1')
        elif request.website.name == "Website A2":
            return request.render('library_management.custom_homepage_a2')
        else:
            return request.render('library_management.custom_homepage')



    @http.route('/policy', type='http', auth='public', website=True)
    def cookie_policy_func(self):
        return request.render('library_management.cookie_policy', {})


    @http.route('/book-data', type='http', auth='public', website=True)
    def book_form_data(self):
        books = request.env['library.books'].sudo().search([])
        return request.render('library_management.book_data', {'books': books})


    @http.route('/book/form', type='http', auth='public', website=True, methods=['GET'])
    def book_form_func(self):
        return request.render('library_management.book_form')


    @http.route('/book-create', type='http', auth='public', website=True, methods=['POST'], csrf=True)
    def create_book(self, **post):
    #     res = request.env.user.partner_id
    #     res2 = request.env.user._is_public()
    #
    #     print("======================>", res)
    #
    #     print("======================>", res2)
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
        })

        return request.redirect('/book-data')
    #
