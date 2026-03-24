from jsonschema import ValidationError
from odoo import fields, models, api
import datetime

class BorrowRequest(models.Model):
    _name = 'library.borrow.request'
    _description = 'Library borrow request'
    _rec_name = 'serial_number'

    serial_number = fields.Char(string='Serial Number')

    student_id = fields.Many2one('res.partner',string='Student')
    librarian_id = fields.Many2one('res.partner',string='Librarian')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('issued', 'Issued'),
        ('returned', 'Returned'),
        ('cancelled', 'Cancelled'),
    ],
        default='draft',
    )

    issue_date = fields.Datetime(string='Issued Date')
    return_date = fields.Datetime(string='Returned Date')

    fine_amount = fields.Float(string='Fine Amount', compute='_compute_all_amount')
    total_amount = fields.Float(string='Total Amount', compute='_compute_all_amount')

    cancelled_date = fields.Datetime(string='Cancelled Date')
    cancellation_reason = fields.Char(string='Cancellation Reason')


    # Relationship
    request_lines_ids = fields.One2many('borrow.request.line', 'borrow_request_id', string='Request Lines')

    book_ids = fields.Many2many('library.books', 'books_borrows_rel', 'books_id', 'borrow_id',
                                  string='Borrow')

    # history_wizard_id = fields.Many2one('borrow.history', string='History')

    @api.depends('request_lines_ids.total_amount', 'request_lines_ids.fine_amount')
    def _compute_all_amount(self):
        for rec in self:
            print(rec.request_lines_ids.mapped('book_id'))
            rec.total_amount = sum(rec.request_lines_ids.mapped('total_amount'))
            rec.fine_amount = sum(rec.request_lines_ids.mapped('fine_amount'))



    # Generate Serial number
    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if not val.get('serial_number'):
                val['serial_number'] = self.env['ir.sequence'].next_by_code('borrow.request.sequence')

        res = super().create(vals_list)
        print("==============>", res)
        return res


    # Stages updated
    def action_issued(self):
        self.update({'state': 'issued'})
        self.issue_date = fields.Datetime.now()

    def action_returned(self):
        self.update({'state': 'returned'})
        self.return_date = fields.Datetime.now()

    def action_cancelled(self):
        # self.update({'state': 'cancelled'})
        # self.cancelled_date = fields.Datetime.now()

        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cancellation',
            'res_model': 'cancellation.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_borrow_id': self.id
            }
        }
    #
    # def action_issues_books(self):
    #     for rec in self:
    #         rec.update({'state': 'issued'})
    #         self.issue_date = fields.Datetime.now()
    #
    #         for line in rec.request_lines_ids:
    #             line.book_id._compute_books_count
    #
    #             if line.book_id.available_copies < 0:
    #                 raise ValidationError("Error exceeds!")
    #             rec.update({'state':'draft'})