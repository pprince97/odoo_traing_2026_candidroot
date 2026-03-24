from odoo import http, _,fields
from odoo.http import request
from odoo.exceptions import AccessError
import base64

class BookController(http.Controller):

    @http.route('/book', type='http', auth='public', website=True)
    def book_view_user_controller(self):
        if request.env.user._is_public():
            return request.render("library_management_jui.book")
        if not request.env.user.has_group('library_management_jui.library_group_librarian'):
            raise AccessError(_('You are not allowed to access this page, this can only be done by a librarian or administrator'))
        return request.render("library_management_jui.book_form")

    @http.route('/book/submit', type='http', auth='public', website=True)
    def book_on_submit_controller(self, **post):
        # Handle image upload separately if present
        if post.get('cover_image'):
            post['cover_image'] = post['cover_image'].read()
            post['cover_image'] = base64.b64encode(post['cover_image']).decode()
        # Create the book record
        library = request.env['library.books'].sudo().create({
            'name': post.get('name'),
            'barcode': post.get('barcode'),
            'description': post.get('description'),
            'category': post.get('category'),
            'stock': int(post.get('stock') or 0),
            'borrow_price': float(post.get('borrow_price') or 0.0),
            'maximum_day_limit': int(post.get('maximum_day_limit') or 0),
            'cover_image': post['cover_image'] if post.get('cover_image') else False,
        })
        return request.render("library_management_jui.thank_you")

    @http.route('/booklist', type='http', auth='public', website=True)
    def book_list_view_controller(self):
        values = request.env['library.books'].sudo().search([])
        return request.render("library_management_jui.book_list", {'docs':values})

    @http.route('/borrow_request', type='http', auth='public', website=True)
    def borrow_request_list_view_controller(self):
        values = request.env['library.borrow.request'].sudo().search([])
        if not request.env.user.has_group('library_management_jui.library_group_admin'):
            user_id = request.env.user
            values = request.env['library.borrow.request'].sudo().search(['|',('student_id','in',user_id.partner_id.id),('librarian_id','in',user_id.partner_id.id)])
        return request.render("library_management_jui.borrow_request_list_template", {'docs': values})

    @http.route('/my/borrow/records', type='http', auth='user', website=True)
    def account_borrow_request_view_controller(self):
        user_id = request.env.user
        values = request.env['library.borrow.request'].sudo().search(['|',('student_id','in',user_id.partner_id.id),('librarian_id','in',user_id.partner_id.id)])
        print(values)
        return request.render("library_management_jui.my_borrow_request_list_template", {'docs': values})


    @http.route('/create_borrow_request', type='http', auth='public', website=True)
    def borrow_request_form_controller(self, **kwargs):
        request_id = request.session.get('borrow_request_id')

        borrow_request = None
        if request_id:
            borrow_request = request.env['library.borrow.request'].sudo().browse(request_id)

        values = {
            'requests': borrow_request or {},
            'id': borrow_request.id if borrow_request else False,
        }
        return request.render('library_management_jui.borrow_request_temp_form', values)

    @http.route('/borrow_request/submit', type='http', auth='user', website=True, methods=['POST'])
    def borrow_request_submit(self, **post):

        BorrowRequest = request.env['library.borrow.request'].sudo()
        BorrowLine = request.env['library.borrow.request.lines'].sudo()

        request_id = request.session.get('borrow_request_id')

        if not request_id:
            borrow_request = BorrowRequest.create({
                'student_id': int(post.get('student_id')),
                'librarian_id': int(post.get('librarian_id')),
                'issue_date': post.get('issue_date'),
                'return_date': post.get('return_date'),
                'state': post.get('state') or 'draft',
            })
            request.session['borrow_request_id'] = borrow_request.id
        else:
            borrow_request = BorrowRequest.browse(request_id)

        if post.get('action') == 'add_line':
            if post.get('new_book_id'):
                BorrowLine.create({
                    'borrow_request_id': borrow_request.id,
                    'book_id': int(post.get('new_book_id')),
                    'quantity': int(post.get('new_qty') or 1),
                    'issue_date': post.get('new_issue_date'),
                    'return_date': post.get('new_return_date'),
                })

            return request.redirect('/create_borrow_request')

        request.session.pop('borrow_request_id', None)

        return request.render('library_management_jui.thank_you')

    @http.route('/library/line/delete/<int:line_id>', type='http', auth='user', website=True)
    def delete_line(self, line_id, **kw):
        line = request.env['library.borrow.request.lines'].sudo().browse(line_id)
        if line:
            line.unlink()
        return request.redirect('/create_borrow_request')
