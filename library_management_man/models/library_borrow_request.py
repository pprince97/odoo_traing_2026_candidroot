import datetime

from odoo import models, fields, api

class LibraryBorrowRequest(models.Model):
    _name = 'library.borrow.request'
    _description = 'Library borrow request'
    _rec_name = 'serial_number'


    serial_number = fields.Char(string='Serial Number')
    student_id = fields.Many2one('res.partner', string='Student')
    librarian_id = fields.Many2one('res.partner', string='Librarian')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('issued', 'Issued'),
        ('returned', 'Returned'),
        ('canceled', 'Canceled'),
    ],default='draft',string='State')
    issue_date = fields.Date(string='Issue Date')
    return_date = fields.Date(string='Returned Date')
    fine_amount = fields.Float(string='Fine Amount',compute='_compute_total_amount')
    total_amount = fields.Float(string='Total Amount',compute='_compute_total_amount')
    canceled_date = fields.Date(string='Canceled Date')
    borrow_request_line_ids = fields.One2many('library.borrow.request.line', 'borrow_request_id',string='Borrow Request Lines')
    cancellation_reason = fields.Char(string='Cancellation Reason')

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            val['serial_number'] = self.env['ir.sequence'].next_by_code('request.sequence') or 'UnKnown'
        res = super().create(vals_list)
        return res

    def draft_request(self):
        self.update({
            'state': 'draft',
        })

    def issue_request(self):
        self.update({
            'state': 'issued',
            'issue_date': datetime.date.today(),
        })

    def returned_request(self):
        self.update({
            'state': 'returned',
            'return_date': datetime.date.today(),
        })

    def cancellation_request(self):
        self.ensure_one()
        return {
            'name': "Cancel Request",
            'type': 'ir.actions.act_window',
            'res_model': 'cancellation.request',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_borrow_request_id': self.id,
            }
        }

    # def canceled_request(self):
    #     self.update({
    #         'state': 'canceled',
    #         'canceled_date' : datetime.date.today(),
    #     })


    @api.depends('borrow_request_line_ids')
    def _compute_total_amount(self):
        for record in self:
            self.total_amount = sum(record.borrow_request_line_ids.mapped('total_amount'))
            self.fine_amount = sum(record.borrow_request_line_ids.mapped('fine_amount'))