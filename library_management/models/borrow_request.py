from odoo import fields, models, api
from datetime import date


class BorrowRequest(models.Model):
    _name = 'library.borrow.request'
    _description = 'Borrow Request'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'serial_number'

    serial_number = fields.Char(string='Serial Number')
    student_id = fields.Many2one('res.partner',string='Student',tracking=True)
    librarian_id = fields.Many2one('res.partner',string='Librarian',tracking=True)
    state = fields.Selection([
        ('draft','Draft'),
        ('issue','Issued'),
        ('return','Returned'),
        ('cancel','Cancelled')
    ],default='draft',tracking=True)
    return_date = fields.Date(string='Return Date',tracking=True)
    issue_date = fields.Date(string='Issue Date',tracking=True)
    fine_amount = fields.Float(string='Fine Amount')
    total_amount = fields.Float(string='Total Amount',compute='_compute_total_amount')
    cancel_date = fields.Date(string='Cancel Date',tracking=True)
    cancellation_reason = fields.Char(string='Cancellation Reason')
    book_id = fields.Many2one('library.books',string='Book')
    borrow_request_lines_ids = fields.One2many('borrow.requestline','borrow_request_id')



    def issue_book(self):
        self.state = 'issue'
        self.issue_date = date.today()
        self.env['library.books'].book_reduce(self.book_id)
        if self.state=='issue':
            for line in self.borrow_request_lines_ids:
                line['issue_date'] = date.today()

        # var = self.env['borrow.requestline']
        # for line in var:
        #     line.issue_date = date.today()


    # def _compute_issue_date(self):
    #     if self.state=='issue':
    #         for line in self.borrow_request_lines_ids:
    #             line['issue_date'] = date.today()


    def return_book(self):
        self.state = 'return'
        self.return_date = date.today()

    def cancel_request(self):
        self.ensure_one()
        self.state = 'cancel'
        self.cancel_date = date.today()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cancel ',
            'res_model': 'cancel.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_borrow_request_id': self.id,
            }
        }



    def _compute_total_amount(self):
        self.total_amount = self.fine_amount #+

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('emp_code'):
                vals['serial_number'] = self.env['ir.sequence'].next_by_code('serial_number.sequence')
        return super().create(vals_list)


# 4. Borrow Request
# Fields:
# Serial Number (required)
# Student (required)
# Librarian
# State (Selection: Draft, Issued, Returned, Canceled)
# Return Date
# Issue Date
# Fine Amount
# Total Amount
# Canceled Date
# Cancellation Reason (required in Cancelled State)
# Business Rules :
# ●​ Librarians can (create, issue, canceled, returned) Borrow Requests. Librarians Only can see only their own Created Borrow Requests.
# ●​ Auto generate Serial Number when while Creating a Borrow Request
# ●​ When Librarian Issued The Borrow Request then Auto set the issue Date (Use Issue Button) and changed state according to it.
# ●​ When Librarian Returned The Borrow Request then Auto set the Return Date (Use Return Button) and changed state according to it. When the user clicks on Return Button.
# ●​ When Librarian Canceled The Borrow Request then Auto set the Canceled Date (Use Cancel Button) and changed state according to it.
# ●​ When the user clicks on ‘Cancel’ Button then one wizard will appear for Cancellation Reason. The wizard needs one field for Reason, where the user
# adds cancellation reason manually, and clicks on the ‘submit’ button in wizard to set the Cancellation Reason in Borrow Request.
# ●​ Only in Draft State, Users can change Borrow Request Details not any other state.
# ●​ In short all details will be Readonly in these states (Issued, Returned, Canceled.)
# ●​ Cancellation Reason Only will be visible in Cancelled State
# ●​ Need to Create a PDF Report in Borrow Request