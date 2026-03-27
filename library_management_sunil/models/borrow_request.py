from odoo import models, fields, api
from datetime import date, timedelta



class BorrowRequest(models.Model):
    _name = 'borrow_request.borrow_request'
    _description = 'Borrow Request'
    _rec_name = 'issue_date'

    name = fields.Char(string="Serial Number", readonly=True, required=True, default="New")
    book_id = fields.Many2one('book.book', string="Book")
    student_id = fields.Many2one('res.partner', string="Student")
    librarian_id = fields.Many2one('res.partner', string="Librarian")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('issued', 'Issued'),
        ('returned', 'Returned'),
        ('cancel', 'Canceled')
    ], default='draft')

    issue_date = fields.Date(string="Issue Date")
    return_date = fields.Date(string="Return Date")
    cancel_date = fields.Date(string="Canceled Date")
    cancellation_reason = fields.Text(string="Cancellation Reason")
    fine_amount = fields.Float(string="Fine Amount")
    total_amount = fields.Float(string="Total Amount")


    request_line_ids = fields.One2many('borrow_request_line.borrow_request_line', 'borrow_id', string="Borrow Lines")



    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('borrow.request') or 'New'

        records = super(BorrowRequest, self).create(vals_list)
        return records

    def action_issue(self):
        for record in self:
            record.write({
                'state': 'issued',
                'issue_date': fields.Date.today()
            })
            for line in self.request_line_ids:
                line['issue_date'] = date.today()

    def action_return(self):
        for record in self:
            record.write({
                'state': 'returned',
                'return_date': fields.Date.today()
            })

    def action_cancel(self):
        return {
            'type': 'ir.actions.act_window',
            'name': ' Borrow Cancel Request',
            'res_model': 'borrow.cancel.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_borrow_id': self.id
            }
        }



