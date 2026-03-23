from dateutil.relativedelta import relativedelta
from odoo import models,fields,api,_
from odoo.exceptions import ValidationError

class LibraryBorrowRequests(models.Model):
    _name = 'library.borrow.requests'
    _description = 'Library borrow Requests'
    _rec_name = 'serial_number'

    serial_number = fields.Char(string='Serial Number')
    student_id = fields.Many2one('res.partner',string='Student',required=True)
    librarian_id = fields.Many2one('res.partner',string='Librarians',required=True,compute='compute_librarian',store=True)
    state = fields.Selection([('draft','Draft'),('issued','Issued'),('returned','Returned'),('canceled','Canceled')],string='State',default='draft')
    return_date = fields.Datetime(string='Returned Date')
    issue_date = fields.Datetime(string='Issued Date', default=fields.Datetime.now())
    fine_amount = fields.Float(string='Fine Amount')
    total_amount = fields.Float(string='Total Amount')
    canceled_date = fields.Datetime(string='Canceled Date',readonly=True)
    cancellation_reason = fields.Text('Cancellation Reason',readonly=True)
    borrow_request_line_ids = fields.One2many('library.borrow.request.lines','borrow_request_id',string='Borrow Request Lines')

    def request_state_issued(self):
        self.issue_date = fields.Datetime.now()
        self.state = 'issued'
        for line in self.borrow_request_line_ids:
            line.issue_date = self.issue_date
            if line.book_id.available_copies - line.quantity < 0 :
                raise ValidationError(_(f"Available copies for book : {line.book_id.name} are {line.book_id.available_copies}"))
            else:
                line.book_id.available_copies -= line.quantity

    def request_state_returned(self):
        self.return_date = fields.Datetime.now()
        self.state = 'returned'
        for line in self.borrow_request_line_ids:
            line.book_id.available_copies += line.quantity
            days_issued = (self.return_date - self.issue_date).days
            if days_issued - line.book_id.maximum_day_limit >0:
                line.fine_amount = (days_issued - line.book_id.maximum_day_limit) * line.quantity * line.fine_settings_amt
            else:
                line.fine_amount = 0
            line.total_amount = line.amount * days_issued * line.quantity + line.fine_amount
        self.fine_amount = sum(self.borrow_request_line_ids.mapped('fine_amount'))
        self.total_amount = sum(self.borrow_request_line_ids.mapped('total_amount'))

    def request_state_canceled(self):
        return {
            'name': 'Cancellation Reason',
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.borrow.status.canceled',
            'view_mode': 'form',
            'context':{'serial_number':self.serial_number},
            'target': 'new',
        }

    @api.model_create_multi
    def create(self, vals_list):
        res = super(LibraryBorrowRequests, self).create(vals_list)
        for rec in res:
            rec.serial_number = self.env['ir.sequence'].next_by_code('borrow.request.sequence')
        return res

    def compute_librarian(self):
        for record in self:
            record.librarian_id = self.env.user.commercial_partner_id.id