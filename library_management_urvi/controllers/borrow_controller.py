from odoo import http
from odoo.http import request


class BorrowController(http.Controller):

    @http.route('/borrow', type='http', auth='user', website=True)
    def list_borrow_records(self, **kw):
        borrow_records = request.env['library.borrow.request'].search([])
        return request.render('library_management_urvi.borrow_list_template', {
            'borrows': borrow_records,
        })

    @http.route('/borrow/<int:record_id>', auth='user', website=True)
    def display_borrow_record(self, record_id):
        borrow_record = request.env['library.borrow.request'].browse(record_id)
        if not borrow_record.exists():
            return request.render('website.404')
        return request.render('library_management_urvi.borrow_record_view_template', {
            'record': borrow_record
        })


    @http.route(['/borrow/create'], type='http', auth="user", website=True)
    def borrow_form(self, **kwargs):
        students = request.env['res.partner'].search([('library_role','=','student')])
        books = request.env['library.book'].search([('state','=','published')])
        currencies = request.env['res.currency'].search([])

        return request.render("library_management_urvi.create_borrow_request_template", {
            'students': students,
            'books': books,
            'currencies': currencies,
        })

    @http.route(['/library/borrow/submit'], type='http', auth="user", methods=['POST'], website=True, csrf=True)
    def borrow_submit(self, **post):

        book_ids = request.httprequest.form.getlist('book_id')
        quantities = request.httprequest.form.getlist('quantity')
        line_issue_dates = request.httprequest.form.getlist('line_issue_date')
        line_return_dates = request.httprequest.form.getlist('line_return_date')

        borrow_line_values = []
        for i in range(len(book_ids)):
            if book_ids[i]:  # Ensure book is selected
                borrow_line_values.append((0, 0, {
                    'book_id': int(book_ids[i]),
                    'quantity': int(quantities[i] or 1),
                    'issue_date': line_issue_dates[i],
                    'return_date': line_return_dates[i],
                }))

        vals = {
            'student_id': int(post.get('student_id')),
            'librarian_id': request.env.user.partner_id.id,
            'issued_date': post.get('issued_date'),
            'currency_id': int(post.get('currency_id')),
            'borrow_request_lines_ids': borrow_line_values,
        }

        new_request = request.env['library.borrow.request'].create(vals)

        # Redirect to a success page or the new record (if portal view exists)
        return request.redirect('/my/borrow/requests')

#
#
#
