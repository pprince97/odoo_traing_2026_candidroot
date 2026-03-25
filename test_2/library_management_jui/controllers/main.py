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

    @http.route('/library/line/delete/<int:line_id>', type='http', auth='public', website=True)
    def delete_line(self, line_id, **kw):
        line = request.env['library.borrow.request.lines'].sudo().browse(line_id)
        if line:
            line.unlink()
        return request.redirect('/create_borrow_request')

    @http.route('/my/action/update/<int:res_id>', type='http', auth='public', website=True)
    def redirect_update_template(self, res_id, **kw):
        record = request.env['library.borrow.request'].browse(res_id)
        return request.render('library_management_jui.update_borrow_record_template', {
            'record': record,
        })

    @http.route('/my/action/view/<int:res_id>', type='http', auth='public', website=True)
    def redirect_view_template(self, res_id, **kw):
        record = request.env['library.borrow.request'].browse(res_id)
        return request.render('library_management_jui.view_borrow_record_page_template', {
            'record': record,
        })

    @http.route('/my/action/delete/<int:res_id>', type='http', auth='public', website=True)
    def delete_record(self, res_id, **kw):
        record = request.env['library.borrow.request'].browse(res_id)
        if record:
            record.unlink()
        return request.redirect('/borrow_request')

    @http.route('/borrow_request/update', type='http', auth='public', website=True, methods=['POST'])
    def borrow_request_update(self, **post):
        borrow_id = int(post.get('request_id'))
        borrow_request = request.env['library.borrow.request'].sudo().browse(borrow_id)
        line_ids = request.httprequest.form.getlist('existing_line_ids')

        # 1. HANDLE "ADD LINE" ACTION
        if post.get('btn_action') == 'add_line':
            # Create the new line immediately so it shows up on reload
            if post.get('new_book_id'):
                request.env['library.borrow.request.lines'].sudo().create({
                    'borrow_request_id': borrow_request.id,
                    'book_id': int(post.get('new_book_id')),
                    'quantity': int(post.get('new_qty') or 1),
                    'issue_date': post.get('new_issue_date'),
                    'return_date': post.get('new_return_date'),
                })
            # Reload the page/modal (redirect back to the edit view)
            return request.redirect(f'/my/action/update/{int(borrow_id)}')

        # 2. HANDLE "SAVE CHANGES" ACTION
        if post.get('btn_action') == 'save_all':
            # Update Main Record Fields
            new_state = post.get('state')
            update_vals = {
                'student_id': int(post.get('student_id')),
                'state': new_state,
                'cancellation_reason': post.get('cancellation_reason') if new_state == 'cancelled' else False
            }

            # Auto-set canceled date if switching to canceled for the first time
            if new_state == 'cancelled' and not borrow_request.canceled_date:
                update_vals['canceled_date'] = fields.Date.today()
            elif new_state != 'cancelled':
                update_vals['canceled_date'] = False

            borrow_request.write(update_vals)

            # Update all existing lines from the form data
            for l_id in line_ids:
                line = request.env['library.borrow.request.lines'].sudo().browse(int(l_id))
                if line.exists():
                    line.write({
                        'book_id': int(post.get(f'book_id_{l_id}')),
                        'quantity': int(post.get(f'qty_{l_id}') or 1),
                        'issue_date': post.get(f'issue_{l_id}'),
                        'return_date': post.get(f'return_{l_id}'),
                    })

            return request.redirect('/borrow_request')

            # Default fallback
        return request.redirect(f'/borrow_request')

    @http.route('/record/line/delete/<int:line_id>', type='http', auth='public', website=True)
    def delete_line(self, line_id, **kw):
        line = request.env['library.borrow.request.lines'].sudo().browse(line_id)
        borrow_id = line.borrow_request_id
        if line:
            line.unlink()
        return request.redirect(f'/my/action/update/{int(borrow_id)}')
