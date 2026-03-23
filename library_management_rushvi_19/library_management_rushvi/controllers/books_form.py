from odoo import models, fields, api, http
from odoo.http import request
import base64
from odoo.exceptions import ValidationError

class BooksForm(http.Controller):

    @http.route('/books', type='http', auth='public',website=True)
    def books(self):
        books = request.env['library.books'].search([])
        return request.render('library_management_rushvi.books_template', {
            'books': books,
            'user': request.env.user
        })

    @http.route('/books/create', type='http', auth='user', methods=['POST'], website=True)
    def create_book(self, **post):
        barcode = post.get('barcode')
        if barcode:
            existing_book = request.env['library.books'].search([('barcode', '=', barcode)], limit=1)
            if existing_book:
                books = request.env['library.books'].search([])
                return request.render('library_management_rushvi.books_template', {
                    'post': post,
                    'books': books,
                    'error_msg': 'A book with this barcode already exists!',
                    'user': request.env.user,
                })
        cover_image = post.get('cover_image')
        image_base64 = False
        if cover_image:
            image_base64 = base64.b64encode(cover_image.read())
        vals = {
            'name': post.get('name'),
            'barcode': barcode,
            'description': post.get('description'),
            'stock': int(post.get('stock', 0)),
            'borrow_price': float(post.get('borrow_price', 0.0)),
            'maximum_day_limit': int(post.get('maximum_day_limit', 0)),
            'category': post.get('category'),
            'state': post.get('state', 'unpublished'),
            'currency': int(post.get('currency')) if post.get('currency') else False,
            'cover_image': image_base64,
        }
        request.env['library.books'].create(vals)
        return request.redirect('/books')

    @http.route(['/my/borrow-requests'], type='http', auth='user', website=True)
    def view_my_borrow_requests(self):
        user = request.env.user
        domain = ['|',('student_id.id', '=', user.partner_id.id),('librarian_id.id', '=', user.partner_id.id)]
        if user.has_group('library_management_rushvi.group_library_admin'):
            borrow_requests = request.env['library.borrow.requests'].sudo().search([])
        elif user.has_group('library_management_rushvi.group_library_student') or request.env.user.has_group(
                'library_management_rushvi.group_library_librarian'):
            borrow_requests = request.env['library.borrow.requests'].sudo().search(domain)
        else:
            borrow_requests = request.env['library.borrow.requests'].browse()
        return request.render('library_management_rushvi.borrow_requests_template', {
            'borrow_requests': borrow_requests,
            'user': request.env.user,
            'borrow_request_count': len(borrow_requests),
            'page_name': 'borrow_request',
        })

    @http.route(['/my/borrow-requests/<int:id>'], type='http', auth='user', website=True)
    def view_borrow_request_form(self, id, **post):
        borrow_request = request.env['library.borrow.requests'].sudo().browse(id)
        return request.render('library_management_rushvi.borrow_requests_template_form', {
            'borrow_request': borrow_request,
            'page_name': 'borrow_request',
            'borrow_requests_lines': borrow_request,
            'user': request.env.user,
        })

    @http.route('/my/borrow-requests/create', type='http', auth='user', methods=['POST'], website=True)
    def create_borrow_requests(self, **post):
        vals={
            'student_id': post.get('student_id'),
            'librarian_id': post.get('librarian_id'),
            'issue_date': post.get('issue_date'),
            'return_date': post.get('return_date'),
        }
        request.env['library.borrow.requests'].sudo().create(vals)
        return request.redirect('/my/borrow-requests')

    @http.route('/my/borrow-requests/<int:id>/write', type='http', auth='user', methods=['POST'], website=True)
    def create_borrow_lines_requests(self, id, **post):
        borrow_line_data = {
            'book_id': int(post.get('book_id')),
            'quantity': float(post.get('quantity', 0)),
            'issue_date': post.get('issue_date'),
            'return_date': post.get('return_date'),
        }
        request.env['library.borrow.requests'].sudo().browse(id).write({
            'borrow_request_line_ids': [(0, 0, borrow_line_data)],
        })
        return request.redirect(f'/my/borrow-requests/{id}')
