import base64

from odoo import http
from odoo.http import request


class BookBackend(http.Controller):

    @http.route('/book', type="http", auth='public', website=True)
    def fetch_book_data(self):
        if self.env.user._is_public():
            return request.render('library_management_tanisha.library_book_template_logout')
        return request.render('library_management_tanisha.library_book_template_login')

    @http.route('/book/form', type="http", auth='public', website=True)
    def create_book(self, **kwargs):
        self.env['library.book'].create({
            'name': kwargs.get('name'),
            'barcode': kwargs.get('barcode'),
            'state': kwargs.get('state'),
            'category': kwargs.get('category'),
            'description': kwargs.get('description'),
            'available_copies': kwargs.get('available_copies'),
            'stock': kwargs.get('stock'),
            'borrow_price': kwargs.get('borrow_price'),
            'max_day_limit': kwargs.get('max_day_limit'),
            'cover_image': base64.b64encode(kwargs.get('cover_image').read()),
        })
        return request.redirect('/library-book')

    @http.route('/library-book', type="http", auth='public', website=True)
    def display_book_data(self):
        books = self.env['library.book'].search([])
        return request.render('library_management_tanisha.book_website_template', {'books': books})

    @http.route('/library-borrow-request', type="http", auth='public', website=True)
    def display_borrow_request_data(self):
        borrow_requests = self.env['library.borrow.request'].search([])
        return request.render('library_management_tanisha.borrow_request_website_template', {'borrow_requests': borrow_requests})

    @http.route('/borrow-request', type="http", auth='public', website=True)
    def borrow_request_form(self):
        students = self.env['res.partner'].search([('is_student','=',True)])
        librarians = self.env['res.partner'].search([('is_librarian','=',True)])
        books = self.env['library.book'].search([('state','=','published')])
        return request.render('library_management_tanisha.borrow_request_form_template', {'students': students, 'librarians': librarians, 'books': books})

    @http.route('/borrow-request-form', type="http", auth='public', website=True)
    def create_borrow_request(self, **kwargs):
        # self.env['library.borrow.request'].create({
        #     'student_id': kwargs.get('student'),
        #     'librarian_id': kwargs.get('librarian'),
        #     'issue_date': kwargs.get('issue_date'),
        #     'return_date': kwargs.get('return_date'),
        #     'state': kwargs.get('state'),
        #     'fine_amount': kwargs.get('fine_amount'),
        #     'total_amount': kwargs.get('total_amount'),
        #     'borrow_request_line_ids': [int(i) for i in kwargs.get('borrow_request_line_ids').split(',')],
        # })

        return request.redirect('/library-borrow-request')


