from odoo import models,fields,api,http
from odoo.http import request
import base64


class BookController(http.Controller):
    # @http.route('/home', type='http', auth="public", website=True)
    # def home_page(self, **kwargs):
    #     return request.render('library_management.my_home_page', {})

    @http.route('/book', type='http', auth="public", website=True)
    def list_books(self, **kwargs):
        books = request.env['library.books'].sudo().search([])
        return request.render('library_management.books_template', {
            'books': books,
            'user': request.env.user
        })

    @http.route('/book/create', type='http', auth='user', methods=['POST'], website=True)
    def create_book(self, **post):
        cover_image = post.get('cover_image')
        image_base64 = False
        if cover_image:
            image_base64 = base64.b64encode(cover_image.read())
        vals = {
            'name': post.get('name'),
            'barcode': post.get('barcode'),
            'description': post.get('description'),
            'stock': int(post.get('stock', 0)),
            'borrow_price': float(post.get('borrow_price', 0.0)),
            'maximum_day': int(post.get('maximum_day', 0)),
            'state': post.get('state', 'unpublished'),
            'currency_id': int(post.get('currency')) if post.get('currency') else False,
            'cover_image': image_base64,
        }
        request.env['library.books'].sudo().create(vals)
        return request.redirect('/book')

    @http.route('/borrow_request', type='http', auth="user", website=True)
    def list_borrow_request(self,**kwargs):
        user = request.env.user
        if user.has_group('library_management.group_project_admin'):
            borrow_requests = request.env['library.borrow.request'].sudo().search([])
        elif user.has_group('library_management.group_project_student') or user.has_group('library_management.group_project_librarian'):
            borrow_requests = request.env['library.borrow.request'].sudo().search(['|',('student_id','=',user.partner_id.id),
                                                                            ('librarian_id','=',user.partner_id.id)])
        # borrow_requests = request.env['library.borrow.request'].search([])
        return request.render('library_management.borrow_request_template', {
            'page_name': 'borrow_request',
            'borrow_requests': borrow_requests,
            'user': request.env.user
        })

    @http.route(['/borrow_request/<int:id>'], type='http', auth="user", website=True)
    def detail_borrow_request(self,id,**kwargs):
        borrow_request = request.env['library.borrow.request'].sudo().browse(id)
        return request.render('library_management.borrow_request_detail_template', {
            'page_name': 'borrow_request',
            'borrow_request': borrow_request,
            'user': request.env.user
        })

    @http.route('/borrow_request/create', type='http', auth='user', methods=['POST'], website=True)
    def create_borrow_request(self, **post):
        vals = {
            'student_id': post.get('student_id'),
            'librarian_id': post.get('librarian_id'),
            'issue_date': post.get('issue_date'),
            'return_date': post.get('return_date'),
        }
        request.env['library.borrow.request'].sudo().create(vals)
        return request.redirect('/borrow_request')

    @http.route('/borrow_request/write', type='http', auth='user', methods=['POST'], website=True)
    def create_borrow_request_lines(self, **post):
        parent_id = int(post.get('borrow_request_id'))
        vals = {
            'book_id': post.get('book_id'),
            'quantity': post.get('quantity'),
            'issue_date': post.get('issue_date'),
            'return_date': post.get('return_date'),
        }
        borrow_request_line = request.env['library.borrow.request.lines'].sudo().create(vals)
        borrow_requests = request.env['library.borrow.request'].sudo().browse(parent_id)
        borrow_requests.sudo().write({'borrow_request_ids':[(4,borrow_request_line.id)]})
        return request.redirect(f'/borrow_request/{parent_id}')